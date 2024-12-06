from django.contrib.auth.views import LogoutView, LoginView
from django.contrib import messages
from django.db.transaction import commit
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.datastructures import MultiValueDictKeyError
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from requests.auth import HTTPBasicAuth
import json
from .utils import MpesaAccessToken, LipanaMpesaPpassword
import requests
from datetime import datetime
from django.conf import settings
from .models import Land
from .forms import CustomUserCreationForm, LandForm

# User registration view
class UserRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Registration successful! You can now log in.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Registration failed. Please correct the errors below.")
        return self.render_to_response(self.get_context_data(form=form))

# User login view
class UserLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        user = self.request.user
        return reverse_lazy('land-create') if user.user_type == 'seller' else reverse_lazy('land-list')

# User logout view
class UserLogoutView(LogoutView):
    template_name = 'logout.html'
    next_page = reverse_lazy('index')

# Land list view
class LandListView(ListView):
    model = Land
    template_name = 'land_list.html'
    context_object_name = 'lands'

# Land form mixin
class LandFormMixin:
    model = Land
    form_class = LandForm
    template_name = 'land_form.html'
    success_url = reverse_lazy('land-list')

# Land create view
class LandCreateView(LoginRequiredMixin, UserPassesTestMixin, LandFormMixin, CreateView):
    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.user_type == 'seller'

# Land update view
class LandUpdateView(LoginRequiredMixin, UserPassesTestMixin, LandFormMixin, UpdateView):
    def test_func(self):
        return self.get_object().seller == self.request.user

# Land delete view
class LandDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Land
    template_name = 'land_confirm_delete.html'
    success_url = reverse_lazy('land-list')

    def test_func(self):
        return self.get_object().seller == self.request.user

# Index view
class IndexView(TemplateView):
    template_name = 'index.html'

# Seller dashboard view
class SellerDashboardView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request):
        return render(request, 'seller_dashboard.html', {
            'lands': Land.objects.filter(seller=request.user),
            'form': LandForm()
        })

    def post(self, request):
        form = LandForm(request.POST, request.FILES)
        if form.is_valid():
            land = form.save(commit=False)
            land.seller = request.user
            land.save()
            return redirect('seller-dashboard')
        return render(request, 'seller_dashboard.html', {
            'lands': Land.objects.filter(seller=request.user),
            'form': form
        })

    def test_func(self):
        return self.request.user.user_type == 'seller'

# Token view
def token(request):
    consumer_key = 'Ni67kOb0rkbNF3APd1Pk0GXGdmm98rwVVQuln17eszAK98bU'
    consumer_secret = 'IqXTqbm6Xk3Sr5rCrWSP1462o4GoxC697B9eAPMTlYbovHcEkVEHrVuwGhmf4d2M'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'token.html', {"token": validated_mpesa_access_token})

# Pay view
from .forms import PaymentForm

from .forms import PaymentForm

from .forms import PaymentForm

def pay(request):
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            amount = float(form.cleaned_data['amount'])  # Convert Decimal to float

            account_reference = request.session.get('account_reference', 'default_reference')  # Default reference if none provided

            if not amount or not account_reference:
                return HttpResponse("Essential data missing from session", status=400)

            try:
                access_token = MpesaAccessToken.validated_mpesa_access_token
                api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
                headers = {"Authorization": "Bearer %s" % access_token}

                request_payload = {
                    "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
                    "Password": LipanaMpesaPpassword.decode_password,
                    "Timestamp": LipanaMpesaPpassword.lipa_time,
                    "TransactionType": "CustomerPayBillOnline",
                    "Amount": amount,
                    "PartyA": phone_number,
                    "PartyB": LipanaMpesaPpassword.Business_short_code,
                    "PhoneNumber": phone_number,
                    "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
                    "AccountReference": 'Collins app',
                    "TransactionDesc": "Payment for land"
                }

                response = requests.post(api_url, json=request_payload, headers=headers)
                if response.status_code == 200:
                    return HttpResponse("success")
                else:
                    return HttpResponse(f"Error from M-PESA API: {response.status_code} {response.text}", status=response.status_code)

            except Exception as e:
                return HttpResponse(f"An error occurred: {str(e)}", status=500)
    else:
        form = PaymentForm()

    return render(request, 'pay.html', {'form': form})


# STK view
def stk(request):
    return render(request, 'pay.html', {'navbar': 'stk'})

# views.py
from django.core.mail import send_mail
from django.http import HttpResponse



from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import UserRegisterView, UserLoginView, UserLogoutView, LandListView, LandCreateView, LandUpdateView, \
    LandDeleteView, IndexView, SellerDashboardView,pay
from landapp import views


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('lands/', LandListView.as_view(), name='land-list'),
    path('lands/new/', LandCreateView.as_view(), name='land-create'),
    path('lands/<int:pk>/edit/', LandUpdateView.as_view(), name='land-update'),
    path('lands/<int:pk>/delete/', LandDeleteView.as_view(), name='land-delete'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('seller-dashboard/', SellerDashboardView.as_view(), name='seller-dashboard'),
    # path('lands/<int:pk>/purchase/', PurchaseRequestView.as_view(), name='land-purchase'),
    # path('purchase-request-success/', purchase_request_success, name='purchase-request-success'),
    path('token', views.token, name='token'),
    path('pay', pay, name='pay'),
    path('stk', views.stk, name="stk")
]

admin_patterns=[
    path('admin/', admin.site.urls),
]
urlpatterns +=admin_patterns






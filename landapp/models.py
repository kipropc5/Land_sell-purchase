from django.db import models



# class User(AbstractUser):
#     USER_TYPE_CHOICES = (
#         ('buyer', 'Buyer'),
#         ('seller', 'Seller'),
#     )
#     user_type = models.CharField(max_length=6, choices=USER_TYPE_CHOICES)
#     email = models.EmailField(unique=True)
#     phone_number = models.CharField(max_length=15, unique=True)
#
#     def __str__(self):
#         return self.username
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    )
    user_type = models.CharField(max_length=6, choices=USER_TYPE_CHOICES)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)

    # Add related_name to avoid conflicts with Django's built-in User model
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    def __str__(self):
        return self.username


class Land(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lands')
    location = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='land_photos/')
    size_in_acres = models.DecimalField(max_digits=5, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text='Price in KSH')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.location} - {self.size_in_acres} acres - ${self.price}"

    class Meta:
        ordering = ['-created_at']


class PurchaseRequest(models.Model):
    land = models.ForeignKey(Land, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=(('Pending', 'Pending'),('Approved', 'Approved'),('Rejected', 'Rejected')))
    request_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Purchase Request by {self.buyer.username} for {self. land.location}"
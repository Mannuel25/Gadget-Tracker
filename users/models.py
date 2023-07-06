from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    User model manager where email address is the unique identifier
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("Enter an email address"))

        # email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('staff', 'Staff'),
        ('vendor', 'Vendor')
        )
    LEVEL_CHOICES = (
        ('JUPEB', 'JUPEB'),
        ('100', '100L'),
        ('200', '200L')
        ('300', '300L')
        ('400', '400L')
        ('500', '500L')
        )
    DEPARTMENT_CHOICES = (
        ('mass_com', 'Mass Communication'),
        ('info_tech', 'Information Technology'),
        ('interel', 'International Relations')
        ('med_lab', 'Medical Laboratory Sciences')
        ('accounting', 'Accounting')
        ('pol_sci', 'Political Science')
        ('nursing', 'Nursing Sciences')
        ('bus_admin', 'Business Administration')
        ('econs', 'Economics')
        ('marketing', 'Marketing')
        ('mico_bio', 'Micobiology')
        ('bio_tech', 'BioTechnology')
        )
    username = None
    email = models.EmailField(_("email address"),  max_length=50, null=True, blank=True, unique=True)
    full_name = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    level = models.CharField(choices=LEVEL_CHOICES, max_length=50, blank=True, null=True)
    department = models.CharField(choices=DEPARTMENT_CHOICES, max_length=50, blank=True, null=True)
    phone_no = models.CharField(max_length=50, blank=True, null=True)
    user_type = models.CharField(choices=USER_TYPE_CHOICES, max_length=50, blank=True, null=True)
    picture = models.ImageField(upload_to="user_pictures", blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.full_name} - {self.email}"

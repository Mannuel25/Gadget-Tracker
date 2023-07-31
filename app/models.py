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

        email = self.normalize_email(email)
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

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('staff', 'Staff'),
        ('vendor', 'Vendor')
        )
    LEVEL_CHOICES = (
        ('JUPEB', 'JUPEB'),
        ('100', '100L'),
        ('200', '200L'),
        ('300', '300L'),
        ('400', '400L'),
        ('500', '500L')
        )
    DEPARTMENT_CHOICES = (
        ('mass_com', 'Mass Communication'),
        ('info_tech', 'Information Technology'),
        ('interel', 'International Relations'),
        ('med_lab', 'Medical Laboratory Sciences'),
        ('accounting', 'Accounting'),
        ('pol_sci', 'Political Science'),
        ('nursing', 'Nursing Sciences'),
        ('bus_admin', 'Business Administration'),
        ('econs', 'Economics'),
        ('marketing', 'Marketing'),
        ('micro_bio', 'Micobiology'),
        ('bio_tech', 'BioTechnology'),
        )
    username = None
    full_name = models.CharField(max_length=50, blank=True, null=True)
    matric_no = models.CharField(_("Matric number"), unique=True, max_length=10, blank=True, null=True)
    staff_id = models.CharField(max_length=10, unique=True, blank=True, null=True)
    user_type = models.CharField(default='staff', choices=USER_TYPE_CHOICES, max_length=50, blank=True, null=True)
    email = models.EmailField(_("email address"),  max_length=50, null=True, blank=True, unique=True)
    phone_no = models.CharField(_("Phone number"), max_length=50, blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    level = models.CharField(choices=LEVEL_CHOICES, max_length=50, blank=True, null=True)
    department = models.CharField(choices=DEPARTMENT_CHOICES, max_length=50, blank=True, null=True)
    picture = models.FileField(upload_to="user_pictures", blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.full_name} - {self.email}"

class Gadget(models.Model):
    STATUS_CHOICES = (
        ('missing', 'Missing'),
        ('available', 'Available'),
    )
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    model = models.CharField(max_length=150, blank=True, null=True)
    color = models.CharField(max_length=150, blank=True, null=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=50, blank=True, null=True)
    device_id = models.CharField(max_length=500, blank=True, null=True)
    picture = models.FileField(upload_to="gadgets_pictures", blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.owner.full_name} - {self.model}"


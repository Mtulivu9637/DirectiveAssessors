from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Custom manager for AssessorProfile
class AssessorProfileManager(BaseUserManager):
    def create_user(self, username, id_number, names, password=None):
        if not username:
            raise ValueError("The Username field must be set")
        if not id_number:
            raise ValueError("The ID Number field must be set")
        
        user = self.model(
            username=username,
            id_number=id_number,
            names=names
        )
        user.set_password(password)  # Store hashed password
        user.save(using=self._db)
        return user

    def create_superuser(self, username, id_number, names, password=None):
        user = self.create_user(
            username=username,
            id_number=id_number,
            names=names,
            password=password
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

# AssessorProfile model with custom user manager
class AssessorProfile(AbstractBaseUser):
    names = models.CharField(max_length=255)
    id_number = models.CharField(max_length=20, unique=True)
    username = models.CharField(max_length=150, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = AssessorProfileManager()  # Custom manager for handling assessors

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['id_number', 'names']

    def __str__(self):
        return self.names

    def has_perm(self, perm, obj=None):
        # Simplified permission check
        return True

    def has_module_perms(self, app_label):
        # Simplified module-level permission check
        return True


# Model for Excel file upload and converted PDF
class AssessmentReports(models.Model):
    file = models.FileField(upload_to='uploads/excel_files/')  # Directory to store the Excel file
    uploaded_at = models.DateTimeField(auto_now_add=True)
    converted_pdf = models.FileField(upload_to='uploads/pdf_files/', null=True, blank=True)

    def __str__(self):
        return self.file.name

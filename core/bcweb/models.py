# models.py

from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from PIL import Image
import uuid
import os
from .contract import store_hash  # Web3.py ile ilgili işlemler için import
import logging
# Set up a logger for the User model
logger = logging.getLogger(__name__)

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.pdf']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension. Only .pdf files are allowed.')

class Company(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    contact_number = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    joined_at = models.DateTimeField(default=timezone.now)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    representative_image = models.ImageField(upload_to='company_representatives/', blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Hash'i Ethereum'a gönderme işlemi
        try:
            hash_value = str(self.id)  # Hash olarak UUID'yi kullanıyoruz
            success, tx_hash = store_hash(hash_value)
            if success:
                logger.info(f"Hash başarılı bir şekilde saklandı: {tx_hash}")
            else:
                logger.warning(f"Hash saklama başarısız: {tx_hash}")
        except Exception as e:
            logger.error(f"Hata oluştu: {e}", exc_info=True)

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    birthday = models.DateField()
    e_mail = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Opsiyonel
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    joined_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} {self.surname}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Hash'i Ethereum'a gönderme işlemi
        try:
            hash_value = str(self.id)  # Hash olarak UUID'yi kullanıyoruz
            success, tx_hash = store_hash(hash_value)
            if success:
                print(f"Hash başarılı bir şekilde saklandı: {tx_hash}")
            else:
                print(f"Hash saklama başarısız: {tx_hash}")
        except Exception as e:
            print(f"Hata oluştu: {e}")
        
        # Resmi yeniden boyutlandırma
        if self.profile_image:
            img = Image.open(self.profile_image.path)
            if img.height > 600 or img.width > 600:
                output_size = (600, 600)
                img.thumbnail(output_size)
                img.save(self.profile_image.path)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class Certificate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    verification_code = models.CharField(max_length=100, unique=True)
    provider_company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='certificates')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificates')
    file = models.FileField(upload_to='certificates/', validators=[validate_file_extension])
    approved = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.file and self.file.size > 5 * 1024 * 1024:
            raise ValidationError("The file size must be under 5MB")
        
        if not self.file.name.endswith('.pdf'):
            raise ValidationError("The file must be a PDF")

    def __str__(self):
        return f"Certificate {self.verification_code} for {self.user}"

    class Meta:
        verbose_name = 'Certificate'
        verbose_name_plural = 'Certificates'
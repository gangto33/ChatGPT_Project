from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extrafields):
        if not email:
            raise ValueError('Email은 필수 값입니다.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extrafields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extrafields):
        extrafields.setdefault('is_staff', True)
        extrafields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extrafields)
	

class User(AbstractBaseUser, PermissionsMixin):
	username = models.CharField(max_length=50, unique=True)
	email = models.EmailField(unique=True)
	nickname = models.CharField(max_length=50, unique=True)
	
	is_staff = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	
	date_joined = models.DateTimeField(auto_now_add=True)
	
	objects = CustomUserManager()
	
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username', 'nickname']
	
	def __str__(self):
		return self.email
	
	def get_short_name(self):
		return self.email
	
	def get_full_name(self):
		return self.email
	
	class Meta:
		verbose_name = '사용자'
		verbose_name_plural = '사용자'
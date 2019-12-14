from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.db.models.signals import post_save
# Create your models here.
class Player(models.Model):
    email = models.EmailField(max_length=254,blank=False)
    best_score = models.IntegerField(default=-1)


class MyAccountManager(BaseUserManager):
    def create_user(self,email,password=None):
        if not email:
            raise ValueError("Users must habe an emial address")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password
        )
        user.is_admin=True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user



class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="Email", unique=True)
    username = models.CharField(max_length=100, blank=True)
    date_joined = models.DateTimeField(verbose_name='date joinded',auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self,app_label):
        return True


def create_profile(sender,**kwargs):
    if kwargs['created']:
        player = Player.objects.create(email=kwargs['instance'])


post_save.connect(create_profile, sender=Account)

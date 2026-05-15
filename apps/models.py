from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.db.models import EmailField, Model, DateTimeField, TextField, ForeignKey, CASCADE
from django.db.models.fields import DecimalField, CharField


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email kiritilishi shart")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser is_staff=True bo'lishi shart.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser is_superuser=True bo'lishi shart.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = EmailField(unique=True)
    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()


class ToDo(Model):
    title = CharField(max_length=444)
    desc = TextField()
    created_at = DateTimeField(auto_now_add=True)
    status = CharField(max_length=50, default="Waiting")
    cate = CharField(max_length=50)
    user = ForeignKey(User, on_delete=CASCADE, related_name="tasks")

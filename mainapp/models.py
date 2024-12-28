from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """_summary_: This model is used to store all user details of the website """
    phonenumber = models.CharField(max_length=20, unique=True, db_index=True)
    updated_at = models.DateTimeField(_("Is updated"), auto_now=True)
    role = models.CharField(
        max_length=25,
        choices=[("superadmin", "Super Admin"),("user", "User"), ("superuser", "Super User")],
    )
    # Adding custom related names to avoid conflict
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_("user groups"),
        related_name='user_groups',  # Custom related name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_("user permissions"),
        related_name='user_permissions',  # Custom related name
        blank=True
    )
    
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'phonenumber'
    REQUIRED_FIELDS = ['username', 'email']

    def __str__(self):
        return f"{self.username} with role {self.role}"

    class Meta:
        verbose_name = _("User")

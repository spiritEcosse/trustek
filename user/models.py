from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from trustek.settings import ROLES
from user.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("Email address"), unique=True)
    first_name = models.CharField(_("First name"), max_length=50)
    last_name = models.CharField(_("Last name"), max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    role = models.CharField(_("Role"), max_length=50, choices=ROLES)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        """
        Returns a string representation of the object.

        :return: The email attribute of the object.
        :rtype: str
        """
        return self.email

    @property
    def is_staff(self):
        """
        Return a boolean value indicating if the user is staff or not.

        :return: A boolean value indicating if the user is staff.
        :rtype: bool
        """
        return self.role == ROLES[0][0]

    @property
    def is_superuser(self):
        """
        Return a boolean indicating whether the user is a superuser.

        :return: A boolean value indicating if the user is a superuser.
        """
        return self.is_staff

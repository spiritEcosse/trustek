from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

from trustek.settings import ROLES


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates a new user with the given email and password.

        Parameters:
            email (str): The email of the user.
            password (str, optional): The password of the user. Defaults to None.
            **extra_fields (dict): Additional fields to be set for the user.

        Returns:
            User: The newly created user.
        """
        if not email:
            raise ValueError(_("The email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create a superuser with the given email, password, and extra fields.

        Parameters:
            email (str): The email of the superuser.
            password (str): The password of the superuser.
            **extra_fields (dict): Additional fields to be passed to the create_user method.

        Returns:
            User: The newly created superuser.
        """
        extra_fields.setdefault("role", ROLES[0][0])
        return self.create_user(email, password, **extra_fields)

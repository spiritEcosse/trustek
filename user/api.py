from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.errors import ValidationError

from django.utils.translation import gettext_lazy as _

from user.models import User
from user.schema import UserSchema, UserUpdateSchema

router = Router()


@router.get("/", response=List[UserSchema])
def user(request):
    """
    A function that handles the GET request to the root endpoint ("/user/") of the API.

    Parameters:
        request: The request object containing information about the HTTP request.

    Returns:
        A list of UserSchema objects representing all the users in the database.
    """
    return User.objects.all()


@router.post("/", response=UserSchema)
def create_user(request, payload: UserSchema):
    """
    Create a new user.

    Args:
        request: The HTTP request object.
        payload (UserSchema): The user data payload.

    Returns:
        UserSchema: The created user object.

    Raises:
        ValidationError: If a user with the provided email already exists.
    """
    if User.objects.filter(email=payload.email).exists():
        raise ValidationError(_("User with this email already exists"))
    return User.objects.create_user(**payload.dict())


@router.get("/{user_id}/", response=UserSchema)
def user(request, user_id: int):
    """
    Retrieve a user by their ID.

    Args:
        request: The request object.
        user_id (int): The ID of the user.

    Returns:
        UserSchema: The user object.

    Raises:
        Http404: If the user does not exist.
    """
    return get_object_or_404(User, pk=user_id)


@router.delete("/{user_id}/")
def delete_user(request, user_id: int):
    """
    Delete a user by their ID.

    Parameters:
    - request: The HTTP request object.
    - user_id (int): The ID of the user to be deleted.

    Returns:
    - dict: A dictionary indicating the success of the operation.
             {"success": True}
    """
    user = get_object_or_404(User, pk=user_id)
    user.delete()
    return {"success": True}


@router.put("/{user_id}/", response=UserSchema)
def update_user(request, user_id: int, payload: UserSchema):
    """
    Update a user with the given user ID and payload data.

    Args:
        request: The HTTP request object.
        user_id (int): The ID of the user to update.
        payload (UserSchema): The data to update the user with.

    Returns:
        UserSchema: The updated user object.
    """
    user = get_object_or_404(User, pk=user_id)
    data = payload.dict()
    data.pop("id", None)
    for attr, value in data.items():
        setattr(user, attr, value)
    user.save()
    return user


@router.patch("/{user_id}/", response=UserSchema)
def update_part_user(request, user_id: int, payload: UserUpdateSchema):
    """
    Update a part of a user's information.

    Args:
        request: The HTTP request object.
        user_id (int): The ID of the user to be updated.
        payload (UserUpdateSchema): The updated user information.

    Returns:
        UserSchema: The updated user object.

    Raises:
        Http404: If the user with the given ID does not exist.
    """
    user = get_object_or_404(User, pk=user_id)
    data = payload.dict(exclude_unset=True)
    data.pop("id", None)
    for attr, value in data.items():
        setattr(user, attr, value)
    user.save()
    return user


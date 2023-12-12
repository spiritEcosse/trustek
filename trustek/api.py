from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from ninja import NinjaAPI
from ninja.errors import ValidationError
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _

from user.models import User
from user.schema import UserAuthSchema

api = NinjaAPI()
api.add_router("/user/", "user.api.router", auth=JWTAuth())


@api.post("/login/")
def get_new_token(request, payload: UserAuthSchema):
    data = payload.dict()
    user = get_object_or_404(User, email=data['email'])
    check = check_password(data['password'], user.password)
    if check:
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }
    raise ValidationError(_("Invalid credentials"))

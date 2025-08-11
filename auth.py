from ninja.security import HttpBearer
from django.contrib.auth import authenticate
from ninja_jwt.tokens import RefreshToken
from ninja_jwt.controller import TokenObtainPairController
from ninja import Router
from .models import User
from .schemas import UserIn

auth_router = Router()

class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            from ninja_jwt.tokens import verify_token
            payload = verify_token(token)
            user_id = payload.get('user_id')
            return User.objects.get(id=user_id)
        except Exception:
            return None

@auth_router.post("/register", response={200: dict, 400: dict})
def register(request, payload: UserIn):
    if User.objects.filter(username=payload.username).exists():
        return 400, {"message": "Пользователь с таким именем уже существует"}
    user = User.objects.create_user(username=payload.username, password=payload.password)
    refresh = RefreshToken.for_user(user)
    return {"access": str(refresh.access_token), "refresh": str(refresh)}

auth_router.add_router("/jwt/", TokenObtainPairController())
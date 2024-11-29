from django.core.exceptions import PermissionDenied
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from django.db.models import Q
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken, TokenError
from .serialize import *
from django.utils.translation import gettext as _
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_registration import signals
from django.contrib.auth import get_user_model


UserModel = get_user_model()


class UserTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        req_data = request.data.copy()
        print(req_data)

        # Check if the request data contains email or phone
        username = req_data.get('username')

        if not username:
            raise AuthenticationFailed("username is required for login")

        # Attempt to authenticate the user with email or phone
        
        try:
            current_user = UserModel.objects.get(Q(email=username) | Q(phone_number=username) | Q(username=username))
        except UserModel.DoesNotExist:
            return Response({'message': 'not found'}, status=status.HTTP_404_NOT_FOUND)

        if not current_user.is_active:
            return Response(
                {'message':'Account not activated. Check your email or whatsapp message to comfirm your account.'},
                 status=status.HTTP_401_UNAUTHORIZED)

        serializer = UserTokenObtainPairSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            print('erreur', e)
            return Response({"message":serializer.errors},
                             status=status.HTTP_406_NOT_ACCEPTABLE)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
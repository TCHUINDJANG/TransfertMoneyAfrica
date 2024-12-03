from typing import Type
from django.shortcuts import render , redirect
from rest_framework import viewsets
from rest_framework.serializers import Serializer
from .models import * 
from .serialize import AccountsSerializer ,  UserRegistrationModelSerializer , ForgotPasswordSerializer
from rest_framework.parsers import JSONParser 
from rest_framework.response import Response 
from rest_framework import status
from django.contrib.auth import authenticate, login , logout
from django.contrib import messages 
from django.core.mail  import send_mail , EmailMessage
from django.utils.http import urlsafe_base64_decode , urlsafe_base64_encode
from django.utils.encoding import force_bytes 
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status , permissions
from rest_registration.api.views.register import RegisterSigner
from rest_registration.api.views.login import login
from rest_registration.api.views.change_password import change_password
from rest_registration.api.views.reset_password import reset_password
from rest_registration.api.views.profile import profile
from rest_registration.api.views.register_email import register_email
from rest_registration.api.views import register
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.signals import user_logged_in, user_login_failed
from .serialize import ProfileSerializer
from django.views.decorators.csrf import csrf_exempt
import random
from django.conf import settings
from rest_registration.api.views.profile import ProfileView
from rest_registration.api.views.register import RegisterView 
from rest_registration.api import views
from rest_registration.api.views.change_password import ChangePasswordView
from rest_registration.api.views.login import LoginView , LogoutView , perform_login
from rest_registration.api.views.reset_password import ResetPasswordView
from rest_registration.utils.responses import get_ok_response
from .Permissions import AuthorProfilePermission
from rest_framework.request import Request
from rest_registration.settings import registration_settings
from rest_registration.exceptions import LoginInvalid, UserNotFound
from rest_framework_simplejwt.views import TokenRefreshView
from django.core.mail import send_mail
from .utils import otp_send_mail
from rest_framework.decorators import api_view , permission_classes
from django.db.models import Q
from rest_framework.authtoken.models import Token
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import update_session_auth_hash
from rest_framework.pagination import PageNumberPagination
from accounts.Permissions import IsAdmin , IsUser




class StandardResultsSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 1000  



@api_view(['POST'])
def register_user(request):
     if request.method == 'POST':
          print('data', request.data)
          serializer = UserRegistrationModelSerializer(data=request.data)
          if serializer.is_valid(raise_exception=True):
               serializer.save()
               try:
                    otp_send_mail(serializer.data['email'])
               except Exception as error:
                    pass
              
               return Response({
                    'status':200,
                    'message':'Registration succcessfully check your mail',
                    'data':serializer.data
               })
     return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
    

class TokenRefresh(TokenRefreshView):
     permission_classes = [permissions.IsAuthenticated]
    
#api logout user
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method == 'POST':
        try:
           
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

@api_view(['GET'])
@permission_classes([IsAuthenticated , AuthorProfilePermission])
def get_all_user(request):
     user =  UserRegistrationModel.objects.all()
     serializer = UserRegistrationModelSerializer(user , many=True)
     pagination_class = StandardResultsSetPagination
     return Response(serializer.data , status=status.HTTP_200_OK)
   
@api_view(['POST'])
def forgot_password(request):
    email = request.data.get('email')
    try:
        user  = UserRegistrationModel.objects.get(email=email)

        if user.reset_attempts >= 6:
            return Response({'error': 'Maximum de tentatives de réinitialisation atteint.'}, status=status.HTTP_400_BAD_REQUEST)
        
        token = get_random_string(5)
        user.code = token
        user.reset_code_expiration = timezone.now() + timedelta(minutes=5) #le code de renitialisatio expire apres 5 minutes
        user.reset_attempts += 1
        user.save()
 # Envoyer l'e-mail avec le lien de réinitialisation
        send_mail(
             'Réinitialisation de mot de passe',
            f'Votre code de réinitialisation est {token}',
            'from@example.com',
            [email],
            fail_silently=False,
        )
        return Response({'success': 'Code de réinitialisation envoyé'}, status=status.HTTP_200_OK)
    
    except UserRegistrationModel.DoesNotExist:
        return Response({'error': 'Email non trouvé'}, status=status.HTTP_404_NOT_FOUND)
    



#api de renitialisation de mot de passe
@api_view(['POST'])
def reset_password(request):
    code = request.data.get('code')
    new_password = request.data.get('new_password') 
    email= request.data.get('email')
# Récupérer l'utilisateur en fonction du code de réinitialisation
    try:
        user = UserRegistrationModel.objects.get(email=email)
         # Mettre à jour le mot de passe de l'utilisateur
       
        if user.code != code or user.reset_code_expiration < timezone.now():
            return Response({'error': 'Code de réinitialisation invalide ou expiré.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        return Response({'success': 'Mot de passe réinitialisé avec succès'}, status=status.HTTP_200_OK)
    except UserRegistrationModel.DoesNotExist:
        return Response({'error': 'Code de réinitialisation invalide'}, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):

    user = request.user
    current_password = request.data.get('current_password')
    new_password = request.data.get('new_password')

# Vérifiez que le mot de passe actuel est correct

    if not user.check_password(current_password):
        return Response({'error': 'Le mot de passe actuel est incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()

    # Met à jour la session de l'utilisateur
    update_session_auth_hash(request, user)
    return  Response({'success': 'Mot de passe changé avec succès.'}, status=status.HTTP_200_OK)




#Créeons une vue pour gérer l'URL de vérification
# @api_view(['POST'])
def verify_email(request , pk):
    user = UserRegistrationModel.objects.get(pk=pk)
    if not user.email_verified:
        user.email_verified = True
        user.save()
        return redirect('http://localhost:8000/')
      # Replace with your desired redirect URL



#Récupère le profil de l'utilisateur authentifié.
@api_view(['GET'])
@permission_classes([IsAuthenticated , AuthorProfilePermission])
def get_user_profile(request):
   try:
     profile = Profile.objects.get(user=request.user)
     
   except Profile.DoesNotExist:
     return Response({"error":"Profil de l'utilisateur non trouve"} , status=status.HTTP_404_NOT_FOUND)
   
   serializer = ProfileSerializer(profile , many=False)
   return Response(serializer.data , status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([ permissions.IsAuthenticated , IsUser])
def create_profil(request):
    document_of_personnel_identification = request.data.get('document_of_personnel_identification')
    adress_of_residence = request.data.get('adress_of_residence')
    region = request.data.get('region')
    birth_day = request.data.get('birth_day')
    bio = request.data.get('bio')
    email = request.data.get('email')
    profile_picture = request.data.get('profile_picture')
    user = request.data.get('user')

    #si le profil n'existe pas je cree
    try:
        profile , created = Profile.objects.get_or_create(user=user)
        
        profile = Profile.objects.create(
        document_of_personnel_identification = document_of_personnel_identification,
        adress_of_residence = adress_of_residence,
        region = region,
        birth_day = birth_day,
        bio = bio,
        email = email,
        profile_picture = profile_picture,
        user = user
    )
        profile.save()
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    except Exception as error:
         return Response({'error':'echec de la creation du profil' } , status=status.HTTP_400_BAD_REQUEST)

   
#Récupère le profil de l'utilisateur authentifié.
@api_view(['GET'])
@permission_classes([IsAuthenticated , AuthorProfilePermission])
def get_all_profile(request):
     profiles =  Profile.objects.all()
     serializer = ProfileSerializer(profiles , many=True)
     pagination_class = StandardResultsSetPagination
     return Response(serializer.data , status=status.HTTP_200_OK)
   



#Met à jour les informations du profil de l'utilisateur.
@api_view(['PUT'])
@permission_classes([IsAuthenticated , AuthorProfilePermission])
def update_partial_profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
     
    except Profile.DoesNotExist:
     return Response({'error':'Profil non trouve'} , status=status.HTTP_404_NOT_FOUND)
    
    serializer = ProfileSerializer(profile , data=request.data , partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'success':'Profil mis a jour avec susses'} , status=status.HTTP_200_OK)
    return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)



@api_view(['PUT'])
@permission_classes([IsAuthenticated , AuthorProfilePermission])
def update_profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
     
    except Profile.DoesNotExist:
     return Response({'error':'Profil non trouve'} , status=status.HTTP_404_NOT_FOUND)
    
    serializer = ProfileSerializer(profile , data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'success':'Profil mis a jour avec susses'} , status=status.HTTP_200_OK)
    return Response(serializer.errors , status=400)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated , AuthorProfilePermission])
def delete_user_profile(request):
    try:
     profile = Profile.objects.get(user=request.user)
     
    except Profile.DoesNotExist:
        return Response({'error':'Profil non trouve'} , status=status.HTTP_404_NOT_FOUND)
    
    profile.delete()
    return Response({'succes':'Profil supprime avec succes'} , status=status.HTTP_200_OK)
     
     

     
    


       
     

        

          
          
# class ForgotPasswordView(ChangePasswordView):

#      def get_serializer_class(self) -> type[Serializer]:
#           return ForgotPasswordSerializer
     

     
class ProfileViewApi(ProfileView):
     permission_classes = [IsAuthenticated , AuthorProfilePermission]

     def get_serializer_class(self) -> Serializer:
          return ProfileSerializer  












           





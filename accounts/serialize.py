from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model 
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from accounts.models import *
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.db.models import Q




UserModel = get_user_model()


class UserTokenObtainPairSerializer(TokenObtainSerializer):

    @classmethod
    def get_token(cls, user):
        """
        Get the token for the user and mark the last login date of the user
        """
        from django.utils import timezone
        _obj = user
        _obj.last_login = timezone.now()
        _obj.save()
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = {}
        password = attrs['password']
        username = attrs['username']

        print(username , password)

        user = UserModel.objects.get(Q(email=username) | Q(phone_number=username) | Q(username=username))

        if user.check_password(password):

            refresh = self.get_token(user)

            data["refresh"] = str(refresh)
            data["access"] = str(refresh.access_token)
            data["user"] = UserRegistrationModelSerializer(user).data
            return data

        else:

            print(user, 'bonjour')

            raise serializers.ValidationError("Invalid credentials")
        



class UserRegistrationModelSerializer(serializers.ModelSerializer):
    

    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    username = serializers.CharField(max_length=255)
    email = serializers.CharField(max_length=255)
    phone_number = serializers.CharField(max_length=19)
#     reset_code_expiration = serializers.DateTimeField()
    
    class Meta:
        model = UserRegistrationModel
        fields = ['username', 'password' ,'confirm_password', 'phone_number' , 'email' , 'role']


     
    def create(self , validated_data):
          user = UserModel(
              username = validated_data['username'],
              confirm_password = validated_data['confirm_password'],
              phone_number = validated_data['phone_number'],
              email = validated_data['email'],

         )
          user.set_password(validated_data['password'])
          user.save()
          return user
    
    def validate(self , attrs):
         if attrs['password'] != attrs['confirm_password']:
              raise serializers.ValidationError("Le Mot de passe doit etre egal au confirm password")
         return attrs

    

    def validate_email(self , value):
         if UserModel.objects.filter(email=value).exists():
              raise serializers.ValidationError('this email is already use in the database')
         return value
    
    def validate_username(self , value):
         if UserModel.objects.filter(username=value).exists():
              raise serializers.ValidationError('this username is already use in the database')
         return value
    
    def validate_phone_number(self , value):
         if UserModel.objects.filter(phone_number=value).exists():
              raise serializers.ValidationError('this phone is already use in the database')
         return value
    


    


class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = ['user', 'solde', 'devise']

class ForgotPasswordSerializer(serializers.ModelSerializer):
     class Meta:
          model = UserRegistrationModel
          fields = ['username']
       

# class ResetPasswordSerializer(serializers.ModelSerializer):
#      class Meta:
#           model = UserRegistrationModel
#           fields = ['old_password', 'new_password' , 'username']
          

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'document_of_personnel_identification', 'adress_of_residence', 'region' , 'profile_picture' , 'bio' , 'email' , 'birth_day']


    def update(self , instance , validated_data):
         instance.profile_picture = validated_data.get('profile_picture' , instance.profile_picture)
         instance.region = validated_data.get('region' , instance.region)
         instance.document_of_personnel_identification = validated_data.get('document_of_personnel_identification' , instance.document_of_personnel_identification)
         instance.bio = validated_data.get('bio')

         instance.save()
         return instance
    
    
    def create(self , validated_data):
         profil = Profile.objects.create(**validated_data)
         return profil
    


    
    
    def patch(self , instance , validated_data):
         pass
    
    def validate_email(self , value):
         if Profile.objects.exclude(user=self.context['request'].user).filter(email=value).exists():
              raise serializers.ValidationError("Cet emailest deja utilise")
         return value
    

    def validate_profile_picture(self , value):
         if value:
              if value.size > 5 * 1024 * 1024: #limite de taille 5mo
                   raise serializers.ValidationError("L'image de profil est trop grande (max 5 Mo) .")
              if not value.name.lower().endswith(('.png' , '.jpg' , '.jpeg')):
                   raise serializers.ValidationError("Le fichier doit etre une image au format PNG , JPG ou JPEG.")
         return value
    

    def validate_bio(self , value):
         if len(value) > 500:
              raise serializers.ValidationError("La bio ne peut pas depasser 500 caracteres.")
         return value
     



class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['name_of_country', 'code_of_country', 'drapeau']



def validate_phone(self, value):
        if value:
            # Ajoute des validations spécifiques pour le numéro de téléphone si nécessaire
            if len(value) < 10:
                raise ValidationError(("Le numéro de téléphone est trop court."))
        return value


          

def validate_email(self , value):
        if UserRegistrationModel.objects.filter(email=value).exists():
            raise serializers.ValidationError('this email is already use in the database')
        return value
    
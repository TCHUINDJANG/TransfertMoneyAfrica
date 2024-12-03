from rest_framework.routers import DefaultRouter

from accounts.api import UserTokenObtainPairView
from .views import  register_user ,get_all_user,create_profil ,  forgot_password ,change_password, reset_password,user_logout, update_profile , TokenRefresh
from django.urls import path, include 
from rest_framework_simplejwt.views import (
    TokenObtainPairView , TokenRefreshView , TokenVerifyView
)

from . import views



# from  rest_registration.api.views import  change_password , logout , profile , verify_email , login
 


urlpatterns = [
    #Authentication
    path('accounts/auth-registers/', register_user, name='register'),
    path('accounts/forgot-password/', forgot_password , name='forgot-password'),
    path('accounts/reset-password/', reset_password, name='reset-password'),
    path('api/token/login/', UserTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('accounts/change_password/', change_password, name='change_password'),
    path('accounts/logout/', user_logout, name='logout'),
    path('accounts/all_user/', get_all_user, name='all_user'),
    # path('accounts/verify_email/', verify_email, name='verify_email'),

    #Profile
    path('profile/update/', update_profile, name='update_profile'),
    path('profile/get-user/', views.get_user_profile, name='get_profile'),
    path('profile/delete/', views.delete_user_profile, name='delete_user_profile'),
    path('profiles/all/', views.get_all_profile, name='get_all_profile'),
    path('profiles/update-partial/', views.update_partial_profile, name='get_all_profile'),
    
    
]


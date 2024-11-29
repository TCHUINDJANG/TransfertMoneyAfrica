from django.contrib import admin
from .models import UserRegistrationModel
from .models import Country
from .models import Accounts
from .models import Profile

class AdminUserRegistrationModel(admin.ModelAdmin):

    list_display = ('user','solde', 'devise')

admin.site.register(UserRegistrationModel)



class AdminCountry(admin.ModelAdmin):

    list_display = ('name_of_country','code_of_country', 'drapeau')

admin.site.register(Country)


class AdminAccount(admin.ModelAdmin):

    list_display = ('user','solde','devise')

admin.site.register(Accounts)
    

class AdminProfile(admin.ModelAdmin):

    list_display = ('user','document_of_personnel_identification', 'adress_of_residence' , 'region' ,'email' , 'profile_picture' , 'bio')

admin.site.register(Profile)
    

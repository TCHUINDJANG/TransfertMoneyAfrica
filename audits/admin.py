from django.contrib import admin
from .models import Operations

class AdminAudit(admin.ModelAdmin):

    list_display = ('result_of_the_operation','status_of_the_operation', 'duration_of_the_operation' , 'description_of_the_operation' , 'user')

admin.site.register(Operations)
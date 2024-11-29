from django.contrib import admin
from .models import Transaction
from .models import TransactionHistory
from .models import Notification
from .models import Devise



class AdminTransaction(admin.ModelAdmin):

    list_display = ('sender','receiver', 'amount' , 'devise' , 'statut' , 'description' ,'timestamp' , 'type_transaction')

admin.site.register(Transaction)



class AdminTransactionHistory(admin.ModelAdmin):

    list_display = ('transaction_id','sender', 'receiver' ,'created_at', 'updated_at')

admin.site.register(TransactionHistory)
    

class AdminNotification(admin.ModelAdmin):

    list_display = ('transaction_id','message' , 'as_read')

admin.site.register(Notification)


class AdminDevise(admin.ModelAdmin):

    list_display = ('base_currency','target_currency' , 'last_updated', 'rate')

admin.site.register(Devise)






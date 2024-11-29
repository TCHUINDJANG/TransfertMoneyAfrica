from django.urls import path
from .views import  getTransactionView ,receive_money,check_solde ,transaction_history, getTransactionByIdView, deleteTransactionView, update_partialTransactionView , create_transactionView , updateTransactionView

urlpatterns = [
    path('transactions/get-transaction/', getTransactionView , name='transaction'),
    path('transactions/get-transcation-id/', getTransactionByIdView, name='transaction'),
    path('transactions/create-transaction/', create_transactionView, name='transaction'),
    path('transactions/update-transactions/', updateTransactionView , name='transaction'),
    path('transactions/updatePartial/', update_partialTransactionView , name='transaction'),
    path('transactions/delete-transaction/', deleteTransactionView , name='transaction'),
    path('transactions/history-transaction/', transaction_history , name='history-transaction'),
    path('transactions/receive-money/', receive_money , name='receive-money'),
    path('transactions/verifier-solde/', check_solde , name='verifier-solde'),



    
]


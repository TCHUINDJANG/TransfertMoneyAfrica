from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Transaction
from .models import Transaction, TransactionHistory




@receiver(post_save , sender=Transaction)
def create_transaction_notification(sender, instance, created , **kwargs):
    if not created:   #si la transaction a ete mis a jour
        subject = f'Status de votre transaction {instance.id} change'
        message = f'Votre transaction dun montant de {instance.amount} a change de status a {instance.statut}'
        recipient = instance.sender.email  #on 'envoie la notification a l'expediteur

        try:
            send_mail(subject ,message , 'paulnicolas519@gmail.com' , [recipient] )
        except Exception as error:
            pass
       

@receiver(post_save , sender=Transaction)
def send_transactions_history(sender, instance, created , **kwargs):
    transaction = instance
    if created:

        try:

            TransactionHistory.objects.create(
                  transaction_id = transaction,
                  sender  = transaction.sender, 
                  receiver  = transaction.receiver,                     
                  user  = transaction.sender,                     

                  )
        except Exception as error:
            print('erruer', error)
            pass
          # Si la transaction est nouvellement créée, on enregistre un nouvel historique
      
        
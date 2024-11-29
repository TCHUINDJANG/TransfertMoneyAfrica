from rest_framework import serializers
from .models import *
from accounts.models import Accounts
from rest_framework.exceptions import ValidationError

class TransactionSerializer(serializers.ModelSerializer):

    sender = serializers.StringRelatedField(read_only=True) #affiche le nom de l'expediteur
    receiver = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Transaction
        fields = [ 'amount', 'statut', 'receiver', 'sender', 'timestamp', 'description' , 'type_transaction']
        read_only_fields = ['timestamp', 'sender']


    def update(self , instance , validated_data):

        #met a jour les champs de la transaction partiellement
        if instance.receiver != validated_data.get('receiver'):
            account_old_receiver = Accounts.objects.get(user=instance.receiver)
            account_sender = Accounts.objects.get(user=instance.sender)
            account_old_receiver.solde -= instance.amount   
            account_old_receiver.save()
            instance.receiver = validated_data.get('receiver')


            if instance.amount != validated_data.get('amount'):
                reste = instance.amount - validated_data.get('amount')
                if reste < 0 and account_sender.solde < reste:
                    raise ValidationError("Impossible de realiser la transaction car l'ajout que vous avez fair sur le montant de la trasaction es superieur au solde de votre compte")


                account_sender.solde +=reste
                account_sender.save()
            
            instance.amount = validated_data.get('amount', instance.amount)
            instance.save()


        else:

            if instance.amount != validated_data.get('amount'):
                account_receiver = Accounts.objects.get(user=instance.receiver)
                account_sender = Accounts.objects.get(user=instance.sender)
                reste = instance.amount - validated_data.get('amount')
                if reste < 0 and account_sender.solde < reste:
                    raise ValidationError("Impossible de realiser la transaction car l'ajout que vous avez fair sur le montant de la trasaction es superieur au solde de votre compte")


                account_receiver.solde -= reste 
                account_sender.solde +=reste
                account_receiver.save()
                account_sender.save()

        instance.status = validated_data.get('status', instance.status)
        instance.updated_at = validated_data.get('updated_at', instance.updated_at) 
        instance.save()
        return instance

    def validate(self , data):
        user = data.get('user')
        amount = data.get('amount')

        if user.balance < amount:
            raise serializers.ValidationError("Le solde de l'utilisateur est insuffisant pour cette transaction.")
        return data
    
    def create(self, validated_data):
        # Si des traitements supplémentaires sont nécessaires avant la création de la transaction
        transaction = Transaction.objects.create(**validated_data)
        return transaction
    
    def patch(self , validated_data):
        pass 



class TransactionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionHistory
        fields = ['transaction_id',  'created_at' , 'sender' , 'receiver' , 'updated_at']
        read_only_fields = ['transaction_id']



class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['message', 'as_read']





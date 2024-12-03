from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Transaction
from .serialize import TransactionSerializer , TransactionHistorySerializer 
from accounts.serialize import AccountsSerializer
from accounts.Permissions import IsAdmin , IsUser , CanUpdateTransaction , AuthorPermission
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view , permission_classes
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from .models import Devise
from transactions.Permissions import AuthorTransactionPermission
from .models import User 
from accounts.models import Accounts
from django.db import transaction as atomictransaction
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q




class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


@api_view(['GET'])
@permission_classes([ permissions.IsAuthenticated , IsUser , AuthorTransactionPermission])
def getTransactionView(request):
    transaction = Transaction.objects.all()
    if not request.user.is_staff:
        transactionGet = Transaction.objects.filter(user=request.user)
    serializer = TransactionSerializer(transaction , many=True)
    pagination_class = StandardResultsSetPagination
    return Response(serializer.data)

#modelviewset  orred_only set qui te donne les details sur les comptes et les details d'un compte avec la permissions d'un supeeuser
#si c'est un utilisateur simple on le renvoit juste les details de son compte
   

@api_view(['GET'])
@permission_classes([ permissions.IsAuthenticated , IsUser , AuthorTransactionPermission])
def getTransactionByIdView(request , pk):
    permission_classes = [IsAuthenticated , AuthorTransactionPermission]
    transaction = get_object_or_404(Transaction , pk)
    serializer = TransactionSerializer(transaction , many=False)
    return Response(serializer.data)


#fonction d'envoi d'email

# def send_transaction_email(user , transaction):
#     subject = "Confirmation de la transaction"
#     message = f"Hi {user.username}"


    

@api_view(['POST'])
@permission_classes([ permissions.IsAuthenticated , IsUser])
def create_transactionView(request):
    sender = request.user  #celui qui envoit es deja connecte
    username = request.data.get('receiver')
    amount = request.data.get('amount')

    try:
        receiver =  User.objects.filter(Q(email=username) | Q(phone_number=username) | Q(username=username)).first()
       
    except User.DoesNotExist or Devise.DoesNotExist:
        return Response({"error": "Invalid user or currency ID"}, status=status.HTTP_400_BAD_REQUEST)

    # Si l'utilisateur n'existe pas on le cree la je recupere le compte des utilisateurs
    account_sender , created = Accounts.objects.get_or_create(user= sender)
    account_receiver , created = Accounts.objects.get_or_create(user= receiver)
    if account_sender.solde < amount:
        return Response({"error": "Insufficient funds"}, status=status.HTTP_400_BAD_REQUEST)
    

    try:
        with atomictransaction.atomic():


        # Création de la transaction
            transaction = Transaction.objects.create(
                sender=sender,
                receiver=receiver,
                amount=amount,
                statut='en_cours',
                devise = account_sender.devise
            )

            # Mise à jour des soldes de celui qui envoit ou debiter le compte de l'utilisateur
            account_sender.solde -= amount
            account_sender.save()

            if account_sender.devise != account_receiver.devise :
                devise_sender = Devise.objects.get(target_currency=account_sender.devise)
                devise_receiver = Devise.objects.get(target_currency=account_receiver.devise)
                account_sender_amount = amount * devise_sender.rate
                amount = account_sender_amount / devise_receiver.rate
                

             # Mise à jour des soldes de celui qui recoit ou crediter le compte du destinataire
            account_receiver.solde += amount
            account_receiver.save()

            # Passer la transaction à 'completed'
            transaction.statut = 'completed'
            transaction.save()

            serializer = TransactionSerializer(transaction)


            # Réponse
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Exception as e:
        # Si une erreur se produit, on met la transaction en "failed"
        transaction.statut = 'failed'
        transaction.save()
        print('erreur', e)
        return Response({'error':'echec de la transaction' } , status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([ permissions.IsAuthenticated , IsUser , AuthorTransactionPermission ,CanUpdateTransaction ])
def updateTransactionView(request , pk):
    
    transaction = get_object_or_404(Transaction , pk=pk)
    serializer = TransactionSerializer(instance=transaction , data = request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#a refaire le traitement des donnes(recoit, la soemd'argent envoye compore les donnes)
@api_view(['PATCH'])
@permission_classes([ permissions.IsAuthenticated , IsUser , AuthorTransactionPermission ,CanUpdateTransaction ])
def update_partialTransactionView(request , pk):
    transaction = get_object_or_404(Transaction , pk=pk)
    serializer = TransactionSerializer(instance=transaction , data = request.data , partial=True)
    try:
    
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data , status=status.HTTP_200_OK) 
    except ValidationError as e:  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'detail': 'Erreur inattendue lors de la mise à jour de la transaction.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#on suprime une traction qui sont en echec a refaire
@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated, AuthorTransactionPermission])
def deleteTransactionView(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)

    # Vérification du statut avant de supprimer la transaction
    if transaction.statut != 'echoue':
        return Response({'error': 'Transaction cannot be deleted unless it failed'}, status=status.HTTP_400_BAD_REQUEST)

    # Si la transaction est en "failed", on peut la supprimer
    transaction.delete()
    return Response({'message': 'Transaction successfully deleted'}, status=status.HTTP_204_NO_CONTENT)


#api recuperer pour recuper l'historique des trnsactions de l'utiisateur connecte
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, AuthorTransactionPermission])
def transaction_history(request):
    transactions = Transaction.objects.filter(sender=request.user).or_filter(receiver=request.user).order_by('-timestamp')
    serializer = TransactionHistorySerializer(transactions , many=True)
    return Response(serializer.data)


#api pour recevoir de l'argent
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, AuthorTransactionPermission])
def receive_money(request):
    #retournons les trnsactions recus par l'utilisateur connecte
    transactions = Transaction.objects.filter(receiver=request.user).order_by('timestamp')
    serializer = TransactionHistorySerializer(transactions , many=True)
    return Response(serializer.data)


#api pour verifier le solde de l'utilisateur connecte
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, AuthorTransactionPermission])
def check_solde(request):
    try:
        solde_user = Accounts.objects.get(user=request.user)
    except Accounts.DoesNotExist:
        return Response({"error":"Le solde de l'utilisateur n'est pas trouve "} , status=status.HTTP_400_BAD_REQUEST)
    
    serializer = AccountsSerializer(solde_user)
    return Response(serializer.data)
#developper une api de retrait

# exporter une facture d'une transaction
import csv
from django.http import HttpResponse

@api_view(['GET'])
@permission_classes([ permissions.IsAuthenticated , IsUser , AuthorTransactionPermission])
def export_transactions(request):
    transactions = Transaction.objects.filter(sender=request.user)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="transactions.csv"'
    writer = csv.writer(response)
    writer.writerow(['Date', 'Sender', 'Receiver', 'Amount', 'Status'])
    for transaction in transactions:
        writer.writerow([transaction.transaction_date, transaction.sender.username, transaction.receiver.username, transaction.amount, transaction.status])
    return response





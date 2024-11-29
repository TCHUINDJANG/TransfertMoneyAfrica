from rest_framework import permissions

#verifie si l'utilisateur es authentifie
class IsAuthenticated(permissions.BasePermission):

    def has_permission(self, request , view):
        return request.user and request.user.is_authenticated
    
#initier un transfert d'argent
class IsUser(permissions.BasePermission):
    """
    Permission spécifique aux utilisateurs : vérifie que l'utilisateur est un utilisateur régulier.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'user'
    

#a le controle total sur toute l'application 
class IsAdmin(permissions.BasePermission):
    """
    Permission spécifique aux administrateurs : permet d'effectuer des actions de gestion.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'admin'
    


class IsTransactionOperator(permissions.BasePermission):
    """
    Permission spécifique aux opérateurs de transaction.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'operator'
    


class  CanUpdateTransaction(permissions.BasePermission):
    """
    Permet uniquement à l'opérateur de transaction de mettre à jour une transaction.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'operator'


    def has_object_permission(self, request, view, obj):
        # Ici, obj est l'instance de la transaction
        # Tu peux définir des règles plus complexes ici, par exemple, vérifier si l'utilisateur a un lien avec la transaction
        return obj.created_by == request.user or request.user.role == 'admin'
    


class AuthorPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ["GET", "OPTIONS" , "HEAD"]:
            return True
        if obj.operator == request.user:
            return True
        return False


class AuthorProfilePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ["GET", "OPTIONS" , "HEAD"]:
            return True
        if  request.method in ["PUT" ,  "PATCH" , "DELETE"]:
            if obj.user == request.user:
                return True
            return False
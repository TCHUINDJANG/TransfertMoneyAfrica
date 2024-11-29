from django.db.models .signals import post_save , pre_save , post_delete , pre_delete , m2m_changed
from django.dispatch import receiver
from .models import UserRegistrationModel
from accounts.models import Profile 



#lorke tu cree un utilisateur ca signale dans la table profile directement
@receiver(post_save , sender = UserRegistrationModel)
def create_profile_on_registration(sender , instance , created ,**kwargs):
        print("Je suis dans le signal")
        user = instance
        if created:
            try:
                Profile.objects.create(user = user)
                print("J'a fini de creer le profil")
            except ValueError:
                 pass
            
@receiver(post_save, sender=UserRegistrationModel)
def save_user_profil(ender, instance, **kwargs):
     instance.profile.save()

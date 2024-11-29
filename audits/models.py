from django.db import models
from accounts.models import Base_cash_send
from django.contrib.auth import get_user_model 


User = get_user_model()


class Operations(Base_cash_send):
    result_of_the_operation = models.CharField(max_length=50)
    status_of_the_operation = models.BooleanField(default=False)
    duration_of_the_operation = models.DurationField(default=0)
    description_of_the_operation = models.TextField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    

    class Meta:
            ordering = ['-date_of_creation'] 

    def __str__(self):
             return self.date_of_creation

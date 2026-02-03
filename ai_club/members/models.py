from django.db import models
from django.conf import settings
# Create your models here.


User = settings.AUTH_USER_MODEL

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    join_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username

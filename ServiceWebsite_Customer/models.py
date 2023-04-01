from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Register(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

    class Meta:
        verbose_name = "申請註冊"
        verbose_name_plural = "申請註冊"

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.username

# class Userinformation(models.Model):
#     user = models.OneToOneField(User, related_name='Userlink', on_delete=models.CASCADE)
#     bouns = models.IntegerField(default=0)

#     class Meta:
#         verbose_name = "使用者資訊"
#         verbose_name_plural = "使用者資訊"

#     def __str__(self):
#         """String for representing the MyModelName object (in Admin site etc.)."""
#         return self.user.username
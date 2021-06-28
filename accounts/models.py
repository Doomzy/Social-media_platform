from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

class UserProfile(models.Model):
    email= models.EmailField()
    f_name= models.CharField(max_length=20)
    l_name= models.CharField(max_length=20)
    fullName=models.CharField(max_length=40, blank=True, null=True)
    user= models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    pfp= models.ImageField(validators=[FileExtensionValidator(['jpg'])], default="placeholder.jpg", upload_to= 'pfp', verbose_name='Profile Picture')
    pgp= models.ImageField(validators=[FileExtensionValidator(['jpg'])], default="placeholder.jpg", upload_to= 'pgp', verbose_name='Background Picture')
    bio = models.TextField(max_length=500, blank=True)
    b_date = models.DateField()
    gender = models.CharField(max_length=1)

    def __str__(self):
        return self.user.username
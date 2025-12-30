from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# from phonenumber_field.phonenumber import PhoneNumber
# from phonenumber_field.validators import validate_international_phonenumber

# phone = PhoneNumber.from_string(phone_number='03001234567', region='PK')
# print(phone.is_valid())  # True
# print(str(phone)) 

# Create your models here.

class Contact (models.Model):
    # user = models.ForeignKey(User, on_delete=models.SET_NULL , null= True, blank=True)
    name = models.CharField(max_length=15)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=11)
    message = models.TextField()

    

    # class Meta:
    #     verbose_name = _("")
    #     verbose_name_plural = _("s")
    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse("_detail", kwargs={"pk": self.pk}



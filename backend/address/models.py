from django.db import models

# Create your models here.
class UserData(models.Model):
    email = models.EmailField(unique=True, max_length=254)

    def __str__(self):
        return self.email

class UserAttribute(models.Model):
    email = models.ForeignKey(UserData, on_delete=models.CASCADE, related_name='attributes')
    streetNo = models.CharField(max_length=200, null=True)
    streetName = models.CharField(max_length=200, null=True)
    postcode = models.CharField(max_length=200, null=True)
    existingBusinesses = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.email.email} - {self.streetName}"
from django.db import models

# Create your models here.
class Address(models.Model):
  address = models.CharField(max_length=200, null=True)
  city = models.CharField(max_length=200, null=True)
  zipcode = models.CharField(max_length=200, null=True)
  date_created = models.DateTimeField(auto_now_add=True, null=True)

  def __str__(self):
    return self.address
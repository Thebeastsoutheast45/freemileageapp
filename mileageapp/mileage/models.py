from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

# Create your models here.
class Driver(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    city = models.CharField(max_length=150)
    state= models.CharField(max_length=200)



    def __str__(self):
        return str(self.name)

class Mileage(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    miles = models.DecimalField(max_digits=5, decimal_places=2)
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.miles)
from django.db import models

# Create your models here.
class Contact(models.Model):
     sno= models.AutoField(primary_key=True)
     name= models.CharField(max_length=30)
     email= models.EmailField(max_length=50)
     issue= models.TextField(max_length=200)
     phone= models.IntegerField(max_length = 10)
     timeStamp=models.DateTimeField(auto_now_add=True, blank=True)

     def __str__(self):
          return "Message from " + self.name + ' - ' + self.email
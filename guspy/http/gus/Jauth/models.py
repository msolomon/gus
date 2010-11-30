from django.db import models

class Jorans_Pending(models.Model):
	real_name=models.CharField(max_length=100)
	email=models.EmailField()
	desired_user=models.CharField(max_length=100)
	pw=models.CharField(max_length=100)
 

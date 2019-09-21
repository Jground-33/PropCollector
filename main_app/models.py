from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User
# Create your models here.


# equivalent to Toy
class Movie(models.Model):
  name = models.CharField(max_length=50)
  category = models.CharField(max_length=20)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('movies_detail', kwargs={'pk': self.pk})


# equivalent to Cat
class Prop(models.Model):
  name = models.CharField(max_length=100)
  movies = models.ManyToManyField(Movie)
  description = models.TextField(max_length=250)
  estimated_value = models.IntegerField()
  user = models.ForeignKey(User, on_delete=models.CASCADE)


  def __str__(self):
   return f"{self.name} ({self.pk})"

  def get_absolute_url(self):
    return reverse('detail', kwargs={'prop_id': self.pk})
  

# equivalent to feeding
class Bid(models.Model):
  date = models.DateField()
  amount = models.IntegerField()
  prop = models.ForeignKey(Prop, on_delete=models.CASCADE)
  
  def __str__(self): 
    return f"{self.get_amount_display()} on {self.date}"

  class Meta:
    ordering = ['amount']


class Photo(models.Model):
  url = models.CharField(max_length=200)
  prop = models.ForeignKey(Prop, on_delete=models.CASCADE)

  def __str__(self):
    return f"Photo for prop_id: {self.prop_id} @{self.url}"
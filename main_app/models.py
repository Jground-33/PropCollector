from django.db import models
from django.urls import reverse

# Create your models here.


# equivilent to Toy
class Movie(models.Model):
  name = models.CharField(max_length=50)
  category = models.CharField(max_length=20)
  premeire_date = models.DateField()

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('movies_detail', kwargs={'pk': self.pk})


# equivilent to Cat
class Prop(models.Model):
  name = models.CharField(max_length=100)
  movies = models.ManyToManyField(Movie)
  description = models.TextField(max_length=250)
  estimated_value = models.IntegerField()

  def __str__(self):
   return f"{self.name} ({self.pk})"

  def get_absolute_url(self):
    return reverse('detail', kwargs={'prop_id': self.pk})
  

  # equivelent to feeding
class Bid(models.Model):
  date = models.DateField()
  amount = models.IntegerField()
  prop = models.ForeignKey(Prop, on_delete=models.CASCADE)
  
  def __str__(self): 
    return f"{self.get_amount_display()} on {self.date}"

  class Meta:
    ordering = ['amount']

from django.contrib import admin
from .models import Prop, Movie, Photo, Bid

# Register your models here.
admin.site.register(Prop)
admin.site.register(Movie)
admin.site.register(Bid)
admin.site.register(Photo)
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
import boto3
import uuid
from .forms import BidForm
from .models import Prop, Movie, Photo
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'jag-prop-collector'


# View functions

class PropCreate(LoginRequiredMixin, CreateView):
  model = Prop
  fields = ['name', 'description', 'estimated_value']

  def form_valid(self, form):
    # Assign the logged in user (self.request.user)
    form.instance.user = self.request.user
    print(form)
    return super().form_valid(form)

class PropUpdate(LoginRequiredMixin, UpdateView):
  model = Prop
  fields = ['name', 'description', 'estimated_value']

class PropDelete(LoginRequiredMixin, DeleteView):
  model = Prop
  success_url = '/props/'

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def props_index(request):
  props = Prop.objects.filter(user = request.user)
  return render(request, 'props/index.html', {'props': props})

@login_required
def props_detail(request, prop_id):
  prop = Prop.objects.get(id=prop_id)
  movies_prop_doesnt_have = Movie.objects.exclude(id__in = prop.movies.all().values_list('id'))
  bid_form = BidForm()
  return render(request, 'props/detail.html', {
    'prop': prop,
    'bid_form': bid_form,
    'movies': movies_prop_doesnt_have,
    })

@login_required
def add_bid(request, prop_id):
  form = BidForm(request.POST)
  if form.is_valid():
    new_bid = form.save(commit=False)
    new_bid.prop_id = prop_id
    new_bid.save()
    return redirect('detail', prop_id=prop_id)

class MovieList(LoginRequiredMixin, ListView):
  model = Movie

class MovieDetail(LoginRequiredMixin, DetailView):
  model = Movie

class MovieCreate(LoginRequiredMixin, CreateView):
  model = Movie
  fields = '__all__'

class MovieUpdate(LoginRequiredMixin, UpdateView):
  model = Movie
  fields = ['name', 'category']

class MovieDelete(LoginRequiredMixin, DeleteView):
  model = Movie
  success_url = '/movies/'

@login_required
def assoc_movie(request, prop_id, movie_id):
  Prop.objects.get(id=prop_id).movies.add(movie_id)
  return redirect('detail', prop_id=prop_id)

@login_required
def unassoc_movie(request, prop_id, movie_id):
  Prop.objects.get(id=prop_id).movies.remove(movie_id)
  return redirect('detail', prop_id=prop_id)

@login_required
def add_photo(request, prop_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Photo(url=url, prop_id=prop_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', prop_id=prop_id)


def signup(request): 
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)
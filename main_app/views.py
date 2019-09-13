from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Prop, Movie
from .forms import BidForm

# View functions

class PropCreate(CreateView):
  model = Prop
  fields = '__all__'

class PropUpdate(UpdateView):
  model = Prop
  fields = ['movie', 'description', 'estimated_value']

class PropDelete(DeleteView):
  model = Prop
  success_url = '/props/'

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def props_index(request):
  props = Prop.objects.all()
  return render(request, 'props/index.html', {'props': props})

def props_detail(request, prop_id):
  prop = Prop.objects.get(id=prop_id)
  bid_form = BidForm()
  return render(request, 'props/detail.html', {
    'prop': prop,
    'bid_form': bid_form
    })

def add_bid(request, prop_id):
  form = BidForm(request.POST)
  if form.is_valid():
    new_bid = form.save(commit=False)
    new_bid.prop_id = prop_id
    new_bid.save()
    return redirect('detail', prop_id=prop_id)

class MovieList(ListView):
  model = Movie

class MovieDetail(DetailView):
  model = Movie
class MovieCreate(CreateView):
  model = Movie
  fields = '__all__'

class MovieUpdate(UpdateView):
  model = Movie
  fields = ['name', 'color']

class MovieDelete(DeleteView):
  model = Movie
  success_url = '/movies/'

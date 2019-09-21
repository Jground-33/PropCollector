from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),

  path('props/', views.props_index, name='index'),
  path('props/<int:prop_id>/', views.props_detail, name='detail'),
  path('props/create/', views.PropCreate.as_view(), name='props_create'),
  path('props/<int:pk>/update/', views.PropUpdate.as_view(), name='props_update'),
  path('props/<int:pk>/delete/', views.PropDelete.as_view(), name='props_delete'),
  path('props/<int:prop_id>/add_bid/', views.add_bid, name='add_bid'),

  path('props/<int:prop_id>/assoc_movie/<int:movie_id>/', views.assoc_movie, name='assoc_movie'),
  path('props/<int:prop_id>/unassoc_movie/<int:movie_id>/', views.unassoc_movie, name='unassoc_movie'),
  path('props/<int:prop_id>/add_photo/', views.add_photo, name='add_photo'),
  
  path('movies/', views.MovieList.as_view(), name='movies_index'),
  path('movies/<int:pk>/', views.MovieDetail.as_view(), name='movies_detail'),
  path('movies/create/', views.MovieCreate.as_view(), name='movies_create'),
  path('movies/<int:pk>/update/', views.MovieUpdate.as_view(), name='movies_update'),
  path('movies/<int:pk>/delete/', views.MovieDelete.as_view(), name='movies_delete'),
  path('accounts/signup/', views.signup, name='signup'),
]
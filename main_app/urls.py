from django.urls import path
from . import views

urlpatterns = [
      path('', views.home, name='home'),
      path('about/', views.about, name='about'),
      path('restaurants/', views.restaurants_index, name='index'),
      path('restaurants/<int:restaurant_id>/', views.restaurants_detail, name='detail'),
      path('restaurants/create/', views.RestaurantCreate.as_view(), name='restaurants_create'),
      path('accounts/signup/', views.signup, name='signup'),
      path('restaurants/<int:pk>/delete/', views.RestaurantDelete.as_view(), name='restaurants_delete'),
      path('restaurants/<int:pk>/update/', views.RestaurantUpdate.as_view(), name='restaurants_update'),
      path('restaurants/<int:restaurant_id>/add_review/', views.add_review, name='add_review'),
      path('restaurants/<int:restaurant_id>/reviews/<int:pk>/edit', views.ReviewUpdate.as_view(), name='edit_review'),
      path('restaurants/<int:restaurant_id>/reviews/<int:pk>/delete', views.ReviewDelete.as_view(), name='delete_review'),

      path('cats/<int:restaurant_id>/add_photo/', views.add_photo, name='add_photo'),
]
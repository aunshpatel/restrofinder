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
      path('restaurants/<int:restaurant_id>/add_photo/', views.add_photo, name='add_photo'),
      path('restaurants/<int:restaurant_id>/photos/<int:pk>/delete', views.ImageDelete.as_view(), name='delete_photo'),
      path('my_wishlist/', views.my_wishlist, name='my_wishlist'),
      path('wishlists/', views.wishlists, name='wishlists'),
      path('restaurants/<int:restaurant_id>/add_to_wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
      path('restaurants/<int:restaurant_id>/remove_from_wishlist/', views.remove_from_wishlist, name='remove_from_wishlist'),
]
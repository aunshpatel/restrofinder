from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse
from .models import Restaurant, Review, Photo, Wishlist
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import boto3, uuid, os
from urllib.parse import urlparse

# Create your views here.
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def restaurants_index(request):
  restaurants = Restaurant.objects.all()
  for restaurant in restaurants:
    reviews = restaurant.review_set.all()
    if reviews.exists():
      restaurant.avg_rating = sum(review.rating for review in reviews) / len(reviews)
    else:
      restaurant.avg_rating = 0
  
  return render(request, 'restaurants/index.html', {
    'restaurants': restaurants
  })

def restaurants_detail(request, restaurant_id):
  restaurant = Restaurant.objects.get(id=restaurant_id)
  review_form = ReviewForm()
  reviews = restaurant.review_set.all()

  avg_rating = 0
  if reviews.exists:
    avg_rating = sum(review.rating for review in reviews) / len(reviews)
  
  return render(request, 'restaurants/detail.html', {
    'restaurant': restaurant, 
    'review_form': review_form,
    'avg_rating': avg_rating
  })

class RestaurantCreate(LoginRequiredMixin, CreateView):
  model = Restaurant
  fields = ['name', 'address', 'description', 'opening_time', 'closing_time']
  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)
  
class RestaurantDelete(LoginRequiredMixin, DeleteView):
  model = Restaurant
  success_url = '/restaurants' 

 
class RestaurantUpdate(LoginRequiredMixin, UpdateView):
  model = Restaurant
  fields = ['name', 'address', 'description', 'opening_time', 'closing_time']

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    print(form)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

@login_required
def add_review(request, restaurant_id):
    form = ReviewForm(request.POST)
    if form.is_valid():
      new_review = form.save(commit=False)
      new_review.restaurant_id = restaurant_id
      new_review.user_id = request.user.id
      new_review.save()
    
    return redirect('detail', restaurant_id=restaurant_id)

class ReviewUpdate(LoginRequiredMixin, UpdateView):
  model = Review
  form_class = ReviewForm
  template_name = 'main_app/edit_review.html'

  def get_success_url(self):
        restaurant_id = self.object.restaurant.id
        return reverse('detail', kwargs={'restaurant_id': restaurant_id})
  
class ReviewDelete(LoginRequiredMixin, DeleteView):
  model = Review
  template_name = 'main_app/review_confirm_delete.html'
  
  def get_success_url(self):
        restaurant_id = self.object.restaurant.id
        return reverse('detail', kwargs={'restaurant_id': restaurant_id})
  

def add_photo(request, restaurant_id):
  # photo-file will be the "name" attribute on the <input type="file">
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    # need a unique "key" for S3 / needs image file extension too
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    # just in case something goes wrong
    try:
      bucket = os.environ['S3_BUCKET']
      s3.upload_fileobj(photo_file, bucket, key)
      url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
      Photo.objects.create(url=url, restaurant_id=restaurant_id, user_id=request.user.id)
    except Exception as e:
      print('An error occurred uploading file to S3')
      print(e)
  return redirect('detail', restaurant_id=restaurant_id)

class ImageDelete(LoginRequiredMixin, DeleteView):
  model = Photo
  template_name = 'main_app/image_confirm_delete.html'
  def get_success_url(self):
    restaurant_id = self.object.restaurant.id
    name = self.object.url.split('/')[-1]

    s3_client = boto3.client("s3")
    response = s3_client.delete_object(Bucket='restrofinder-aunsh', Key=name)
    print(f'response:{response}')
    return reverse('detail', kwargs={'restaurant_id': restaurant_id})

@login_required
def my_wishlist(request):
    user_wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    return render(request, 'main_app/my_wishlist.html', {'user_wishlist': user_wishlist})

def wishlists(request):
    all_wishlists = Wishlist.objects.all()
    return render(request, 'main_app/wishlists.html', {'all_wishlists': all_wishlists})

@login_required
def add_to_wishlist(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    user_wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    user_wishlist.restaurants.add(restaurant)
    return redirect('my_wishlist')

@login_required
def remove_from_wishlist(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    user_wishlist = get_object_or_404(Wishlist, user=request.user)
    user_wishlist.restaurants.remove(restaurant)
    return redirect('my_wishlist')

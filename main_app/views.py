from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.views.generic import ListView, DetailView
from .models import Restaurant, Review, Photo
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import boto3, uuid, os

# Create your views here.
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def restaurants_index(request):
  restaurants = Restaurant.objects.all()
  return render(request, 'restaurants/index.html', {
    'restaurants': restaurants
  })

def restaurants_detail(request, restaurant_id):
  restaurant = Restaurant.objects.get(id=restaurant_id)
  print(restaurant)
  review_form = ReviewForm()
  return render(request, 'restaurants/detail.html', {
    'restaurant': restaurant, 
    'review_form': review_form 
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
      # build the full url string
      url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
      # we can assign to restaurant_id or cat (if you have a cat object)
      Photo.objects.create(url=url, restaurant_id=restaurant_id, user_id=request.user.id)
    except Exception as e:
      print('An error occurred uploading file to S3')
      print(e)
  return redirect('detail', restaurant_id=restaurant_id)
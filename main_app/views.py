from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Restaurant
from .forms import ReviewForm

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

class RestaurantCreate(CreateView):
  model = Restaurant
  fields = ['name', 'address', 'description', 'opening_time', 'closing_time']
  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)
  
class RestaurantDelete(DeleteView):
  model = Restaurant
  success_url = '/restaurants'

 
class RestaurantUpdate(UpdateView):
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


def add_review(request, restaurant_id):
    form = ReviewForm(request.POST)
    if form.is_valid():
      new_review = form.save(commit=False)
      new_review.restaurant_id = restaurant_id
      new_review.user_id = request.user.id
      new_review.save()
    
    return redirect('detail', restaurant_id=restaurant_id)
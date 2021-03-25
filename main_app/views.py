from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.http import HttpResponse, HttpResponseRedirect

# import models
from .models import Cat
# access the FeedingForm
from .forms import FeedingForm, CatForm

# import Django form classes
# these handle CRUD for us
# we will comment this one out
class CatCreate(CreateView):
  model = Cat
  fields = '__all__'
  success_url = '/cats'

class CatUpdate(UpdateView):
  model = Cat
  fields = ['name', 'breed', 'description', 'age']

  def form_valid(self, form):
    self.object = form.save(commit=False)
    self.object.save()
    return HttpResponseRedirect('/cats/' + str(self.object.pk))

class CatDelete(DeleteView):
  model = Cat
  success_url = '/cats'


# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')


# CATS
def cats_index(request):
    cats = Cat.objects.all()
    return render(request, 'cats/index.html', { 'cats': cats })

def cats_show(request, cat_id):
    # we get access to that cat_id variable
    # query for the specific cat clicked
    cat = Cat.objects.get(id=cat_id)
    # lets make a feeding_form
    feeding_form = FeedingForm()
    return render(request, 'cats/show.html', { 
      'cat': cat,
      'feeding_form': feeding_form 
    })

# build out cats_create custom to use the userId

# FEEDING
def add_feeding(request, pk):
  # this time we are passing the data from our request in that form
  form = FeedingForm(request.POST)
  # validate form.is_valid built in
  if form.is_valid():
    # don't save yet!! First lets add out cat_id
    new_feeding = form.save(commit=False)
    new_feeding.cat_id = pk
    # cats been added we can save
    new_feeding.save()
  return redirect('cats_show', cat_id = pk)

# Instrcutions
# 1. Update index view function to look similar to the contact view function
# 2. Add a index.html page with the current HTML that is displayed
# 3. Update about view function to look similar to the contact view function
# 4. Add a about.html page with the current HTML that is displayed
# 5. Update your urls.py file (main_app) to look similar to the contact path

# 1. Make a view function
# 2. Make the html page
# 3. Add the view to the urls.py inside of main_app.urls

# In browser
# When I go to localhost:8000/contact
# Django -> urls -> /contact -> vews.contact (runs function) -> templates -> contact.html

from django.shortcuts import render
from .models import Hero, About, Category, Work

# Create your views here.

def service_view(request):
    return render(request, 'service.html')  # Path remains the same

def index_view(request):
    hero_data = Hero.objects.all()
    about_data = About.objects.first()  # Assuming only one "About" entry is needed
    categories = Category.objects.all().order_by('position')  # Fetch categories ordered by position
    works = Work.objects.all()  # Fetch all works
    return render(request, 'index.html', {
        'hero_data': hero_data,
        'about_data': about_data,
        'categories': categories,
        'works': works
    })

def gears_view(request):
    return render(request, 'gears.html')  # Path remains the same

def contact_us_view(request):
    return render(request, 'contact-us.html')  # Path remains the same

def blog_view(request):
    return render(request, 'blog.html')  # Path remains the same

def about_us_view(request):
    return render(request, 'about-us.html')  # Path remains the same

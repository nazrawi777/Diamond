from django.shortcuts import render

# Create your views here.

def service_view(request):
    return render(request, 'service.html')  # Path remains the same

def index_view(request):
    return render(request, 'index.html')  # Path remains the same

def gears_view(request):
    return render(request, 'gears.html')  # Path remains the same

def contact_us_view(request):
    return render(request, 'contact-us.html')  # Path remains the same

def blog_view(request):
    return render(request, 'blog.html')  # Path remains the same

def about_us_view(request):
    return render(request, 'about-us.html')  # Path remains the same

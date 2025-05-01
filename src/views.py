from django.shortcuts import render
from .models import Hero,Blog, About, Category, Work,ClientLogo,BlogCategory,GearCategory,Gear,TeamMember,Testimonial

# Create your views here.

def service_view(request):
    return render(request, 'service.html')  # Path remains the same

def index_view(request):
    hero_data = Hero.objects.all()
    about_data = About.objects.first()  # Assuming only one "About" entry is needed
    categories = Category.objects.all().order_by('position')  # Fetch categories ordered by position
    works = Work.objects.all()  # Fetch all works
    client_logs = ClientLogo.objects.all()
    return render(request, 'index.html', {
        'hero_data': hero_data,
        'about_data': about_data,
        'categories': categories,
        'works': works,
        'client_logs': client_logs,
    })

def gears_view(request):
    gears = Gear.objects.all()
    gear_category = GearCategory.objects.all()  # Fetch all gear categories
    return render(request, 'gears.html', {'gears': gears, 'gear_category': gear_category})  # Pass the fetched data to the template
    

def contact_us_view(request):
    return render(request, 'contact-us.html')  # Path remains the same

def blog_view(request):
    blogs = Blog.objects.select_related('category').all()  # Fetch blogs with their categories
    blog_category = BlogCategory.objects.all()  # Fetch all blog categories
    return render(request, 'blog.html', {'blogs': blogs , 'blog_category': blog_category})

def about_us_view(request):
    team_members = TeamMember.objects.all()
    testimonials = Testimonial.objects.all()
    return render(request, 'about-us.html', { 'team_members':team_members , 'testimonials':testimonials})  # Path remains the same


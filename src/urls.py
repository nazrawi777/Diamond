from django.urls import path  # type: ignore
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('service/', views.service_view, name='service'),
    path('gears/', views.gears_view, name='gears'),
    path('contact-us/', views.contact_us_view, name='contact_us'),
    path('blog/', views.blog_view, name='blog'),
    path('about-us/', views.about_us_view, name='about_us'),
]
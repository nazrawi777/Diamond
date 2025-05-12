from django.urls import path  # type: ignore
from django.conf import settings
from django.conf.urls.static import static
from . import views

from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap, BlogSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'blogs': BlogSitemap,
}

urlpatterns = [
    path('', views.index_view, name='index'),
    path('service/', views.service_view, name='service'),
    path('gears/', views.gears_view, name='gears'),
    path('contact-us/', views.contact_us_view, name='contact_us'),
    path('blog/', views.blog_view, name='blog'),
    path('about-us/', views.about_us_view, name='about_us'),
     path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
] 

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
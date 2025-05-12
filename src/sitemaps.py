from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Blog

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return ['index_view', 'service_view', 'blog_view','contact_us_view','about_us_view','gears_view'] 

    def location(self, item):
        return reverse(item)

class BlogSitemap(Sitemap):
    priority = 0.8
    changefreq = 'daily'

    def items(self):
        return Blog.objects.all()

    def lastmod(self, obj):
        return obj.created_at
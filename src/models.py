from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Hero(models.Model):
    TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]

    title = models.CharField(max_length=255)
    subtitle = models.TextField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='video')  # Default set to 'video'
    image = models.ImageField(upload_to='hero/', blank=True, null=True)
    video = models.FileField(upload_to='hero/videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        from django.core.exceptions import ValidationError

        # Ensure only one of image or video is uploaded based on type
        if self.type == 'image' and not self.image:
            raise ValidationError("Please upload an image for type 'image'.")
        if self.type == 'video' and not self.video:
            raise ValidationError("Please upload a video for type 'video'.")
        if self.type == 'image' and self.video:
            raise ValidationError("Video should not be uploaded for type 'image'.")
        if self.type == 'video' and self.image:
            raise ValidationError("Image should not be uploaded for type 'video'.")

    def __str__(self):
        return self.title          

class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    position = models.PositiveIntegerField(default=0)  # Field for custom ordering
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name   
    
class Blog(models.Model):
    category = models.ForeignKey(
        BlogCategory,
        on_delete=models.CASCADE,
        related_name='blogs',
        default=1  # Set a default category ID
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='blog/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class About(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='about/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    position = models.PositiveIntegerField(default=0)  # Field for custom ordering
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Work(models.Model):
    TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='works')  # Updated to use ForeignKey
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='image')
    image = models.ImageField(upload_to='works/images/', blank=True, null=True)
    video = models.FileField(upload_to='works/videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ClientLogo(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='client_logos/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class TeamMember(models.Model):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    image = models.ImageField(upload_to='team_members/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Testimonial(models.Model):
    name = models.CharField(max_length=255)
    pdf = models.FileField(upload_to='testimonials/pdfs/', blank=True, null=True)
    image = models.ImageField(upload_to='testimonials/images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class GearCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Gear(models.Model):
    category = models.ForeignKey(GearCategory, on_delete=models.CASCADE, related_name='gears')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='gears/images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


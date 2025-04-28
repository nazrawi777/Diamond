import os
import django
from django.core.files import File

# Setup Django
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dimond.settings')  # Replace 'your_project_name'
django.setup()

from src.models import Hero, Blog, About, Category, Work, ClientLogo, TeamMember, Testimonial, GearCategory, Gear

from django.conf import settings

def get_file(path):
    try:
        return File(open(path, 'rb'))
    except FileNotFoundError:
        print(f"File not found: {path}")
        return None

def seed():
    # --- Hero ---
    hero_data = [
        ('hero1.jpg', 'Hero Title 1', 'Hero Subtitle 1'),
        ('hero2.jpg', 'Hero Title 2', 'Hero Subtitle 2'),
    ]

    for img, title, subtitle in hero_data:
        img_path = os.path.join(settings.BASE_DIR, 'src', 'static', 'images', img)
        hero = Hero(title=title, subtitle=subtitle)
        img_file = get_file(img_path)
        if img_file:
            hero.image.save(os.path.basename(img_path), img_file, save=False)
        hero.save()

    # --- Blog ---
    blog_data = [
        ('blog1.jpg', 'Blog Title 1', 'Blog Content 1'),
        ('blog2.jpg', 'Blog Title 2', 'Blog Content 2'),
    ]

    for img, title, content in blog_data:
        img_path = os.path.join(settings.BASE_DIR, 'src', 'static', 'images', img)
        blog = Blog(title=title, content=content)
        img_file = get_file(img_path)
        if img_file:
            blog.image.save(os.path.basename(img_path), img_file, save=False)
        blog.save()

    # --- About ---
    about_data = [
        ('about1.jpg', 'About Title 1', 'About Description 1'),
        ('about2.jpg', 'About Title 2', 'About Description 2'),
    ]

    for img, title, desc in about_data:
        img_path = os.path.join(settings.BASE_DIR, 'src', 'static', 'images', img)
        about = About(title=title, description=desc)
        img_file = get_file(img_path)
        if img_file:
            about.image.save(os.path.basename(img_path), img_file, save=False)
        about.save()

    # --- Category ---
    categories = [
        'Photography',
        'Videography',
        'Drone Shots',
    ]

    category_objs = []
    for name in categories:
        category = Category(name=name)
        category.save()
        category_objs.append(category)

    # --- Work ---
    work_data = [
        ('work1.jpg', 'Work Title 1', 'Work Desc 1', 'image'),
        ('work2.jpg', 'Work Title 2', 'Work Desc 2', 'image'),
    ]

    for img, title, desc, type_ in work_data:
        img_path = os.path.join(settings.BASE_DIR, 'src', 'static', 'images', img)
        work = Work(
            title=title,
            description=desc,
            type=type_,
            content_type=ContentType.objects.get_for_model(Category),  # Dummy
            object_id=category_objs[0].id  # Dummy
        )
        img_file = get_file(img_path)
        if img_file:
            work.image.save(os.path.basename(img_path), img_file, save=False)
        work.save()

    # --- Client Logos ---
    logo_data = [
        ('logo1.png', 'Client 1'),
        ('logo2.png', 'Client 2'),
    ]

    for img, name in logo_data:
        img_path = os.path.join(settings.BASE_DIR, 'src', 'static', 'images', img)
        client = ClientLogo(name=name)
        img_file = get_file(img_path)
        if img_file:
            client.logo.save(os.path.basename(img_path), img_file, save=False)
        client.save()

    # --- Team Members ---
    team_data = [
        ('team1.jpg', 'Member 1', 'Photographer'),
        ('team2.jpg', 'Member 2', 'Editor'),
    ]

    for img, name, role in team_data:
        img_path = os.path.join(settings.BASE_DIR, 'src', 'static', 'images', img)
        member = TeamMember(name=name, role=role)
        img_file = get_file(img_path)
        if img_file:
            member.image.save(os.path.basename(img_path), img_file, save=False)
        member.save()

    # --- Testimonials ---
    testimonial_data = [
        ('testimonial1.jpg', 'testimonial1.pdf', 'John Doe'),
        ('testimonial2.jpg', 'testimonial2.pdf', 'Jane Smith'),
    ]

    for img, pdf, name in testimonial_data:
        img_path = os.path.join(settings.BASE_DIR, 'src', 'static', 'images', img)
        pdf_path = os.path.join(settings.BASE_DIR, 'src', 'static', 'pdfs', pdf)
        testimonial = Testimonial(name=name)
        img_file = get_file(img_path)
        pdf_file = get_file(pdf_path)
        if img_file:
            testimonial.image.save(os.path.basename(img_path), img_file, save=False)
        if pdf_file:
            testimonial.pdf.save(os.path.basename(pdf_path), pdf_file, save=False)
        testimonial.save()

    # --- Gear Category and Gear ---
    gear_categories = [
        'Cameras',
        'Drones',
    ]

    for name in gear_categories:
        gear_cat = GearCategory(name=name)
        gear_cat.save()

        gear = Gear(
            category=gear_cat,
            name=f"{name} Gear",
            description=f"Best {name.lower()} gear"
        )
        # You can add image if needed the same way
        gear.save()

if __name__ == "__main__":
    seed()

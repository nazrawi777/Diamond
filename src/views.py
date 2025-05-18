from django.shortcuts import render, redirect
from .models import Hero,Blog, About, Category, Work,ClientLogo,BlogCategory,GearCategory,Gear,TeamMember,Testimonial
import base64
import os
from django.contrib import messages
from django.conf import settings
from .forms import ChatForm
from google import genai
from google.genai import types # type: ignore


def service_view(request):
    request.session['current_page'] = 'service'
    request.session['current_template'] = 'service.html'
    return render(request, 'service.html')  # Path remains the same

def index_view(request):
    request.session['current_page'] = 'index'
    request.session['current_template'] = 'index.html'
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
    request.session['current_page'] = 'gears'
    request.session['current_template'] = 'gears.html'
    gears = Gear.objects.all()
    gear_category = GearCategory.objects.all()  # Fetch all gear categories
    return render(request, 'gears.html', {'gears': gears, 'gear_category': gear_category})  # Pass the fetched data to the template
    

def contact_us_view(request):
    request.session['current_page'] = 'contact_us'
    request.session['current_template'] = 'contact-us.html'
    client_logs = ClientLogo.objects.all()
    return render(request, 'contact-us.html',{'client_logs': client_logs})  # Path remains the same

def blog_view(request):
    request.session['current_page'] = 'blog'
    request.session['current_template'] = 'blog.html'
    blogs = Blog.objects.select_related('category').all()  # Fetch blogs with their categories
    blog_category = BlogCategory.objects.all()  # Fetch all blog categories
    return render(request, 'blog.html', {'blogs': blogs , 'blog_category': blog_category})

def about_us_view(request):
    request.session['current_page'] = 'about_us'
    request.session['current_template'] = 'about-us.html'
    team_members = TeamMember.objects.all()
    testimonials = Testimonial.objects.all()
    return render(request, 'about-us.html', { 'team_members':team_members , 'testimonials':testimonials})  # Path remains the sam
    
    
    

def chat_view(request):
    # Configure Gemini API
    client = genai.Client(
        api_key=settings.GEMINI_API_KEY,
    )

    # Initialize chat history in session
    if 'chat_history' not in request.session:
        request.session['chat_history'] = [
            {
                'role': 'model',
                'parts': [{'text': 'Hey there! How can I help you today?'}]
            }
        ]

    chat_history = request.session['chat_history']
    show_chatbot = request.session.get('show_chatbot', True)

    if request.method == 'POST':
        form = ChatForm(request.POST, request.FILES)
        if form.is_valid():
            user_message = form.cleaned_data['message']
            user_file = form.cleaned_data['file']

            # Validate file size and type
            if user_file:
                if user_file.size > 5 * 1024 * 1024:  # 5MB limit
                    messages.error(request, 'File size exceeds 5MB.')
                    return render(request, 'chatbot/chatbot.html', {
                        'form': form,
                        'chat_history': chat_history,
                        'show_chatbot': show_chatbot
                    })
                if not user_file.content_type.startswith('image/'):
                    messages.error(request, 'Only image files are allowed.')
                    return render(request, 'chatbot/chatbot.html', {
                        'form': form,
                        'chat_history': chat_history,
                        'show_chatbot': show_chatbot
                    })

            # Prepare user message parts
            user_parts = [Part.from_text(text=user_message)]
            if user_file:
                file_content = user_file.read()
                mime_type = user_file.content_type
                file_base64 = base64.b64encode(file_content).decode('utf-8')
                user_parts.append(Part.from_data(data=file_base64, mime_type=mime_type))

            # Add user message to chat history
            chat_history.append({
                'role': 'user',
                'parts': user_parts
            })

            # Convert session history to Gemini API format
            contents = [
                types.Content(role=msg['role'], parts=[
                    types.Part.from_text(part['text']) if 'text' in part else types.Part.from_data(part['inline_data']['data'], part['inline_data']['mime_type'])
                    for part in msg['parts']
                ]) for msg in chat_history
            ]

            # Configure Gemini model
            model = genai.GenerativeModel('gemini-1.5-flash')
            config = types.GenerateContentConfig(
                response_mime_type='text/plain',
                system_instruction=[types.Part.from_text(text="You are a helpful chatbot for Diamond Marketing. Provide accurate and friendly responses.")]
            )

            try:
                # Generate response
                response = model.generate_content(
                    contents=contents,
                    generation_config=config
                )
                bot_response = response.text.strip()

                # Add bot response to chat history
                chat_history.append({
                    'role': 'model',
                    'parts': [{'text': bot_response}]
                })
                messages.success(request, 'Message sent successfully!')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
                bot_response = f"Error: {str(e)}"
                chat_history.append({
                    'role': 'model',
                    'parts': [{'text': bot_response}]
                })

            # Save updated chat history to session
            request.session['chat_history'] = chat_history
            request.session.modified = True

            return redirect(request.path or 'index')  # Redirect to current page
    else:
        form = ChatForm()

    return render(request, request.session.get('current_template', 'index.html'), {
        'form': form,
        'chat_history': chat_history,
        'show_chatbot': show_chatbot
    })

def toggle_chatbot(request):
    request.session['show_chatbot'] = not request.session.get('show_chatbot', True)
    request.session.modified = True
    return redirect(request.session.get('current_page', 'index'))

def clear_chat(request):
    request.session['chat_history'] = [
        {
            'role': 'model',
            'parts': [{'text': 'Hey there! How can I help you today?'}]
        }
    ]
    request.session.modified = True
    return redirect(request.session.get('current_page', 'index'))    
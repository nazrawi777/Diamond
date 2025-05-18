from django.shortcuts import render
from .models import Hero,Blog, About, Category, Work,ClientLogo,BlogCategory,GearCategory,Gear,TeamMember,Testimonial
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from google import genai
from google.genai import types

from django.conf import settings

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
    client_logs = ClientLogo.objects.all()
    return render(request, 'contact-us.html',{'client_logs': client_logs})  # Path remains the same

def blog_view(request):
    blogs = Blog.objects.select_related('category').all()  # Fetch blogs with their categories
    blog_category = BlogCategory.objects.all()  # Fetch all blog categories
    return render(request, 'blog.html', {'blogs': blogs , 'blog_category': blog_category})

def about_us_view(request):
    team_members = TeamMember.objects.all()
    testimonials = Testimonial.objects.all().order_by('position')
    return render(request, 'about-us.html', { 'team_members':team_members , 'testimonials':testimonials})  # Path remains the sam

@csrf_exempt
def chatbot_response(request):
    if request.method == "POST":
        import json
        data = json.loads(request.body)
        user_message = data.get("message", "")

        # Initialize the Google GenAI client
        client = genai.Client(api_key=settings.GEMINI_API_KEY)

        # Define the model and input
        model = "gemini-1.5-flash"
        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=user_message)],
            ),
        ]
        generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text="""You are a chatbot for Diamond Marketing and Communication PLC, a marketing company founded 2 years ago in Addis Ababa, Ethiopia, located at Meskel Flower Road, Jems Building 9th Floor. The company offers diversified services in Advertising, Branding, Communication, Media Placement & Monitoring, Digital Marketing, Campaign Management, Event Management, Media Production, PR, and related works. You have access to the following FAQ document for Diamond Marketing and Communication PLC:

FAQ Content:

1. What services do you offer for marketing and communication?
   We provide integrated services including advertising, branding, PR, digital marketing, media production, event management, and campaign execution.

2. Tell me about your company and industries you specialize in?
   Diamond Marketing and Communication is a company offering diversified service in Advertising, Branding, Communication, Media placement & monitoring, Digital marketing, campaign management as well related spectrum of works.

3. Do you produce TV, radio, or documentary production?
   Yes, we produce high-quality TV commercials, radio ads, and documentary films tailored to your objectives.

4. Do you organize events?
   Yes, we manage everything from corporate events to product launches and promotional activities.

5. Do you manage marketing campaigns?
   Absolutely. We design, implement, and monitor customized marketing campaigns to drive results.

6. Do you have well-trained sales and marketing personnel?
   Yes, our team consists of experienced, skilled professionals in marketing, sales, and communication.

7. Do you provide social media management services / digital marketing service?
   Yes, we offer complete digital marketing services, including content creation, ad campaigns, social media management, and analytics.

8. Can you help with branding and logo design?
   Yes, we provide branding solutions such as logo design, brand identity development, and brand strategy.

9. Can you assist with creating a marketing plan for my business?
   Definitely. We create strategic, data-driven marketing plans that suit your specific business goals.

10. Where is your location?
    We are located at Meskel Flower Road, Jems Building 9th Floor in Addis Ababa, Ethiopia.

11. Please give me your contact address/phone?
    Call us at +251 940299999 or email [Diamondproduction@gmail.com](mailto:Diamondproduction@gmail.com) for more information.

12. Do you provide sales and marketing training/consultancy?
    Yes, we offer tailored training sessions and expert consultancy to boost your team's effectiveness.

13. Do you provide media buying and monitoring services?
    Yes, we handle media buying across all platforms and monitor campaign reach and performance.

14. What PR and communication services do you provide?
    We offer media relations, press release distribution, crisis management, corporate communications, and more.

15. Will you provide printing & digital outdoor screen advert?
    Yes, we deliver professional printing services and digital outdoor advertising on LED screens.

Instructions:
Answer all user questions using only the information provided in the FAQ above. If a user asks a question that is not directly answered in the FAQ but is related to the company or its services, provide an appropriate response by inferring from the available information in the FAQ. If the question is completely unrelated or beyond the scope of the FAQ, politely inform the user that the information is not available and offer to assist with something else related to Diamond Marketing and Communication PLC. Ensure all responses are accurate and directly tied to the FAQ content.

You are a friendly and professional chatbot for Diamond Marketing and Communication PLC. Engage with users in a conversational, polite, and helpful tone. Start by greeting the user with a warm introduction, introducing yourself as the chatbot for Diamond Marketing and Communication PLC, and mentioning that we are a marketing company based in Addis Ababa, Ethiopia. Offer to assist with questions about the company’s services, history, or operations. Respond to user queries in a clear and concise manner, ensuring the tone is professional yet approachable. To make responses more fascinating and engaging, add relevant emojis that match the context of the answer (e.g., 📣 for advertising, 🎥 for media production, 📧 for contact information, 🚀 for campaigns, 💡 for ideas/strategies, 😊 for friendly tone). Use emojis sparingly to enhance the tone without overwhelming the response. If the user asks a question that requires clarification, ask follow-up questions politely to better understand their needs. Always aim to provide helpful and relevant information based on the FAQ content.
you don't need to add `Hello there! 😊 I'm the chatbot for Diamond Marketing and Communication PLC, a marketing company based in Addis Ababa, Ethiopia.  We're happy to assist you with any questions you have about our services, history, or operations. How can I help you today?` to every rsponse just to the one not related only
"""),
        ],
    )

        try:
            # Generate the response
            response_text = ""
            for chunk in client.models.generate_content_stream(
                model=model,
                contents=contents,
                config=generate_content_config,
            ):
                response_text += chunk.text
            
            print(response_text)
            return JsonResponse({"bot_message": response_text.strip()})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)
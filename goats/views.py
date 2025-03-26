from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from rest_framework.decorators import api_view
from rest_framework import viewsets
from .models import Goat # Import your Goat model
from .serializers import GoatSerializer
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.contrib.auth import logout
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView

# Frontend views
def home(request):
    """Render the home page."""
    return render(request, 'goats/home.html')

def inventory(request):
    """Render the inventory page."""
    return render(request, 'goats/inventory.html')

def tree(request):
    """Render the family tree page."""
    return render(request, 'goats/tree.html')

def reports(request):
    # Fetch data for the reports page (e.g., all goats)
    goats = Goat.objects.all()
    
    # Pass the data to the template
    context = {
        'goats': goats,
    }
    return render(request, 'goats/reports.html', context)

def about(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Construct the email message
        email_message = f"""
        Name: {name}
        Email: {email}
        Subject: {subject}
        Message: {message}
        """

        # Send the email
        send_mail(
            subject,  # Subject of the email
            email_message,  # Body of the email
            settings.EMAIL_HOST_USER,  # From email
            ['goatpedigree34@gmail.com'],  # To email
            fail_silently=False,
        )

        # Add a success message
        messages.success(request, 'Your message has been sent successfully!')
        return redirect('about')  # Redirect to the same page after sending the email

    return render(request, 'goats/about.html')

# Custom login up and logout views
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')  # Redirect to the home page after signup
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to the home page after login
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

# Custom admin section
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

# Custom logout view
class CustomLogoutView(LogoutView):
    template_name = 'admin/logout.html'  # Redirect to the home page after logout

# Custom 404 Page
def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

# API views
@api_view(['GET'])
def get_goat_data(request):
    """API endpoint to retrieve goat data."""
    goats = Goat.objects.all()
    serializer = GoatSerializer(goats, many=True, context={'request': request})
    return JsonResponse(serializer.data, safe=False)


class GoatViewSet(viewsets.ModelViewSet):
    serializer_class = GoatSerializer
    queryset = Goat.objects.all().select_related(
        'father', 'mother'
    ).prefetch_related(
        'father_children', 'mother_children'
    ).order_by('-birth_date')

    def get_serializer_context(self):
        """Add request context to serializer."""
        return {'request': self.request}


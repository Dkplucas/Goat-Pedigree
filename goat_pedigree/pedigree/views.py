from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Count, Avg, F, ExpressionWrapper, fields
from django.utils import timezone
from .models import Goat
import json
import logging

logger = logging.getLogger(__name__)

# Home Page
def home(request):
    return render(request, 'pedigree/home.html')

# Goat Profiles Page
@login_required
def goat_profiles(request):
    goats = Goat.objects.all()
    return render(request, 'pedigree/goat_profiles.html', {'goats': goats})

# Pedigree Charts Page
@login_required
def pedigree_charts(request):
    # Fetch all goats for the dropdown
    goats = Goat.objects.all()

    # Get the selected goat ID from the request
    selected_goat_id = request.GET.get('goat_id')

    # If a goat is selected, fetch its pedigree
    if selected_goat_id:
        selected_goat = get_object_or_404(Goat, id=selected_goat_id)  # Fetch goat or raise 404
    else:
        selected_goat = None

    # Function to recursively build the pedigree
    def build_pedigree(goat):
        if not goat:
            return None
        return {
            "name": goat.name,
            "id": goat.id,
            "sire": build_pedigree(goat.sire) if goat.sire else None,
            "dam": build_pedigree(goat.dam) if goat.dam else None,
        }

    # Build the pedigree for the selected goat
    pedigree_data = []
    if selected_goat:
        pedigree_data.append(build_pedigree(selected_goat))

    # Pass the data to the template as JSON
    return render(request, 'pedigree/pedigree_charts.html', {
        'pedigree_data': json.dumps(pedigree_data),
        'goats': goats,
        'selected_goat_id': selected_goat_id,
    })

# About Page
def about(request):
    return render(request, 'pedigree/about.html')

# Reports Page
@login_required
def reports(request):
    try:
        # Total number of goats
        total_goats = Goat.objects.count()

        # Number of goats by breed
        goats_by_breed = Goat.objects.values('breed').annotate(count=Count('id')).order_by('-count')

        # Number of goats by gender
        goats_by_gender = Goat.objects.values('gender').annotate(count=Count('id')).order_by('-count')

        # Calculate average age of goats in Python
        today = timezone.now().date()
        goats_with_age = Goat.objects.exclude(birth_date__isnull=True).annotate(
            age_days=ExpressionWrapper(
                today - F('birth_date'),
                output_field=fields.DurationField()
            )
        )

        total_age_years = 0
        count = 0
        for goat in goats_with_age:
            age_days = goat.age_days.days  # Get the age in days
            age_years = age_days / 365.0  # Convert to years
            total_age_years += age_years
            count += 1

        average_age = total_age_years / count if count > 0 else 0

        # Pass the data to the template
        return render(request, 'pedigree/reports.html', {
            'total_goats': total_goats,
            'goats_by_breed': goats_by_breed,
            'goats_by_gender': goats_by_gender,
            'average_age': average_age,
        })
    except Exception as e:
        logger.error(f"Error in reports view: {e}")
        raise  # Re-raise the exception after logging
        
# Custom 404 Page
def custom_404(request, exception=None):
    return render(request, '404.html', status=404)

# Signup pages
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')  # Redirect to the login page after successful signup
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
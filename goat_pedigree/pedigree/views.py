from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.utils import timezone
from .models import Goat
import json

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
            "sire": build_pedigree(goat.sire),
            "dam": build_pedigree(goat.dam),
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
    # Total number of goats
    total_goats = Goat.objects.count()

    # Number of goats by breed
    goats_by_breed = Goat.objects.values('breed').annotate(count=Count('id')).order_by('-count')

    # Number of goats by gender
    goats_by_gender = Goat.objects.values('gender').annotate(count=Count('id')).order_by('-count')

    # Calculate average age of goats
    today = timezone.now().date()
    total_age = 0
    valid_goats = 0  # Count of goats with valid birth dates

    for goat in Goat.objects.all():
        if goat.birth_date:  # Check if birth_date is not None
            try:
                age = (today - goat.birth_date).days / 365  # Convert days to years
                total_age += age
                valid_goats += 1
            except (TypeError, ValueError):
                # Handle invalid birth_date format
                continue

    # Calculate average age only if there are goats with valid birth dates
    average_age = total_age / valid_goats if valid_goats > 0 else None

    # Pass the data to the template
    return render(request, 'pedigree/reports.html', {
        'total_goats': total_goats,
        'goats_by_breed': goats_by_breed,
        'goats_by_gender': goats_by_gender,
        'average_age': average_age,
    })

# Custom 404 Page
def custom_404(request, exception=None):
    return render(request, '404.html', status=404)
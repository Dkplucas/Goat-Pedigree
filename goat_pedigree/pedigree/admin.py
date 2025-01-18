# pedigree/admin.py
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Goat, HealthRecord, BreedingRecord
from .resources import GoatResource, HealthRecordResource, BreedingRecordResource

# Inline editing for BreedingRecord
class BreedingRecordInline(admin.TabularInline):  # or admin.StackedInline
    model = BreedingRecord
    fk_name = 'sire'  # Specify which ForeignKey to use
    extra = 1  # Number of empty forms to display

# Goat Admin with Import/Export and Inline Editing
class GoatAdmin(ImportExportModelAdmin):
    resource_class = GoatResource
    list_display = ('id', 'name', 'breed', 'gender', 'birth_date', 'sire', 'dam')
    list_filter = ('breed', 'gender')
    search_fields = ('name', 'breed')
    ordering = ('name',)
    inlines = [BreedingRecordInline]  # Add inline editing for BreedingRecord

# HealthRecord Admin with Import/Export
class HealthRecordAdmin(ImportExportModelAdmin):
    resource_class = HealthRecordResource
    list_display = ('goat', 'date', 'description')
    list_filter = ('date',)
    search_fields = ('goat__name', 'description')

# BreedingRecord Admin with Import/Export
class BreedingRecordAdmin(ImportExportModelAdmin):
    resource_class = BreedingRecordResource
    list_display = ('id', 'sire', 'dam', 'mating_date', 'offspring')
    list_filter = ('mating_date',)
    search_fields = ('sire__name', 'dam__name')

# Custom Admin Site
class PedigreeAdminSite(admin.AdminSite):
    site_header = 'Goat Pedigree Administration'
    site_title = 'Goat Pedigree Admin'
    index_title = 'Welcome to the Goat Pedigree Admin Panel'

# Create an instance of the custom admin site
pedigree_admin_site = PedigreeAdminSite(name='pedigree_admin')

# Register models with the custom admin site
pedigree_admin_site.register(Goat, GoatAdmin)
pedigree_admin_site.register(HealthRecord, HealthRecordAdmin)
pedigree_admin_site.register(BreedingRecord, BreedingRecordAdmin)

# Optionally, register models with the default admin site as well
admin.site.register(Goat, GoatAdmin)
admin.site.register(HealthRecord, HealthRecordAdmin)
admin.site.register(BreedingRecord, BreedingRecordAdmin)
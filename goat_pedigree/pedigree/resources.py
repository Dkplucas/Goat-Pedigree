# pedigree/resources.py
from import_export import resources, fields
from .models import Goat, HealthRecord, BreedingRecord

class GoatResource(resources.ModelResource):
    # Custom field for importing/exporting
    custom_field = fields.Field(column_name='custom_field', attribute='name')

    class Meta:
        model = Goat
        fields = ('id', 'name', 'breed', 'gender', 'birth_date', 'sire', 'dam', 'custom_field')  # Include custom_field
        export_order = ('id', 'name', 'breed', 'gender', 'birth_date', 'sire', 'dam', 'custom_field')  # Include custom_field

    def before_import_row(self, row, **kwargs):
        # Custom logic before importing a row
        if row['name'] == 'Invalid':
            raise ValueError("Invalid name detected!")


class HealthRecordResource(resources.ModelResource):
    class Meta:
        model = HealthRecord
        fields = ('id', 'goat', 'date', 'description')  # Fields to include
        export_order = ('id', 'goat', 'date', 'description')  # Export order


class BreedingRecordResource(resources.ModelResource):
    # Custom field for importing/exporting
    custom_field = fields.Field(column_name='custom_field', attribute='sire__name')

    class Meta:
        model = BreedingRecord
        fields = ('id', 'sire', 'dam', 'mating_date', 'offspring', 'custom_field')  # Include custom_field
        export_order = ('id', 'sire', 'dam', 'mating_date', 'offspring', 'custom_field')  # Include custom_field

    def before_import_row(self, row, **kwargs):
        # Custom logic before importing a row
        if row['sire'] == 'Invalid':
            raise ValueError("Invalid sire detected!")
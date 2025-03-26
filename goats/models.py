from django.db import models

class Goat(models.Model):
    name = models.CharField(max_length=200)
    breed = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, null=True,choices=[('male', 'Male'), ('female', 'Female')])
    birth_date = models.DateField(null=True, blank=True)
    registration = models.CharField(max_length=50, null=True,blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(
    upload_to='goats/',  # Specifies the directory where images will be uploaded
    null=True,           # Allows the field to be NULL in the database
    blank=True,          # Allows the field to be blank in forms
    help_text='Upload an image of the goat with a clear view of the face. Use the goat\'s name in .jpg format, e.g., lucy.jpg'  # Provides help text for the field
)
    # Parent relationships
    father = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='father_children'  # Add related_name
    )
    mother = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='mother_children'  # Add related_name
    )

    def __str__(self):
        return self.name

    @property
    def children(self):
        """Get all children through both parent relationships."""
        return self.father_children.all() | self.mother_children.all()
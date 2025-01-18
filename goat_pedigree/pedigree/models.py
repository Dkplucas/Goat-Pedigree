from django.db import models

class Goat(models.Model):
    id = models.CharField(primary_key=True, max_length=10)  # Custom ID field
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    birth_date = models.DateField()
    sire = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='sire_goats')
    dam = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='dam_goats')

    def __str__(self):
        return self.name

class HealthRecord(models.Model):
    goat = models.ForeignKey(Goat, on_delete=models.CASCADE, related_name='health_records')
    date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return f"{self.goat.name} - {self.date}"

class BreedingRecord(models.Model):
    sire = models.ForeignKey(Goat, on_delete=models.CASCADE, related_name='sire_breedings')
    dam = models.ForeignKey(Goat, on_delete=models.CASCADE, related_name='dam_breedings')
    mating_date = models.DateField()
    offspring = models.ForeignKey(Goat, on_delete=models.CASCADE, related_name='offspring_breedings', null=True, blank=True)

    def __str__(self):
        return f"{self.sire.name} x {self.dam.name} - {self.mating_date}"
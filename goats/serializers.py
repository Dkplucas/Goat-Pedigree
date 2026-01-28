from rest_framework import serializers
from .models import Goat

class GoatSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    father = serializers.SerializerMethodField()
    mother = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    class Meta:
        model = Goat
        fields = [
            'id', 'name', 'breed', 'gender', 'species', 'birth_date', 
            'registration', 'description', 'image', 'father', 
            'mother', 'children'
        ]

    def get_image(self, obj):
        """Return the full URL for the goat's image."""
        if obj.image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None

    def get_father(self, obj):
        """Return the father's details."""
        if obj.father:
            return {
                'id': obj.father.id,
                'name': obj.father.name,
                'image': self.get_image(obj.father)
            }
        return None

    def get_mother(self, obj):
        """Return the mother's details."""
        if obj.mother:
            return {
                'id': obj.mother.id,
                'name': obj.mother.name,
                'image': self.get_image(obj.mother)
            }
        return None

    def get_children(self, obj):
        """Return the children's details."""
        children = obj.children  # Assuming obj.children returns a queryset
        if children.exists():
            return [{
                'id': child.id,
                'name': child.name,
                'image': self.get_image(child)
            } for child in children]
        return []  # Return an empty array if there are no children
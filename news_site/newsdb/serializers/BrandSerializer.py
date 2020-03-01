from rest_framework import serializers
from newsdb.models import Brand


# Brand Serializer
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


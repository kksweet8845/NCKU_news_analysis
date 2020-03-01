from rest_framework import serializers
from newsdb.models import Brand_sub


# Brand_sub Serializer
class Brand_subSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand_sub
        fields = '__all__'
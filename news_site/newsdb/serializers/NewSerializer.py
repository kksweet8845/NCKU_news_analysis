from rest_framework import serializers
from newsdb.models import New

# News Serializer
class NewSerializer(serializers.ModelSerializer):
    class Meta:
        model = New
        fields = '__all__'
from rest_framework import serializers
from newsdb.models import New

# News Serializer
class NewSerializer(serializers.ModelSerializer):

    sub = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='id'
    )
    brand = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='id'
    )
    class Meta:
        model = New
        fields = '__all__'
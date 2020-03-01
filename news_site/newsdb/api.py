from newsdb.models import New, Brand_sub, Brand, Subject
from rest_framework import viewsets, permissions
from .serializers import NewSerializer, Brand_subSerializer, BrandSerializer, SubjectSerializer


class NewViewSet(viewsets.ModelViewSet):
    queryset = New.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = NewSerializer

class Brand_subViewSet(viewsets.ModelViewSet):
    queryset = Brand_sub.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = Brand_subSerializer


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = BrandSerializer

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = SubjectSerializer



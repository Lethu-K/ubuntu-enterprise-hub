from rest_framework import viewsets
from .models import Business
from .serializers import BusinessSerializer

class BusinessViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
from django.shortcuts import render

def home(request):
    businesses = Business.objects.all()
    return render(request, 'home.html', {'businesses': businesses})
# Create your views here.

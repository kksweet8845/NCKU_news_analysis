from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def keywordPage(request):
    return render(request, 'keyword.html')

def publisherPage(request):
    return render(request, 'publisher.html')
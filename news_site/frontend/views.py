from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def keywordPage(request):
    return render(request, 'keyword.html')
from django.shortcuts import render

# Create your views here.

def landing_index(request):
    return render(request,'rm/landing_index.html')
def relationship_index(request):
    return render(request,'rm/relationship_index.html')

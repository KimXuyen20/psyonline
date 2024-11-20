from django.shortcuts import render

# Create your views here.
def dprofile(request):
    return render(request,'doctor/dprofile.html')
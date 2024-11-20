from urllib.parse import uses_relative
from accounts.models import UserProfile
from doctor.models import Doctor
from django.conf import settings

def get_doctor(request):
    try:
       doctor = Doctor.objects.get(user=request.user)
    except:
       doctor = None
    return dict(doctor=doctor)


def get_user_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except:
        user_profile = None
    return dict(user_profile=user_profile)


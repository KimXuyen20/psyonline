from django import forms
from doctor.models import Doctor

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['doctor_name', 'doctor_license']


    def __init__(self, *args, **kwargs):
            super(DoctorForm, self).__init__(*args, **kwargs)
            self.fields['doctor_name'].widget.attrs['placeholder'] = 'Enter Specialty Name'

            for field in self.fields:
                self.fields[field].widget.attrs['class'] = 'form-control'

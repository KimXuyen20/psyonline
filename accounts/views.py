from django.shortcuts import redirect, render
from django.contrib import messages, auth
from accounts.forms import UserForm
from accounts.models import User, UserProfile
from django.core.exceptions import PermissionDenied

from doctor.forms import DoctorForm
# Create your views here.


# Restrict the vendor from accessing the customer page
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied


# Restrict the customer from accessing the vendor page
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied

def registerUser(request):
    # if request.user.is_authenticated:
    #     messages.warning(request, 'You are already logged in!')
    #     return redirect('dashboard')
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # Create the user using the form
            # password = form.cleaned_data['password']
            # user = form.save(commit=False)
            # user.set_password(password)
            # user.role = User.CUSTOMER
            # user.save()

            # Create the user using create_user method
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.CUSTOMER
            user.save()

            # Send verification email
            # mail_subject = 'Please activate your account'
            # email_template = 'accounts/emails/account_verification_email.html'
            # send_verification_email(request, user, mail_subject, email_template)
            # messages.success(request, 'Your account has been registered sucessfully!')
            return redirect('registerUser')
        else:
            print('invalid form')
            print(form.errors)
    else:
        form = UserForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/registerUser.html', context)


def login(request):
    # if request.user.is_authenticated:
    #     messages.warning(request, 'You are already logged in!')
    #     return redirect('myAccount')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('login')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request, 'You are logged out.')
    return redirect('login')


def registerDoctor(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        d_form = DoctorForm(request.POST, request.FILES)
        
        # Kiểm tra cả hai form
        if form.is_valid() and d_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]  # Lấy phần đầu của email làm username
            
            # Tạo đối tượng User
            user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.role = User.DOCTOR
            user.save()
            
            # Tạo đối tượng Doctor từ d_form
            doctor = d_form.save(commit=False)
            doctor.user = user
            user_profile = UserProfile.objects.get(user=user)
            doctor.user_profile = user_profile
            doctor.save()
            
            messages.success(request, 'Your account has been registered sucessfully! Please wait for the approval.')
            return redirect('login')
        else:
            # In lỗi từ cả hai form
            print('Invalid form:')
            print(form.errors)
            
    else:        
        form = UserForm()
        d_form = DoctorForm()

    context = {
        'form': form,
        'd_form': d_form,
    }
    
    return render(request, 'accounts/registerDoctor.html', context)

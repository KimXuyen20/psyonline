from django.shortcuts import redirect, render
from django.contrib import messages, auth
from accounts.forms import UserForm
from accounts.models import User, UserProfile
from django.core.exceptions import PermissionDenied
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.decorators import login_required, user_passes_test

from doctor.models import Doctor
from .utils import detectUser, send_verification_email
from doctor.forms import DoctorForm
# Create your views here.


# Restrict the vendor from accessing the customer page
def check_role_doctor(user):
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
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('myAccount')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
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
            send_verification_email(request, user)
            messages.success(request, 'Your account has been registered sucessfully!')
            return redirect('login')
        else:
            print('invalid form')
            print(form.errors)
    else:
        form = UserForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/registerUser.html', context)

def activate(request, uidb64, token):
    # Activate the user by setting the is_active status to True
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulation! Your account is activated.')
        return redirect('myAccount')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('myAccount')
        
def login(request):
    # Nếu người dùng đã đăng nhập, chuyển hướng họ ra khỏi trang đăng nhập
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('home')

    if request.method == 'POST':
        # Lấy dữ liệu từ form
        email = request.POST.get('email').strip()
        password = request.POST.get('password')

        # Xác thực người dùng
        user = auth.authenticate(email=email, password=password)

        if user is not None:
            # Đăng nhập người dùng
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('home')  # Hoặc URL mong muốn
        else:
            messages.error(request, 'Invalid login credentials. Please try again.')
            return redirect('login')  # Hiển thị lại form login với thông báo lỗi

    return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request, 'You are logged out.')
    return redirect('login')

@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)

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

            send_verification_email(request, user)
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

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    return render(request, 'accounts/custDashboard.html')



@login_required(login_url='login')
@user_passes_test(check_role_doctor)
def doctorDashboard(request):
    return render(request, 'accounts/doctorDashboard.html')
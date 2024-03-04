from django.shortcuts import render, redirect
from .forms import Register, UserCreationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
# def login_user(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('dashboard')
#         else:
#             messages.success(request, ("There was an error logging in, please try again.."))
#             return render(request, 'user/login.html')
#     else:
#         return render(request, 'user/login.html')

def register(request):
    if request.method == "POST":
        form = Register(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password1")
            form.save()
            new_user = authenticate(username=username, password=password, first_name=first_name, last_name=last_name, email=email)
            if new_user is not None:
                login(request, new_user)
                return redirect('user-login')
            
            
    else:
        form = Register()

    context = {
        'form' : form,
    }
    return render(request, 'user/register.html', context)

def passwordreset(request):
    

    return render(request, 'user/passwordreset.html')

def passwordresetcomplete(request):
    
    return render(request, 'user/passwordresetcomplete.html')

def passwordresetsent(request):

    return render(request, 'user/passwordresetsent.html')

def passwordresetconfirm(request):

    return render(request, 'user/passwordresetconfirm.html')

def logout_view(request):
    logout(request)
    return render(request, 'user/logout.html')

def profile(request):
    return render(request, 'user/profile.html')

def profile_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'user_form' : user_form,
        'profile_form' : profile_form,
    }
    return render(request, 'user/profile_update.html', context)


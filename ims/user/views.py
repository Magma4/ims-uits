from django.shortcuts import render, redirect
from .forms import Register, UserCreationForm
from django.contrib.auth import authenticate, login
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

# def logout_user(request):

#     return render(request, 'user/logout.html')


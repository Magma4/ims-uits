from django.shortcuts import render, redirect
from .forms import Register, UserCreationForm
from django.contrib.auth import authenticate, login

# Create your views here.
def login(request):
    return render(request, 'user/login.html')

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
                return redirect('dashboard')
            
    else:
        form = Register()

    context = {
        'form' : form,
    }
    return render(request, 'user/register.html', context)


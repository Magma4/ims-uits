from django.shortcuts import render, redirect
from .forms import Register, UserCreationForm

# Create your views here.
def index(request):
    return render(request, 'user/index.html')

def register(request):
    form = Register(request.POST)
    if form.is_valid():
        form.save()
        return redirect('dashboard')
    else:
        form = Register()
        
    context = {
        'form' : form,
    }
    return render(request, 'user/register.html', context)


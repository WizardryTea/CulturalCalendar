from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('affiche:index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('affiche:index')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('affiche:index')
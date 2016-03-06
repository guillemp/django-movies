from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required()
def settings_view(request):
    errors = ""
    if request.POST:
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        if password and password2:
            if password == password2:
                request.user.set_password(password)
                request.user.save()
                return redirect('/settings?')
            else:
                errors = "Password doesn't match"
    
    return render(request, 'settings.html', {
        "errors": errors,
    })

def login_view(request):
    if request.user.is_authenticated():
        return redirect('/')
    
    errors = False
    next = request.REQUEST.get('next', '')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if next:
                    return redirect(next)
                else:
                    return redirect('/')
            else:
                errors = "The password is valid, but the account has been disabled!"
        else:
            errors = "The username and password were incorrect."
    
    return render(request, 'login.html', {
        'errors': errors,
        'next': next,
    })

def logout_view(request):
    logout(request)
    return redirect('/')
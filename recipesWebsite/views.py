# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from recipesWebsite.forms import RegisterUserForm
from django.contrib.auth import logout

# View used to create an account
def userRegistration(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return redirect('recipesWebsite:userLogin')
    else:
        form = RegisterUserForm()
    return render(request, "authentification/userRegistration.html", {
        'form': form,
    })

# View which enable the user to log out
def userLogout(request):
    logout(request)
    return redirect('recipesWebsite:index')

def index(request):
    return render(request, "content/index.html")
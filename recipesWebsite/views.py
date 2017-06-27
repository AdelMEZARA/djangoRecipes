# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from recipesWebsite.forms import RegisterUserForm, RecipeForm
from recipesWebsite.models import Recipe
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

@login_required
def addRecipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)

        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('recipesWebsite:index')
    else:
        form = RecipeForm()
    return render(request, 'recipes/recipeForm.html', {'form': form})

@login_required
def editRecipe(request, recipeId):
    recipe = get_object_or_404(Recipe, id=recipeId)

    if recipe.user.id != request.user.id:
        return HttpResponseForbidden("Forbidden access")

    form = RecipeForm(request.POST or None, request.FILES or None, instance=recipe)
    if form.is_valid():
        form.save()
        return redirect('recipesWebsite:index')
    return render(request, 'recipes/recipeForm.html', {'form': form})

@login_required
def deleteRecipe(request, recipeId):
    recipe = get_object_or_404(Recipe, id=recipeId)

    if recipe.user.id != request.user.id:
        return HttpResponseForbidden("Forbidden access")

    if request.method == 'POST':
        recipe.delete()
        return redirect('recipesWebsite:index')
    return render(request, 'recipes/recipeConfirmDelete.html', {'object': recipe})
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from recipesWebsite.forms import RegisterUserForm, RecipeForm, RecipeFilter
from recipesWebsite.models import Recipe, RecipeAttachment
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

def listRecipe(request):
    page = request.GET.get('page', 1)

    paginator = Paginator(Recipe.objects.all(), 10)
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)

    return render(request, 'recipes/recipeList.html', {'results': results})

@login_required
def addRecipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)

        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('recipesWebsite:listRecipe')
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
        return redirect('recipesWebsite:listRecipe')
    return render(request, 'recipes/recipeForm.html', {'form': form})

@login_required
def deleteRecipe(request, recipeId):
    recipe = get_object_or_404(Recipe, id=recipeId)

    if recipe.user.id != request.user.id:
        return HttpResponseForbidden("Forbidden access")

    if request.method == 'POST':
        recipe.delete()
        return redirect('recipesWebsite:listRecipe')
    return render(request, 'recipes/recipeConfirmDelete.html', {'object': recipe})

def showRecipe(request, recipeId):
    recipe = get_object_or_404(Recipe, id=recipeId)
    images = RecipeAttachment.objects.filter(recipe=recipe)

    return render(request, 'recipes/recipeDetail.html', {'recipe': recipe, 'images': images})
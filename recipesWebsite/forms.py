import django_filters

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from recipesWebsite.models import Recipe, RecipeAttachment
from multiupload.fields import MultiFileField

class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email")

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('name', 'type', 'difficultyLevel', 'cost', 'prepareTime',
                  'cookTime', 'restTime', 'ingredientList', 'steps')

    files = MultiFileField(min_num=1, max_num=3, max_file_size=1024 * 1024 * 5)

    def save(self, commit=True):
         instance = super(RecipeForm, self).save(commit)
         for each in self.cleaned_data['files']:
            RecipeAttachment.objects.create(file=each, recipe=instance)

         return instance

class RecipeFilter(django_filters.FilterSet):

    class Meta:
        model = Recipe
        fields = {
            'name': ['icontains'],
            'type': ['exact'],
        }
        order_by = True
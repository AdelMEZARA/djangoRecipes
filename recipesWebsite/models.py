# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.core import validators
from django.db import models
from star_ratings.models import Rating


class Recipe(models.Model):
    name = models.CharField("Nom de la recette", max_length=200)

    TYPE = (
        ('E', 'Entrée'),
        ('P', 'Plat principal'),
        ('D', 'Dessert')
    )
    DIFFICULTY = (
        (1, u'Simple'),
        (2, u'Moyen'),
        (3, u'Difficile')
    )

    type = models.CharField("Type", max_length=24, choices=TYPE, default='P', editable=True)

    difficultyLevel = models.IntegerField("Niveau de difficulté", choices=DIFFICULTY, default='Simple')

    cost = models.DecimalField("Coût", max_digits=5, decimal_places=2,
                               validators=[validators.MinValueValidator(0)], blank=True, null=True)

    prepareTime = models.PositiveIntegerField("Temps de préparation", blank=True, null=True)
    restTime = models.PositiveIntegerField("Temps de repos", blank=True, null=True)
    cookTime = models.PositiveIntegerField("Temps de cuisson", blank=True, null=True)

    ingredientList = models.TextField("Liste des ingrédients")
    steps = models.TextField("Eapes de préparation")

    user = models.ForeignKey(User, blank=True, null=True)

    createdAt = models.DateTimeField("Date de création", auto_now_add=True)
    updatedAt = models.DateTimeField("Date de modification", auto_now=True)

    ratings = GenericRelation(Rating, related_query_name='recipes')

    def __str__(self):
        return self.name

class RecipeAttachment(models.Model):
    recipe = models.ForeignKey(Recipe, verbose_name='Recipe')
    file = models.ImageField('Attachement', upload_to='attachments')

class RecipeComment(models.Model):
    recipe = models.ForeignKey(Recipe, verbose_name='Recipe')
    user = models.ForeignKey(User, verbose_name='user')

    content = models.TextField("Commentaire")

    createdAt = models.DateTimeField("Date de création", auto_now_add=True)
    updatedAt = models.DateTimeField("Date de modification", auto_now=True)

    def __str__(self):
        return self.content
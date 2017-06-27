from django.conf.urls import url
from django.contrib.auth import views as auth_views

from recipesWebsite import views

app_name="recipesWebsite"

urlpatterns = [
    url(r'^userRegistration/$', views.userRegistration, name='userRegistration'),
    url(r'^userLogin/$', auth_views.login, {'template_name': 'authentification/userLogin.html'}, name='userLogin'),
    url(r'^userLogout/$', views.userLogout, name='userLogout'),
    url(r'^index/$', views.index, name='index'),
    url(r'^addRecipe/$', views.addRecipe, name='addRecipe'),
    url(r'^editRecipe/(\d+)/$', views.editRecipe, name='editRecipe'),
    url(r'^deleteRecipe/(\d+)/$', views.deleteRecipe, name='deleteRecipe'),
]
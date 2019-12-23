"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from skill.skill001 import myskill001
from skill.skill002 import myskill002

from django_ask_sdk.skill_adapter import SkillAdapter

my_skill_view = SkillAdapter.as_view(skill=myskill001)

urlpatterns = [
    path('skillentry/', my_skill_view, name='index'),
    path('skillentry2/', my_skill_view, name='index2'),
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]

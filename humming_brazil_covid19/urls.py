"""teste URL Configuration

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
from django.urls import include, path
from django.views.generic.base import RedirectView
from rest_framework import routers

from humming_brazil_covid19.report import views

router = routers.DefaultRouter()

router.register(r"all_cases", views.AllCasesViewSet, "all_cases")
router.register(r"last_cases", views.LastCasesViewSet, "last_cases")
# router.register(r"states", views.StatesList, "states_list")


urlpatterns = [
    path("", RedirectView.as_view(url="api/v1/")),
    path(r"api/v1/", include(router.urls)),
    # path(r"api/v1/states", views.StatesList.as_view(), name="states_list"),
]

from django.urls import path 
from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("food/<int:food_id>/", views.food, name="food"),
    path("totals/", views.totals, name="totals"),
    path("delete/<int:food_id>", views.delete, name="delete")
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('parse', views.parse, name="parse"),
    path('parse/<int:id>', views.image, name="image"),
    path('parse/<int:id>/original', views.original_image, name="original_image"),
    path('parse/images', views.images, name="images"),
]


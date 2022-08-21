from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('home/update/<int:note_id>', views.update_notes, name='update_note'),
    path('registration/', views.register, name='registration'),
]
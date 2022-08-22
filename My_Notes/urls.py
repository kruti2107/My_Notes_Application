from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('home/update/<int:note_id>', views.update_notes, name='update_note'),
    path('home/edit_note/<int:note_id>', views.edit_notes_details, name='edit_note_details'),
    path('registration/', views.register, name='registration'),
    path('home/logout/', views.logout_user, name='logout'),
]
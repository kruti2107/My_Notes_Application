from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import *
# Create your views here.
from My_Notes.serializer import RegistrationSerializer, NotesSerializer


def login(request):
    if request.method == "POST":
        request_email = request.POST.get('email')
        request_password = request.POST.get('password')
        user = User.objects.get(email=request_email)
        print(request_password)
        print(user.password)
        if user.email == request_email and user.password == request_password:
            response = HttpResponseRedirect('home/')
            response.set_cookie('user', user.id, max_age=None, expires=None)
            request.session['user'] = user.id
            return response
        else:
            messages.info(request, 'Your Username or Password is Invalid')
            return render(request, 'login.html', context={'message': messages})
    return render(request, 'login.html')


def register(request):
    serializer = RegistrationSerializer(request.POST)
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return redirect('/')
        else:
            print(serializer.errors.as_data())
    return render(request, 'registration.html', context={'form': serializer})


def home(request):
    serializer = NotesSerializer(request.POST)
    note_list = Note.objects.filter(user_id=request.session.get('user'))
    if request.method == 'POST':
        serializer = NotesSerializer(request.POST)
        if serializer.is_valid():
            serializer.instance.user = User.objects.get(id=request.session.get('user'))
            serializer.save()
            return render(request, 'home.html')
    elif request.method == 'GET':
        serializer = NotesSerializer(request.POST)
        note_list = Note.objects.filter(user_id=request.session.get('user'))
        return render(request, 'home.html', context={'serializer': serializer, 'notes': note_list})
    return render(request, 'home.html', context={'serializer': serializer, 'notes': note_list})


def update_notes(request, note_id):
    note = Note.objects.get(id=note_id)
    if note:
        note.favourite = not note.favourite
        note.save()
        return HttpResponseRedirect('/home')
    return render(request, 'home.html')

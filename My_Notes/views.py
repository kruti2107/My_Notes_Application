from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import *
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
    if request.session.get('user'):
        note_list = Note.objects.filter(user_id=request.session.get('user'))
        if request.method == 'POST':
            serializer = NotesSerializer(request.POST)
            print('POST!@#$%')
            serializer = NotesSerializer(request.POST)
            if serializer.is_valid():
                serializer.instance.user = User.objects.get(id=request.session.get('user'))
                serializer.save()
                serializer = NotesSerializer()
                return render(request, 'home.html', context={'notes': note_list})
        elif request.method == 'GET':
            serializer = NotesSerializer()
            note_list = Note.objects.filter(user_id=request.session.get('user'))
            return render(request, 'home.html', context={'notes': note_list})
        return render(request, 'home.html', context={'notes': note_list})
    return redirect('/')


def edit_notes_details(request, note_id):
    if request.method == 'GET':
        note = Note.objects.get(id=note_id)
        if note:
            serializer = NotesSerializer()
            return render(request, 'home.html', context={'serializer': serializer, 'note_selected': note})
    elif request.method == 'POST':
        serializer = NotesSerializer(request.POST)
        if serializer.is_valid():
            Note.objects.filter(id=note_id).update(title=serializer.cleaned_data['title'], description=serializer.cleaned_data['description'], favourite=serializer.cleaned_data['favourite'])
            return redirect('/home/')
    return render(request, 'home.html')


def update_notes(request, note_id):
    if request.method == 'GET':
        note = Note.objects.get(id=note_id)
        if note:
            note.favourite = not note.favourite
            note.save()
            return redirect('/home/')
    elif request.method == 'DELETE':
        Note.objects.get(id=note_id).delete()
        notes = Note.objects.filter(user_id=request.session.get('user'))
        note_list = Note.objects.filter(user_id=request.session.get('user'))
        return render(request, 'home.html', context={'notes': notes})
    return render(request, 'home.html')


# function to handle user logout
def logout_user(request):
    del request.session['user']
    return redirect('/')

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import *
from My_Notes.serializer import RegistrationSerializer, NotesSerializer

# function to handle user login
def login(request):
    if request.method == "POST":
        request_email = request.POST['email']
        request_password = request.POST.get('password')
        print(request_email)
        user = User.objects.filter(email=request_email)
        if len(user) and user[0].email == request_email and user[0].password == request_password:
            response = HttpResponseRedirect('home/')
            response.set_cookie('user', user[0].id, max_age=None, expires=None)
            request.session['user'] = user[0].id
            return response
        else:
            # execute when useid/email and password doesn't match
            print("dsfbdjfbdjf")
            messages.info(request, 'Your Username or Password is Invalid')
            return render(request, 'login.html', context={'message': messages})
    return render(request, 'login.html')

# function to handle user registration
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

# function to handle creation and retrieval of note list of user
def home(request):
    if request.session.get('user'):
        # execute when request for new notes creation comes
        note_list = Note.objects.filter(user_id=request.session.get('user'))
        if request.method == 'POST':
            serializer = NotesSerializer(request.POST)
            serializer = NotesSerializer(request.POST)
            if serializer.is_valid():
                serializer.instance.user = User.objects.get(id=request.session.get('user'))
                serializer.save()
                serializer = NotesSerializer()
                return render(request, 'home.html', context={'notes': note_list})
        elif request.method == 'GET':
            # execute when request to get notes comes
            serializer = NotesSerializer()
            note_list = Note.objects.filter(user_id=request.session.get('user'))
            return render(request, 'home.html', context={'notes': note_list})
        return render(request, 'home.html', context={'notes': note_list})
    return redirect('/')

# function to update the edited note details in database
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

# function to handle make notes favourite and delete comes
def update_notes(request, note_id):
    if request.method == 'GET':
        # to make notes favourite/unfavourite
        note = Note.objects.get(id=note_id)
        if note:
            note.favourite = not note.favourite
            note.save()
            return redirect('/home/')
    elif request.method == 'DELETE':
        # delete the notes
        Note.objects.get(id=note_id).delete()
        notes = Note.objects.filter(user_id=request.session.get('user'))
        note_list = Note.objects.filter(user_id=request.session.get('user'))
        return render(request, 'home.html', context={'notes': notes})
    return render(request, 'home.html')


# function to handle user logout
def logout_user(request):
    del request.session['user']
    return redirect('/')

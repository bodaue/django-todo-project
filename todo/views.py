from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.datetime_safe import datetime

from .forms import ToDoForm
from .models import ToDo


def home(request):
    return render(request, 'todo/home.html')


def signup_user(request):
    if request.method == 'GET':
        return render(request, 'todo/signup_user.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'],
                                                password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('current_todos')
            except IntegrityError:
                return render(request, 'todo/signup_user.html',
                              {'form': UserCreationForm(),
                               'error': 'Это имя пользователя уже занято. Пожалуйста, задайте другое.'})

        else:
            return render(request, 'todo/signup_user.html',
                          {'form': UserCreationForm(), 'error': 'Пароли не сходятся'})


def login_user(request):
    if request.method == 'GET':
        return render(request, 'todo/login_user.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('current_todos')
        else:
            return render(request, 'todo/login_user.html',
                          {'form': AuthenticationForm(), 'error': 'Неверный логин или пароль'})


@login_required
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


@login_required
def create_todo(request):
    if request.method == 'GET':
        return render(request, 'todo/create_todo.html', {'form': ToDoForm()})
    else:
        try:
            form = ToDoForm(request.POST)
            new_todo = form.save(commit=False)
            new_todo.user = request.user
            new_todo.save()
            return redirect('current_todos')
        except ValueError:
            return render(request, 'todo/create_todo.html', {'form': ToDoForm(), 'error': 'Bad Data'})


@login_required
def current_todos(request):
    todos = ToDo.objects.filter(user=request.user, achieve_date__isnull=True)
    return render(request, 'todo/current_todos.html', {'todos': todos})


@login_required
def completed_todos(request):
    todos = ToDo.objects.filter(user=request.user, achieve_date__isnull=False).order_by('-achieve_date')
    return render(request, 'todo/completed_todos.html', {'todos': todos})


@login_required
def get_todo(request, todo_pk):
    todo = get_object_or_404(ToDo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = ToDoForm(instance=todo)
        return render(request, 'todo/get_todo.html', {'todo': todo, 'form': form})
    else:
        try:
            form = ToDoForm(request.POST, instance=todo)
            form.save()
            return redirect('current_todos')

        except ValueError:
            return render(request, 'todo/get_todo.html', {'todo': todo, 'form': form, 'error': 'Bad Info'})


@login_required
def complete_todo(request, todo_pk):
    todo = get_object_or_404(ToDo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.achieve_date = datetime.now()
        todo.save()
        return redirect('current_todos')


@login_required
def delete_todo(request, todo_pk):
    todo = get_object_or_404(ToDo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('current_todos')

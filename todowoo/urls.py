from django.contrib import admin
from django.urls import path

from todo import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth
    path('signup/', views.signup_user, name='signup_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('login/', views.login_user, name='login_user'),

    # Todos
    path('', views.home, name='home'),
    path('create/', views.create_todo, name='create_todo'),
    path('current/', views.current_todos, name='current_todos'),
    path('completed/', views.completed_todos, name='completed_todos'),

    path('todo/<int:todo_pk>', views.get_todo, name='get_todo'),
    path('todo/<int:todo_pk>/completed', views.complete_todo, name='complete_todo'),
    path('todo/<int:todo_pk>/delete', views.delete_todo, name='delete_todo')

]

from django.urls import path
from mytodo import views as mytodo
from . import views

urlpatterns = [
    path("", mytodo.index,name="index"),
    path("add/", mytodo.add,name="add"),
    path("update_task_complete/", mytodo.update_task_complete, name="update_task_complete"),
    path('edit/<int:pk>/', mytodo.edit, name='edit'),
    path('delete/<int:pk>/', views.delete, name='delete'),
    path('delete/<int:pk>/confirm/', views.delete_confirm, name='delete_confirm'),


]
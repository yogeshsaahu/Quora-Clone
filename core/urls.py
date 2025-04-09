from django.urls import path
from . import views

urlpatterns = [
    path('', views.question_list, name='question_list'),
    path('register/', views.register_view, name='register'),
    path('post/', views.post_question, name='post_question'),
    path('question/<int:pk>/', views.question_detail, name='question_detail'),
    path('answer/like/<int:pk>/', views.like_answer, name='like_answer'),
    path('logout/', views.custom_logout_view, name='logout'),
]

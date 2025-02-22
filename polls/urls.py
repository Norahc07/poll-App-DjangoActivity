from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:question_id>/", views.DetailView.as_view(), name="detail"),
    path("<int:question_id>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path('add/', views.add_question, name='add_question'),
    path('save/', views.save_question, name='save_question'),
    path('<int:question_id>/choice/add/', views.add_choice, name='add_choice'),
    path('<int:question_id>/choice/save/', views.save_choice, name='save_choice'),
    path('<int:question_id>/edit/', views.edit_question, name='edit_question'),
    path('<int:question_id>/delete/', views.delete_question, name='delete_question'),
    path('<int:question_id>/choice/<int:choice_id>/edit/', views.edit_choice, name='edit_choice'),
    path('<int:question_id>/choice/<int:choice_id>/update/', views.update_choice, name='update_choice'),
    path('<int:question_id>/choice/<int:choice_id>/delete/', views.delete_choice, name='delete_choice'),
]

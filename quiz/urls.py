from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('categories/', views.CategoryListView.as_view(), name='categorys'),
    path('category/<int:pk>', views.CategoryDetailView.as_view(),
         name='category-detail'),
    path('allquestions/', views.QuestionListView.as_view(), name='all-questions'),
    path('question/<int:pk>', views.QuestionDetailView.as_view(),
         name='question-detail'),
    path('answer/<int:pk>',
         views.show_answer, name='show-answer'),
    path('myanswered/', views.questions_doneby_user, name='my-answered'),
    path('addactegory/', views.create_new_category, name='new-category'),
    path('addquestion/', views.create_new_question, name='new-question'),
    path('register/', views.register, name='register')
]

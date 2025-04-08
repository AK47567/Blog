from .views import *
from django.urls import path, include

urlpatterns = [
    path('user/registration/', UserRegistrationAPIView.as_view()),
    path('user/login/', UserLoginAPIView.as_view()),
    path('user/logout/', UserLogoutAPIView.as_view()),
    path('questions/', PostQuestionView.as_view(), name='post-question'),
    path('questions/all/', ListQuestionsView.as_view(), name='list-questions'),
    path('questions/<int:question_id>/answer/', PostAnswerView.as_view(), name='post-answer'),
    path('answers/<int:answer_id>/like/', LikeAnswerView.as_view(), name='like-answer'),
]
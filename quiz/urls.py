from django.conf.urls import url, re_path
from quiz.views import QuizlistAPI, QuizDetailView, MyQuizList, SaveUsersAnswer, SubmitQuizAPI

urlpatterns = [

    url("my-quizzes/", MyQuizList.as_view()),
    url("quizzes/", QuizlistAPI.as_view()),
    url("save-answer/", SaveUsersAnswer.as_view()),
    re_path("quizzes/(?P<slug>[\w\-]+)$", QuizDetailView.as_view()),
    re_path("quizzes/(?P<slug>[\w\-]+)/submit/$", SubmitQuizAPI.as_view()),
]

from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import generics, permissions
from rest_framework.response import Response
from quiz.models import Quiz, QuizTaker, Answer
from quiz.serializers import QuizListSerialzer, QuizDetailSerializer, MyQuizListSerialzer, UsersAnswerSerializer


class MyQuizList(generics.ListAPIView):
    #makes sure the user is IsAuthenticated before using the quiz
    persmission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = MyQuizListSerialzer

    def get_queryset(self, *arg, **kwargs):
        queryset = Quiz.objects.filter(quiztaker__user=self.request.user)
        query = self.request.GET.get("q")

        if query:
            queryset = queryset.filter(

            Q(name__icontains= query) |
            Q(description__icontains=query)
            ).distinct()

        return queryset

    def get_serializer_context(self, *args, **kwargs):
        return{'request': self.request}

class QuizlistAPI(generics.ListAPIView):
    serializer_class = QuizListSerialzer
    persmission_classes = [
        permissions.IsAuthenticated
    ]
    #serializer_class = QuizlistSerialzer
    def get_queryset(self, *args, **kwargs):
        #queryset = Quiz.objects.filter(roll_out=True)
        queryset = Quiz.objects.filter(roll_out=True).exclude(quiztaker__user=self.request.user)
        query = self.request.GET.get("q")

        if query:
            queryset = queryset.filter(

                Q(name__icontains= query) |
                Q(description__icontains=query)
            ).distinct()

        return queryset


class QuizDetailView(generics.RetrieveAPIView):
    serializer_class = QuizDetailSerializer
    #persmission_classes = []

    def get(self, *args, **kwargs):
        slug = self.kwargs["slug"]
        quiz = get_object_or_404(Quiz, slug=slug)
        last_question = None
        obj, created = QuizTaker.objects.get_or_create(user=self.requst.user, quiz=quiz)
        if created:
            for question in Question.objects.filter(quiz=quiz):
                UsersAnswer.objects.create(quiz_taker=obj, question=question)
        else:
            last_question = UsersAnswer.obj.filter(quiz_taker=obj, answer_isnull=False)
            if last_question.count() > 0:
                last_question = last_question.last().question.id
            else:
                last_question = None

        return Response({'quiz':self.get_serializer(quiz, context={'request': self.request}).data, 'last_question_id':last_question})


class SaveUsersAnswer(generics.UpdateAPIView):
    serializer_class = UsersAnswerSerializer
    persmission_classes = [
    permissions.IsAuthenticated
    ]

    def patch(self,request, *args,**kwargs):
        quiztaker_id = request.data['quiztaker'],
        question_id = request.data['question'],
        answer_id = request.data['answer']

        quiztaker = get_object_or_404(QuizTaker, id=quiztaker_id)
        question = get_object_or_404(Question, id=question_id)
        answer = get_object_or_404(Answer, id=answer_id)

        if quiztaker.completed:
            return Response({"message": "This quiz is completed!"}, status= status.HTTP_412_PRECONDITION_FAILED)

        obj = get_object_or_404(UsersAnswer,quiztaker = quiztaker, question=question)
        obj.answer = answer
        obj.save()

        return Response(self.get_serializer(obj).data)

from rest_framework import serializers
from quiz.models import Quiz, QuizTaker, Questions, UsersAnswer, Answer

class QuizListSerialzer(serializers.ModelSerializer):
    questions_count = serializers.SerializerMethodField()
    class Meta:
        model = Quiz
        fields = ["id", "name", "description", "image", "slug", "questions_count"]
        read_only_fields = ["questions_count"]

    def get_questions_count(self, obj):
        return obj.questions_set.all().count()


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ["id", "questions", "label"]

class QuestionSerializer(serializers.ModelSerializer):
    answer_set = AnswerSerializer(many=True)

    class Meta:
        model = Questions
        fields = "__all__"

class UsersAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersAnswer
        fields = "__all__"

class QuizTakerSerializer(serializers.ModelSerializer):
    users_answer_set = UsersAnswerSerializer(many=True)

    class Meta:
        model = QuizTaker
        fields = "__all__"

class QuizDetailSerializer(serializers.ModelSerializer):
    quiztakers_set = serializers.SerializerMethodField()
    questions_set = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = "__all__"

    def get_quiztakers_set(self, obj):
        try:
            quiz_taker = QuizTaker.objects.get(user=self.context['request'].user, quiz=obj)
            serializer = QuizTakerSerializer(quiz_taker)
            return serializer.data
        except QuizTaker.DoesNotExist:
            return None



class MyQuizListSerialzer(serializers.ModelSerializer):

    progress = serializers.SerializerMethodField()
    completed = serializers.SerializerMethodField()
    score = serializers.SerializerMethodField()
    questions_count = serializers.SerializerMethodField()
    class Meta:
        model = Quiz
        fields = ["id", "name", "description", "image", "slug", "questions_count", "completed", "score", "progress"]
        read_only_fields = ["questions_count", "completed", "score", "progress"]

    def get_completed(self, obj):
        try:
            quiztaker = QuizTaker.objects.get(user=self.context['request'].user, quiz=obj)
            return quiztaker.completed
        except QuizTaker.DoesNotExist:
            return None

    def get_progress(self,obj):
        try:
            quiztaker = QuizTaker.objects.get(user=self.context['request'].user, quiz=obj)
            if quiztaker.completed == False:
                questions_answered = UsersAnswer.object.filter(quiz_taker=quiztaker, answer__isnull=False).count()
                total_questions = obj.questions_set.all().count()
                return int(questions_answered/total_questions) #return the count of the answers the user has completed
            return None
        except QuizTaker.DoesNotExist:
            return None


    def get_questions_count(self, obj):
        return obj.questions_set.all().count()

    def get_score(self, obj):
        try:
            quiztaker = QuizTaker.objects.get(user=self.context['request'].user, quiz=obj)
            if quiztaker.completed == True:
                return quiztaker.score #return the count of the answers the user has completed
            return None
        except QuizTaker.DoesNotExist:
            return None

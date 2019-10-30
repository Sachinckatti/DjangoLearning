from core_app.models import *
from rest_framework import serializers


class ACommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AComment
        fields = '__all__'

class UpVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UpVote
        fields = '__all__'

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('a_id', 'q_id', 'a_text', 'a_isaccepted')
        #exclude = ('acomments', 'upvotes')

    def get_upvotes(self, obj):
        try:
           counts = UpVote.objects.filter(a_id = obj.a_id).count()
        except UpVote.DoesNotExist:
            counts = 0
        return counts

class AnswerGetSerializer(serializers.ModelSerializer):
    acomments = ACommentSerializer(many=True, required=False)
    upvotes = serializers.SerializerMethodField()
    class Meta:
        model = Answer
        fields = ('a_id', 'a_text', 'a_isaccepted', 'acomments', 'upvotes')

    def get_upvotes(self, obj):
        try:
           counts = UpVote.objects.filter(a_id = obj.a_id).count()
        except UpVote.DoesNotExist:
            counts = 0
        return counts

class QCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = QComment
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerGetSerializer(many=True)
    class Meta:
        model = Question
        fields = ('q_id', 'q_text', 'q_desc', 'q_isClosed', 'answers')




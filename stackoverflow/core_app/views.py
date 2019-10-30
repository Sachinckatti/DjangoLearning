from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.http import HttpResponseRedirect
from core_app.models import *
from core_app.serializers import *
# Create your views here.

class CoreView(viewsets.ViewSet):
    model = None
    serializer = None

    def __init__(self):
        pass
    def retrieve(self, request, pk):
        item = self.model.objects.get(q_id = pk)
        #import pdb;pdb.set_trace()
        #instance = self.get_object()
        serializer = self.serializer(instance = item)
        return Response(serializer.data)

    #permission_classes([IsAuthenticated])
    @method_decorator(cache_page(60))
    def list(self, request,  **kwargs):
        if not request.query_params:
            all_items = self.model.objects.all()
        else:
            all_items = self.model.objects.filter(a_id = request.query_params['a_id'][0])
        serializer = self.serializer(all_items, many=True)
        return Response(serializer.data)

    def create(self, request,  **kwargs):
        #import pdb;pdb.set_trace()
        serializer = self.serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return HttpResponseRedirect(redirect_to=f"/")

class QuestionView(CoreView):
    #permission_classes = (IsAuthenticated,)
    def __init__(self, **kwargs):
        self.model = Question
        self.serializer = QuestionSerializer
        super().__init__()

    def retrieve(self, request, pk):
        item = self.model.objects.get(q_id = pk)
        serializer = self.serializer(instance=item)
        return Response(serializer.data)

class AnswerView(CoreView):
    def __init__(self, **kwargs):
        self.model = Answer
        self.serializer = AnswerSerializer
        super().__init__()

    def retrieve(self, request, pk):
        #import pdb;pdb.set_trace()
        self.serializer = AnswerGetSerializer
        print(request.query_params)
        item = self.model.objects.get(a_id = pk)
        serializer = self.serializer(instance=item)
        return Response(serializer.data)

    def list(self, request,  **kwargs):
        self.serializer = AnswerGetSerializer
        if not request.query_params:
            all_items = self.model.objects.all()
        else:
            all_items = self.model.objects.filter(a_id = request.query_params['a_id'][0])
        serializer = self.serializer(all_items, many=True)
        return Response(serializer.data)


class ACommentView(CoreView):
    def __init__(self, **kwargs):
        self.model = AComment
        self.serializer = ACommentSerializer

    def retrieve(self, request, pk):
        item = self.model.objects.get(ac_id = pk)
        serializer = self.serializer(instance=item)
        return Response(serializer.data)


class UpVoteView(CoreView):
    def __init__(self, **kwargs):
        self.model = UpVote
        self.serializer = UpVoteSerializer
        super().__init__()

    def retrieve(self, request, pk):
        item = self.model.objects.get(up_id = pk)
        serializer = self.serializer(instance=item)
        return Response(serializer.data)

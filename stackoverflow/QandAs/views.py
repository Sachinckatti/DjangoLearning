from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from QandAs.serializers import UserSerializer, GroupSerializer, FooSerializer, QuestionSerializer
from QandAs.models import get_mongo_database, Foo, Question, Answer, UpVote, Comment
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated
import json

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    #print(queryset)
    serializer_class = UserSerializer
    #get_mongo_database("stackoverflow")


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class BaseMongoView(viewsets.ViewSet):
    entity = None
    serializer = None
    def __init__(self, **kwargs):
        self.conn = get_mongo_database("stackoverflow")
        self.entity_model = self.entity(self.conn)
        print("Instantiating")
        self.keys = self.entity_model.keys

    def retrieve(self, request, pk=None):
        item = self.entity_model.get_one_by_key("id", pk)
        #serializer = self.get_serializer("retrieve")(item, fields=self.keys)
        serializer = self.serializer(item)
        return Response(serializer.data)

    #@permission_classes([IsAuthenticated])
    def list(self, request,  **kwargs):
        all_items = self.entity_model.get_all()
        serializer = self.serializer(all_items, many=True)
        return Response(serializer.data)

    def create(self, request,  **kwargs):
        self.entity_model.base_data = request.data
        self.entity_model.create_entity()
        return HttpResponseRedirect(redirect_to=f"/")

class QuestionMongoView(BaseMongoView):
    def __init__(self, **kwargs):
        self.entity = Question
        self.serializer = QuestionSerializer
        super().__init__(**kwargs)

class FooMongoView(BaseMongoView):
    def __init__(self, **kwargs):
        self.entity = Foo
        self.serializer = FooSerializer
        print('Foo View')
        #import pdb;pdb.set_trace()
        super().__init__(**kwargs)

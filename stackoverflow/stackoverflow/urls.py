"""stackoverflow URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from QandAs import views
from core_app.views import *

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'question', QuestionView, basename='put_question')
router.register(r'answer', AnswerView, basename='put_answer')
router.register(r'comment', ACommentView, basename='answer_comments')
router.register(r'upvote', UpVoteView, basename='add_upvote')

'''
router.register(r'test', views.FooMongoView, basename='MongoModel')
router.register(r'question', views.QuestionMongoView, basename='add question')
router.register(r'question/<pk>', views.QuestionMongoView, basename='get_question')
'''
urlpatterns = [
    path('', include(router.urls)),
    path(r'admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
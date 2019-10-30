from django.db import models

# Create your models here.
class Question(models.Model):
    q_id = models.AutoField(primary_key=True)
    q_text = models.CharField(max_length=250)
    q_desc = models.CharField(max_length=500)
    q_isClosed = models.BooleanField(default=False)

class Answer(models.Model):
    a_id = models.AutoField(primary_key=True)
    q_id = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    a_text = models.CharField(max_length=500)
    a_isaccepted = models.BooleanField(default=False)

class QComment(models.Model):
    qc_id = models.AutoField(primary_key=True)
    q_id = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='comments')
    qc_text = models.CharField(max_length=250)

class AComment(models.Model):
    ac_id = models.AutoField(primary_key=True)
    a_id = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='acomments')
    ac_text = models.CharField(max_length=250)

class UpVote(models.Model):
    up_id = models.AutoField(primary_key=True)
    a_id = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='upvotes')

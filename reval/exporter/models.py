from django.db import models
# Create your models here.


class Topic(models.Model):
    topic_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.topic_text

class Question(models.Model):
    topic = models.ForeignKey(Topic, on_delete= models.CASCADE)
    question_text = models.CharField(max_length=200)
    answer = models.IntegerField(default=0)

    def __str__(self):
        return self.question_text
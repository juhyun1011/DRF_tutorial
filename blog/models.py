from django.db import models
from datetime import datetime, timedelta
from django.utils import timezone


# Create your models here.
class Category(models.Model):
    name  = models.CharField("이름", max_length=20)
    desc = models.TextField("설명")

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField("제목", max_length=100)
    author = models.ForeignKey('user.User', verbose_name="작성자", on_delete=models.CASCADE)
    category = models.ManyToManyField(Category)
    content = models.TextField("내용")
    exposed_start =  models.DateField("노출 시작 일자")
    exposed_end = models.DateField("노출 종료 일자")

    def __str__(self):
        return self.title

class Comment(models.Model):
    article = models.ForeignKey('Article', verbose_name="게시글", on_delete=models.CASCADE)
    author = models.ForeignKey('user.User', verbose_name="작성자", on_delete=models.CASCADE)
    content = models.TextField("내용")

    def __str__(self):
        return (f"{self.article}의 댓글")
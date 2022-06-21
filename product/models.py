from django.db import models

# Create your models here.
class Product(models.Model):
    title = models.CharField("제목", max_length=100)
    author = models.ForeignKey('user.User', verbose_name="작성자", on_delete=models.CASCADE)
    thumbnail = models.ImageField("썸네일")
    desc = models.TextField("설명")
    registered_date = models.DateField("등록 일자")
    exposed_start =  models.DateField("노출 시작 일자")
    exposed_end = models.DateField("노출 종료 일자")

    def __str__(self):
        return self.title
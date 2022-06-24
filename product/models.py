from django.db import models

# Create your models here.
class Product(models.Model):
    title = models.CharField("제목", max_length=100)
    user = models.ForeignKey('user.User', verbose_name="작성자", on_delete=models.CASCADE)
    thumbnail = models.FileField("썸네일", upload_to="product/")
    desc = models.TextField("설명")
    registered_date = models.DateField("등록 일자", auto_now_add=True)
    exposed_end = models.DateField("노출 종료 일자")
    price = models.IntegerField("상품 가격", default=0)
    updated_date = models.DateField("수정 일자", auto_now=True)
    is_active = models.BooleanField("활성화 여부", null=True, default='')


    def __str__(self):
        return self.title


class Review(models.Model):
    user = models.ForeignKey('user.User', verbose_name="작성자", on_delete=models.CASCADE)
    product = models.ForeignKey('Product', verbose_name="상품", on_delete=models.CASCADE)
    content = models.TextField("내용")
    rate = models.IntegerField("평점", default=0)
    registered_date = models.DateField("등록 일자", auto_now_add=True)
    
    def __str__(self):
        return (f"{self.product}의 리뷰")

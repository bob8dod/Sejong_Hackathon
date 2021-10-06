from django.db import models

class StockModel(models.Model):
    class Meta:
        db_table = "stock_model"
    stock_name= models.CharField(max_length=256, default='') # 주식 이름
    stock_code= models.CharField(max_length=256, default='') # 주식 코드
    stock_logo_img = models.CharField(max_length=256, default='') # 주식 로고 이미지
    stock_rate= models.FloatField(null=True, default=0) # 상승률
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Abnormal(models.Model):
    class Meta:
        db_table = "abnormal_stock"
    stock_model = models.ForeignKey(StockModel, on_delete=models.CASCADE,default='')
    idx = models.IntegerField(null=True) # 주식 csv파일 경로
    abnormal_date = models.CharField(max_length=256, default='')
    related_news_title_url = models.CharField(max_length=256, default='')# 관련 기사 제목
    related_news_wordcloud = models.CharField(max_length=256, default='')# 관련 기사 keyword wordcloud link
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
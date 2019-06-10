from django.db import models

#凶宅資料庫
class HouseLocation(models.Model):
    address = models.CharField(max_length=150)
    category = models.CharField(max_length=15, default='自殺')
    article = models.TextField()
    website = models.URLField()
    date = models.DateField(null=True, blank=True)

    #QuerySet中object顯示名稱
    def __str__(self):
        return self.address

#交通事故資料庫
class TrafficLocation(models.Model):
    address = models.CharField(max_length=150)
    category = models.CharField(max_length=15, default='汽車擦撞')
    date = models.DateField(null=True, blank=True)

    #QuerySet中object顯示名稱
    def __str__(self):
        return self.address

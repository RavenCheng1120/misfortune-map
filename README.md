## 第一步：收集資料    
|文件類型|出處| 
|-------|:----| 
|凶宅資料|https://unluckyhouse.com/archive/index.php/f-13.html| 
|交通事故|https://opendata.taichung.gov.tw/dataset?q=%E4%BA%A4%E9%80%9A%E4%BA%8B%E6%95%85| 
  
此地圖使用交通事故資料集與凶宅網所搜集下來的資料，經過人工處理後，製作成json格式的文件，並將地址轉換成經緯度存取。 
  
  
## 第二步：啟用google Maps API  
啟用google maps javescript api，先申請憑證，建立專屬的金鑰key，可以讓 Google 識別是哪個使用者在用對應的服務，並且根據使用者權限和使用的服務，提供對應的功能和限制。  
教學網址：https://www.oxxostudio.tw/articles/201707/google-maps-1.html 
  
  
## 第三步：打造Django專案 
Django是一個基於Python語言所寫出來的框架，簡化了很多寫網頁的流程。 
Django有屬於它的MTV(Model-Template-Views)
+ Model：描述你的資料類型  
+ Template：使用者看到網頁的形式   
+ Views：傳達資料內容  
  
### 創建
+ 首先，先下載Django。在終端機下達指令`pip install django`   
  
+ 輸入`django-admin startproject misfortuneMap`創建Django project，misfortuneMap是root app名稱。  
    
+ 若要開啟server，輸入`python manage.py runserver`，則 http://127.0.0.1:8000/ 可開啟網站。  
  
+ 為了將各作用的網站分開，我們在root app之下創建一個新的app，作為地圖頁面，以方便日後有更多功能時，管理比較便利。  
`python manage.py startapp mapPage`創建新的app。 隨後在settings.py中加入app名稱-mapPage。
    
+ 安裝django REST Framework`pip install djangorestframework`，在settings.py中加入rest_framework。   
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'mapPage',
]
```
---   
### urls.py 
在mapPage的urls.py之下，建立網址連結。  
`path('', views.map_Page)`代表輸入網址 http://127.0.0.1:8000/map/ 時，會連接到views.py的map_Page函數。    
而`path('api/', include(router.urls))`是REST Framework的功能，當輸入 http://127.0.0.1:8000/map/api/house/ 時，可以連接到凶宅資料庫，觀看與更改資料庫內容。
```python
from django.urls import path,include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('house', views.housesView,basename='HouseLocation')
router.register('traffic', views.trafficView,basename='TrafficLocation')

urlpatterns = [
    path('', views.map_Page),
    path('api/', include(router.urls)),
]
```   
--- 
### views.py  
mapPage views.py中建立map_Page function，這樣urls.py才能連結到此處，map_Page function回傳html檔案讓網頁顯示。  
housesView和trafficView兩個class是用於REST framework的serialize，`HouseLocation.objects.all()`指令可以選取該資料庫中的所有資料。   
HouseSerializer, TrafficSerializer是serializers.py中的class，稍後會提到。   
```python
# -*- coding: UTF-8 -*-
from django.shortcuts import render
from .models import HouseLocation, TrafficLocation
from rest_framework import viewsets
from .serializers import HouseSerializer, TrafficSerializer

def map_Page(request):
    #houses = HouseLocation.objects.all()
    #return render(request,'mapPage/mapDisplay.html',{'houses':houses})
    return render(request,'mapPage/mapDisplay.html')

class housesView(viewsets.ModelViewSet):
    queryset = HouseLocation.objects.all()
    serializer_class = HouseSerializer

class trafficView(viewsets.ModelViewSet):
    queryset = TrafficLocation.objects.all()
    serializer_class = TrafficSerializer
```   
---
### models.py 
建立資料庫格式，分為`凶宅資料`與`交通事故資料`。 
Django 預設是使用 SQLite ，如果想要修改為其他的資料庫，可以在 settings.py 裡面進行修改。  
各models有不同的資料型態，可觀看官網上的文件，使用適合的資料型態。https://docs.djangoproject.com/en/2.2/topics/db/models/    
```python
from django.db import models

#凶宅資料庫
class HouseLocation(models.Model):
    address = models.CharField(max_length=150)
    lat = models.FloatField(default=None)
    lng = models.FloatField(default=None)
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
    lat = models.FloatField(default=None)
    lng = models.FloatField(default=None)
    category = models.CharField(max_length=15, default='汽車擦撞')
    date = models.DateField(null=True, blank=True)

    #QuerySet中object顯示名稱
    def __str__(self):
        return self.address
```
--- 
### serializers.py  
在mapPage下創建serializers python檔案，配合rest framework使用，可序列化資料庫中的資料，給views.py與urls.py使用。   
```python
from rest_framework import serializers
from .models import HouseLocation, TrafficLocation

class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseLocation
        fields = '__all__'
        #fields = ('id','address','article','website','date')

class TrafficSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficLocation
        fields = '__all__'
``` 
---
### admin.py
將model放到django administration，以方便控管。
> python manage.py createsuperuser   
  先設定super user，可以進入admin區域，設定好user和密碼，就可以透過 http://127.0.0.1:8000/admin/ 進入django administration。  
```python
from django.contrib import admin
from .models import HouseLocation, TrafficLocation

admin.site.register(HouseLocation)
admin.site.register(TrafficLocation)
```
---
### 設定template  
要連接html，要先新增一個templates資料夾，將html檔案放進去，並在setting.py中的'DIRS'連接上templates。  
```
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```
--- 
### 連接assets
在最外層建立一個assets資料夾，存放圖片、javascript、css等檔案。   
並在settings.py中將它連接到static，方便以後取用。
```
STATIC_URL = '/static/'

STATICFILES_DIRS=(
    os.path.join(BASE_DIR,'assets'),
)
```
    
    
## 第四步：撰寫html文件   
將google map呈現在網頁上，並配合SQLite資料庫的資料取用。  


## 參考資料
使用django REST framework傳輸資料庫內資料給javascript使用，參考：https://www.youtube.com/watch?v=B4Vmm3yZPgc     
在地圖上加點擊資訊視窗，參考：https://www.oxxostudio.tw/articles/201801/google-maps-5-marker-click-event.html     
地圖標記圖案：https://mapicons.mapsmarker.com/     
將csv加入資料庫：http://abhishekchhibber.com/django-importing-a-csv-file-to-database-models/    
轉換地址到經緯度：https://maplocation.sjfkai.com/    

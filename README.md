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
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mapPage',
]
```
  
---   
在mapPage的urls.py之下，建立網址連結。  
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
mapPage中建立map_Page function，這樣urls.py才能連結到此處，map_Page function回傳html檔案讓網頁顯示。    
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
  
## 參考資料
使用django REST framework傳輸資料庫內資料給javascript使用，參考：https://www.youtube.com/watch?v=B4Vmm3yZPgc     
在地圖上加點擊資訊視窗，參考：https://www.oxxostudio.tw/articles/201801/google-maps-5-marker-click-event.html     
地圖標記圖案：https://mapicons.mapsmarker.com/     
將csv加入資料庫：http://abhishekchhibber.com/django-importing-a-csv-file-to-database-models/    
轉換地址到經緯度：https://maplocation.sjfkai.com/    

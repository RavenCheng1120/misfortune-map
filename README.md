## 第一步：收集資料    
|文件類型|出處| 
|-------|:----| 
|凶宅資料|https://unluckyhouse.com/archive/index.php/f-13.html| 
|交通事故|https://opendata.taichung.gov.tw/dataset?q=%E4%BA%A4%E9%80%9A%E4%BA%8B%E6%95%85| 
  
此地圖使用交通事故資料集與凶宅網所搜集下來的資料，經過人工處理後，製作成csv格式的文件，並將地址轉換成經緯度存取。 
  
  
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
``` 
```python
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
將html file存在mapPage/templates/mapPage，以免跟root app中的template搞混。  
在html檔案上方加入`{% load static from staticfiles %}`，用來存取assests中的文件與圖片。   
+ 首先，在head的部分連結上stylesheet和jquery。  
```html
<!DOCTYPE html>
<html>
  <head>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.0/jquery.min.js"></script>
    <meta charset="utf-8">
    <title>厄運地圖</title>
    <link rel="stylesheet" href="{% static 'mapStyle.css'%}">
    <meta name="viewport" content="initial-scale=1.0">
  </head>
```   
    
+ 設置左側欄位的按鈕，以及隱藏起來的查詢bar，最後是地圖區塊。  
```html
<body>
    <div class="side-bar">
      <a id="search-bar" onclick="searchFunction()">查詢地點</a>
      
      <button class="dropdown-btn">篩選
        <i class="fa fa-caret-down"></i>
      </button>
      <div class="dropdown-container">
        <label id="h-container" style="color:white;">凶宅
          <input type="checkbox" checked="checked" id="houseCheck" onclick="houseCheckbox()">
        </label>
        <label id="traf-container">交通事故
          <input type="checkbox" id="trafficCheck" onclick="trafficCheckbox()">
        </label>
      </div>

    </div>
    <div class="search-box">
      <form>
        請輸入地址：<input type="text" style="padding:3px;" size="50" id="inputAddress">
        <button type="button" onclick="startSearching()">搜尋</button>
      </form>
    </div>
  
    <div id="map"></div>
```
    
+ 連接google map api，以及地圖標示的js檔案。 
```html
<script src="{% static 'markerclusterer.js'%}">
</script>
<script src="https://maps.googleapis.com/maps/api/js?key=my_KEY&callback=initMap"
  async defer>
</script>
```
+ intiMap()初始化地圖的位置、樣式。   
將mapTypeControl和fullscreenControl功能關閉。
```html
<script>
      var map;
      var geocoder;
      var markerClusterTraf;
      var markerClusterHouse;
      var markersHouse = [];
      var markersTraffic = [];

      //設定地圖初始位置
      function initMap() {
        var styledMapType = new google.maps.StyledMapType(
          [
            {
                "featureType": "all",
                "elementType": "all",
                "stylers": [
                    {
                        "invert_lightness": true
                    },
                    {
                        "saturation": 20
                    },
                    {
                        "lightness": 50
                    },
                    {
                        "gamma": 0.4
                    },
                    {
                        "hue": "#00ffee"
                    }
                ]
            },
            {
                "featureType": "all",
                "elementType": "geometry",
                "stylers": [
                    {
                        "visibility": "simplified"
                    }
                ]
            },
            {
                "featureType": "all",
                "elementType": "labels",
                "stylers": [
                    {
                        "visibility": "on"
                    }
                ]
            },
            {
                "featureType": "administrative",
                "elementType": "all",
                "stylers": [
                    {
                        "color": "#ffffff"
                    },
                    {
                        "visibility": "simplified"
                    }
                ]
            },
            {
                "featureType": "administrative.land_parcel",
                "elementType": "geometry.stroke",
                "stylers": [
                    {
                        "visibility": "simplified"
                    }
                ]
            },
            {
                "featureType": "landscape",
                "elementType": "all",
                "stylers": [
                    {
                        "color": "#405769"
                    }
                ]
            },
            {
                "featureType": "water",
                "elementType": "geometry.fill",
                "stylers": [
                    {
                        "color": "#232f3a"
                    }
                ]
            }
          ],
            {name:'黑暗模式'});
        geocoder = new google.maps.Geocoder();
        map = new google.maps.Map(document.getElementById('map'), {
          center: {lat: 24.135, lng: 120.65},
          zoom: 11,
          mapTypeControl: false,
          fullscreenControl: false
        });
        map.mapTypes.set('黑暗模式', styledMapType);
        map.setMapTypeId('黑暗模式');
      }
    </script>
```
+ 側邊欄展開或收起
```html
<script>
  var dropdown = document.getElementsByClassName("dropdown-btn");
    var i;
    for (i = 0; i < dropdown.length; i++) {
      dropdown[i].addEventListener("click", function() {
        this.classList.toggle("active");
        var dropdownContent = this.nextElementSibling;
        if (dropdownContent.style.display === "block") {
          dropdownContent.style.display = "none";
        } else {
          dropdownContent.style.display = "block";
        }
      });
    }
</script>
```
+ 開關地圖上的標記，setMapOnAll(null)是清除所有地圖標記的函數，setMapOnAll(map)則是將地圖標記重新放上。   
使用checkbox觀察哪一個選項被開啟或關閉。
```html
<script>
  //開關地圖上的凶宅標記
    function houseCheckbox(){
      var checkBox = document.getElementById("houseCheck");
      if (checkBox.checked == true){
        document.getElementById("h-container").style.color= 'white';
        setMapOnAll(map,0);
        markerClusterHouse.addMarkers(markersHouse);
      } else {
        document.getElementById("h-container").style.color= '#818181';
        setMapOnAll(null,0);
        markerClusterHouse.clearMarkers();
      }
    }

    //開關地圖上的交通事故標記
    function trafficCheckbox(){
      var checkBox = document.getElementById("trafficCheck");
      if (checkBox.checked == true){
        document.getElementById("traf-container").style.color= 'white';
        setMapOnAll(map,1);
        markerClusterTraf.addMarkers(markersTraffic);
      } else {
        document.getElementById("traf-container").style.color= '#818181';
        setMapOnAll(null,1);
        markerClusterTraf.clearMarkers();
      }
    }
</script>
```
+ setMapOnAll function，num=0時是設定凶宅，num=1則是設定交通事故。
```html
<script>
    //放上或清除地圖上的標記
    function setMapOnAll(map,num) {
      //凶宅
      if(num==0){
        for (var i = 0; i < markersHouse.length; i++)
          markersHouse[i].setMap(map);
      }
      //交通事故
      else if(num==1) {
        for (var i = 0; i < markersTraffic.length; i++)
          markersTraffic[i].setMap(map);
      }
    }
</script>
```
+ 搜尋bar開啟或收起
```html
<script>
  //彈出或收起地址搜尋框
    var search_check = 0;
    function searchFunction(){
      var searchBar = document.getElementById("search-bar");
      var searchBox = document.getElementsByClassName("search-box");
      if(search_check==0){
        searchBar.style.color = "white";
        searchBar.style.background = "green";
        searchBox[0].style.display = "block";
        search_check=1;
      }else if (search_check==1) {
        searchBar.style.color = "#818181";
        searchBar.style.background = "#111";
        searchBox[0].style.display = "none";
        search_check=0;
      }
    }
</script>  
```
+ 使用google map api : geocoding，將搜尋框的地址轉換成經緯度，再由經緯度在地圖上放上標記
```html
<script> 
  //開始搜尋地址
    var old_address_marker=null;
    function startSearching(){
      //抓取搜尋欄的地址，放上地標
      var address = document.getElementById('inputAddress').value;
      geocoder.geocode( { 'address': address}, function(results, status) {
      if (status == 'OK') {
        map.setCenter(results[0].geometry.location);
        var marker = new google.maps.Marker({
            map: map,
            position: results[0].geometry.location
        });
        //去除上次搜尋的地標
        if(old_address_marker!=null)
          old_address_marker.setMap(null);
        old_address_marker = marker;
      } else {
        alert('找不到這個地點，請重新輸入地址。');
      }
    });
    }
</script>
```
+ 利用ajax和REST Framework，透過url將資料庫中的data取出，呼叫place_marker_house或place_marker_traf函數，將地點存入陣列中，方便清除與重新標記。    
MarkerClusterer可以製作標記群集，把相近的標記歸類到同一點顯示，如此一來地圖標記就不會太密集。
```html
<script>
    var options = {
          imagePath: "{% static '/m'%}"
      };
    //獲得資料庫中資訊，根據地址在地圖上
      $(document).ready(function(){
        //凶宅
        var endpoint = '/map/api/house/';
        $.ajax({
          method:'GET',
          url:endpoint,
          success:function(data){
            for(var i = 0;i<data.length;i++){
              console.log(data[i].address);
              place_marker_house(map,data[i]);
            }
            markerClusterHouse = new MarkerClusterer(map, markersHouse,
                options,{ ignoreHiddenMarkers: true });
          },
          error:function(error_data){
            console.log("error");
            console.log(error_data);
          }
        })

        //交通事故
        var endpoint_traf = '/map/api/traffic/';
        $.ajax({
          method:'GET',
          url:endpoint_traf,
          success:function(data_traf){
            for(var i = 0;i<data_traf.length;i++){
              console.log(data_traf[i].address);
              place_marker_traf(map,data_traf[i]);
            }
            markerClusterTraf = new MarkerClusterer(map, markersTraffic,
                options,{ ignoreHiddenMarkers: true });
            setMapOnAll(null,1);
            markerClusterTraf.clearMarkers();
          },
          error:function(error_data){
            console.log("error");
            console.log(error_data);
          }
        })
      })
</script>
```
+ 放下交通事故的地圖標記，而icon是儲存在assets中的圖片，用template tag去取得圖片位址。   
google.maps.InfoWindow可以加入訊息視窗。   
marker的addListener控制資訊卡可以彈出或收回。
```html
<script>
    function place_marker_traf(map,data_traf){
      var check = -1;
      var marker = new google.maps.Marker({
        position: {lat:data_traf.lat, lng:data_traf.lng},
        map: map,
        icon: "{% static 'car.png'%}"
      });
      markersTraffic.push(marker);
      //加上點擊事件與資訊視窗
      var infowindow = new google.maps.InfoWindow({
        content:'<strong>地點:'+data_traf.address+'</strong><br/>時間：'+data_traf.date+'<br/>交通事故類別：'+data_traf.category
      });

      marker.addListener('click',function(){
        check = check * -1;
        if(check > 0){
          infowindow.open(map, marker);
        }else{
          infowindow.close();
        }
      });
    }
</script>
```
```html
<script>
    function place_marker_house(map,location){
        var check = -1;
        var marker = new google.maps.Marker({
          position: {lat:location.lat, lng:location.lng},
          map: map,
          icon: "{% static 'skull.png'%}"
        });
        markersHouse.push(marker);
        //加上點擊事件與資訊視窗
        var infowindow = new google.maps.InfoWindow({
          content:'<strong>事件'+location.category+'</strong><br/>地點：'+location.address+'<br/><a href="'+location.website+'">點我觀看詳情</a>'
        });

        marker.addListener('click',function(){
          check = check * -1;
          if(check > 0){
            infowindow.open(map, marker);
          }else{
            infowindow.close();
          }
        });
      }
</script>
```
    
    
## 第五步：套上css樣式
將css file存在assets資料夾中。  
主要控制側邊欄位的縮放與點擊。
```css
#map {
  height: 100%;
  margin-left:12%;
}
.search-box{
  position: fixed;
  z-index: 2;
  margin-left:13%;
  margin-top: 21px;
  padding: 6px 8px;
  background-color: #bbffee;
  display: none;
}
.side-bar{
  height: 100%;
  width: 12%;
  position: fixed;
  z-index: 1;
  top: 0;
  left: 0;
  background-color: #111;
  overflow-x: hidden;
  padding-top: 20px;
}
.side-bar a, .dropdown-btn, .side-bar label{
  padding: 6px 8px 6px 16px;
  text-decoration: none;
  font-size: 20px;
  color: #818181;
  display: block;
  border: none;
  background: none;
  width: 100%;
  text-align: left;
  cursor: pointer;
  outline: none;
}
.side-bar a:hover, .dropdown-btn:hover, .side-bar label:hover{
  color: #f1f1f1;
}
.active {
  background-color: green;
  color: white;
}
.dropdown-container {
  display: none;
  background-color: #262626;
  padding-left: 8px;
}
.dropdown-container input:checked + label {
  color: #f1f1f1;
}
.fa-caret-down {
  float: right;
  padding-right: 8px;
}
html, body{
  height: 100%;
  margin: 0;
  padding: 0;
  font-family: "Lato", sans-serif;
}
```

## 第六步：將資料存進database，以及migrate
每當model有做變動，或是第一次創建model時，需要使用migrate來告知django有哪些變動。  
`python manage.py makemigrations`   
創建migration文件。  
    
`python manage.py migrate`  
更新資料庫。  
    
---    
使用ORM來跟資料庫互動。
`python manage.py shell`開啟互動式shell。 
輸入以下指令，將csv檔案中的資料存入database。
```
> import csv
> from mapPage.models import HouseLocation
> with open('houseData.csv') as csvfile:
> ...     reader = csv.DictReader(csvfile)
> ...     for row in reader:
> ...       p=HouseLocation(address=row['address'],category=row['category'],
   ...: date=row['date'],lat=row['lat'],lng=row['lng'],article=row['article'],we
   ...: bsite=row['website'])
> ...       p.save()
> ...  
> exit()
```

## 參考資料
使用django REST framework傳輸資料庫內資料給javascript使用，參考：https://www.youtube.com/watch?v=B4Vmm3yZPgc     
在地圖上加點擊資訊視窗，參考：https://www.oxxostudio.tw/articles/201801/google-maps-5-marker-click-event.html     
地圖標記圖案：https://mapicons.mapsmarker.com/     
將csv加入資料庫：http://abhishekchhibber.com/django-importing-a-csv-file-to-database-models/    
轉換地址到經緯度：https://maplocation.sjfkai.com/    

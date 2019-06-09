# -*- coding: UTF-8 -*-
from django.shortcuts import render
from .models import HouseLocation
from rest_framework import viewsets
from .serializers import HouseSerializer

def map_Page(request):
    #houses = HouseLocation.objects.all()
    #return render(request,'mapPage/mapDisplay.html',{'houses':houses})
    return render(request,'mapPage/mapDisplay.html')

class housesView(viewsets.ModelViewSet):
    queryset = HouseLocation.objects.all()
    serializer_class = HouseSerializer

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

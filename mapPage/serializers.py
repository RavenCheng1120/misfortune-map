from rest_framework import serializers
from .models import HouseLocation

class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseLocation
        fields = '__all__'
        #fields = ('id','address','article','website','date')

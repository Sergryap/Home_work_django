from rest_framework import serializers
from .models import *


# TODO: опишите необходимые сериализаторы

class SensorSerializer(serializers.ModelSerializer):
	class Meta:
		model = Sensor
		fields = "__all__"


class MeasurementSerializer(serializers.ModelSerializer):

	class Meta:
		model = Measurement
		fields = ['id', 'temperature', 'time_create', 'time_update', 'sensor', 'image']

	image = serializers.ImageField(allow_empty_file=True, use_url=True, allow_null=True, default=None)



class SensorDetailSerializer(serializers.ModelSerializer):
	measurements = MeasurementSerializer(read_only=True, many=True)

	class Meta:
		model = Sensor
		fields = ['id', 'name', 'description', 'measurements']

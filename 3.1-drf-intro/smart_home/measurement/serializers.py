from rest_framework import serializers
from .models import *


# TODO: опишите необходимые сериализаторы

class SensorSerializer(serializers.ModelSerializer):
	class Meta:
		model = Sensor
		fields = "__all__"


class MeasurementSerializer(serializers.ModelSerializer):
	image = serializers.ImageField(allow_empty_file=True, use_url=True, allow_null=True, default=None)

	class Meta:
		model = Measurement
		fields = "__all__"


class SensorDetailSerializer(serializers.ModelSerializer):
	measurements = MeasurementSerializer(read_only=True, many=True)

	class Meta:
		model = Sensor
		fields = ['id', 'name', 'description', 'measurements']

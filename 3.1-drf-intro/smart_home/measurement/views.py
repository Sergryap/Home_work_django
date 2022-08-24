from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser, JSONParser


class SensorDetailAPIView(generics.RetrieveUpdateAPIView):
	queryset = Sensor.objects.all()
	serializer_class = SensorDetailSerializer


class SensorAPIList(generics.ListCreateAPIView):
	queryset = Sensor.objects.all()
	serializer_class = SensorSerializer


class SensorAPIUpdate(generics.RetrieveUpdateAPIView):
	queryset = Sensor.objects.all()
	serializer_class = SensorSerializer


class MeasurementAPIList(generics.ListCreateAPIView):
	queryset = Measurement.objects.all()
	serializer_class = MeasurementSerializer
	parser_classes = [JSONParser, FileUploadParser]


class MeasurementAPIUpdate(generics.RetrieveUpdateAPIView):
	queryset = Measurement.objects.all()
	serializer_class = MeasurementSerializer


# Далее оставил для себя, чтоб лучше понимать как работают классы
class OldSensorDetailAPIView(generics.ListAPIView):
	def get(self, request, *args, **kwargs):
		pk = kwargs.get("pk", None)
		if not pk:
			return Response({"error": "Method GET not allowed"})

		try:
			queryset = Sensor.objects.get(pk=pk)
		except:
			return Response({"error": "Object does not exists"})

		serializer = SensorDetailSerializer(queryset)
		return Response({"sensor": serializer.data})


class SensorAPIView(APIView):
	def get(self, request):
		s = Sensor.objects.all()
		return Response({'sensors': SensorSerializer(s, many=True).data})

	def post(self, request):
		serializer = SensorSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response({'sensor': serializer.data})

	def put(self, request, *args, **kwargs):
		pk = kwargs.get("pk", None)
		if not pk:
			return Response({"error": "Method PUT not allowed"})

		try:
			instance = Sensor.objects.get(pk=pk)
		except:
			return Response({"error": "Object does not exists"})

		serializer = SensorSerializer(data=request.data, instance=instance)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response({"sensor": serializer.data})


class MeasurementAPIView(APIView):
	def post(self, request):
		serializer = MeasurementSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(serializer.data)

	def put(self, request, *args, **kwargs):
		pk = kwargs.get("pk", None)
		if not pk:
			return Response({"error": "Method PUT not allowed"})

		try:
			instance = Measurement.objects.get(pk=pk)
		except:
			return Response({"error": "Object does not exists"})

		serializer = MeasurementSerializer(data=request.data, instance=instance)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(serializer.data)

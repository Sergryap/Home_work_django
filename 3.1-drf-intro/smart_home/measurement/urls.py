from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('sensors/', SensorAPIList.as_view()),  # Получени информации о датчиках, а также создание датчика
    path('sensors/<int:pk>/', SensorAPIUpdate.as_view()),  # Изменение датчика
    path('sensor_details/<int:pk>/', SensorDetailAPIView.as_view()),  # Получени информации о датчиках
    path('мeasurement/', MeasurementAPIList.as_view()),  # создание измерения
    path('мeasurement/<int:pk>/', MeasurementAPIUpdate.as_view())  # Изменение измерения
]

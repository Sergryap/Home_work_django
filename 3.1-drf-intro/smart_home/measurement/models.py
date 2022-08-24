from django.db import models
from datetime import datetime as dt
from django.utils import timezone


# TODO: опишите модели датчика (Sensor) и измерения (Measurement)

class Sensor(models.Model):
	name = models.CharField(max_length=50, verbose_name="Название")
	description = models.CharField(max_length=255, blank=True, null=True, verbose_name="Описание")

	class Meta:
		verbose_name = 'Датчик'
		verbose_name_plural = 'Датчики'
		ordering = ['pk']

	def __str__(self):
		return f"{self.pk}_{self.name}"


class Measurement(models.Model):
	temperature = models.FloatField(verbose_name="Температура при измерении")
	time_create = models.DateTimeField(auto_now_add=True)
	time_update = models.DateTimeField(auto_now=True)
	sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='measurements', verbose_name='Датчик')
	image = models.ImageField(upload_to='measurement_images', null=True, blank=True, verbose_name='Изображение')


	class Meta:
		verbose_name = 'Измерение'
		verbose_name_plural = 'Измерения'
		ordering = ['-time_create', '-time_update']

	def __str__(self):
		return f"{self.sensor.name}_{self.date}_{self.temperature}"

from rest_framework import serializers

from django_testing import settings
from students.models import Course


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "students")

    def validate(self, data):
        if data.get('students', None) and len(data['students']) > settings.MAX_STUDENTS_PER_COURSE:
            raise serializers.ValidationError(f"Число студентов на курсе не должно быть больше {settings.MAX_STUDENTS_PER_COURSE}!")
        return data

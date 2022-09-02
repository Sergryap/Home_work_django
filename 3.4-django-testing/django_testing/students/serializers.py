from rest_framework import serializers

from students.models import Course


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "students")

    def validate(self, data):
        if len(data['students']) > 20:
            raise serializers.ValidationError("Число студентов на курсе не должно быть больше 20!")
        return data

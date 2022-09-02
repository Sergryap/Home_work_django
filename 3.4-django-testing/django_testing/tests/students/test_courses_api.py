import random
import pytest
from django.urls import reverse
from model_bakery import baker
from rest_framework.test import APIClient
from students.models import Course


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def course():
    return Course.objects.create(name='Test')


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


# проверка получения 1го курса (retrieve-логика)
@pytest.mark.django_db
def test_get_course(client, course_factory):
    course = course_factory(_quantity=1)
    response = client.get(f"/api/v1/courses/{course[0].id}/")
    data = response.json()
    assert Course.objects.get(pk=course[0].id).name == data['name']


# проверка получения списка курсов (list-логика)
@pytest.mark.django_db
def test_get_courses(client, course_factory):
    courses = course_factory(_quantity=10)
    response = client.get(f"/api/v1/courses/")
    data = response.json()
    for i, course in enumerate(data):
        assert course['name'] == courses[i].name


# проверка фильтрации списка курсов по id
@pytest.mark.django_db
def test_filter_courses(client, course_factory):
    courses = course_factory(_quantity=10)
    id_course = courses[random.randint(0, len(courses) - 1)].pk
    response = client.get(f"/api/v1/courses/{id_course}/")
    data = response.json()
    assert data['id'] == id_course


# проверка фильтрации списка курсов по name
@pytest.mark.django_db
def test_filter_name_courses(client, course_factory):
    courses = course_factory(_quantity=10)
    name_course = courses[random.randint(0, len(courses) - 1)].name
    response = client.get(f"/api/v1/courses/?name={name_course}")
    data = response.json()
    assert data[0]['name'] == name_course

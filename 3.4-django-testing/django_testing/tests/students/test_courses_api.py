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
def courses(course_factory):
    return course_factory(_quantity=10)


@pytest.fixture
def id_course(courses):
    return random.choice([course.pk for course in courses])


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
def test_filter_courses(client, course_factory, id_course):
    response = client.get(f"/api/v1/courses/{id_course}/")
    data = response.json()
    assert data['id'] == id_course


# проверка фильтрации списка курсов по name
@pytest.mark.django_db
def test_filter_name_course(client, course_factory, courses):
    name_course = courses[random.randint(0, len(courses) - 1)].name
    response = client.get(f"/api/v1/courses/?name={name_course}")
    data = response.json()
    assert data[0]['name'] == name_course


# тест успешного создания курса
@pytest.mark.django_db
def test_create_course(client):
    count = Course.objects.count()
    name_course = 'test_course'
    client.post("/api/v1/courses/", data={'name': f'{name_course}'})
    assert Course.objects.count() == count + 1
    response = client.get(f"/api/v1/courses/?name={name_course}")
    data = response.json()
    assert data[0]['name'] == name_course


# тест успешного обновления курса
@pytest.mark.django_db
def test_update_course(client, course_factory, id_course):
    new_name_course = 'test_course'
    data_update = {'name': f'{new_name_course}'}
    client.patch(f"/api/v1/courses/{id_course}/", data=data_update)
    assert Course.objects.get(pk=id_course).name == new_name_course


# тест успешного удаления курса
@pytest.mark.django_db
def test_delete_course(client, course_factory, id_course):
    client.delete(f"/api/v1/courses/{id_course}/")
    assert Course.objects.filter(pk=id_course).count() == 0

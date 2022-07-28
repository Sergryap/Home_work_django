from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.urls import reverse
import csv


def index(request):
    return redirect(reverse('bus_stations'))


def count_row():
    """Подсчет количества строк в файле, кроме первой"""
    with open('data-398-2018-08-30.csv', encoding='utf-8') as csvfile:
        rows = csv.reader(csvfile, delimiter=",")
        return len(list(rows)[1:])


def count_page(n):
    """Подсчет количества страниц пагинации"""
    i = count_row()
    return i // n if not i % n else i // n + 1


def get_ind(page: int, n: int):
    """Вычисление индексов для загрузки части данных из общего списка для страницы page"""
    start_ind = (page - 1) * n
    end_ind = page * n
    if end_ind > count_row():
        end_ind = end_ind - n + count_row() % n
    return start_ind, end_ind


def stations_load(page: int, n: int) -> list:
    """функция загрузки данных из csv-файла для заданной страницы"""
    stations = []
    start_ind = get_ind(page, n)[0]
    end_ind = get_ind(page, n)[1]
    with open('data-398-2018-08-30.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = [i for i in reader]

        for row in rows[start_ind:end_ind]:
            stations.append({
                'Name': row['Name'],
                'Street': row['Street'],
                'District': row['District']
            })
    return stations


def bus_stations(request, n=10):
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице
    # n - количество станций на странице

    pages = [i for i in range(count_page(n))]
    page_number = int(request.GET.get('page', 1))
    paginator = Paginator(pages, 1)
    page = paginator.get_page(page_number)

    context = {
        'bus_stations': stations_load(page_number, n),
        'page': page
    }
    return render(request, 'stations/index.html', context)

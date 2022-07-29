from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.urls import reverse
import csv
from pprint import pprint


def index(request):
    return redirect(reverse('bus_stations'))


def get_content():
    with open('data-398-2018-08-30.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return [(i, {'Name': station['Name'],
                     'Street': station['Street'],
                     'District': station['District']})
                for i, station in enumerate(reader)]


def bus_stations(request, n=10):
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице
    # n - количество станций на странице

    content = get_content()
    page_number = int(request.GET.get('page', 1))
    paginator = Paginator(content, n)
    page = paginator.get_page(page_number)
    stations = [i[1] for i in page]

    context = {
        'bus_stations': stations,
        'page': page
    }
    return render(request, 'stations/index.html', context)

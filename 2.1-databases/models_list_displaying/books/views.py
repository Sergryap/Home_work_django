from django.shortcuts import render
from .models import Book
from datetime import datetime as dt
from django.core.paginator import Paginator
from django.db.models import Count


def get_context(books: Book):
    """Создание переменных context для каталога"""
    for book in books:
        book.pub_date_str = dt.strftime(book.pub_date, '%Y-%m-%d')
    return {'books': books}


def get_context_paginator(pub_date: str):
    """Создание переменных context для пагинатора"""
    dates = (Book.objects
             .values('pub_date')
             .annotate(total=Count('id'))
             .order_by('pub_date'))
    dates = [dt.strftime(c['pub_date'], '%Y-%m-%d') for c in dates]
    page_number = dates.index(pub_date) + 1
    paginator = Paginator(dates, 1)
    page = paginator.get_page(page_number)
    i = dates.index(pub_date)
    page_next = dates[i + 1] if i < len(dates) - 1 else None
    page_previous = dates[i - 1] if i > 0 else None

    return {'page': page,
            'page_next': page_next,
            'page_previous': page_previous
            }


def books_view(request):
    template = 'books/books_list.html'
    books = Book.objects.all().order_by('pub_date')
    context = get_context(books)
    return render(request, template, context)


def books_view_date(request, pub_date):
    template = 'books/books_list.html'
    books = Book.objects.all().filter(pub_date=dt.strptime(pub_date, '%Y-%m-%d'))
    context = get_context(books)
    context.update(get_context_paginator(pub_date))
    return render(request, template, context)

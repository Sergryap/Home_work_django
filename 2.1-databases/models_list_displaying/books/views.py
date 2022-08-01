from django.shortcuts import render
from .models import Book
from datetime import datetime as dt


def get_context(books):
    for book in books:
        book.pub_date_f = dt.strftime(book.pub_date, '%Y-%m-%d')
    return {'books': books}


def books_view(request):
    template = 'books/books_list.html'
    books = Book.objects.all()
    context = get_context(books)
    return render(request, template, context)


def books_view_date(request, pub_date):
    template = 'books/books_list.html'
    pub_date_date = dt.strptime(pub_date, '%Y-%m-%d')
    books = Book.objects.all().filter(pub_date=pub_date_date)
    context = get_context(books)
    return render(request, template, context)

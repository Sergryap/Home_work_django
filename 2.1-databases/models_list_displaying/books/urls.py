from django.urls import path
from .views import books_view, books_view_date


urlpatterns = [
	path('books/', books_view, name='books'),
	path('books/<slug:pub_date>/', books_view_date, name='pub_date'),
]

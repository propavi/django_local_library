from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('author/<int:pk>/update/', views.AuthorUpdateView.as_view(), name='author-update'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('mark-returned/', views.MarkBookReturnedView.as_view(), name='mark-returned'),
    path('book/<uuid:pk>/return/', views.return_book, name='return-book'),
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
    
    path('borrowed/', views.AllBorrowedBooksListView.as_view(), name='all-borrowed'),
]

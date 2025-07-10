from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy

def index(request):
    """View function for home page of site."""
    num_visits = request.session.get("num_visits",0)
    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        "num_visits" : num_visits + 1
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class AuthorListView(generic.ListView):
    """Generic class-based list view for a list of authors."""
    model = Author
    paginate_by = 10

class AuthorDetailView(generic.DetailView):
    """Generic class-based detail view for an author."""
    model = Author

class BookListView(generic.ListView):
    model = Book
    context_object_name = "book_list"
    template_name = 'catalog/book_list.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context

class BookDetailView(generic.DetailView):
    model = Book
    
    def book_detail_view(request, primary_key):
        book = get_object_or_404(Book, pk=primary_key)
        return render(request, 'catalog/book_detail.html', context={'book': book})

class AuthorUpdateView(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    template_name = 'catalog/author_form.html'
    success_url = reverse_lazy('authors')





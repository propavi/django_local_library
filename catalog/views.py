from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from catalog.models import BookInstance
from catalog.models import BookInstance
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Author
from django.http import HttpResponseRedirect
from django.urls import reverse

class MyView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'  # Optional custom login URL
    redirect_field_name = 'next' 


@login_required
def secret_page(request):
    return HttpResponse("You are logged in and can see this!")


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

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')  # 'o' = on loan
            .order_by('due_back')
        )
class MarkBookReturnedView(PermissionRequiredMixin, View):
    permission_required = 'catalog.can_mark_returned'

    def get(self, request, *args, **kwargs):
        return HttpResponse("You can mark books as returned.")

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def return_book(request, pk):
    """View to mark a BookInstance as returned."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # Update fields
    book_instance.status = 'a'  # 'a' = Available
    book_instance.borrower = None
    book_instance.due_back = None
    book_instance.save()

    return redirect('my-borrowed') 



class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/11/2023'}
    permission_required = 'catalog.add_author'

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = '__all__'
    permission_required = 'catalog.change_author'

class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.delete_author'

    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception:
            return HttpResponseRedirect(
                reverse("author-delete", kwargs={"pk": self.object.pk})
            )

class AllBorrowedBooksListView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    permission_required = 'catalog.can_mark_returned'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

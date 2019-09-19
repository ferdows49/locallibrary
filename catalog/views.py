import datetime
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from catalog.forms import RenewBookForm
from catalog.models import Book, BookInstance, Author, Genre, Language
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

def index(request):
    """view page for homepage of site"""

    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_avaiable = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_avaiable': num_instances_avaiable,
        'num_authors': num_authors,
    }
    return render(request, 'index.html', context=context)

@permission_required('catalog.can_make_returned')
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        form = RenewBookForm(request.POST)

        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            return HttpResponseRedirect(reverse('all-borrowed'))
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})
    
    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)

class AuthorListViews(generic.ListView):
    model = Author
    paginate_by = 2

    def get_queryset(self):
        return Author.objects.all()

    def get_context_data(self, **kwargs):
        context = super(AuthorListViews, self).get_context_data(**kwargs)
        context['some_data'] = 'This is just some data'
        return context

    template_name='locallibrary/catalog/templates/catalog/author_list.html'

class AuthorDetailView(generic.DetailView):
    model = Author

    def author_detail_view(request, primary_key):
        
        try:
            author = Author.objects.get(pk=primary_key)
        except Author.DoesNotExist:
            raise Http404('author does not exist')
        
        return render(request, 'catalog/author_detail.html', context={'author': author})

class BookListView(generic.ListView):
    model = Book
    paginate_by = 3

    def get_queryset(self):
        return Book.objects.all() #filter(title__icontains='The')[:2]

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['some_data'] = 'This is just some data'
        return context

    template_name='locallibrary/catalog/templates/catalog/book_list.html'

class BookDetailView(generic.DetailView):
    model = Book
    def book_detail_view(request, primary_key):
        
        try:
            book = Book.objects.get(pk=primary_key)
        except Book.DoesNotExist:
            raise Http404('Book does not exist')
        
        return render(request, 'catalog/book_detail.html', context={'book': book})

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 3

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from catalog.models import Author

class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial = {'date_of_death': '05/06/2018'}

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
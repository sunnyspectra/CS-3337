from django.http import HttpResponse
from django.shortcuts import render
from .models import MainMenu
from .forms import BookForm
from django.http import HttpResponseRedirect
from .models import Book

from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    #return HttpResponse("<h1> Hello </h1>")
    return render(request, 'bookMng/index.html',
    {
        'item_list': MainMenu.objects.all()
    })

def aboutus(request):
    #return HttpResponse("<h1> Hello </h1>")
    return render(request, 'bookMng/aboutus.html',
    {
        'item_list': MainMenu.objects.all()
    })

@login_required(login_url=reverse_lazy('login'))
def postbook(request):
    #return HttpResponse("<h1> Hello </h1>")
    submitted = False
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            try:
                book.username = request.user
            except Exception:
                pass
            book.save()
            return HttpResponseRedirect('/postbook?submitted=True')
    else:
        form = BookForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'bookMng/postbook.html',
    {
        'item_list': MainMenu.objects.all(),
        'form': form,
        'submitted':submitted
    })

@login_required(login_url=reverse_lazy('login'))
def displaybooks(request):
    #return HttpResponse("<h1> Hello </h1>")
    books = Book.objects.all()
    for b in books:
        b.pic_path = b.picture.url[14:]
    return render(request, 'bookMng/displaybooks.html',
    {
        'item_list': MainMenu.objects.all(),
        'books': books
    })

@login_required(login_url=reverse_lazy('login'))
def book_detail(request, book_id):
    #return HttpResponse("<h1> Hello </h1>")
    book = Book.objects.get(id=book_id)
    book.pic_path = book.picture.url[14:]
    return render(request, 'bookMng/book_detail.html',
    {
        'item_list': MainMenu.objects.all(),
        'book': book
    })

class Register(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register-success')

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)



@login_required(login_url=reverse_lazy('login'))
def mybooks(request):
    #return HttpResponse("<h1> Hello </h1>")
    books = Book.objects.filter(username=request.user)
    for b in books:
        b.pic_path = b.picture.url[14:]
    return render(request, 'bookMng/mybooks.html',
    {
        'item_list': MainMenu.objects.all(),
        'books': books
    })

@login_required(login_url=reverse_lazy('login'))
def book_delete(request, book_id):
    #return HttpResponse("<h1> Hello </h1>")
    book = Book.objects.get(id=book_id)
    book.delete()
    return render(request, 'bookMng/book_delete.html',
    {
        'item_list': MainMenu.objects.all(),
        'book': book
    })

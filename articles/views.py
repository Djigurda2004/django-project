from django.shortcuts import render,redirect,get_object_or_404
from .models import Article
from .forms import ArticleForm
from django.views.generic import DetailView,UpdateView,DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.db.models import Q

def articles(request):
    query = request.GET.get("q", "")
    articles = Article.objects.all()
    if query:
        articles = articles.filter(Q(title__icontains=query) | Q(author__username__icontains=query))
    paginator = Paginator(articles, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "articles/articles.html", {"page_obj": page_obj,"query": query})

class ArticleDetailView(DetailView):
    model = Article
    template_name = "articles/details_view.html"
    context_object_name = 'article'
    def get_object(self,queryset=None):
        article = super().get_object(queryset)
        article.views += 1
        article.save(update_fields=["views"])
        return article
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(parent=None).order_by('-created_at')
        return context


class ArticleEditView(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = Article
    template_name = "articles/create_article.html"
    form_class = ArticleForm
    raise_exception = True
    def test_func(self):
        article = self.get_object()
        return article.author == self.request.user


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = Article
    success_url = '/articles/'
    raise_exception = True
    def test_func(self):
        article = self.get_object()
        return article.author == self.request.user


@login_required
def create_article(request):
    error = ''
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('articles:articles')
        else:
            error = 'The form is incorrect'
    form = ArticleForm()
    return render(request,'articles/create_article.html',{'form' : form,'error' : error})


@login_required
def like_article(request,pk):
    article = get_object_or_404(Article,pk=pk)
    if request.user in article.likes.all():
        article.likes.remove(request.user)
    else:
        article.likes.add(request.user)
    if request.headers.get('HX-Request'):
        return render(request,'articles/like_area.html',{'article':article})
    return redirect("articles:detail",pk=pk)


@login_required
def liked_articles(request):
    articles = request.user.liked_articles.all()
    return render(request,'articles/liked_articles.html',{'articles':articles})
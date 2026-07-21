from django.shortcuts import render,redirect,get_object_or_404
from .models import Article
from .forms import ArticleForm
from django.views.generic import DetailView,UpdateView,DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .utils import pagination
from .redis_keys import get_article_views_key
from common.redis_client import redis_client

def articles(request):
    articles = Article.objects.all().order_by("-created_at")
    data = pagination(request,articles,5)
    return render(request, "articles/articles.html", data)

class ArticleDetailView(DetailView):
    model = Article
    template_name = "articles/details_view.html"
    context_object_name = 'article'
    def get_object(self,queryset=None):
        article = super().get_object(queryset)
        redis_client.incr(get_article_views_key(article.id))
        return article
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(parent=None).order_by('-created_at')
        context['redis_views'] = redis_client.get(get_article_views_key(self.object.id))
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
            redis_client.set(get_article_views_key(article.id),0)
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
    articles = request.user.liked_articles.all().order_by("-created_at")
    articles_count = articles.count()
    data = pagination(request,articles,5)
    data["articles_count"] = articles_count
    return render(request,'articles/liked_articles.html',data)
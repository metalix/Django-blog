from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import View
from django.views.decorators.http import require_POST
from django.db.models import Count
from taggit.models import Tag
from .models import Article, Comment
from .forms import CommentForm, SearchForm

# Create your views here.
def list_of_articles(request, tag_slug = None):
    articles = Article.publishedArticles.all()

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug = tag_slug)
        articles = articles.filter(tags__in = [tag])

    paginator = Paginator(articles, 3)
    page_number = request.GET.get('page', 1)

    try:
        articles = paginator.page(page_number)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        articles = paginator.page(1)    

    return render(request, 'blog/list.html', {'articles': articles, 'tag': tag})


def article_details(request, year, month, day, article):
    try:
        article = get_object_or_404(Article, status=Article.Status.PUBLISHED,
                                    slug=article,
                                    publish__year=year,
                                    publish__month=month,
                                    publish__day=day
                                    )
        
        comments = article.comments.filter(active=True)
        
        form = CommentForm()

        article_tags_ids = article.tags.values_list('id', flat=True)
        similar_published_articles = Article.publishedArticles.filter(tags__in=article_tags_ids)\
                                .exclude(id=article.id)
        similar_articles = similar_published_articles.annotate(same_tags_in_article=Count('tags'))\
                                .order_by('-same_tags_in_article','-publish')[:3]
    except Article.DoesNotExist:
        raise Http404('No article found.')
    
    return render(request, 'blog/detail.html', {
        'article': article,
        'comments': comments,
        'form': form,
        'similar_articles': similar_articles
        })

def article_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Article.objects.raw("SELECT * FROM blog_article WHERE MATCH (title, body) AGAINST (%s)", [query])

    return render(request, 
                  'blog/search.html',
                  { 'form': form, 'query': query, 'results': results }
                  )

@require_POST
def comment_for_article(request, article_id):
    article = get_object_or_404(Article, id = article_id, status = Article.Status.PUBLISHED)
    comment = None

    form = CommentForm(data=request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.article = article
        comment.save()

    return render(request, 'blog/comment.html', {'article': article, 'form': form, 'comment': comment})


class SearchArticleView(View):
    query = None
    results = []
    form_class = SearchForm

    def get(self, request):
        form = self.form_class
        
        if 'query' in request.GET:
            
            form = self.form_class(request.GET)
            if form.is_valid():
                query = form.cleaned_data['query']
                results = Article.objects.raw("SELECT * FROM blog_article WHERE MATCH (title, body) AGAINST (%s)", [query])
                return render(request, 'blog/search.html', {'form': form, 'query': query,'results': results})
                
        return render(request, 'blog/search.html', {'form': form})

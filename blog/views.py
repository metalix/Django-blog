from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST
from .models import Article, Comment
from .forms import CommentForm

# Create your views here.
def list_of_articles(request):
    articles = Article.publishedArticles.all()

    paginator = Paginator(articles, 3)
    page_number = request.GET.get('page', 1)

    try:
        articles = paginator.page(page_number)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        articles = paginator.page(1)    

    return render(request, 'blog/list.html', {'articles': articles})


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
    except Article.DoesNotExist:
        raise Http404('No article found.')
    
    return render(request, 'blog/detail.html', {
        'article': article,
        'comments': comments,
        'form': form
        })


@require_POST
def comment_for_article(request, article_id):
    article = get_object_or_404(Article, id = article_id, status = Article.Status.PUBLISHED)
    comment = None

    form = CommentForm(data=request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.article = article
        comment.save(
        )

    return render(request, 'blog/comment.html', {article: article, 'form': form, 'comment': comment})
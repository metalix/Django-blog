from django.shortcuts import render
from django.http import HttpResponse
from .models import Article

# Create your views here.
def list_of_articles(request):
    articles = Article.publishedArticles.all()

    return render(request, 'blog/list.html', {'articles': articles})
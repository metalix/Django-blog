from django import template
from django.db.models import Count
from ..models import Article

register = template.Library()

@register.simple_tag
def total_articles():
    return Article.publishedArticles.count()

@register.inclusion_tag('blog/latest_articles.html')
def show_latest_articles(count=3):
    latest_articles = Article.publishedArticles.order_by('-publish')[:count]
    return {'latest_articles': latest_articles}

@register.inclusion_tag('blog/most_commented_articles.html')
def show_most_commented_articles(count=3):
    most_commented_articles = Article.publishedArticles.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]
    
    return {
        "most_commented_articles": most_commented_articles
        
    }

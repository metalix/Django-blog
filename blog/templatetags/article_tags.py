from django import template
from ..models import Article

register = template.Library()

@register.simple_tag
def total_articles():
    return Article.publishedArticles.count()

@register.inclusion_tag('blog/latest_articles.html')
def show_latest_articles(count=3):
    latest_articles = Article.publishedArticles.order_by('-publish')[:count]
    return {'latest_articles': latest_articles}
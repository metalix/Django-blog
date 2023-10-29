from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.list_of_articles, name='list_of_articles'),
    #path('<int:id>/', views.article_details, name='article_details'),
    path('<int:year>/<int:month>/<int:day>/<slug:article>/', views.article_details, name='article_details'),
    path('<int:article_id>/comment/', views.comment_for_article, name='comment_for_article'),
    path('tag/<slug:tag_slug>', views.list_of_articles, name='list_of_articles_by_tag')
]

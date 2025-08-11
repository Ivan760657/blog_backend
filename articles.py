from ninja import Router
from ninja.security import HttpBearer
from django.shortcuts import get_object_or_404
from typing import List
from .models import Article, Category
from .schemas import ArticleIn, ArticleOut, UserOut
from .auth import AuthBearer
import structlog

logger = structlog.get_logger(__name__)
articles_router = Router(tags=["Статьи"])

@articles_router.post("/", response=ArticleOut, auth=AuthBearer())
def create_article(request, payload: ArticleIn):
    article = Article.objects.create(
        title=payload.title,
        content=payload.content,
        author=request.auth
    )
    if payload.category_ids:
        article.categories.add(*payload.category_ids)
    logger.info(f"Создана статья {article.id} пользователем {request.auth.username}")
    return article

@articles_router.get("/", response=List[ArticleOut])
def list_articles(request):
    return Article.objects.all().select_related('author')

@articles_router.get("/{article_id}", response=ArticleOut)
def get_article(request, article_id: int):
    return get_object_or_404(Article, id=article_id)

@articles_router.put("/{article_id}", response=ArticleOut, auth=AuthBearer())
def update_article(request, article_id: int, payload: ArticleIn):
    article = get_object_or_404(Article, id=article_id)
    if article.author != request.auth:
        return {"message": "Редактировать можно только свои статьи"}, 403
    article.title = payload.title
    article.content = payload.content
    article.categories.set(payload.category_ids)
    article.save()
    logger.info(f"Обновлена статья {article.id} пользователем {request.auth.username}")
    return article

@articles_router.delete("/{article_id}", response={204: None}, auth=AuthBearer())
def delete_article(request, article_id: int):
    article = get_object_or_404(Article, id=article_id)
    if article.author != request.auth:
        return {"message": "Удалять можно только свои статьи"}, 403
    article.delete()
    logger.info(f"Удалена статья {article_id} пользователем {request.auth.username}")
    return 204, None
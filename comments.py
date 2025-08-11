from ninja import Router
from ninja.security import HttpBearer
from django.shortcuts import get_object_or_404
from typing import List
from .models import Article, Comment
from .schemas import CommentIn, CommentOut
from .auth import AuthBearer
import structlog

logger = structlog.get_logger(__name__)
comments_router = Router(tags=["Комментарии"])

@comments_router.post("/articles/{article_id}/comments", response=CommentOut, auth=AuthBearer())
def create_comment(request, article_id: int, payload: CommentIn):
    article = get_object_or_404(Article, id=article_id)
    comment = Comment.objects.create(article=article, author=request.auth, text=payload.text)
    logger.info(f"Создан комментарий {comment.id} пользователем {request.auth.username}")
    return comment

@comments_router.get("/articles/{article_id}/comments", response=List[CommentOut])
def list_comments(request, article_id: int):
    article = get_object_or_404(Article, id=article_id)
    return article.comments.all().select_related('author')

@comments_router.put("/comments/{comment_id}", response=CommentOut, auth=AuthBearer())
def update_comment(request, comment_id: int, payload: CommentIn):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.auth:
        return {"message": "Редактировать можно только свои комментарии"}, 403
    comment.text = payload.text
    comment.save()
    logger.info(f"Обновлен комментарий {comment.id} пользователем {request.auth.username}")
    return comment

@comments_router.delete("/comments/{comment_id}", response={204: None}, auth=AuthBearer())
def delete_comment(request, comment_id: int):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.auth:
        return {"message": "Удалять можно только свои комментарии"}, 403
    comment.delete()
    logger.info(f"Удалён комментарий {comment_id} пользователем {request.auth.username}")
    return 204, None
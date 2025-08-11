from ninja import Schema
from typing import List

class UserIn(Schema):
    username: str
    password: str

class UserOut(Schema):
    username: str

class ArticleIn(Schema):
    title: str
    content: str
    category_ids: List[int] = []

class ArticleOut(Schema):
    id: int
    title: str
    content: str
    author: UserOut
    created_at: str

class CommentIn(Schema):
    text: str

class CommentOut(Schema):
    id: int
    text: str
    author: UserOut
    created_at: str
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ArticleType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    US: _ClassVar[ArticleType]
    WORLD: _ClassVar[ArticleType]
    BUSINESS: _ClassVar[ArticleType]
    ARTS: _ClassVar[ArticleType]
    LIFESTYLE: _ClassVar[ArticleType]
US: ArticleType
WORLD: ArticleType
BUSINESS: ArticleType
ARTS: ArticleType
LIFESTYLE: ArticleType

class Article(_message.Message):
    __slots__ = ("articleType", "author", "title", "summary", "comments")
    ARTICLETYPE_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    COMMENTS_FIELD_NUMBER: _ClassVar[int]
    articleType: ArticleType
    author: str
    title: str
    summary: str
    comments: _containers.RepeatedCompositeFieldContainer[Comment]
    def __init__(self, articleType: _Optional[_Union[ArticleType, str]] = ..., author: _Optional[str] = ..., title: _Optional[str] = ..., summary: _Optional[str] = ..., comments: _Optional[_Iterable[_Union[Comment, _Mapping]]] = ...) -> None: ...

class Comment(_message.Message):
    __slots__ = ("author", "comment")
    AUTHOR_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    author: str
    comment: str
    def __init__(self, author: _Optional[str] = ..., comment: _Optional[str] = ...) -> None: ...

class SubscriptionRequest(_message.Message):
    __slots__ = ("articleType",)
    ARTICLETYPE_FIELD_NUMBER: _ClassVar[int]
    articleType: ArticleType
    def __init__(self, articleType: _Optional[_Union[ArticleType, str]] = ...) -> None: ...

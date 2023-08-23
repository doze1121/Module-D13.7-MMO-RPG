from django.urls import path

from .views import *

app_name = 'newsboard'
urlpatterns = [

    # -----------------posts---------------------
    path('', PostList.as_view(), name='home'),
    path('<int:pk>', PostDetail.as_view(), name='detail'),
    path('create/', PostCreate.as_view(), name='create'),
    path('update/<int:post_pk>', PostUpdate.as_view(), name='update'),
    # -----------------endposts---------------------

    # -----------------comments---------------------
    path('<int:post_pk>/comments', CommentsList.as_view(), name='post_comments'),
    path('<int:post_pk>/create_comment', CommentCreate.as_view(), name='comment_create'),
    path('<int:post_pk>/comments/<int:comment_pk>/confirm', CommentConfirm.as_view(), name='comment_confirm'),
    path('<int:post_pk>/comments/<int:comment_pk>/reject', CommentReject.as_view(), name='comment_reject'),
    path('<int:post_pk>/comments/<int:comment_pk>/delete', CommentDelete.as_view(), name='comment_delete'),
    path('my_comments/', MyComments.as_view(), name='my_comments'),
    # -----------------endcomments---------------------
]
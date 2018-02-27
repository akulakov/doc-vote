
from django.conf.urls import url, include
from django.urls import path

from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.MainRedirectView.as_view(), name='main_redirect'),
    path('<int:pk>/', views.PageView.as_view(), name='page'),

    # path('<int:page_pk>/delete-node/<int:pk>/', views.DeleteNodeView.as_view(), name='delete_node'),
    # path('/vote/', views.VoteView.as_view(), name='vote'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, dict(next_page='/'), name='logout'),

    path('<int:page_pk>/vote/<int:pk>/<int:plus>/', views.VoteView.as_view(), name='vote'),
    path('<int:page_pk>/vote/<int:pk>/<str:dir>/', views.MoveNodeView.as_view(), name='move_node'),

    path('ajax-node/<int:pk>/', views.AjaxNodeView.as_view(), name='ajax_node'),
    path('node/<int:pk>/', views.NodeView.as_view(), name='node'),

    path('<int:node_pk>/create-update-comment/<int:pk>/', views.CreateUpdateCommentView.as_view(), name='create_update_comment'),
    path('<int:node_pk>/create-update-comment/', views.CreateUpdateCommentView.as_view(), name='create_update_comment'),

    path('<int:pk>/create-update-node/', views.CreateUpdateNodeView.as_view(), name='create_update_node'),
    path('<int:pk>/ajax-create-update-node/<int:node_pk>/after/', views.AjaxCreateUpdateNodeView.as_view(after=True), name='ajax_create_update_node'),
    path('<int:pk>/create-update-node/<int:node_pk>/after/', views.CreateUpdateNodeView.as_view(after=True), name='create_update_node'),
    path('<int:pk>/create-update-node/<int:node_pk>/', views.CreateUpdateNodeView.as_view(), name='create_update_node'),
]

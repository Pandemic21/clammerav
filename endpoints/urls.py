from django.urls import path
#from django.contrib.auth import urls

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]

### assets ###
urlpatterns += [
    path('assets/', views.AssetListView.as_view(), name='assets'),
    path('assets/<uuid:pk>/', views.AssetDetailView.as_view(), name='asset-detail'),
    path('assets/<uuid:pk>/sendrawlog/', views.AssetSendRawLog, name='asset-send-rawlog'),
]

### rawlogs ###
urlpatterns += [
    path('rawlogs/', views.RawLogListView.as_view(), name='rawlogs'),
    path('rawlogs/<int:pk>/', views.RawLogDetailView.as_view(), name='rawlog-detail'),
]

### ingest ###
urlpatterns += [
    path('ingest/', views.IngestListView.as_view(), name='ingest'), # lists all ingest
    path('ingest/create/', views.IngestCreate.as_view(), name='ingest-create'), # creates a new ingest
    path('ingest/<uuid:pk>/', views.IngestDetailView.as_view(), name='ingest-detail'), # detailed view of a specific ingest
    path('ingest/<uuid:pk>/join/', views.IngestJoin, name='ingest-join'), # URL used by asset to join clammer-av
    path('ingest/<uuid:pk>/agent.tar.gz', views.IngestAgent.as_view(), name='ingest-agent'), # URL used to download the agent
    path('ingest/<uuid:pk>/delete/', views.IngestDelete.as_view(), name='ingest-delete'), # deletes a specific ingest
]

'''
urlpatterns += [
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
]
'''

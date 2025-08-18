from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.NewsListView.as_view(), name='list'),
    path('create/', views.NewsCreateView.as_view(), name='create'),
    path('<int:pk>/', views.NewsDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', views.NewsUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.NewsDeleteView.as_view(), name='delete'),
    
    # API endpoints
    path('api/list/', views.NewsAPIListView.as_view(), name='api_list'),
    path('api/create/', views.NewsAPICreateView.as_view(), name='api_create'),
    path('api/<int:pk>/', views.NewsAPIDetailView.as_view(), name='api_detail'),
    path('api/categories/', views.NewsCategoryAPIListView.as_view(), name='api_categories'),
]

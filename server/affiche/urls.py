#server/affiche/urls.py
from django.urls import path
from . import views

app_name = 'affiche'

urlpatterns = [
    path('', views.PerformanceListView.as_view(), name='index'),
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('performance/<int:pk>/', views.PerformanceDetailView.as_view(), name='performance_detail'),
    path('performance/new/', views.PerformanceCreateView.as_view(), name='performance_create'),
    path('performance/<int:pk>/update/', views.PerformanceUpdateView.as_view(), name='performance_update'),
    path('performance/<int:pk>/delete/', views.PerformanceDeleteView.as_view(), name='performance_delete'),
    path('scrape/', views.scrape_performances, name='scrape_performances'),
    path('performance/<int:pk>/comment/', views.CommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
]

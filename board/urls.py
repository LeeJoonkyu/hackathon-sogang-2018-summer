from django.urls import path

from board import views

app_name = 'board'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('detail/<int:id>/', views.post_detail, name='post_detail'),
    path('new',views.post_create,name='post_create'),
    path('update/<int:id>', views.post_update, name='post_update'),
    path('delete/<int:id>', views.post_delete, name='post_delete'),
]

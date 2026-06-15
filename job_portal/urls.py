from django.urls import path
from . import views

urlpatterns = [

    path('', views.auth_page, name='auth'),
    path('auth/', views.auth_page, name='auth'),
    path('logout/', views.logout_page, name='logout'),
    path('index/', views.index, name='index'),
    path('jobs/', views.jobs, name='jobs'),
    path('companies/', views.companies, name='companies'),
    path('premium/', views.premium, name='premium'),
    path('ai/', views.ai_page, name='ai'),
    path('apply-job/<int:id>/', views.apply_job, name='apply_job'),
    path('delete-resume/<int:id>/', views.delete_resume, name='delete_resume'),
]
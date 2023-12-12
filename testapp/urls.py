from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('map', views.MapView.as_view(), name='map'),
    path('list', views.ListView.as_view(), name='list'),
    path('ajax/load-cities/', views.load_subname, name='ajax_load_subnames'),
    path('tiles/<int:z>/<int:x>/<int:y>.pbf', views.get_tile, name='tileserver'),    
    
]

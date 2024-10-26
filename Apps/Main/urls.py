
from django.urls import path
from Apps.Main.views import RopaListView, prenda_detail

app_name = 'Main'
 
urlpatterns = [
    path('', RopaListView.as_view(), name='Main_list'),
    path('details/', prenda_detail.as_view(), name='detail_prenda'),
]



from django.urls import path
from Apps.Main.views import RopaListView, PrendaDetail,ProductList

app_name = 'Main'
 
urlpatterns = [
    path('', RopaListView.as_view(), name='Main_list'),
    path('details/', PrendaDetail.as_view(), name='detail_prenda'),
    path('product/', ProductList.as_view(), name='product_list'),
]


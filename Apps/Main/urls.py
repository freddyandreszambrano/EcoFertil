
from django.urls import path
from Apps.Main.views import RopaListView, PrendaDetail,ProductList,fertilziantelist,productfertilizerlist

app_name = 'Main'
 
urlpatterns = [
    path('', RopaListView.as_view(), name='Main_list'),
    path('details/', PrendaDetail.as_view(), name='detail_prenda'),
    path('product/', ProductList.as_view(), name='product_list'),
    path('fertilizantes/', fertilziantelist.as_view(), name='fertilizer_list'),
    path('productFertilizante/', productfertilizerlist.as_view(), name='product_ferilizante_list'),

]


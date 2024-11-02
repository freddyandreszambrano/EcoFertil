from django.views.generic import ListView
from .models import Producto, Categoria

class RopaListView(ListView):
    template_name = 'Home/main.html'
    context_object_name = 'prendas'

    def get_queryset(self):
        # Puedes definir una lista de datos manualmente
        return [
            {'nombre': 'Camiseta', 'precio': 20, 'color': 'Rojo'},
            {'nombre': 'Pantalones', 'precio': 50, 'color': 'Azul'},
            {'nombre': 'Chaqueta', 'precio': 100, 'color': 'Negro'}
        ]

class PrendaDetail(ListView):
    template_name = 'Item_details/details.html'
    context_object_name = 'prendas'

    def get_queryset(self):
        # Datos de ejemplo para la vista de detalles
        return [
            {'nombre': 'Camiseta', 'precio': 20, 'color': 'Rojo', 'descripcion': 'Una camiseta de algodón'},
            {'nombre': 'Pantalones', 'precio': 50, 'color': 'Azul', 'descripcion': 'Pantalones de mezclilla'},
            {'nombre': 'Chaqueta', 'precio': 100, 'color': 'Negro', 'descripcion': 'Chaqueta de cuero'}
        ]
        
class ProductList(ListView):
    template_name = 'product/Product.html'
    model = Producto
    context_object_name = 'productos' 
    
    def get_queryset(self):
        return Producto.objects.filter(categoria__nombre__iexact='plantas')
    
    def get_context_data(self, **kwargs):
        # Llamar al método de la clase base para obtener el contexto
        context = super().get_context_data(**kwargs)
        
        # Agregar el título dinámico al contexto
        context['titulo'] = 'Plantas'
        context['descripcion'] = 'Descripcion de las plantas'
        return context
    
    


class fertilziantelist(ListView):
    template_name = 'fertilizantes/fertizantes.html'
    model = Categoria
    
class productfertilizerlist(ListView):
    template_name = 'product/Product.html'
    model = Producto
    context_object_name = 'productos'
    
    def get_queryset(self):
        return Producto.objects.filter(categoria__nombre__iexact='fertilizantes')
    
    def get_context_data(self, **kwargs):
        # Llamar al método de la clase base para obtener el contexto
        context = super().get_context_data(**kwargs)
        
        # Agregar el título dinámico al contexto
        context['titulo'] = 'Fertilizantes'
        context['descripcion'] = 'Descripcion de las fertilizantes'
        
        return context
    
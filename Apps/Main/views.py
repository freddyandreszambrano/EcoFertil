from django.views.generic import ListView

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
    context_object_name = 'producto'

    def get_queryset(self):
        # Datos de ejemplo para la vista de detalles
        return [
            {'nombre': 'Camiseta', 'precio': 20, 'color': 'Rojo', 'descripcion': 'Una camiseta de algodón'},
            {'nombre': 'Pantalones', 'precio': 50, 'color': 'Azul', 'descripcion': 'Pantalones de mezclilla'},
            {'nombre': 'Chaqueta', 'precio': 100, 'color': 'Negro', 'descripcion': 'Chaqueta de cuero'}
        ]


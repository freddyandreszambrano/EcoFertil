from django.db import models
from django.db.models import Sum, F




class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100)
    precio = models.FloatField()
    stock = models.IntegerField()
    imagen = models.ImageField(upload_to='productos')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return self.nombre
    

class Carrito(models.Model):
    fecha = models.DateField()
    
    def __str__(self):
        return f"Carrito - {self.fecha}"
    
class CarritoProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} en Carrito {self.carrito.id}"

    
class Pedido(models.Model):
    fecha = models.DateField()
    direccion = models.CharField(max_length=100)   
    total_pedido = models.FloatField(default=0) 
    estado = models.CharField(max_length=100)
    metodoPago = models.CharField(max_length=100)
    
    def calcular_total(self):
        # Sumamos cantidad * precio para cada producto en el pedido
        total = self.pedidoproducto_set.aggregate(
            total=Sum(F('cantidad') * F('precio'))
        )['total'] or 0
        return total

    def save(self, *args, **kwargs):
        # Calculamos el total antes de guardar
        self.total_pedido = self.calcular_total()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"Pedido {self.id} - {self.fecha}"

class PedidoProducto(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio = models.FloatField()
    
    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} en Pedido {self.pedido.id}"

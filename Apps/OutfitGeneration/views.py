import json
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import CreateView, TemplateView
from Apps.Wardrobe.models import Clothes
from Apps.OutfitSaving.models import OutfitSaving 
from Apps.OutfitGeneration.Logic.Combinacion_colores_outfit import Fn_combinacion_colores_outfit
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
import webcolors
import ast
import random
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View


def obtener_nombre_color(rgb_color):
    min_color_diff = float('inf')
    closest_color = None
    for hex_color, color_name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(hex_color)
        color_diff = sum(abs(component1 - component2) for component1, component2 in zip(rgb_color, (r_c, g_c, b_c)))
        if color_diff < min_color_diff:
            min_color_diff = color_diff
            closest_color = color_name
    return closest_color

def procesar_prenda(prenda, lista_categorias):
    if prenda.category in lista_categorias:
        try:
            rgb_color = ast.literal_eval(prenda.dominant_color)
        except (SyntaxError, ValueError) as e:
            return None
        color_name = obtener_nombre_color(rgb_color)
        return {
            'garment': prenda.garment.url,
            'category': prenda.category,
            'dominant_color': color_name,
            'type': prenda.type
        }
    return None

def encontrar_prenda_aleatoria(prendas, lista_categorias):
    prendas_filtradas = [prenda for prenda in prendas if prenda.category in lista_categorias]
    return random.choice(prendas_filtradas) if prendas_filtradas else None

outfits_seleccionados = []

def Fn_seleccionar_prendas():
    global outfits_seleccionados
    outfits_seleccionados = []

    
    prendas = list(Clothes.objects.all())  # Convertir a lista para selección aleatoria
    print(prendas)
    lista_categorias_superior = ['Coat', 'Dress', 'Pullover', 'Shirt', 'T-shirt']
    lista_categorias_inferior = ['Trouser']
    lista_categorias_zapatos = ['Sneaker', 'Sandal', 'Ankle boot']

    selected_outfits = []

    while True:
        prenda_superior = encontrar_prenda_aleatoria(prendas, lista_categorias_superior)
        if not prenda_superior:
            break
        prenda_zapato = encontrar_prenda_aleatoria(prendas, lista_categorias_zapatos)

        prenda_superior_info = procesar_prenda(prenda_superior, lista_categorias_superior)
        zapato_info = procesar_prenda(prenda_zapato, lista_categorias_zapatos)
        prenda_inferior = None

        for prenda in prendas:
            if prenda.category in lista_categorias_inferior:
                prenda_inferior_info = procesar_prenda(prenda, lista_categorias_inferior)
                if prenda_inferior_info and Fn_combinacion_colores_outfit(prenda_superior_info['dominant_color'], prenda_inferior_info['dominant_color']):
                    prenda_inferior = prenda_inferior_info
                    break

        if not prenda_inferior:
            prenda_inferior = procesar_prenda(encontrar_prenda_aleatoria(prendas, lista_categorias_inferior), lista_categorias_inferior)

        outfit_seleccionado = {
            'prenda_superior': prenda_superior_info,
            'prenda_inferior': prenda_inferior,
            'zapato': zapato_info
        }

        # Verificar si el outfit ya ha sido seleccionado previamente
        if outfit_seleccionado in outfits_seleccionados:
            break

        selected_outfits.append(outfit_seleccionado)
        outfits_seleccionados.append(outfit_seleccionado)

    return selected_outfits

class OutfitGenerationView(CreateView):
    model = Clothes
    template_name = 'Outfit_Generation/OutfitGeneration.html'
    context_object_name = 'ctx_clothes'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        outfit_seleccionado = Fn_seleccionar_prendas()
        context['ctx_clothes'] = outfit_seleccionado
        return context


class PreseleccionView(TemplateView):
    template_name = 'PreSeleccion_Outfit/Preseleccion.html'
    
    
    
class SeleccionPrendasOutfitGeneratorView(TemplateView):
    model = Clothes
    template_name = 'Seleccion_Prenda/SeleccionPrenda.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ctx_Prendas_superior'] = Clothes.objects.filter(category__in=['Coat', 'Dress', 'Pullover', 'Shirt', 'T-shirt'])
        context['ctx_Prendas_inferior'] = Clothes.objects.filter(category__in=['Trouser'])
        context['ctx_zapato'] = Clothes.objects.filter(category__in=['Sneaker', 'Sandal', 'Ankle boot'])
        return context




class Eleccion_filtrosView(TemplateView):
    template_name = 'PresentarFiltros/Prensentar_filtros.html'




class ProcessSelectionView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        request.session['selected_items'] = data
        return JsonResponse({'status': 'success'})

    def get(self, request, *args, **kwargs):
        return JsonResponse({'status': 'fail'})

class ShowSelectionView(TemplateView):
    template_name = 'outfit_preseleccionado/outfit_preseleccionado.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_items = self.request.session.get('selected_items', {})
        
        categories = ['superior', 'inferior', 'zapatos']
        for category in categories:
            if category not in selected_items:
                # Si falta una categoría, obtener una prenda aleatoria de esa categoría
                print("No se ha seleccionado una prenda de la categoría " + category)
                random_item = self.get_random_item_by_category(category)
                selected_items[category] = random_item

        # Agregar las selecciones al contexto
        context['selected_items'] = selected_items
        return context

    def get_random_item_by_category(self, category):
        # Obtener una prenda aleatoria de la categoría especificada del modelo Clothes
        # Aquí asumimos que el modelo Clothes tiene un campo 'category' que representa la categoría de la prenda
        random_item = Clothes.objects.filter(category=category).order_by('?').first()
        
        # Aquí podrías agregar más lógica según la estructura de tu modelo Clothes
        # por ejemplo, seleccionar la prenda según alguna otra condición
        
        # Retornar la prenda aleatoria encontrada (o None si no se encontró ninguna)
        return random_item
    


class GuardarOutfitView(View):
    def post(self, request, *args, **kwargs):

        # Obtener los IDs de las prendas
        top_clothes_id = request.POST.get('top_clothes_id')
        bottom_clothes_id = request.POST.get('bottom_clothes_id')
        shoe_clothes_id = request.POST.get('shoe_clothes_id')

        # Imprimir los IDs para verificar
        print('ID de la prenda superior:', top_clothes_id)
        print('ID de la prenda inferior:', bottom_clothes_id)
        print('ID de la prenda de calzado:', shoe_clothes_id)

        return JsonResponse({'message': 'Outfit guardado correctamente'})

    def get(self, request, *args, **kwargs):
        return JsonResponse({'error': 'Método no permitido'}, status=405)




from django.views.generic import ListView, DetailView
from Apps.Wardrobe.models import Clothes

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from Apps.Wardrobe.models import Clothes

class RopaListView(ListView):
    model = Clothes
    template_name = 'Home/main.html'
    context_object_name = 'prendas'


class prenda_detail(ListView):
    model = Clothes
    template_name = 'Item_details/details.html'




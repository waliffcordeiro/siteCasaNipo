from django.shortcuts import render
from .models import Geladeira
# Create your views here.

def core(request):
    template_name = 'core.html'
    context = {
        'Geladeira': Geladeira.objects.all().get()
    }
    return render(request, template_name, context)
from django.http import HttpResponse
from django.shortcuts import render 
import datetime
import logging
from van2enjoy_app.models import Sitios

#log = '/home/raul/desarrollos_python/virtualenv_con_python3/Proyectos/van2enjoy/van2enjoy1.log'
#logging.basicConfig(filename=log,level=logging.DEBUG)

#def prueba(request):
#    
#    ahora = datetime.datetime.now() 
#    html = []
    #for clave,valor in request.META.items():
    #    html.append('<tr><td>%s</td><td>%s</td></tr>' % (clave, valor))
    
    #html = "<html><body><h1>Fecha:</h1><h3>%s<h/3></body></html>" % ahora 
    #return HttpResponse('<table>%s</table>' %'\n'.join(html))
#    if request.META['REQUEST_METHOD'] ==  'GET':
#        logging.debug("GET")
#        items = request.GET.items()
#        logging.debug(request.GET.keys())
#    elif request.META['REQUEST_METHOD'] ==  'POST':
#        logging.debug("GET")
#        items = request.POST.items()
#    
#    for clave,valor in items:
#        html.append('<tr><td>%s</td><td>%s</td></tr>' % (clave, valor))
#    
#    logging.debug(html)
#    return HttpResponse('<table>%s</table>' %'\n'.join(html))

#def formulario_buscar(request): 
#    return render(request, 'formulario_buscar.html') 

#def buscar(request):
#    logging.debug(request.GET)
#    if 'consulta' in request.GET and request.GET['consulta']: 
#        consulta = request.GET['consulta'] 
#        sitios = Sitios.objects.filter(descripcion__icontains=consulta) 
#        return render(request, 'resultados.html',  {'sitios': sitios, 'query': consulta}) 
#    else: 
#        return HttpResponse('Por favor introduce un termino de búsqueda.') 
    
    

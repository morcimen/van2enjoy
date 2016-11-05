
from tastypie.authorization import Authorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.resources import ModelResource
from django.contrib.auth.models import User
#from van2enjoy_app.models import Usuarios
from van2enjoy_app.models import Sitios
from van2enjoy_app.models import Tipos
from van2enjoy_app.models import Provincias
from van2enjoy_app.models import Favoritos
from van2enjoy_app.models import Fotos
from tastypie_extras.resource import MultipartResourceMixin
from django.conf.urls import url
from django.http import HttpResponse
import logging

log = '/home/raul/desarrollos_python/virtualenv_con_python3/Proyectos/van2enjoy/van2enjoy.log'
logging.basicConfig(filename=log,level=logging.DEBUG)
logging.debug("estos es una prueba")

class TiposResource(ModelResource):
    class Meta:
        queryset = Tipos.objects.all()
        resource_name = 'tipos'
        filtering = {
            'tipo': ALL,
        }
        allowed_methods = ['get']

class UsuariosResource(ModelResource):
    class Meta: 
        queryset = User.objects.all()
        resource_name = 'usuarios'
        filtering = {
            'username': ALL,
            'First name' : ALL,
            'Email address' : ALL,
            'id' : ALL,
        }
        allowed_methods = ['get']
 
class ProvinciasResource(ModelResource):
    class Meta: 
        queryset = Provincias.objects.all()
        resource_name = 'provincias'
        filtering = {
            'provincia': ALL,
        }
        allowed_methods = ['get']
        
        
class SitiosResource(ModelResource):
    usuario = fields.ForeignKey(UsuariosResource,'usuario')
    tipo = fields.ForeignKey(TiposResource, 'tipo',full=True)
    provincia = fields.ForeignKey(ProvinciasResource, 'provincia',full=True)
    resource_name = 'sitios'
    
    class Meta:
        queryset = Sitios.objects.all().select_related("usuario","provincia","tipo")
        authorization = Authorization()
        filtering = {
            "id" : ALL,
            "descripcion" : ALL,
            "usuario" : ALL_WITH_RELATIONS,
            "tipo" : ALL_WITH_RELATIONS,
            "provincia" : ALL_WITH_RELATIONS,
            "fecha_creacion" : ALL,
        }
        ordering = ["fecha_creacion",]


class FavoritosResource(ModelResource):
   sitio = fields.ForeignKey(SitiosResource,'sitio')
   usuario = fields.ForeignKey(UsuariosResource,'usuario')
   resource_name = 'favoritos'
   
   class Meta:
        queryset = Favoritos.objects.all() 
        authorization = Authorization()
        filtering = {
            "sitio" : ALL_WITH_RELATIONS,
            "usuario" : ALL_WITH_RELATIONS,
        }

# MultipartResourceMixin suple la carencia de Tastypie de hacer POST con
# un Content-Type: multipart/form-data (necesario en la subidad de ficheros)
class FotosResource(MultipartResourceMixin, ModelResource):
    logging.debug("Entramos aqui")
    sitio = fields.ForeignKey(SitiosResource,'sitio')
    imagen = fields.FileField(attribute="imagen", null=True, blank=True)
    resource_name = 'fotos'

    class Meta:
        queryset = Fotos.objects.all() 
        authorization = Authorization()
        filtering = {
            "sitio" : ALL_WITH_RELATIONS,
        }
    
    def prepend_urls(self):
        logging.debug("Entramos en prepend_urls")
        return [
            #url to download image file.
            url(r"^(?P<resource_name>%s)/(?P<pk>\w+)/imagen/$"% self._meta.resource_name,
                self.wrap_view('get_image'), name="api_get_image"),
        ]
 
    # Vista que permite descargar las imagenes
    def get_image(self, request, **kwargs):
        obj = Fotos.objects.get(id=kwargs['pk'])
        image_file = obj.imagen
        return HttpResponse(image_file.read(), content_type="image/jpeg")



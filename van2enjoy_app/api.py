
from tastypie.authorization import Authorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.resources import ModelResource
from django.contrib.auth.models import User
from van2enjoy_app.models import Sitios
from van2enjoy_app.models import Tipos
from van2enjoy_app.models import Provincias
from van2enjoy_app.models import Favoritos
from van2enjoy_app.models import Fotos
from van2enjoy_app.models import Imeis
from tastypie_extras.resource import MultipartResourceMixin
from django.conf.urls import url
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from tastypie.http import HttpUnauthorized, HttpForbidden
from django.conf.urls import url
from tastypie.utils import trailing_slash
from django.db.models import signals
from tastypie.models import ApiKey
import logging

logger = logging.getLogger(__name__)

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


class LoginResource(ModelResource):
    resource_name = 'login'
    
    class Meta:
        queryset = User.objects.all()
        fields = ['username']
        allowed_methods = ['get','post']
        
    def prepend_urls(self):
        return [
               url(r"^(?P<resource_name>%s)/$" %self._meta.resource_name,   
               self.wrap_view('login'), name="api_login"),
               ]
    
    def login(self, request, **kwargs):
        """
        Valida usuario, contraseña e imei y si todo es correcto genera una
        nueva ApiKey para el mismo, delvolviéndola en la respuesta.
        
        Params:
            - Request
        
        Return:
            - Respuesta HTTP
        """
           
        self.method_check(request, allowed=['post'])
        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))
        username = data.get('username', '')
        password = data.get('password', '')
        imei = data.get('imei', '')
        logger.debug("Iniciando autenticación para el usuario: '%s' con imei: '%s'"
            %(username,imei))
        if not username or not password or not imei:
            logger.debug("Falta usuario, password y/o imei")
            return self.create_response(request, {
                'success': False,
                'reason': 'Falta usuario, password y/o imei',
                }, HttpUnauthorized )
        user = authenticate(username=username, password=password) 
        if user:
            if user.is_active:
                if not self.check_imei(user.username, imei):
                    texto = "El imei no es válido para el usuario"
                    return self.create_response(request, {
                        'success': False,
                        'reason': texto,
                        }, HttpUnauthorized )
                api_key = self.genera_ApiKey(user)
                logger.debug("Autenticación correcta. ApyKey creada: %s" %api_key)
                return self.create_response(request, {
                    'success': True,
                    'apikey' : api_key
                })
            else:
                logger.debug("Autenticación correcta, pero el suario no está activo")
                return self.create_response(request, {
                    'success': False,
                    'reason': 'disabled',
                    }, HttpForbidden )
        else:
            logger.debug("Usuario y/o password incorrectos")
            return self.create_response(request, {
                'success': False,
                'reason': 'incorrect',
                }, HttpUnauthorized )

    def genera_ApiKey(self, usuario):
        """
        Genera una nueva ApiKey para usuario
        
        Params:
            - Una entidad Usuario
        
        Devuelve:
            - ApiKey creada
        """
        api_key = ApiKey.objects.get_or_create(user=usuario)
        api_key[0].key = api_key[0].generate_key()
        api_key[0].save()
        
        logger.debug("Devolviendo ApiKey")
        return api_key[0].key
    
    def check_imei(self,usuario,imei_request):
        """
        Comprueba si el imei es correcto para el usuario
        
        Params:
            - Usuario (cadena de texto)
            - imei 
        
        Return:
            - True, si el imei es válido para el usuario
            - False, si el imei no es válido para el usuario
        """
        imei = Imeis.objects.get(usuario__username=usuario)
        if imei.imei == imei_request:
            logger.debug(imei.imei)
            logger.debug(imei_request)
            return True
        else:
            return False
            
        

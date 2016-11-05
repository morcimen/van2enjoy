from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin
from van2enjoy_app.models import Tipos, Provincias
from van2enjoy_app.models import Sitios, Favoritos, Fotos
from django.contrib.auth.models import User
import json

class TiposResourceTest(ResourceTestCaseMixin, TestCase):
    
    #def setUp(self):
        #super(TiposResourceTest, self).setUp()

    def genera_uri(self,variable):
        return "/api/v1/%s/1/" %variable
    
    def crea_estructura_de_datos_basica(self):
        """
        Crear una estructura básica de datos para poder realizar los tests
        Crea una provincia, un usuario, un tipo. A continuación, crea un 
        un sitio asociado a estos, lo marca como favorito y le añade una foto 
        
        Params:
            - Ninguno
        
        Return:
            - Nada
        """
        Tipos.objects.create(tipo = "tipo1")
        User.objects.create(username = "usuario1", email = "usuario1@loquesea.com")
        Provincias.objects.create(provincia = "provincia1")
        
        uris = self.consulta_uris()
        
        # Se añade un sitio
        resp = self.crea_sitio(uris['provincia'],uris['tipo'],uris['usuario'])
        self.assertHttpCreated(resp)
        sitio = Sitios.objects.get(descripcion="Prueba api_client")
        uri_sitio = "/api/v1/sitios/%d/" %sitio.pk
        
        # Se añade un favorito al sitio
        resp = self.crea_favorito(uri_sitio,uris['usuario'])
        self.assertHttpCreated(resp)
   
        # Se añade una foto al sitio
        resp = self.crea_foto(uri_sitio)
        self.assertHttpCreated(resp)
         
    
    def crea_sitio(self,uri_provincia,uri_tipo,uri_usuario):
        self.post_data = {
            "aguapotable": "False",
            "servicios": "False",
            "descripcion": "Prueba api_client",
            "latitud": "123456",
            "longitud": "7891011",
            "provincia": uri_provincia,
            "restauracion": "False",
            "tipo": uri_tipo,
            "usuario": uri_usuario
            }
        resp = self.api_client.post('/api/v1/sitios/', format='json', data=self.post_data)
        return resp
    
    def crea_favorito(self,uri_sitio,uri_usuario):
        self.post_data = {
            "sitio" : uri_sitio,
            "usuario" : uri_usuario
            }
        resp = self.api_client.post('/api/v1/favoritos/', format='json', data=self.post_data)
        return resp
    
    def crea_foto(self,uri_sitio):
        self.post_data = {
            "sitio" : uri_sitio
            }
        resp = self.api_client.post('/api/v1/fotos/', format='json', data=self.post_data)
        return resp
    
    def consulta_uris(self):
        """
        Consulta el valor de las uris del único registro de cada una de las
        tablas: Tipo, Usuario, Provincia
        
        Param:
            - Ninguno
            
        Return:
            - Un diccionario con las uris para cada uno de ellos
        """
        
        uris = {}
        tipo = Tipos.objects.get(tipo = "tipo1")
        usuario = User.objects.get(username = "usuario1")
        provincia = Provincias.objects.get(provincia = "provincia1")
        uris['tipo'] = "/api/v1/tipos/%d/" %tipo.pk
        uris['usuario'] = "/api/v1/usuarios/%d/" %usuario.pk
        uris['provincia'] = "/api/v1/provincias/%d/" %provincia.pk
        
        return uris
    
    def test_consulta_info_cuenta(self):
        self.crea_estructura_de_datos_basica()
        resp = self.api_client.get('/api/v1/usuarios/?usuario=usuario1',format='json')
        self.assertHttpOK(resp)
        self.assertEqual(len(self.deserialize(resp)['objects']),1)
    
    def test_consulta_tus_favoritos(self):
        self.crea_estructura_de_datos_basica()
        resp = self.api_client.get('/api/v1/favoritos/?usuario__username=usuario1',format='json')
        self.assertHttpOK(resp)
        self.assertEqual(len(self.deserialize(resp)['objects']),1)
    
    def test_consulta_tus_sitios(self):
        self.crea_estructura_de_datos_basica()
        resp = self.api_client.get('/api/v1/sitios/?usuario__username=usuario1',format='json')
        self.assertHttpOK(resp)
        self.assertEqual(len(self.deserialize(resp)['objects']),1)
    
    def test_consulta_ultimos_20(self):
        self.crea_estructura_de_datos_basica()
        uris = self.consulta_uris()
        
        for i in range(40):
            self.crea_sitio(uris['provincia'],uris['tipo'],uris['usuario'])
        
        resp = self.api_client.get('/api/v1/sitios/?order_by=-fecha_creacion',format='json')
        self.assertHttpOK(resp)
        self.assertEqual(len(self.deserialize(resp)['objects']),20)
    
    def test_consulta_sitio_por_id(self):
        self.crea_estructura_de_datos_basica()
        sitio = Sitios.objects.get(descripcion="Prueba api_client")
        resp = self.api_client.get('/api/v1/sitios/%s/'%sitio.pk,format='json')
        self.assertHttpOK(resp)
    
    def test_desmarca_favorito(self):
        self.crea_estructura_de_datos_basica()
        favorito = Favoritos.objects.get(sitio__descripcion="Prueba api_client")
        resp = self.api_client.delete('/api/v1/favoritos/%s/'%favorito.pk, format='json')
        self.assertHttpAccepted(resp)
    
    def test_consulta_foto_por_id_sitio(self):
        self.crea_estructura_de_datos_basica()
        
    
    def test_elimina_sitio(self):
        self.crea_estructura_de_datos_basica()
        sitio = Sitios.objects.get(descripcion="Prueba api_client")
        resp = self.api_client.delete('/api/v1/sitios/%s/'%sitio.pk, format='json')
        self.assertHttpAccepted(resp)
    
    def test_elimina_foto(self):
        self.crea_estructura_de_datos_basica()
        foto = Fotos.objects.get(sitio__descripcion="Prueba api_client")
        resp = self.api_client.delete('/api/v1/fotos/%s/'%foto.pk, format='json')
        self.assertHttpAccepted(resp)
    
    #def test_elimina_favorito_fotos_sitio(self):
    #    self.crea_estructura_de_datos_basica()
    #    uris = self.consulta_uris()
    #    for recurso in ["favoritos", "fotos", "sitios"]:
    #        resp = self.api_client.delete(uris[recurso[:-1]], format='json')
    #        self.assertHttpAccepted(resp)
    

 

import os
from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin


for p in dir(ResourceTestCaseMixin):
    print(p)

class ResourceTest(TestCase):

    def crea_usuario(self):
        self.post_data = {
            "aguapotable": "False",
            "baños": "False",
            "descripcion": "Prueba api_client",
            "latitud": "123456",
            "longitud": "7891011",
            "provincia": "/api/v1/provincias/70/",
            "restauracion": "False",
            "tipo": "/api/v1/tipos/1/",
            "usuario": "/api/v1/usuarios/12/"
            }

        self.api_client.post('/api/v1/sitios/', format='json', data=self.post_data)

if __name__ == "__main__":

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "van2enjoy.settings")   
    prueba = ResourceTest()
    prueba.crea_usuario()

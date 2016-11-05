from django.db import models
from django_resized import ResizedImageField
from django.contrib.auth.models import User

# Create your models here.

#class Usuarios(models.Model):
#    usuario = models.CharField(max_length=30)
#    nombre = models.CharField(max_length=30)
#    mail = models.EmailField()
#    imei = models.CharField(max_length=15)
#
#    def __str__(self):  
#        return self.usuario 
#
#    class Meta: 
#        verbose_name_plural = "Usuarios" 

class Tipos(models.Model):
    tipo = models.CharField(max_length=30)

    def __str__(self):               
        return self.tipo

    class Meta:
        verbose_name_plural = "Tipos" 

class Provincias(models.Model):
    provincia = models.CharField(max_length=30, unique = True)

    def __str__(self):
        return self.provincia

    class Meta:
        verbose_name_plural = "Provincias"
        ordering = ['provincia']

class Sitios(models.Model):
    descripcion = models.TextField(max_length=4096)
    usuario = models.ForeignKey(User)
    tipo = models.ForeignKey(Tipos)
    provincia = models.ForeignKey(Provincias)
    latitud = models.CharField(max_length=30)
    longitud = models.CharField(max_length=30)
    aguapotable = models.BooleanField()
    servicios = models.BooleanField()
    restauracion = models.BooleanField()
    fecha_creacion = models.DateTimeField(auto_now_add = True, blank = False)
    fecha_modificacion = models.DateTimeField(auto_now = True, blank = False)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name_plural = "Sitios" 
    
class Favoritos(models.Model):
    usuario = models.ForeignKey(User)
    sitio = models.ForeignKey(Sitios)
    
    def __str__(self):
        return "%s" %self.sitio
    
    class Meta:
        verbose_name_plural = "Favoritos"
        
class Fotos(models.Model):
    sitio = models.ForeignKey(Sitios)
    #imagen = models.ImageField(upload_to='sitios')
    imagen = ResizedImageField(upload_to='sitios')
    
    def __str__(self):
        return "%s %s" %(self.sitio, self.imagen)
    
    class Meta:
        verbose_name_plural = "Fotos"
     

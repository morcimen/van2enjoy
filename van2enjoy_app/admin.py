from django.contrib import admin

# Register your models here.

from django.contrib import admin 
from van2enjoy_app.models import Usuarios, Tipos, Sitios, Provincias, Favoritos, Fotos

class SitiosAdmin(admin.ModelAdmin):
    list_display = ('descripcion','provincia','usuario','tipo','fecha_creacion','fecha_modificacion',)
    search_fields = ('descripcion',)
    list_filter = ('usuario','tipo','fecha_creacion','fecha_modificacion')
    fields = ('descripcion','provincia','tipo','usuario','aguapotable','baños','restauracion')
 
class FavoritosAdmin(admin.ModelAdmin):
    list_display = ('sitio','usuario',)
    
admin.site.register(Usuarios) 
admin.site.register(Tipos) 
admin.site.register(Sitios,SitiosAdmin) 
admin.site.register(Provincias)
admin.site.register(Favoritos,FavoritosAdmin)
admin.site.register(Fotos)

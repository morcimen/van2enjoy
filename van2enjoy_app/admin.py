from django.contrib import admin

# Register your models here.

from django.contrib import admin 
from van2enjoy_app.models import Tipos, Sitios, Provincias, Favoritos, Fotos, Imeis

class SitiosAdmin(admin.ModelAdmin):
    list_display = ('descripcion','provincia','usuario','tipo','fecha_creacion','fecha_modificacion',)
    search_fields = ('descripcion',)
    list_filter = ('usuario','tipo','fecha_creacion','fecha_modificacion')
    fields = ('descripcion','provincia','tipo','usuario','aguapotable','servicios','restauracion','latitud','longitud')
 
class FavoritosAdmin(admin.ModelAdmin):
    list_display = ('sitio','usuario',)

class ImeisAdmin(admin.ModelAdmin):
    list_display = ('usuario','imei',)

admin.site.register(Tipos) 
admin.site.register(Sitios, SitiosAdmin) 
admin.site.register(Provincias)
admin.site.register(Favoritos, FavoritosAdmin)
admin.site.register(Fotos)
admin.site.register(Imeis, ImeisAdmin)

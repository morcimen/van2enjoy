"""van2enjoy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from van2enjoy_app.api import SitiosResource
from van2enjoy_app.api import UsuariosResource
from van2enjoy_app.api import TiposResource
from van2enjoy_app.api import ProvinciasResource
from van2enjoy_app.api import FavoritosResource
from van2enjoy_app.api import FotosResource

from tastypie.api import Api

v1_api = Api(api_name='v1')
v1_api.register(SitiosResource())
v1_api.register(UsuariosResource())
v1_api.register(TiposResource())
v1_api.register(ProvinciasResource())
v1_api.register(FavoritosResource())
v1_api.register(FotosResource())

entry_resource = UsuariosResource()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(v1_api.urls)),
]

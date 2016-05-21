from django.conf.urls import url, include

from . import views


urlpatterns = [
    url(r'^$', views.login),
    url(r'^admin/$', views.admin),
    url(r'^admin/adicionarcliente/$', views.addcliente),
    url(r'^admin/listarcliente/$', views.listCliente),
    url(r'^sair/$', views.sair)
]
from django.urls import path
from .views import Index, Sobre, Contato
from .views import *

urlpatterns = [
    #path("admin/", admin.site.urls),

    path("inicio", Index.as_view(), name="pagina_inicial"),
    path("sobre", Sobre.as_view(), name="sobre"),
    path("contato", Contato.as_view(), name="contato"),


    #urls 
    path("Casdatrar/tema", TemaCreate.as_view(), name="tema_creator"),
    path("listar/tema/<int:pk>/", TemaList.as_view(), name="tema_listar"),
    path("editar/tema/<int:pk>/", TemaUpdate.as_view(), name="tema_update"),
    path("delete/tema/<int:pk>/", TemaDelete.as_view(), name="tema_delete"),
    path("detail/tema/<int:pk>/", TemaDetail.as_view(), name="tema_detail"),



    path("Cadastrar/subtema", SubtemaCreate.as_view(), name="subtema_creator"),
    path("listar/subtema/", SubtemaList.as_view(), name="subtema_listar"),
    path("editar/subtema/<int:pk>/", SubtemaUpdate.as_view(), name="subtema_update"),
    path("delete/subtema/<int:pk>/", SubtemaDelete.as_view(), name="subtema_delete"),
    path("detail/subtema/<int:pk>/", SubtemaDetail.as_view(), name="subtema_detail"),



    path("Cadastrar/video", VideoCreate.as_view(), name="video_creator"),
    path("listar/video/", VideoList.as_view(), name="video_listar"),
    path("editar/video/<int:pk>/", VideoUpdate.as_view(), name="video_update"),
    path("delete/video/<int:pk>/", VideoDelete.as_view(), name="video_delete"),
    path("detail/video/<int:pk>/", VideoDetail.as_view(), name="video_detail"),



    path("Cadastrar/comentario", ComentarioCreate.as_view(), name="comentario_creator"),


    path("Cadastrar/avaliacao", AvaliacaoCreate.as_view(), name="avaliacao_creator"),


    path("Cadastrar/like", LikeCreate.as_view(), name="like_creator"),
]
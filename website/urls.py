from django.urls import path
from .views import Index, Sobre, Contato
from .views import *

urlpatterns = [
    #path("admin/", admin.site.urls),

    path("inicio", Index.as_view(), name="menu"),
    path("sobre", Sobre.as_view(), name="sobre"),
    path("contato", Contato.as_view(), name="contato"),
    path("menuCadastro", MenuCadastro.as_view(), name="menuCadastro"),
    path("CadastroAluno", CadastroAluno.as_view(), name="CadastroAluno"),
    path("CadastroProfessor", CadastroProfessor.as_view(), name="CadastroProfessor"),
    path("menuLogin", MenuLogin.as_view(), name="menuLogin"),
    path("LoginAluno", LoginAluno.as_view(), name="LoginAluno"),
    path("LoginProfessor", LoginProfessor.as_view(), name="LoginProfessor"),
    path("Tela", Tela.as_view(), name="Tela"),

    


    #urls 
    path("cadastrar/tema", TemaCreate.as_view(), name="tema_creator"),
    path("listar/tema/", TemaList.as_view(), name="tema_listar"),
    path("editar/tema/<int:pk>/", TemaUpdate.as_view(), name="tema_update"),
    path("delete/tema/<int:pk>/", TemaDelete.as_view(), name="tema_delete"),
    path("detail/tema/<int:pk>/", TemaDetail.as_view(), name="tema_detail"),



    path("cadastrar/subtema", SubtemaCreate.as_view(), name="subtema_creator"),
    path("listar/subtema/", SubtemaList.as_view(), name="subtema_listar"),
    path("editar/subtema/<int:pk>/", SubtemaUpdate.as_view(), name="subtema_update"),
    path("delete/subtema/<int:pk>/", SubtemaDelete.as_view(), name="subtema_delete"),
    path("detail/subtema/<int:pk>/", SubtemaDetail.as_view(), name="subtema_detail"),



    path("cadastrar/video", VideoCreate.as_view(), name="video_creator"),
    path("listar/video/", VideoList.as_view(), name="video_listar"),
    path("editar/video/<int:pk>/", VideoUpdate.as_view(), name="video_update"),
    path("delete/video/<int:pk>/", VideoDelete.as_view(), name="video_delete"),
    path("detail/video/<int:pk>/", VideoDetail.as_view(), name="video_detail"),



    path("cadastrar/comentario", ComentarioCreate.as_view(), name="comentario_creator"),


    path("cadastrar/avaliacao", AvaliacaoCreate.as_view(), name="avaliacao_creator"),


    path("cadastrar/like", LikeCreate.as_view(), name="like_creator"),
]
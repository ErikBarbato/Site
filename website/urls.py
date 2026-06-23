from django.urls import path
# Views implementadas para o projeto
from .views import *
# Views importadas do DJango para login, logut e alterar senha
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView
)

urlpatterns = [
    
    # URLs para o usuário fazer login
    path("login/", LoginView.as_view(
        template_name = "website/form.html",
        extra_context = {
            "titulo": "Autenticação",
            "botao": "Entrar"
        }
    ), name="login"),
    # URL para o usuário fazer logout
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    # URL para o usuário alterar a senha
    path("password_change/", PasswordChangeView.as_view(
        template_name = "website/form.html",
        extra_context = {
            "titulo": "Alterar minha senha",
            "botao": "Alterar"
        }
    ), name="alterar_senha"),

    path("", Index.as_view(), name="menu"),
    path("sobre/", Sobre.as_view(), name="sobre"),
    path("criadores/", Criadores.as_view(), name="criadores"),
    path("Config_user/", Config_user.as_view(), name="Config_user"),
    path("Config_noti/", Config_noti.as_view(), name="Config_noti"),
    path("Config_priva/", Config_priva.as_view(), name="Config_priva"),
    path("contato/", Contato.as_view(), name="contato"),
    path("video/", Video.as_view(), name="video"),
    path("menuCadastro/", MenuCadastro.as_view(), name="menuCadastro"),
    path("CadastroAluno/", CadastroAluno.as_view(), name="CadastroAluno"),
    path("CadastroProfessor/", CadastroProfessor.as_view(), name="CadastroProfessor"),
    path("menuLogin/", MenuLogin.as_view(), name="menuLogin"),
    path("LoginAluno/", LoginView.as_view(
        template_name="website/LoginAluno.html",
        authentication_form=AuthenticationForm,
        extra_context={"titulo": "Login Aluno", "botao": "Entrar"}
    ), name="LoginAluno"),
    path("LoginProfessor/", LoginView.as_view(
        template_name="website/LoginProfessor.html",
        authentication_form=AuthenticationForm,
        extra_context={"titulo": "Login Professor", "botao": "Entrar"}
    ), name="LoginProfessor"),
    path("Tela/", Tela.as_view(), name="Tela"),

    # URLs para o models de Tema
    path("cadastrar/tema/", TemaCreate.as_view(), name="tema_creator"),
    path("listar/tema/", TemaList.as_view(), name="tema_listar"),
    path("editar/tema/<int:pk>/", TemaUpdate.as_view(), name="tema_update"),
    path("delete/tema/<int:pk>/", TemaDelete.as_view(), name="tema_delete"),
    path("detail/tema/<int:pk>/", TemaDetail.as_view(), name="tema_detail"),

    # URLs para o models de Subtema
    path("cadastrar/subtema/", SubtemaCreate.as_view(), name="subtema_creator"),
    path("listar/subtema/", SubtemaList.as_view(), name="subtema_listar"),
    path("editar/subtema/<int:pk>/", SubtemaUpdate.as_view(), name="subtema_update"),
    path("delete/subtema/<int:pk>/", SubtemaDelete.as_view(), name="subtema_delete"),
    path("detail/subtema/<int:pk>/", SubtemaDetail.as_view(), name="subtema_detail"),

    # URls para o models de Video
    path("cadastrar/video/", VideoCreate.as_view(), name="video_creator"),
    path("listar/video/", VideoList.as_view(), name="video_listar"),
    path("editar/video/<int:pk>/", VideoUpdate.as_view(), name="video_update"),
    path("delete/video/<int:pk>/", VideoDelete.as_view(), name="video_delete"),
    path("detail/video/<int:pk>/", VideoDetail.as_view(), name="video_detail"),



    path("cadastrar/comentario/", ComentarioCreate.as_view(), name="comentario_creator"),


    path("cadastrar/avaliacao/", AvaliacaoCreate.as_view(), name="avaliacao_creator"),


    path("cadastrar/like/", LikeCreate.as_view(), name="like_creator"),
]
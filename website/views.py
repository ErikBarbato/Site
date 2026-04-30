from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from django.urls import reverse_lazy

from .models import Tema, Subtema, Video, Comentario, Avaliacao, Like

class Index(TemplateView):
    template_name = "website/menu.html"

class Sobre(TemplateView):
    template_name = "website/sobre.html"

class Contato(TemplateView):
    template_name = "website/contato.html"

class MenuCadastro(TemplateView):
    template_name = "website/menuCadastro.html"

class CadastroAluno(TemplateView):
    template_name = "website/CadastroAluno.html"

class CadastroProfessor(TemplateView):
    template_name = "website/CadastroProfessor.html"



class MenuLogin(TemplateView):
    template_name = "website/menuLogin.html"

class LoginAluno(TemplateView):
    template_name = "website/LoginAluno.html"

class LoginProfessor(TemplateView):
    template_name = "website/LoginProfessor.html"



class Tela(TemplateView):
    template_name = "website/modelo.html"






class TemaCreate(CreateView): 
    model = Tema
    fields = ["nome", "cadastrado_por"]
    template_name = "website/form.html"
    success_url = reverse_lazy("Tela")
    extra_context = {
        "titulo": "Cadastro de Tema",
        "botao": "Cadastrar"
    }

class TemaUpdate(UpdateView): 
    model = Tema
    fields = ["nome"]
    template_name = "website/form.html"
    success_url = reverse_lazy("Tela")
    extra_context = {
        "titulo": "Atualizar Tema",
        "botao": "Atualizar"
    }

class TemaDelete(DeleteView):
    model= Tema
    template_name = "website/form.html"
    success_url = reverse_lazy("Tela")
    extra_context = {
        "titulo": "Cadastro de Tema",
        "botao": "Excluir"
    }

class TemaList(ListView):
    model= Tema
    template_name = "website/lista/Tema.html"

class TemaDetail(DetailView):
    model = Tema
    template_name= "website/ver/Tema.html"







class SubtemaCreate(CreateView):
    model = Subtema
    fields = ["nome", "tema", "cadastrado_por"]
    template_name = "website/form.html"
    success_url = reverse_lazy("Tela")
    extra_context = {
        "titulo": "Cadastro de Subtemas",
        "botao": "Cadastrar"
    }

    # def form_valid(self, form):
    #     form.instance.cadastrado_por = self.request.user
    #     return super().form_valid(form)


class SubtemaUpdate(UpdateView):
    model = Subtema
    fields = ["nome", "tema"]
    template_name = "website/form.html"
    success_url = reverse_lazy("Tela")
    extra_context = {
        "titulo": "Atualizar Subtema",
        "botao": "Atualizar"
    }


class SubtemaDelete(DeleteView):
    model = Subtema
    template_name = "website/form.html"
    success_url = reverse_lazy("Tela")
    extra_context = {
        "titulo": "Deletar Subtema",
        "botao": "Excluir"
    }


class SubtemaList(ListView):
    model = Subtema
    template_name = "website/lista/subtema.html"


class SubtemaDetail(DetailView):
    model = Subtema
    template_name = "website/ver/subtema.html"







class VideoCreate(CreateView):
    model = Video
    fields = ["titulo", "descricao", "link", "subtema", "ativo", "cadastrado_por"]
    template_name = "website/form.html"
    success_url = reverse_lazy("Tela")
    extra_context = {
        "titulo": "Cadastro de Video",
        "botao": "Cadastrar"
    }

    # def form_valid(self, form):
    #     form.instance.cadastrado_por = self.request.user
    #     return super().form_valid(form)


class VideoUpdate(UpdateView):
    model = Video
    fields = ["titulo", "descricao", "link", "subtema", "ativo"]
    template_name = "website/form.html"
    success_url = reverse_lazy("Tela")
    extra_context = {
        "titulo": "Atualizar Video",
        "botao": "Atualizar"
    }


class VideoDelete(DeleteView):
    model = Video
    template_name = "website/form.html"
    success_url = reverse_lazy("Tela")
    extra_context = {
        "titulo": "Deletar de Video",
        "botao": "Excluir"
    }


class VideoList(ListView):
    model = Video
    template_name = "website/lista/video.html"

    def get_queryset(self):
        return Video.objects.filter(ativo=True)


class VideoDetail(DetailView):
    model = Video
    template_name = "website/ver/video.html"



class ComentarioCreate(CreateView):
    model = Comentario
    fields = ["texto", "video"]
    template_name = "website/form.html"
    extra_context = {
        "titulo": "Cadastro de Comentario",
        "botao": "Cadastrar"
    }

    def form_valid(self, form):
        form.instance.cadastrado_por = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("video_detail", kwargs={"pk": self.object.video.pk})
    





class AvaliacaoCreate(CreateView):
    model = Avaliacao
    fields = ["nota", "video"]
    template_name = "website/form.html"
    extra_context = {
        "titulo": "Cadastro de Avaliação",
        "botao": "Cadastrar"
    }

    def form_valid(self, form):
        form.instance.cadastrado_por = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("video_detail", kwargs={"pk": self.object.video.pk})





class LikeCreate(CreateView):
    model = Like
    fields = ["comentario", "like"]
    template_name = "website/form.html"
    extra_context = {
        "titulo": "Cadastro de like",
        "botao": "Cadastrar"
    }

    def form_valid(self, form):
        form.instance.cadastrado_por = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("Tela")
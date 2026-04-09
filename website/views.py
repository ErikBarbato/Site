from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from django.urls import reverse_lazy

from .models import Tema, Subtema, Video, Comentario, Avaliacao, Like

class Index(TemplateView):
    template_name = "website/modelo.html"

class Sobre(TemplateView):
    template_name = "website/sobre.html"

class Contato(TemplateView):
    template_name = "website/contato.html"

class TemaCreate(CreateView): 
    model = Tema
    fields = ["nome"]
    template_name = "website/form.html"
    success_url = reverse_lazy("pagina_inicial")
    extra_context = {
        "Titulo": "Cadastro de Tema",
        "botão": "Cadastrar"
    }

class TemaUpdate(UpdateView): 
    model = Tema
    fields = ["nome"]
    template_name = "website/form.html"
    success_url = reverse_lazy("pagina_inicial")
    extra_context = {
        "Titulo": "Edição de Tema",
        "botão": "Salvar"
    }

class TemaDelete(DeleteView):
    model: Tema
    template_name = "website/form.html"
    success_url = reverse_lazy("pagina_inicial")
    extra_context = {
        "Titulo": "Cadastro de Tema",
        "botão": "Excluir"
    }

class TemaList(ListView):
    model: Tema
    template_name = "website/lista/Tema.html"

class TemaDetail(DetailView):
    model = Tema
    template_name= "website/lista/Tema.html"







class SubtemaCreate(CreateView):
    model = Subtema
    fields = ["nome", "tema"]
    template_name = "website/form.html"
    success_url = reverse_lazy("pagina_inicial")

    def form_valid(self, form):
        form.instance.cadastrado_por = self.request.user
        return super().form_valid(form)


class SubtemaUpdate(UpdateView):
    model = Subtema
    fields = ["nome", "tema"]
    template_name = "website/form.html"
    success_url = reverse_lazy("pagina_inicial")


class SubtemaDelete(DeleteView):
    model = Subtema
    template_name = "website/confirm_delete.html"
    success_url = reverse_lazy("pagina_inicial")


class SubtemaList(ListView):
    model = Subtema
    template_name = "website/lista/subtema.html"


class SubtemaDetail(DetailView):
    model = Subtema
    template_name = "website/detalhe/subtema.html"







class VideoCreate(CreateView):
    model = Video
    fields = ["titulo", "descricao", "link", "subtema", "ativo"]
    template_name = "website/form.html"
    success_url = reverse_lazy("pagina_inicial")

    def form_valid(self, form):
        form.instance.cadastrado_por = self.request.user
        return super().form_valid(form)


class VideoUpdate(UpdateView):
    model = Video
    fields = ["titulo", "descricao", "link", "subtema", "ativo"]
    template_name = "website/form.html"
    success_url = reverse_lazy("pagina_inicial")


class VideoDelete(DeleteView):
    model = Video
    template_name = "website/confirm_delete.html"
    success_url = reverse_lazy("pagina_inicial")


class VideoList(ListView):
    model = Video
    template_name = "website/lista/video.html"

    def get_queryset(self):
        return Video.objects.filter(ativo=True)


class VideoDetail(DetailView):
    model = Video
    template_name = "website/detalhe/video.html"



class ComentarioCreate(AlunoRequiredMixin, LoginRequiredMixin, CreateView):
    model = Comentario
    fields = ["texto", "video"]
    template_name = "website/form.html"

    def form_valid(self, form):
        form.instance.cadastrado_por = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("video_detail", kwargs={"pk": self.object.video.pk})
    





class AvaliacaoCreate(AlunoRequiredMixin, LoginRequiredMixin, CreateView):
    model = Avaliacao
    fields = ["nota", "video"]
    template_name = "website/form.html"

    def form_valid(self, form):
        form.instance.cadastrado_por = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("video_detail", kwargs={"pk": self.object.video.pk})





class LikeCreate(AlunoRequiredMixin, LoginRequiredMixin, CreateView):
    model = Like
    fields = ["comentario", "like"]
    template_name = "website/form.html"

    def form_valid(self, form):
        form.instance.cadastrado_por = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("pagina_inicial")
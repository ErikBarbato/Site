from decimal import Decimal, InvalidOperation

from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.http import JsonResponse

from django.urls import reverse, reverse_lazy

from .models import Tema, Subtema, Video, Comentario, Avaliacao, Like
from django.db.models import Avg, Count, F
from django.db.models.functions import Round

class Index(TemplateView):
    template_name = "website/menu.html"

class Sobre(TemplateView):
    template_name = "website/sobre.html"
    
class Criadores(TemplateView):
    template_name = "website/criadores.html"

class Config_user(TemplateView):
    template_name = "website/config_user.html"

class Config_priva(TemplateView):
    template_name = "website/config_priva.html"

class Config_noti(TemplateView):
    template_name = "website/config_noti.html"

class Contato(TemplateView):
    template_name = "website/contato.html"

class MenuCadastro(TemplateView):
    template_name = "website/menuCadastro.html"


def sair(request):
    logout(request)
    return redirect("login")


class CadastroAluno(TemplateView):
    template_name = "website/CadastroAluno.html"

class CadastroProfessor(TemplateView):
    template_name = "website/CadastroProfessor.html"


class VideoTela(TemplateView):
    template_name = "website/video.html"




class MenuLogin(TemplateView):
    template_name = "website/menuLogin.html"

class LoginAluno(TemplateView):
    template_name = "website/LoginAluno.html"

class LoginProfessor(TemplateView):
    template_name = "website/LoginProfessor.html"





class Tela(TemplateView):
    template_name = "website/modelo.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["videos"] = Video.objects.annotate(
            media_avaliacao=Avg('avaliacoes__nota'),
            media_avaliacao_rounded=Round(Avg('avaliacoes__nota')),
            comentarios_qtd=Count('comentarios')
        )[:9]

        return context


class TemaCreate(LoginRequiredMixin, CreateView): 
    model = Tema
    fields = ["nome", "cadastrado_por"]
    template_name = "website/form.html"
    success_url = reverse_lazy("Tela")
    extra_context = {
        "titulo": "Cadastro de Tema",
        "botao": "Cadastrar"
    }

    def form_valid(self, form):
        form.instance.cadastrado_por = self.request.user
        return super().form_valid(form)

class TemaUpdate(LoginRequiredMixin, UpdateView): 
    model = Tema
    fields = ["nome"]
    template_name = "website/form.html"
    success_url = reverse_lazy("Tela")
    extra_context = {
        "titulo": "Atualizar Tema",
        "botao": "Atualizar"
    }
    def get_queryset(self):
        return super().get_queryset().filter(cadastrado_por=self.request.user)

class TemaDelete(LoginRequiredMixin, DeleteView):
    model= Tema
    template_name = "website/form.html"
    success_url = reverse_lazy("Tela")
    extra_context = {
        "titulo": "Cadastro de Tema",
        "botao": "Excluir"
    }
    def get_queryset(self):
        return super().get_queryset().filter(cadastrado_por=self.request.user)

class TemaList(LoginRequiredMixin, ListView):
    model= Tema
    template_name = "website/lista/Tema.html"

    def get_queryset(self):
        return super().get_queryset().filter(cadastrado_por=self.request.user)

class TemaDetail(LoginRequiredMixin, DetailView):
    model = Tema
    template_name= "website/ver/Tema.html"

    def get_queryset(self):
        return super().get_queryset().filter(cadastrado_por=self.request.user)







class SubtemaCreate(LoginRequiredMixin, CreateView):
    model = Subtema
    fields = ["nome", "tema"]
    template_name = "website/form.html"
    success_url = reverse_lazy("Tela")
    extra_context = {
        "titulo": "Cadastro de Subtemas",
        "botao": "Cadastrar"
    }

    def form_valid(self, form):
        form.instance.cadastrado_por = self.request.user
        return super().form_valid(form)


class SubtemaUpdate(LoginRequiredMixin, UpdateView):
    model = Subtema
    fields = ["nome", "tema"]
    template_name = "website/form.html"
    success_url = reverse_lazy("Tela")
    extra_context = {
        "titulo": "Atualizar Subtema",
        "botao": "Atualizar"
    }

    def get_queryset(self):
        return super().get_queryset().filter(cadastrado_por=self.request.user)


class SubtemaDelete(LoginRequiredMixin, DeleteView):
    model = Subtema
    template_name = "website/form.html"
    success_url = reverse_lazy("Tela")
    extra_context = {
        "titulo": "Deletar Subtema",
        "botao": "Excluir"
    }

    def get_queryset(self):
        return super().get_queryset().filter(cadastrado_por=self.request.user)


class SubtemaList(LoginRequiredMixin, ListView):
    model = Subtema
    template_name = "website/lista/subtema.html"

    def get_queryset(self):
       return super().get_queryset().filter(cadastrado_por=self.request.user)


class SubtemaDetail(LoginRequiredMixin, DetailView):
    model = Subtema
    template_name = "website/ver/subtema.html"

    def get_queryset(self):
        return super().get_queryset().filter(cadastrado_por=self.request.user)







class VideoCreate(LoginRequiredMixin, CreateView):
    model = Video
    fields = ["titulo", "descricao", "link", "subtema", "ativo", "cadastrado_por"]
    template_name = "website/form.html"
    success_url = reverse_lazy("Tela")
    extra_context = {
        "titulo": "Cadastro de Video",
        "botao": "Cadastrar"
    }

    def form_valid(self, form):
        form.instance.cadastrado_por = self.request.user
        return super().form_valid(form)


class VideoUpdate(LoginRequiredMixin, UpdateView):
    model = Video
    fields = ["titulo", "descricao", "link", "subtema", "ativo"]
    template_name = "website/form.html"
    success_url = reverse_lazy("Tela")
    extra_context = {
        "titulo": "Atualizar Video",
        "botao": "Atualizar"
    }
    def get_queryset(self):
        return super().get_queryset().filter(cadastrado_por=self.request.user)


class VideoDelete(LoginRequiredMixin,DeleteView):
    model = Video
    template_name = "website/form.html"
    success_url = reverse_lazy("Tela")
    extra_context = {
        "titulo": "Deletar de Video",
        "botao": "Excluir"
    }
    def get_queryset(self):
        return super().get_queryset().filter(cadastrado_por=self.request.user)


class VideoList(LoginRequiredMixin, ListView):
    model = Video
    template_name = "website/lista/video.html"


    def get_queryset(self):
        return super().get_queryset().filter(cadastrado_por=self.request.user)


class VideoDetail(DetailView):
    model = Video
    template_name = "website/video.html"
    context_object_name = "video"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        Video.objects.filter(pk=self.object.pk).update(visualizacoes=F('visualizacoes') + 1)
        self.object.refresh_from_db(fields=['visualizacoes'])
        self.object.link = self.object.converter_link
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        tema_id = request.GET.get("tema")
        # Handle rating (nota) submission (supports 0.5 - 5.0)
        rating_response = None

        if request.POST.get("nota") is not None:
            if request.user.is_authenticated:
                try:
                    nota = Decimal(request.POST.get("nota"))
                    if Decimal("0.5") <= nota <= Decimal("5.0"):
                        Avaliacao.objects.update_or_create(
                            video=self.object,
                            cadastrado_por=request.user,
                            defaults={"nota": nota}
                        )
                except (ValueError, TypeError, InvalidOperation):
                    nota = None

            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                self.object.refresh_from_db()
                return JsonResponse({
                    "success": request.user.is_authenticated,
                    "average_rating": float(self.object.average_rating),
                    "rating": float(nota) if request.user.is_authenticated and nota is not None else None,
                }, status=200 if request.user.is_authenticated else 401)

        # Handle comment submission
        if request.POST.get("texto") is not None:
            if request.user.is_authenticated:
                texto = request.POST.get("texto", "").strip()
                if texto:
                    Comentario.objects.create(
                        video=self.object,
                        texto=texto,
                        cadastrado_por=request.user
                    )
        redirect_url = reverse("video_detail", kwargs={"pk": self.object.pk})
        if tema_id:
            redirect_url = f"{redirect_url}?tema={tema_id}"
        return redirect(redirect_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comentarios"] = self.object.comentarios.order_by("-cadastrado_em")
        context["avaliacao_media"] = self.object.average_rating
        context["tema_filtros"] = Tema.objects.all()
        context["sidebar_videos"] = Video.objects.filter(
            ativo=True,
            ).exclude(pk=self.object.pk).select_related("subtema__tema").order_by("-cadastrado_em")[:20]
        return context


class ComentarioDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comentario
    template_name = "website/form.html"
    extra_context = {
        "titulo": "Excluir Comentário",
        "botao": "Excluir"
    }

    def test_func(self):
        comentario = self.get_object()
        return comentario.cadastrado_por == self.request.user

    def get_success_url(self):
        return reverse_lazy("video_detail", kwargs={"pk": self.object.video.pk})


# class ComentarioCreate(CreateView):
#     model = Comentario
#     fields = ["texto", "video"]
#     template_name = "website/form.html"
#     extra_context = {
#         "titulo": "Cadastro de Comentario",
#         "botao": "Cadastrar"
#     }

#     def form_valid(self, form):
#         form.instance.cadastrado_por = self.request.user
#         return super().form_valid(form)

#     def get_success_url(self):
#         return reverse_lazy("video_detail", kwargs={"pk": self.object.video.pk})
    





# class AvaliacaoCreate(CreateView):
#     model = Avaliacao
#     fields = ["nota", "video"]
#     template_name = "website/form.html"
#     extra_context = {
#         "titulo": "Cadastro de Avaliação",
#         "botao": "Cadastrar"
#     }

#     def form_valid(self, form):
#         form.instance.cadastrado_por = self.request.user
#         return super().form_valid(form)

#     def get_success_url(self):
#         return reverse_lazy("video_detail", kwargs={"pk": self.object.video.pk})





# class LikeCreate(CreateView):
#     model = Like
#     fields = ["comentario", "like"]
#     template_name = "website/form.html"
#     extra_context = {
#         "titulo": "Cadastro de like",
#         "botao": "Cadastrar"
#     }

#     def form_valid(self, form):
#         form.instance.cadastrado_por = self.request.user
#         return super().form_valid(form)

#     def get_success_url(self):
#         return reverse_lazy("Tela")
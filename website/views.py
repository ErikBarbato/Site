from django.views.generic import TemplateView

class Index(TemplateView):
    template_name = "website/modelo.html"

class Sobre(TemplateView):
    template_name = "website/sobre.html"

class Contato(TemplateView):
    template_name = "website/contato.html"


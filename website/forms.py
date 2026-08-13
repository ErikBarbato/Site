from django import forms

from .models import Subtema, Tema, Video


class SubtemaForm(forms.ModelForm):
    class Meta:
        model = Subtema
        fields = ["nome", "tema"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        queryset = Tema.objects.all()
        if self.user is not None:
            queryset = queryset.filter(cadastrado_por=self.user)

        self.fields["tema"].queryset = queryset.select_related("cadastrado_por").order_by("nome")


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ["titulo", "descricao", "link", "subtema", "ativo"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        queryset = Subtema.objects.select_related("tema", "cadastrado_por")
        if self.user is not None:
            queryset = queryset.filter(cadastrado_por=self.user)

        self.fields["subtema"].queryset = queryset.order_by("tema__nome", "nome")

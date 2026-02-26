from django.urls import path
from .views import Index

urlpatterns = [
    #path("admin/", admin.site.urls),

    path("inicio", Index.as_view(), name="pagina_inicial"),
]
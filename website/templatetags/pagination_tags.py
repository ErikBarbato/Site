from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def pagination_url(context, page_number):
    """Cria a URL da página preservando filtros e parâmetros da querystring."""
    request = context.get("request")
    if request is None:
        return f"?page={page_number}"

    params = request.GET.copy()
    params["page"] = page_number
    querystring = params.urlencode()

    if querystring:
        return f"{request.path}?{querystring}"
    return request.path


@register.filter
def querystring_without_page(request):
    """Remove o parâmetro page da querystring mantendo o restante dos filtros."""
    if request is None:
        return ""

    params = request.GET.copy()
    params.pop("page", None)
    querystring = params.urlencode()

    if querystring:
        return f"?{querystring}"
    return ""

from .models import SiteText


def site_texts(request):
    """Expose les textes modifiables dans tous les templates."""
    try:
        texts = {
            item.key: item.content
            for item in SiteText.objects.filter(is_active=True)
        }
    except Exception:
        # Important pendant les migrations / collectstatic : ne jamais casser le rendu.
        texts = {}
    return {'site_texts': texts}

"""Outils de mise en forme pour les contenus éditables.

Le but est de laisser la cliente écrire un texte simple dans l'admin
avec une syntaxe Markdown légère, puis de produire un HTML propre,
sûr et compatible email.
"""

import re
from html import escape

from django.utils.safestring import mark_safe


_LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^\s)]+|mailto:[^\s)]+)\)")


EMAIL_STYLES = {
    "h2": "font-family:Georgia,serif;font-size:23px;line-height:1.35;color:#5A0E28;margin:34px 0 14px;font-weight:600;text-align:left;",
    "h3": "font-family:Georgia,serif;font-size:19px;line-height:1.45;color:#7B1733;margin:28px 0 12px;font-weight:600;text-align:left;",
    "p": "font-family:Arial,Helvetica,sans-serif;font-size:16px;line-height:1.85;color:#342629;margin:0 0 18px;text-align:left;",
    "li": "font-family:Arial,Helvetica,sans-serif;font-size:16px;line-height:1.75;color:#342629;margin:0 0 9px;text-align:left;",
    "ul": "padding-left:22px;margin:0 0 22px;text-align:left;",
    "quote": "font-family:Georgia,serif;font-size:18px;line-height:1.7;color:#7B1733;font-style:italic;margin:24px 0;padding:18px 22px;background:#FBF3EA;border-left:3px solid #B88757;text-align:left;",
    "hr": "border:none;border-top:1px solid #E7D8CB;margin:30px 0;",
    "strong": "color:#5A0E28;font-weight:700;",
    "em": "color:#7B1733;font-style:italic;",
    "a": "color:#7B1733;text-decoration:underline;font-weight:700;",
}


def _format_inline(text: str) -> str:
    """Échappe le texte et applique liens, gras, italique de façon sûre."""
    if not text:
        return ""

    placeholders = []

    def store_link(match):
        label = escape(match.group(1), quote=False)
        url = escape(match.group(2), quote=True)
        html = f'<a href="{url}" target="_blank" style="{EMAIL_STYLES["a"]}">{label}</a>'
        placeholders.append(html)
        return f"@@LINK{len(placeholders) - 1}@@"

    text = _LINK_RE.sub(store_link, text)
    text = escape(text, quote=False)

    # Gras : **texte**
    text = re.sub(
        r"\*\*(.+?)\*\*",
        rf'<strong style="{EMAIL_STYLES["strong"]}">\1</strong>',
        text,
    )

    # Italique simple : *texte* ; évite de toucher aux **gras** déjà transformés.
    text = re.sub(
        r"(?<!\*)\*([^*]+)\*(?!\*)",
        rf'<em style="{EMAIL_STYLES["em"]}">\1</em>',
        text,
    )

    for i, html in enumerate(placeholders):
        text = text.replace(f"@@LINK{i}@@", html)

    return text


def render_email_markdown(text: str):
    """Transforme un Markdown très simple en HTML email safe.

    Syntaxes acceptées dans l'admin :
    ## Titre
    ### Sous-titre
    **gras**
    *italique*
    - liste
    > citation
    --- séparation
    [lien](https://exemple.com)
    """
    if not text:
        return mark_safe("")

    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    html_parts = []
    paragraph = []
    list_items = []

    def flush_paragraph():
        nonlocal paragraph
        if paragraph:
            joined = " ".join(line.strip() for line in paragraph if line.strip())
            if joined:
                html_parts.append(f'<p style="{EMAIL_STYLES["p"]}">{_format_inline(joined)}</p>')
            paragraph = []

    def flush_list():
        nonlocal list_items
        if list_items:
            items = "".join(
                f'<li style="{EMAIL_STYLES["li"]}">{_format_inline(item)}</li>'
                for item in list_items
            )
            html_parts.append(f'<ul style="{EMAIL_STYLES["ul"]}">{items}</ul>')
            list_items = []

    for raw_line in lines:
        line = raw_line.strip()

        if not line:
            flush_paragraph()
            flush_list()
            continue

        if line in {"---", "***", "___"}:
            flush_paragraph()
            flush_list()
            html_parts.append(f'<hr style="{EMAIL_STYLES["hr"]}">')
            continue

        if line.startswith("### "):
            flush_paragraph()
            flush_list()
            html_parts.append(f'<h3 style="{EMAIL_STYLES["h3"]}">{_format_inline(line[4:].strip())}</h3>')
            continue

        if line.startswith("## "):
            flush_paragraph()
            flush_list()
            html_parts.append(f'<h2 style="{EMAIL_STYLES["h2"]}">{_format_inline(line[3:].strip())}</h2>')
            continue

        if line.startswith(">"):
            flush_paragraph()
            flush_list()
            quote = line.lstrip(">").strip()
            html_parts.append(f'<div style="{EMAIL_STYLES["quote"]}">“{_format_inline(quote)}”</div>')
            continue

        if line.startswith(("- ", "* ", "• ")):
            flush_paragraph()
            if line.startswith("• "):
                list_items.append(line[2:].strip())
            else:
                list_items.append(line[2:].strip())
            continue

        if list_items:
            flush_list()
        paragraph.append(line)

    flush_paragraph()
    flush_list()

    return mark_safe("\n".join(html_parts))

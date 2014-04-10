"""Template tags to hook into weblate's UI."""

from django import template
register = template.Library()


@register.simple_tag
def gengo_language():
    """Return gengo dashboard for a project's language overview."""
    return "<h2>Gengo Project Language</h2>"


@register.simple_tag
def gengo_translation():
    """Return gengo ui for a specific translation."""
    return "<h2>Gengo Translation</h2>"

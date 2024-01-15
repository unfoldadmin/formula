from modeltranslation.translator import TranslationOptions, register

from formula.models import Circuit


@register(Circuit)
class CircuitTranslation(TranslationOptions):
    fields = ["name"]

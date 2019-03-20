import django_filters
from lang.models import Word

class WordFilter(django_filters.FilterSet):
    class Meta:
        model = Word
        fields = {
            'word': ['icontains'],
            'grammar_part': ['exact'],
            'success_rate': ['icontains'],
        }
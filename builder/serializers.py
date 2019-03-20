from rest_framework import serializers
from lang import models

class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Word
        fields = ('pk', 'word', 'grammar_part', 'date_created')

class MeaningSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Word
        fields = ('pk', 'word', 'grammar_part', 'date_created')
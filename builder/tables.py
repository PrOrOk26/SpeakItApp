import django_tables2 as tables
from lang.models import Word

class WordsTable(tables.Table):

    actions = tables.TemplateColumn(template_name='builder/edit_delete.html',
                                extra_context={'label': 'Actions'})
    
    class Meta:
        attrs = {
            'th' : {
                '_ordering': {
                    'orderable': 'sortable', # Instead of `orderable`
                    'ascending': 'ascend',   # Instead of `asc`
                    'descending': 'descend'  # Instead of `desc`
                }
            }
        }
        model = Word
        fields = ['id', 'word', 'grammar_part', 'success_rate', 'date_created']
        template_name = 'django_tables2/bootstrap.html'
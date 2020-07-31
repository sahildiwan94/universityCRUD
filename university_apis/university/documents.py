from django_elasticsearch_dsl import Document, Index, fields
from elasticsearch_dsl import normalizer
from elasticsearch_dsl.analysis import token_filter
from .models import University
from django_countries.fields import CountryField

# Formatting of Django Country field to Object field of Elasticsearch
CountryField.to_dict = lambda self: {"code":self.code,"name":self.name}

# Name of the Elasticsearch index
UNIVERSITY_INDEX = Index('university')

# Elasticsearch Indices settings
UNIVERSITY_INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1
)

# Normalizer for keyword fields
keyword_normalizer = normalizer(
    'keyword_normalizer',
    type="custom",
    filter=["lowercase"],
)


@UNIVERSITY_INDEX.doc_type
class UniversityDocument(Document):
    """University Elasticsearch document."""

    id = fields.IntegerField(attr='id')
    name = fields.TextField(
        fields={
            'raw': fields.KeywordField(normalizer=keyword_normalizer),
        },
    )
    domain = fields.TextField(
        fields={
            'raw': fields.KeywordField(normalizer=keyword_normalizer)
        }
    )
    web_page = fields.TextField(
        fields={
            'raw': fields.KeywordField(normalizer=keyword_normalizer)
        }
    )
    country = fields.ObjectField(properties={
        'name': fields.TextField(),
        'code': fields.TextField(
            fields={
            'raw': fields.KeywordField(normalizer=keyword_normalizer)
        }),
        }
    )
    createdAt = fields.DateField()
    isDelete = fields.BooleanField()
    


    class Django(object):
        """Meta options."""

        model = University  # The model associate with this DocType

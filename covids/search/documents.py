from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from common.models import *
from datetime import datetime

@registry.register_document
class StatesDocument(Document):
    class Index:
        # Name of the Elasticsearch index
        name = 'states'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = allStates  # The model associated with this Document
        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'province',
            'Update',
            'confirmed',
            'death',
            'recovered',
            'active',
            'rate',
            'updateTime',
        ]

    def save(self, **kwargs):
        self.updateTime = datetime.now()
        return super().save(**kwargs)

@registry.register_document
class ConfirmedDocument(Document):
    class Index:
        # Name of the Elasticsearch index
        name = 'confirmed'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = timeSeriseConfirmed  # The model associated with this Document
        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'uid',
            'city',
            'province',
            'cityName',
            'confirmed',
            'Range',
        ]

@registry.register_document
class DeathDocument(Document):
    class Index:
        # Name of the Elasticsearch index
        name = 'death'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = timeSeriseDeath  # The model associated with this Document
        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'uid',
            'city',
            'province',
            'cityName',
            'death',
            'Range',
        ]

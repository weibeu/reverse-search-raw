from .search import Elasticsearch
from .. import config


client = Elasticsearch(hosts=config.ELASTICSEARCH["hosts"])

from .search import Elasticsearch
from .. import config


client = Elasticsearch(
    hosts=config.ELASTICSEARCH["hosts"],
    timeout=30, max_retries=10, retry_on_timeout=True
)

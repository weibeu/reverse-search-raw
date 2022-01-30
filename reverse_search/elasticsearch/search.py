from elasticsearch.helpers import bulk

import csv
import elasticsearch


class Elasticsearch(elasticsearch.Elasticsearch):

    def bulk_index_from_csv(self, filepath, index):
        with open(filepath, newline=str(), encoding="utf-8") as file:
            reader = csv.DictReader(file)
            bulk(self, reader, index=index)

    # def get_resource(self, name, cls, session, **kwargs):
    #     result = self.search({
    #         "query": {
    #             "match": {"name": name, **kwargs}
    #         }
    #     }, index=cls.ELASTICSEARCH_INDEX)
    #     try:
    #         document = result["hits"]["hits"][0]
    #     except IndexError:
    #         return
    #     return session.query(cls).filter_by(id=document["_id"]).first()

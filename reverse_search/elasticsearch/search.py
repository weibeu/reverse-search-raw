from elasticsearch.helpers import bulk

import csv
import sys
import elasticsearch


class Elasticsearch(elasticsearch.Elasticsearch):

    def bulk_index_from_csv(self, filepath, index):
        max_int = sys.maxsize
        while True:
            # decrease the maxInt value by factor 10
            # as long as the OverflowError occurs.

            try:
                csv.field_size_limit(max_int)
                break
            except OverflowError:
                max_int = int(max_int / 10)

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

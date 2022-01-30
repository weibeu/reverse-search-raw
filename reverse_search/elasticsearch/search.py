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

    def get_hits(self, index, **field_queries):
        result = self.search(index=index, query={
            "match": {
                fn: {"query": query} for fn, query in field_queries.items()
            }})
        return result["hits"]["hits"]

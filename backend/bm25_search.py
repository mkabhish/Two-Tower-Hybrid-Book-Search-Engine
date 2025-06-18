from whoosh.fields import Schema, TEXT, ID
from whoosh.index import create_in
from whoosh.qparser import QueryParser
import os
import shutil

class BM25Search:
    def __init__(self, index_dir='whoosh_index'):
        self.index_dir = index_dir
        self.schema = Schema(id=ID(stored=True), title=TEXT(stored=True))
        if os.path.exists(index_dir):
            shutil.rmtree(index_dir)
        os.mkdir(index_dir)
        self.ix = create_in(index_dir, self.schema)

    def build_index(self, products, id_key='book_id', text_key='title'):
        writer = self.ix.writer()
        for product in products:
            writer.add_document(id=str(product[id_key]), title=product[text_key])
        writer.commit()

    def search(self, query, top_k=5):
        with self.ix.searcher() as searcher:
            qp = QueryParser("title", schema=self.ix.schema)
            q = qp.parse(query)
            results = searcher.search(q, limit=top_k)
            return [int(r['id']) for r in results] 
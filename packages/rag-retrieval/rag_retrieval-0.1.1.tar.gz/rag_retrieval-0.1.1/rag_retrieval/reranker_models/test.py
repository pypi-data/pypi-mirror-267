from ranker import BaseRanker
from typing import Union, List, Optional, Tuple

class llmreranker(BaseRanker):

    def __init__(self, model_name_or_path: str, verbose: int):
        super().__init__(model_name_or_path, verbose)
        print(1)
    
    def rerank(self, query: str, docs: List[str], doc_ids: Optional[Union[List[str], str]] = None):
        return 1


s=llmreranker('1',1)
from .acs import (
    simple_search_with_score,
    semantic_search_with_score,
    with_metadata_unpacker as with_acs_metadata_unpacker
)

from ..common_index_lookup_utils.constants import QueryTypes

from ...core.contracts.entities import SearchResultDocument

from azureml.rag import MLIndex
import functools
from langchain.docstore.document import Document
from typing import Callable, List, Tuple


def build_search_func(index: MLIndex, top_k: int, query_type: str) -> Callable[[str], List[Tuple[Document, float]]]:
    # Override the embeddings section if we're making keyword queries.
    if query_type in {QueryTypes.Simple, QueryTypes.Semantic}:
        index.embeddings_config = {
            'schema_version': '2',
            'kind': 'none'
        }

        index.index_config.get('field_mapping', {})['embedding'] = ''

    index_kind = index.index_config.get("kind", "none")

    if index_kind == 'acs':
        # Copy the MLIndex's metadata field mapping value, and force-set the value in the MLIndex to None.
        # This will make langchain dump all the fields in the index, and we can manually extract metadata after.
        metadata_field_name = index.index_config.get('field_mapping', {}).get('metadata', 'meta_json_string')
        if 'field_mapping' in index.index_config:
            index.index_config['field_mapping']['metadata'] = '@'
        store = index.as_langchain_vectorstore()

        if query_type == QueryTypes.Simple:
            search_func = functools.partial(
                simple_search_with_score,
                store=store,
                k=top_k,
                field_mapping=index.index_config.get('field_mapping'),
            )

        elif query_type == QueryTypes.Semantic:
            search_func = functools.partial(
                semantic_search_with_score,
                store=store,
                k=top_k,
                field_mapping=index.index_config.get('field_mapping')
            )

        elif query_type == QueryTypes.Vector:
            search_func = functools.partial(store.vector_search_with_score, k=top_k)

        elif query_type == QueryTypes.VectorSimpleHybrid:
            search_func = functools.partial(store.hybrid_search_with_score, k=top_k)

        elif query_type == QueryTypes.VectorSemanticHybrid:
            search_func = functools.partial(store.semantic_hybrid_search_with_score, k=top_k)

        else:
            raise ValueError(f'Unsupported query type: {query_type} for index kind {index_kind}.')

        return with_acs_metadata_unpacker(search_func, metadata_field_name)
    else:
        if query_type == QueryTypes.Vector:
            return with_type_mapper(
                functools.partial(index.as_langchain_vectorstore().similarity_search_with_score, k=top_k)
            )

    raise ValueError(f'Unsupported query type: {query_type} for index kind {index_kind}.')


def with_type_mapper(
    search_func: Callable[[str], List[Tuple[Document, float]]]
) -> Callable[[str], List[Tuple[SearchResultDocument, float]]]:
    def wrapper(query: str) -> List[Tuple[Document, float]]:
        results = search_func(query)
        processed_results = []
        for result, score in results:
            processed_results.append((
                SearchResultDocument(
                    page_content=result.page_content,
                    score=score,
                    metadata=result.metadata,
                    additional_fields=result.metadata,
                ),
                score
            ))

        return processed_results

    return wrapper

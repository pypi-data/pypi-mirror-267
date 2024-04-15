# pub fn serialize_tree(
#     py: Python,
#     tree_object: TreeObject,
#     prefetch_objects: Vec<Prefetch>,
#     is_tree: bool,
# ) -> Vec<PythonInstance> {
from typing import Any
from rusty.types import CaseSearchQueryParams as CSQP, Prefetch as P, DataSetObject as DSO


class CaseSearchQueryParams(CSQP):
    """"""


class Prefetch(P):
    """"""


class DataSetObject(DSO):
    """"""


def serialize_tree(
    data_set_object: DataSetObject,
    prefetch_objects: list[Prefetch],
    is_tree: bool,
) -> list[dict[str, Any]]:
    """
    Retrieve python objects retrieved from queries and build dict for json.

    Args:
        data_set_object: description type of provided data
        prefetch_objects: description type of data that should be "prefetched" on main object
        is_tree: boolean flag to build main data set as tree.

    Returns:
        _description_
    """


def cases_search(query_params: CaseSearchQueryParams) -> str:
    """
    Search for cases and build tree structure from retrieved data.

    Create new db connection execute request to retrieve cases and then suites by provided
    requests, build tree structure.

    Args:
        query_params: db query and params for connection

    Returns:
        Json string.
    """

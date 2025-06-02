"""Module specifications.py"""
import typing

class Specifications(typing.NamedTuple):
    """
    The data type class ⇾ Specifications

    Attributes
    ----------

    """

    hospital_code: str
    hospital_name: str
    health_board_code: str
    health_board_name: str
    post_code: str
    hscp_code: str
    council_area: str
    intermediate_zone: str
    data_zone: str

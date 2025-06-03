"""Module specifications.py"""
import typing

class Specifications(typing.NamedTuple):
    """
    The data type class ⇾ Specifications

    Attributes
    ----------

    hospital_code: str
        <a href="https://www.opendata.nhs.scot/dataset/hospital-codes" target="_blank">Hospital Code</a><br>
    hospital_name: str
        The hospital's/institution's name.<br>
    health_board_code: str
        <a href="https://geoportal.statistics.gov.uk/documents/844159d820da487686d124a25e2eb84d/about" target="_blank">
        Health Board</a> Code<br>
    health_board_name: str
        Health Board Name<br>
    post_code: str
        The hospital's/institution's post code.<br>
    hscp_code: str
        The codes of <a href="https://hscscotland.scot/hscps/" target="_blank">Health and Social Care Partnerships</a><br>
    council_area: str
        The <a href="https://www.mygov.scot/organisations#scottish-local-authority" target="_blank">council area</a> locale
        of the hospital/institution;
        <a href="https://geoportal.statistics.gov.uk/documents/7ef19fb100de4c1ab964f65599e9534b/explore"
        target="_blank">map</a>.<br>
    intermediate_zone: str
        <a
        href="https://geoportal.statistics.gov.uk/datasets/ons::intermediate-zones-december-2001-names-and-codes-in-sc/about"
        target="_blank">Intermediate Zone</a><br>
    data_zone: str
        <a href="https://geoportal.statistics.gov.uk/datasets/ons::data-zones-december-2011-names-and-codes-in-sc/about">
        Data Zones</a>
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

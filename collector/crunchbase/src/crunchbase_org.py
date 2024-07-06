from __future__ import annotations

import json, os, dataclasses, logging
from typing import ClassVar

import requests

from src.exceptions import CrunchbaseQueryError
from src.config import CRUNCHBASE_API_ENDPOINT
from utils import get_env_vars

logger = logging.getLogger(__package__)

@dataclasses.dataclass
class CrunchbaseOrganization():
    """
    A class that encapsulates data received from crunchbase about a company.
    Supports getting additional info from crunchbase about the org.
    """

    name: str
    uuid: int
    website_url: str

    @classmethod
    def get_required_fields(cls) -> list[str]:
        """
        Returns the info fields about an org required to create this object.
        """
        return [field.name for field in dataclasses.fields(cls)]
        
    @classmethod
    def create_from_uuid(cls, uuid: int) -> CrunchbaseOrganization:
        """
        Factory method to generate a CrunchbaseOrganization from an organization uuid.
        Performs an API call to crunchbase to get info on the requested org.
        :param uuid: The uuid of the org to create an CrunchbaseOrganization object from.
        :returns: The generated CrunchbaseOrganization object.
        """

        logger.debug(f"Creating CrunchbaseOrganization for uuid '{uuid}'")

        org_info = cls._get_org_info_by_uuid(uuid)
        fields = org_info["cards"]["fields"]
        return cls(fields["name"], uuid, fields["website_url"])

    @classmethod
    def create_from_org_fields(cls, org_fields: dict, query_for_missing_info: bool = True) -> CrunchbaseOrganization:
        """
        Factory method to generate a CrunchbaseOrganization from an organization info dict.
        If required info is missing, can perform additional crunchbase API calls to get additional data.
        :param org_fields: Org info dict, as received from crunchbase. Should include all required info about the org.
        :param query_for_missing_info: Whether or not this method should attempt to perform extra calls to crunchbase to get missing info,
                                       or just fail on such a case.
        :returns: The generated CrunchbaseOrganization object.
        """

        logger.debug(f"Creating CrunchbaseOrganization for org_fields '{org_fields}'")

        if not all((field in org_fields) for field in cls.get_required_fields()):
            if query_for_missing_info and "uuid" in org_fields:
                return cls.create_from_uuid(org_fields["uuid"])
            else:
                raise CrunchbaseQueryError(f"Missing fields in organization info: {org_fields}, cannot initialize organization object.")
            
        return cls(org_fields["name"], org_fields["uuid"], org_fields["website_url"])

    @classmethod
    def _get_org_info_by_uuid(cls, uuid: int) -> dict:
        """
        Performs a Crunchbase API call to get info on an org by its uuid.
        :param uuid: The uuid of the org to get the info of.
        :returns: An org info dict for the org.
        """
        api_key, = get_env_vars(["CRUNCHBASE_API_KEY"], required=True)

        query = {"field_ids": cls.get_required_fields(), "card_ids": []}
        logger.debug(f"Getting additional fields about org uuid '{uuid}'. Query is '{query}'.")
        resp = requests.get(f"{CRUNCHBASE_API_ENDPOINT}/entities/organizations/{uuid}", params={"user_key": api_key}, json=query)
        logger.debug(f"Got '{repr(resp)}'")
        return resp.content

    @property
    def json(self) -> str:
        """
        Get json string with the organization data.
        :returns: A json-formatted string with all the data of the org object.
        """

        return json.dumps(dataclasses.asdict(self))
    

    

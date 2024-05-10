from __future__ import annotations

import requests, json, os

from src.exceptions import CrunchbaseQueryError

class CrunchbaseOrganization():
    required_fields = ["name", "uuid", "website_url"]

    def __init__(self, name, uuid, url):
        self.name = name
        self.uuid = uuid
        self.url = url
    
    @classmethod
    def create_from_uuid(cls, uuid: str) -> CrunchbaseOrganization:
        """
        Factory method to generate a CrunchbaseOrganization from an organization uuid.
        Performs an API call to crunchbase to get info on the requested org.
        :param uuid: The uuid of the org to create an CrunchbaseOrganization object from.
        :returns: The generated CrunchbaseOrganization object.
        """

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

        if not all((field in org_fields) for field in cls.required_fields):
            if query_for_missing_info and "uuid" in org_fields:
                return cls.create_from_uuid(org_fields["uuid"])
            else:
                raise CrunchbaseQueryError("Missing uuid field in organization info, cannot initialize organization object.")
            
        return cls(org_fields["name"], org_fields["uuid"], org_fields["website_url"])

    @classmethod
    def _get_org_info_by_uuid(cls, uuid: str) -> dict:
        """
        Performs a Crunchbase API call to get info on an org by its uuid.
        :param uuid: The uuid of the org to get the info of.
        :returns: An org info dict for the org.
        """
        api_key = os.getenv("CRUNCHBASE_API_KEY")
        query = {"field_ids": cls.required_fields, "card_ids": []}
        resp = requests.get(f"https://api.crunchbase.com/api/v4/entities/organizations/{uuid}", params={"user_key": api_key}, json=query)
        return resp.content

    def json(self) -> str:
        """
        Get json string with the organization data.
        :returns: A json-formatted string with all the data of the org object.
        """
        
        dict_values =  {
            "name": self._name,
            "uuid": self._uuid,
            "url": self._url
        }

        return json.dumps(dict_values)

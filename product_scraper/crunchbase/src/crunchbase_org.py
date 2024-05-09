import requests, json, os

class CrunchbaseOrganization():
    required_fields = ["name", "uuid", "website_url"]

    def __init__(self, name, uuid, url):
        self.name = name
        self.uuid = uuid
        self.url = url
    
    @classmethod
    def create_from_uuid(cls, uuid):
        org_info = cls._get_org_info_by_uuid(uuid)
        fields = org_info["cards"]["fields"]
        return cls(fields["name"], uuid, fields["website_url"])

    @classmethod
    def create_from_org_fields(cls, org_fields, query_for_missing_info = True):
        if not all((field in org_fields) for field in cls.required_fields):
            if query_for_missing_info and "uuid" in org_fields:
                return cls.create_from_uuid(org_fields["uuid"])
            else:
                raise Exception("Missing fields in organization info, cannot initialize organization object.")
            
        return cls(org_fields["name"], org_fields["uuid"], org_fields["website_url"])

    @classmethod
    def _get_org_info_by_uuid(cls, uuid):
        api_key = os.getenv("CRUNCHBASE_API_KEY")
        query = {"field_ids": cls.required_fields, "card_ids": []}
        resp = requests.get(f"https://api.crunchbase.com/api/v4/entities/organizations/{uuid}", params={"user_key": api_key}, json=query)
        return resp.content

    def json(self):
        dict_values =  {
            "name": self._name,
            "uuid": self._uuid,
            "url": self._url
        }

        return json.dumps(dict_values)

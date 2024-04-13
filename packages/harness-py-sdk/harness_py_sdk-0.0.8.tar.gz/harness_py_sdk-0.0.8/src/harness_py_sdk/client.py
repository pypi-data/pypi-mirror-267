import requests

from .harness_pipelines import *
from .harness_connectors import *
from .harness_services import *

class Client:
    def __init__(self, api_key, account_identifier):
        self._session = requests.Session()
        self._session.   headers.update({
            'x-api-key': api_key,
            'Harness-Account': account_identifier,
            'Content-Type': 'application/json'
        })
        self._account_identifier = account_identifier
        self._base_url = "https://app.harness.io"
        self._pipelines = None  # Placeholder for the Pipelines class
        self._connectors = None  # Placeholder for the Connectors class
        self._services = None  # Placeholder for the Services class

    @property
    def pipelines(self):
        if self._pipelines is None:
            self._pipelines = HarnessPipelines(self)  # Initialize with self to pass the session
        return self._pipelines

    @property
    def services(self):
        if self._services is None:
            self._services = HarnessServices(self)  # Initialize with self to pass the session
        return self._services

    @property
    def connectors(self):
        if self._connectors is None:
            self._connectors = HarnessConnectors(self)  # Initialize with self to pass the session
        return self._connectors

    def _make_request(self, method, endpoint, **kwargs):
        url = f"{self._base_url}{endpoint}"
        response = self._session.request(method, url, **kwargs)
        if response.ok:
            return response.json()
        print(response.text)
        response.raise_for_status()
    
    # Build the url dynamically for the new beta API
    def _construct_url(self, entity, identifier=None, org_identifier=None, project_identifier=None):
        parts = ["/v1"]

        if org_identifier:
            parts.extend(["orgs", org_identifier])
            if project_identifier:
                parts.extend(["projects", project_identifier])
        
        parts.append(entity)

        if identifier:
            if identifier.startswith("org"):
                identifier = identifier.replace("org.", "")
            elif identifier.startswith("account"):
                identifier = identifier.replace("account.", "")
            
            parts.append(identifier)
        
        return "/".join(parts)



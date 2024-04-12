

class HarnessServices():
    def __init__(self, harness_service):
        self.harness_service = harness_service
    
    def fetch_services(self, params = None, org_identifier=None, project_identifier=None):
        endpoint = self.harness_service.construct_url("services", None, org_identifier, project_identifier)
        return self.harness_service._make_request("GET", endpoint, params = params)
    
    def update_service(self, identifier, data, org_identifier=None, project_identifier=None):
        endpoint = self.harness_service.construct_url("services", identifier, org_identifier, project_identifier)
        return self.harness_service._make_request("PUT", endpoint, json=data)
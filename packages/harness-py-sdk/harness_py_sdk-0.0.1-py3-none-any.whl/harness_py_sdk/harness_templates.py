from harness_base_service import HarnessService

class HarnessTemplates(HarnessService):
    def fetch_template_yaml(self, template_identifier, version, org_identifier=None, project_identifier=None):
        endpoint = self.construct_url(template_identifier, "templates", org_identifier, project_identifier) + f"/versions/{version}"
        return self._make_request("GET", endpoint)
    
    def fetch_stable_template_yaml(self, template_identifier, org_identifier=None, project_identifier=None):
        return self._make_request("GET", self.construct_url(template_identifier, "templates", org_identifier, project_identifier))
    
    def create_template_pipeline(self, template_data, org_identifier=None, project_identifier=None):
        return self._make_request(
            "POST", 
            self.construct_url(entity = "templates", org_identifier = org_identifier, project_identifier = project_identifier), 
            json=template_data
        )
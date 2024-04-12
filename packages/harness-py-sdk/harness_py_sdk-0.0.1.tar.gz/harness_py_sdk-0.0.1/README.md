## Prerequisites

Before running the script, ensure that you have installed the required libraries. You can install them via pip using the following commands:

```bash
pip install requests pyyaml
```

- `requests`: This library is required for making HTTP requests to the Harness platform.
- `pyyaml`: This library is necessary for handling YAML files. It may be required by the script for configuration or data manipulation.

## Getting Started

The first step to utilize this SDK is to authenticate with Harness API, you achieve the following by doing the below:

```python
harness_service = HarnessBaseService(os.environ.get('HARNESS_PLATFORM_API_KEY'), "my-account-identifier")
```

### Example 1 - Listing Services

```python
harness_service.services.fetch_services()
```
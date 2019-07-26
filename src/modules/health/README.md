# Service health check 

Implementation of [standart](https://inadarei.github.io/rfc-healthcheck/)

Example:

```python
from modules.health import *
from modules.shadowsocks.service import SSConf
import json

# Define your checks:

# health check 1 - required
def config_presented():
    result = CheckResult(
        check_name='file_presented',
        pass_status_is_required_for_service=True
    )
    try:
        result.status=HealthStatus.PASS()
        result.observed_value=len(SSConf.get_instance().ss_keys)
        result.observed_unit='Count of ss keys'
    except Exception as e:
        result.output = e
        result.status = HealthStatus.FAIL()
    return result

# health check 1 - not required (Makes service status "warn")
def demo_check(param):
    raise Exception(param)


auth_service_health = ServiceHealth(
    service_id='auth_service',
    components=[
        Component(
            'config',
            ComponentType.SYSTEM,
            checks=[
                Check('config', config_presented, pass_status_is_required_for_service=True)
            ]
        ),
        Component(
            'demo_component',
            ComponentType.SYSTEM,
            checks=[
                Check(
                    'demo_check',
                    demo_check,
                    check_func_kwargs={'param':'demo error'},
                    pass_status_is_required_for_service=False
                )
            ]
        ),
    ],
    version='',
    release_id='',
    description='VPN auth service'
)

auth_service_health = auth_service_health.check()

print("HTTP status code is: {}".format(str(auth_service_health.status.http_code)))
print(json.dumps(auth_service_health.serialize(), indent=4))

```

Result is:

```text
HTTP status code is: 300
{
    "checks": [
        [
            {
                "name": "config:file_presented",
                "componentId": "",
                "output": "",
                "status": "pass",
                "observedUnit": "Count of ss keys",
                "observedValue": 3000,
                "componentType": "system"
            }
        ],
        [
            {
                "name": "demo_component:no_name",
                "componentId": "",
                "output": "demo error",
                "status": "fail",
                "observedUnit": "",
                "observedValue": "",
                "componentType": "system"
            }
        ]
    ],
    "version": "",
    "output": "",
    "status": "warn",
    "serviceId": "auth_service",
    "releaseId": "",
    "notes": [
        ""
    ],
    "description": "VPN auth service"
}

```
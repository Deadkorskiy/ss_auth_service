from flask import Blueprint, jsonify
from settings import settings


router = Blueprint('health', __name__)


@router.route('/',methods=['GET'])
def health():
    """Service health check"""
    from modules.shadowsocks.service import SSConf
    from modules.health import CheckResult, Check, Component, ServiceHealth, HealthStatus, ComponentType

    def config_presented():
        result = CheckResult(
            check_name='file_presented',
            pass_status_is_required_for_service=True
        )
        try:
            result.status = HealthStatus.PASS()
            result.observed_value = len(SSConf.get_instance().ss_keys)
            result.observed_unit = 'Count of ss keys'
        except Exception as e:
            result.output = e
            result.status = HealthStatus.FAIL()
        return result

    auth_service_health = ServiceHealth(
        service_id=settings.SERVICE_ID,
        components=[
            Component(
                'config',
                ComponentType.SYSTEM,
                checks=[
                    Check('config', config_presented, pass_status_is_required_for_service=True)
                ]
            ),
        ],
        version=settings.VERSION,
        release_id=settings.RELEASE_ID,
        description=settings.DESCRIPTION
    )

    auth_service_health = auth_service_health.check()
    return jsonify(auth_service_health.serialize()), auth_service_health.status.http_code

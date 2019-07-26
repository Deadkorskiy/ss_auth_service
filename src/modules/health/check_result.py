from typing import Any
from . import HealthStatus


class CheckResult(object):

    def __init__(
        self,
        status: HealthStatus = None,
        observed_value: Any = '',
        observed_unit: str = '',
        output: str = '',
        check_name: str = None,
        pass_status_is_required_for_service: bool = True
    ):
        self.status = status
        self.observed_value = observed_value
        self.observed_unit = observed_unit
        self.output = output
        self.check_name = check_name or 'no_name'
        self.pass_status_is_required_for_service = pass_status_is_required_for_service

    def serialize(self) -> dict:
        return {
            'status': self.status.name,
            'observedValue': self.observed_value,
            'observedUnit': str(self.observed_unit),
            'output': str(self.output),
        }

    @classmethod
    def get_pass_result(cls) -> 'CheckResult':
        return cls(
            status=HealthStatus.PASS(),
            observed_value='',
            observed_unit='',
            output=''
        )

    @classmethod
    def get_fail_result(cls, error: Exception) -> 'CheckResult':
        return cls(
            status=HealthStatus.FAIL(),
            observed_value='',
            observed_unit='',
            output=str(error)
        )

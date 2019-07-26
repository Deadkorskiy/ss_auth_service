from . import timeout
from typing import Union, Any, Callable
from . import CheckResult


class Check(object):
    def __init__(
            self,
            check_name: str,
            check_func: Callable[[Any], Union[None, CheckResult]],
            check_func_args: tuple = None,
            check_func_kwargs: dict = None,
            timeout: int = 3,
            pass_status_is_required_for_service: bool = True,
            *args, **kwargs
    ):
        self.check_name = check_name
        self.check_func = check_func
        self.check_func_args = check_func_args or ()
        self.check_func_kwargs = check_func_kwargs or {}
        self.timeout = timeout
        self.pass_status_is_required_for_service = pass_status_is_required_for_service

    def check(self) -> CheckResult:
        try:
            result = timeout(
                self.check_func, self.check_func_args, self.check_func_kwargs, timeout=self.timeout
            )
            if isinstance(result, Exception):
                raise result
            if isinstance(result, CheckResult):
                result.pass_status_is_required_for_service = self.pass_status_is_required_for_service
                return result
            return CheckResult.get_pass_result()
        except Exception as e:
            result = CheckResult.get_fail_result(e)
            result.pass_status_is_required_for_service = self.pass_status_is_required_for_service
            return result

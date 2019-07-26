from typing import List, Union
from . import ComponentType
from . import CheckResult, Check


class Component(object):

    def __init__(
            self,
            name: str,
            component_type: Union[str, ComponentType],
            checks: List[Check],
            id: str = '',
            *args, **kwargs
    ):
        self.name = name
        self.checks = checks
        self.id = id
        self.__check_result = None
        if isinstance(type, ComponentType):
            self.component_type = component_type.component_type
        else:
            self.component_type = component_type

    def check(self) -> 'Component':
        result = []
        for check in self.checks:
            try:
                check_result = check.check()
                result.append(check_result)
            except Exception as e:
                result.append(CheckResult.get_fail_result(e))
        self.__check_result = result
        return self

    @property
    def result(self) -> List[CheckResult]:
        if self.__check_result:
            return self.__check_result
        self.check()
        return self.__check_result

    def serialize(self) -> List[dict]:
        serialized_result = []
        for row in self.result:
            s = row.serialize()
            s.update({
                'name': '{}:{}'.format(self.name, row.check_name),
                'componentId': self.id,
                'componentType': self.component_type
            })
            serialized_result.append(s)
        return serialized_result

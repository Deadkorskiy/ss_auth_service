from typing import List
from . import Component, HealthStatus


class ServiceHealth(object):

    def __init__(
            self,
            service_id: str,
            components: List[Component],
            version: str = '',
            release_id: str = '',
            description: str = '',
            notes: List[str] = None,
            *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.service_id = service_id
        self.version = version
        self.release_id = release_id
        self.description = description
        self.components = components
        self.notes = notes or ['']
        self.__checked_component = []
        self.__status = None

    def check(self) -> 'ServiceHealth':
        status = HealthStatus.PASS()
        self.__checked_component = []
        for component in self.components:
            component = component.check()
            self.__checked_component.append(component)
            for component_check in component.result:
                if all([
                    component_check.status.name == HealthStatus.FAIL().name,
                    not component_check.pass_status_is_required_for_service,
                    status.name != HealthStatus.FAIL().name
                ]):
                    status = HealthStatus.WARN()
                if all([
                    component_check.status.name == HealthStatus.FAIL().name,
                    component_check.pass_status_is_required_for_service,
                ]):
                    status = HealthStatus.FAIL()
        self.__status = status
        return self

    @property
    def status(self) -> HealthStatus:
        if self.__status is not None:
            return self.__status
        self.check()
        return self.__status

    def serialize(self) -> dict:
        if not self.__checked_component:
            self.check()

        return {
            'status': self.status.name,
            'version': self.version,
            'releaseId': self.release_id,
            'notes': self.notes,
            'output': '',
            'serviceId': self.service_id,
            'description': self.description,
            'checks': [x.serialize() for x in self.__checked_component],
        }

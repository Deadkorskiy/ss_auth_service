class ComponentType(object):

    COMPONENT = 'component'
    DATASTORE = 'datastore'
    SYSTEM = 'system'

    def __init__(self, component_type: str):
        if component_type not in [self.COMPONENT, self.DATASTORE, self.SYSTEM]:
            raise ValueError('Unknown component type "{}"'.format(component_type))
        self.component_type = component_type

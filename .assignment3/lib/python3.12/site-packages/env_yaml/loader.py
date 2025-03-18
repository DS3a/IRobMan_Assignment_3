import logging
import os
import re

import yaml

logger = logging.getLogger(__name__)

path_matcher = re.compile(r'\$\{(?P<env_name>[^}^{:]+)(?::(?P<default_value>[^}^{]*))?\}')


def path_constructor(loader, node):
    value = node.value
    match = path_matcher.match(value)
    new_value = os.getenv(match.group('env_name'), match.group('default_value'))
    logger.debug("Replacing %s, with %s", value, new_value)
    return new_value


class EnvLoader(yaml.SafeLoader):
    pass


EnvLoader.add_implicit_resolver('!env_substitute', path_matcher, None)
EnvLoader.add_constructor('!env_substitute', path_constructor)

from flask import Blueprint


def _factory(partial_module_string, url_prefix):
    name = partial_module_string
    import_name = 'services.{}'.format(partial_module_string)
    blueprint = Blueprint(name, import_name, url_prefix=url_prefix)
    return blueprint


common_blueprint_v1 = _factory('common.v1.api', url_prefix='/v1')

all_blueprints = (common_blueprint_v1, )
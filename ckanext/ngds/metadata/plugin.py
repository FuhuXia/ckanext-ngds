import ckanext.ngds.metadata.logic.action as action
import ckanext.ngds.metadata.logic.converters as converters
from ckanext.ngds.common import plugins as p

def create_protocol_codes():
    user = p.toolkit.get_action('get_site_user')({'ignore_auth': True}, {})
    context = {'user': user['name']}
    try:
        data = {'id': 'protocol_codes'}
        p.toolkit.get_action('vocabulary_show')(context, data)
    except p.toolkit.ObjectNotFound:
        data = {'name': 'protocol_codes'}
        vocab = p.toolkit.get_action('vocabulary_create')(context, data)
        for tag in ('OGC:WMS', 'OGC:WFS', 'OGC:WCS', 'OGC:CSW', 'OGC:SOS',
                    'OPeNDAP', 'ESRI', 'other'):
            data = {'name': tag, 'vocabulary_id': vocab['id']}
            p.toolkit.get_action('tag_create')(context, data)

def protocol_codes():
    create_protocol_codes()
    try:
        tag_list = p.toolkit.get_action('tag_list')
        protocol_codes = tag_list(data_dict={'vocabulary_id': 'protocol_codes'})
        return protocol_codes
    except p.toolkit.ObjectNotFound:
        return None

class MetadataPlugin(p.SingletonPlugin, p.toolkit.DefaultDatasetForm):

    p.implements(p.IConfigurer)
    p.implements(p.IActions)
    p.implements(p.IRoutes, inherit=True)
    p.implements(p.IDatasetForm)
    p.implements(p.ITemplateHelpers)

    # IConfigurer
    def update_config(self, config):
        templates = 'templates'
        public = 'public'
        p.toolkit.add_template_directory(config, templates)
        p.toolkit.add_public_directory(config, public)

    # IRoutes
    def before_map(self, map):
        controller = 'ckanext.ngds.metadata.controllers.view:ViewController'
        map.connect('metadata_iso_19139', '/metadata/iso-19139/{id}.xml',
                    controller=controller, action='show_iso_19139')
        return map

    # IActions
    def get_actions(self):
        return {
            'iso_19139': action.iso_19139,
        }

    # IDatasetForm
    def _modify_package_schema(self, schema):
        schema.update({
            'publication_date': [p.toolkit.get_converter('convert_to_extras')],
            'resource_id': [p.toolkit.get_validator('ignore_missing'),
                            p.toolkit.get_converter('convert_to_extras')],
            'authors': [p.toolkit.get_validator('ignore_missing'),
                        p.toolkit.get_converter('convert_to_extras')],
            'keywords': [p.toolkit.get_validator('ignore_missing'),
                         p.toolkit.get_converter('convert_to_extras')],
            'geographic_extent': [p.toolkit.get_validator('ignore_missing'),
                                  p.toolkit.get_converter('convert_to_extras')],
            'distributors': [p.toolkit.get_validator('ignore_missing'),
                             p.toolkit.get_converter('convert_to_extras')],
            'metadata_contact': [p.toolkit.get_validator('ignore_missing'),
                                 p.toolkit.get_converter('convert_to_extras')],
            'harvest_information': [p.toolkit.get_validator('ignore_missing'),
                                    p.toolkit.get_converter('convert_to_extras')]
        })

        schema['resources'].update({
            'url': [p.toolkit.get_validator('ignore_missing')],
            'distributor': [p.toolkit.get_validator('ignore_missing')],
            'service_type': [p.toolkit.get_validator('ignore_missing')],
            'layer': [p.toolkit.get_validator('ignore_missing')],
            'content_model_uri': [p.toolkit.get_validator('ignore_missing')],
            'content_model_version': [p.toolkit.get_validator('ignore_missing')]
        })

        return schema

    def create_package_schema(self):
        schema = super(MetadataPlugin, self).create_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def update_package_schema(self):
        schema = super(MetadataPlugin, self).update_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def show_package_schema(self):
        schema = super(MetadataPlugin, self).show_package_schema()
        schema['tags']['__extras'].append(p.toolkit.get_converter('free_tags_only'))
        schema.update({
            'publication_date': [p.toolkit.get_converter('convert_to_extras')],
            'resource_id': [p.toolkit.get_validator('ignore_missing'),
                            p.toolkit.get_converter('convert_from_extras')],
            'authors': [p.toolkit.get_validator('ignore_missing'),
                        p.toolkit.get_converter('convert_from_extras')],
            'keywords': [p.toolkit.get_validator('ignore_missing'),
                         p.toolkit.get_converter('convert_from_extras')],
            'geographic_extent': [p.toolkit.get_validator('ignore_missing'),
                                  p.toolkit.get_converter('convert_from_extras')],
            'distributors': [p.toolkit.get_validator('ignore_missing'),
                             p.toolkit.get_converter('convert_from_extras')],
            'metadata_contact': [p.toolkit.get_validator('ignore_missing'),
                                 p.toolkit.get_converter('convert_from_extras')],
            'harvest_information': [p.toolkit.get_validator('ignore_missing'),
                                    p.toolkit.get_converter('convert_from_extras')]
        })

        schema['resources'].update({
            'url': [p.toolkit.get_validator('ignore_missing')],
            'distributor': [p.toolkit.get_validator('ignore_missing')],
            'service_type': [p.toolkit.get_validator('ignore_missing')],
            'layer': [p.toolkit.get_validator('ignore_missing')],
            'content_model_uri': [p.toolkit.get_validator('ignore_missing')],
            'content_model_version': [p.toolkit.get_validator('ignore_missing')]
        })

        return schema

    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # packages not handled by any other IDatasetForm plugin
        return True

    def package_types(self):
        return []

    # ITemplateHelpers
    def get_helpers(self):
        return {'protocol_codes': protocol_codes}

# Copyright (c) 2016 VMware, Inc.
# All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import abc
import six

from neutron_lib import exceptions as nexception

from neutron._i18n import _
from neutron.api import extensions
from neutron.api.v2 import attributes as attr
from neutron.api.v2 import resource_helper
from neutron.plugins.common import constants as n_const
from neutron_lib.api import converters

ADDRESS_GROUP = 'address_group'
ADDRESS_GROUPS = ADDRESS_GROUP + 's'
CIDRS = 'cidrs'

RESOURCE_ATTRIBUTE_MAP = {
    ADDRESS_GROUPS: {
        'id': {'allow_post': False, 'allow_put': False,
               'validate': {'type:uuid': None},
               'is_visible': True,
               'primary_key': True},
        'name': {'allow_post': True, 'allow_put': True,
                 'validate': {'type:string': attr.NAME_MAX_LEN},
                 'is_visible': True, 'default': ''},
        'description': {'allow_post': True, 'allow_put': True,
                        'validate': {'type:string': attr.DESCRIPTION_MAX_LEN},
                        'is_visible': True, 'default': ''},
        'tenant_id': {'allow_post': True, 'allow_put': False,
                      'required_by_policy': True,
                      'validate': {'type:string': attr.TENANT_ID_MAX_LEN},
                      'is_visible': True},
        attr.SHARED: {'allow_post': True,
                      'allow_put': True,
                      'default': False,
                      'convert_to': converters.convert_to_boolean,
                      'is_visible': True,
                      'required_by_policy': True,
                      'enforce_policy': True},
        CIDRS: {'allow_post': True, 'allow_put': True,
                'validate': {'type:subnet_list': None},
                'convert_to': converters.convert_none_to_empty_list,
                'default': None, 'is_visible': True}
    }
}


class AddressGroupNotFound(nexception.NotFound):
    message = _("Address group %(address_group_id)s could not be found")


class AddressGroupContainsDuplicateCidrs(nexception.InvalidInput):
    message = _("Address group contains duplicate cidrs")


class AddressGroupUpdateError(nexception.BadRequest):
    message = _("Unable to update address group %(address_group_id)s : "
                "%(reason)s")


class AddressGroupInUse(nexception.InUse):
    message = _("Unable to complete operation on "
                "address group %(address_group_id)s. There are one or more "
                "objects that reference the address group")


class Address_group(extensions.ExtensionDescriptor):
    @classmethod
    def get_name(cls):
        return "address-group"

    @classmethod
    def get_alias(cls):
        return "address-group"

    @classmethod
    def get_description(cls):
        return "The address groups extension."

    @classmethod
    def get_updated(cls):
        return "2016-10-04T10:00:00-00:00"

    @classmethod
    def get_resources(cls):
        """Returns Ext Resources."""
        plural_mapping = resource_helper.build_plural_mappings(
            {}, RESOURCE_ATTRIBUTE_MAP)
        attr.PLURALS.update(plural_mapping)
        return resource_helper.build_resource_info(plural_mapping,
                                                   RESOURCE_ATTRIBUTE_MAP,
                                                   n_const.ADDRESS_GROUP,
                                                   register_quota=True,
                                                   translate_name=True)

    def update_attributes_map(self, attributes):
        super(Address_group, self).update_attributes_map(
            attributes, extension_attrs_map=RESOURCE_ATTRIBUTE_MAP)

    def get_extended_resources(self, version):
        if version == "2.0":
            return dict(list(RESOURCE_ATTRIBUTE_MAP.items()))
        else:
            return {}


@six.add_metaclass(abc.ABCMeta)
class AddressGroupPluginBase(object):

    @abc.abstractmethod
    def create_address_group(self, context, address_group):
        pass

    @abc.abstractmethod
    def update_address_group(self, context, id, address_group):
        pass

    @abc.abstractmethod
    def get_address_group(self, context, id, fields=None):
        pass

    @abc.abstractmethod
    def get_address_groups(self, context, filters=None, fields=None,
                           sorts=None, limit=None, marker=None,
                           page_reverse=False):
        pass

    @abc.abstractmethod
    def get_address_groups_count(self, context, filters=None):
        pass

    @abc.abstractmethod
    def delete_address_group(self, context, address_group):
        pass

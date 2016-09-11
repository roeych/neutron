# Copyright 2016 VMware, Inc.
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

from neutron.db import common_db_mixin
from neutron.plugins.common import constants as n_const
from neutron.services import service_base


class AddressGroupPlugin(service_base.ServicePluginBase,
                         common_db_mixin.CommonDbMixin):
    path_prefix = '/address-groups'

    supported_extension_aliases = ['address-group']

    __native_pagination_support = True
    __native_sorting_support = True

    def get_plugin_type(self):
        return n_const.ADDRESS_GROUP

    def get_plugin_description(self):
        # TODO(roeyc):
        return "TODO"

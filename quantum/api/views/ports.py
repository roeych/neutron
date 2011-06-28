# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2011 Citrix Systems
# All Rights Reserved.
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


def get_view_builder(req):
    base_url = req.application_url
    return ViewBuilder(base_url)


class ViewBuilder(object):

    def __init__(self, base_url):
        """
        :param base_url: url of the root wsgi application
        """
        self.base_url = base_url

    def build(self, port_data, is_detail=False):
        """Generic method used to generate a port entity."""
        if is_detail:
            port = self._build_detail(port_data)
        else:
            port = self._build_simple(port_data)
        return port

    def _build_simple(self, port_data):
        """Return a simple model of a server."""
        return dict(port=dict(id=port_data['port-id']))

    def _build_detail(self, port_data):
        """Return a simple model of a server."""
        return dict(port=dict(id=port_data['port-id'],
          attachment=port_data['attachment'],
          state=port_data['port-state']))

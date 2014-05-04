# vim: tabstop=4 shiftwidth=4 softtabstop=4
#    Copyright (c) 2012 - 2014 EMC Corporation
#    All Rights Reserved
#
#    Licensed under EMC Freeware Software License Agreement
#    You may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        https://github.com/emc-openstack/freeware-eula/
#        blob/master/Freeware_EULA_20131217_modified.md
#

"""
ISCSI Drivers for EMC VNX array based on CLI.

"""

from cinder.openstack.common import log as logging
from cinder.volume import driver
from cinder.volume.drivers.emc import emc_vnx_cli

LOG = logging.getLogger(__name__)


class EMCCLIISCSIDriver(driver.ISCSIDriver):
    """EMC ISCSI Drivers for VNX using CLI."""

    def __init__(self, *args, **kwargs):

        super(EMCCLIISCSIDriver, self).__init__(*args, **kwargs)
        self.cli = emc_vnx_cli.getEMCVnxCli(
            'iSCSI',
            configuration=self.configuration)

    def check_for_setup_error(self):
        pass

    def create_volume(self, volume):
        """Creates a EMC(VMAX/VNX) volume."""
        self.cli.create_volume(volume)

    def create_volume_from_snapshot(self, volume, snapshot):
        """Creates a volume from a snapshot."""
        self.cli.create_volume_from_snapshot(volume, snapshot)

    def create_cloned_volume(self, volume, src_vref):
        """Creates a cloned volume."""
        self.cli.create_cloned_volume(volume, src_vref)

    def extend_volume(self, volume, new_size):
        """Extend a volume."""
        self.cli.extend_volume(volume, new_size)

    def delete_volume(self, volume):
        """Deletes an EMC volume."""
        self.cli.delete_volume(volume)

    def migrate_volume(self, ctxt, volume, host):
        return self.cli.migrate_volume(ctxt, volume, host)

    def create_snapshot(self, snapshot):
        """Creates a snapshot."""
        self.cli.create_snapshot(snapshot)

    def delete_snapshot(self, snapshot):
        """Deletes a snapshot."""
        self.cli.delete_snapshot(snapshot)

    def ensure_export(self, context, volume):
        """Driver entry point to get the export info for an existing volume."""
        pass

    def create_export(self, context, volume):
        """Driver entry point to get the export info for a new volume."""
        self.cli.create_export(context, volume)

    def remove_export(self, context, volume):
        """Driver entry point to remove an export for a volume."""
        pass

    def check_for_export(self, context, volume_id):
        """Make sure volume is exported."""
        pass

    def initialize_connection(self, volume, connector):
        """Initializes the connection and returns connection info.

        The iscsi driver returns a driver_volume_type of 'iscsi'.
        the format of the driver data is defined in _get_iscsi_properties.
        Example return value::

            {
                'driver_volume_type': 'iscsi'
                'data': {
                    'target_discovered': True,
                    'target_iqn': 'iqn.2010-10.org.openstack:volume-00000001',
                    'target_portal': '127.0.0.0.1:3260',
                    'volume_id': 1,
                }
            }

        """
        return self.cli.initialize_connection(volume, connector)

    def terminate_connection(self, volume, connector, **kwargs):
        """Disallow connection from connector."""
        self.cli.terminate_connection(volume, connector)

    def get_volume_stats(self, refresh=False):
        """Get volume status.

        If 'refresh' is True, run update the stats first.
        """
        if refresh:
            self.update_volume_status()

        return self._stats

    def update_volume_status(self):
        """Retrieve status info from volume group."""
        LOG.debug(_("Updating volume status"))
        #retrieving the volume update from the VNX
        data = self.cli.update_volume_status()

        backend_name = self.configuration.safe_get('volume_backend_name')
        data['volume_backend_name'] = backend_name or 'EMCCLIISCSIDriver'
        data['storage_protocol'] = 'iSCSI'

        self._stats = data

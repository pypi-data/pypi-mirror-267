# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs

__all__ = [
    'GetPrivateCloudResult',
    'AwaitableGetPrivateCloudResult',
    'get_private_cloud',
    'get_private_cloud_output',
]

@pulumi.output_type
class GetPrivateCloudResult:
    """
    A collection of values returned by getPrivateCloud.
    """
    def __init__(__self__, description=None, hcxes=None, id=None, location=None, management_clusters=None, name=None, network_configs=None, nsxes=None, project=None, state=None, type=None, uid=None, vcenters=None):
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if hcxes and not isinstance(hcxes, list):
            raise TypeError("Expected argument 'hcxes' to be a list")
        pulumi.set(__self__, "hcxes", hcxes)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if management_clusters and not isinstance(management_clusters, list):
            raise TypeError("Expected argument 'management_clusters' to be a list")
        pulumi.set(__self__, "management_clusters", management_clusters)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if network_configs and not isinstance(network_configs, list):
            raise TypeError("Expected argument 'network_configs' to be a list")
        pulumi.set(__self__, "network_configs", network_configs)
        if nsxes and not isinstance(nsxes, list):
            raise TypeError("Expected argument 'nsxes' to be a list")
        pulumi.set(__self__, "nsxes", nsxes)
        if project and not isinstance(project, str):
            raise TypeError("Expected argument 'project' to be a str")
        pulumi.set(__self__, "project", project)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if uid and not isinstance(uid, str):
            raise TypeError("Expected argument 'uid' to be a str")
        pulumi.set(__self__, "uid", uid)
        if vcenters and not isinstance(vcenters, list):
            raise TypeError("Expected argument 'vcenters' to be a list")
        pulumi.set(__self__, "vcenters", vcenters)

    @property
    @pulumi.getter
    def description(self) -> str:
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def hcxes(self) -> Sequence['outputs.GetPrivateCloudHcxResult']:
        return pulumi.get(self, "hcxes")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> str:
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="managementClusters")
    def management_clusters(self) -> Sequence['outputs.GetPrivateCloudManagementClusterResult']:
        return pulumi.get(self, "management_clusters")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="networkConfigs")
    def network_configs(self) -> Sequence['outputs.GetPrivateCloudNetworkConfigResult']:
        return pulumi.get(self, "network_configs")

    @property
    @pulumi.getter
    def nsxes(self) -> Sequence['outputs.GetPrivateCloudNsxResult']:
        return pulumi.get(self, "nsxes")

    @property
    @pulumi.getter
    def project(self) -> Optional[str]:
        return pulumi.get(self, "project")

    @property
    @pulumi.getter
    def state(self) -> str:
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def type(self) -> str:
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def uid(self) -> str:
        return pulumi.get(self, "uid")

    @property
    @pulumi.getter
    def vcenters(self) -> Sequence['outputs.GetPrivateCloudVcenterResult']:
        return pulumi.get(self, "vcenters")


class AwaitableGetPrivateCloudResult(GetPrivateCloudResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetPrivateCloudResult(
            description=self.description,
            hcxes=self.hcxes,
            id=self.id,
            location=self.location,
            management_clusters=self.management_clusters,
            name=self.name,
            network_configs=self.network_configs,
            nsxes=self.nsxes,
            project=self.project,
            state=self.state,
            type=self.type,
            uid=self.uid,
            vcenters=self.vcenters)


def get_private_cloud(location: Optional[str] = None,
                      name: Optional[str] = None,
                      project: Optional[str] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetPrivateCloudResult:
    """
    Use this data source to get details about a private cloud resource.

    To get more information about private cloud, see:
    * [API documentation](https://cloud.google.com/vmware-engine/docs/reference/rest/v1/projects.locations.privateClouds)

    ## Example Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_gcp as gcp

    my_pc = gcp.vmwareengine.get_private_cloud(name="my-pc",
        location="us-central1-a")
    ```
    <!--End PulumiCodeChooser -->


    :param str location: Location of the resource.
           
           - - -
    :param str name: Name of the resource.
    :param str project: The ID of the project in which the resource belongs. If it
           is not provided, the provider project is used.
    """
    __args__ = dict()
    __args__['location'] = location
    __args__['name'] = name
    __args__['project'] = project
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('gcp:vmwareengine/getPrivateCloud:getPrivateCloud', __args__, opts=opts, typ=GetPrivateCloudResult).value

    return AwaitableGetPrivateCloudResult(
        description=pulumi.get(__ret__, 'description'),
        hcxes=pulumi.get(__ret__, 'hcxes'),
        id=pulumi.get(__ret__, 'id'),
        location=pulumi.get(__ret__, 'location'),
        management_clusters=pulumi.get(__ret__, 'management_clusters'),
        name=pulumi.get(__ret__, 'name'),
        network_configs=pulumi.get(__ret__, 'network_configs'),
        nsxes=pulumi.get(__ret__, 'nsxes'),
        project=pulumi.get(__ret__, 'project'),
        state=pulumi.get(__ret__, 'state'),
        type=pulumi.get(__ret__, 'type'),
        uid=pulumi.get(__ret__, 'uid'),
        vcenters=pulumi.get(__ret__, 'vcenters'))


@_utilities.lift_output_func(get_private_cloud)
def get_private_cloud_output(location: Optional[pulumi.Input[str]] = None,
                             name: Optional[pulumi.Input[str]] = None,
                             project: Optional[pulumi.Input[Optional[str]]] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetPrivateCloudResult]:
    """
    Use this data source to get details about a private cloud resource.

    To get more information about private cloud, see:
    * [API documentation](https://cloud.google.com/vmware-engine/docs/reference/rest/v1/projects.locations.privateClouds)

    ## Example Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_gcp as gcp

    my_pc = gcp.vmwareengine.get_private_cloud(name="my-pc",
        location="us-central1-a")
    ```
    <!--End PulumiCodeChooser -->


    :param str location: Location of the resource.
           
           - - -
    :param str name: Name of the resource.
    :param str project: The ID of the project in which the resource belongs. If it
           is not provided, the provider project is used.
    """
    ...

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
    'GetHcVpnGatewayResult',
    'AwaitableGetHcVpnGatewayResult',
    'get_hc_vpn_gateway',
    'get_hc_vpn_gateway_output',
]

@pulumi.output_type
class GetHcVpnGatewayResult:
    """
    A collection of values returned by getHcVpnGateway.
    """
    def __init__(__self__, description=None, id=None, name=None, network=None, project=None, region=None, self_link=None, stack_type=None, vpn_interfaces=None):
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if network and not isinstance(network, str):
            raise TypeError("Expected argument 'network' to be a str")
        pulumi.set(__self__, "network", network)
        if project and not isinstance(project, str):
            raise TypeError("Expected argument 'project' to be a str")
        pulumi.set(__self__, "project", project)
        if region and not isinstance(region, str):
            raise TypeError("Expected argument 'region' to be a str")
        pulumi.set(__self__, "region", region)
        if self_link and not isinstance(self_link, str):
            raise TypeError("Expected argument 'self_link' to be a str")
        pulumi.set(__self__, "self_link", self_link)
        if stack_type and not isinstance(stack_type, str):
            raise TypeError("Expected argument 'stack_type' to be a str")
        pulumi.set(__self__, "stack_type", stack_type)
        if vpn_interfaces and not isinstance(vpn_interfaces, list):
            raise TypeError("Expected argument 'vpn_interfaces' to be a list")
        pulumi.set(__self__, "vpn_interfaces", vpn_interfaces)

    @property
    @pulumi.getter
    def description(self) -> str:
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def network(self) -> str:
        return pulumi.get(self, "network")

    @property
    @pulumi.getter
    def project(self) -> Optional[str]:
        return pulumi.get(self, "project")

    @property
    @pulumi.getter
    def region(self) -> Optional[str]:
        return pulumi.get(self, "region")

    @property
    @pulumi.getter(name="selfLink")
    def self_link(self) -> str:
        return pulumi.get(self, "self_link")

    @property
    @pulumi.getter(name="stackType")
    def stack_type(self) -> str:
        return pulumi.get(self, "stack_type")

    @property
    @pulumi.getter(name="vpnInterfaces")
    def vpn_interfaces(self) -> Sequence['outputs.GetHcVpnGatewayVpnInterfaceResult']:
        return pulumi.get(self, "vpn_interfaces")


class AwaitableGetHcVpnGatewayResult(GetHcVpnGatewayResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetHcVpnGatewayResult(
            description=self.description,
            id=self.id,
            name=self.name,
            network=self.network,
            project=self.project,
            region=self.region,
            self_link=self.self_link,
            stack_type=self.stack_type,
            vpn_interfaces=self.vpn_interfaces)


def get_hc_vpn_gateway(name: Optional[str] = None,
                       project: Optional[str] = None,
                       region: Optional[str] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetHcVpnGatewayResult:
    """
    Get a HA VPN Gateway within GCE from its name.

    ## Example Usage


    :param str name: The name of the forwarding rule.
           
           
           - - -
    :param str project: The project in which the resource belongs. If it
           is not provided, the provider project is used.
    :param str region: The region in which the resource belongs. If it
           is not provided, the project region is used.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['project'] = project
    __args__['region'] = region
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('gcp:compute/getHcVpnGateway:getHcVpnGateway', __args__, opts=opts, typ=GetHcVpnGatewayResult).value

    return AwaitableGetHcVpnGatewayResult(
        description=pulumi.get(__ret__, 'description'),
        id=pulumi.get(__ret__, 'id'),
        name=pulumi.get(__ret__, 'name'),
        network=pulumi.get(__ret__, 'network'),
        project=pulumi.get(__ret__, 'project'),
        region=pulumi.get(__ret__, 'region'),
        self_link=pulumi.get(__ret__, 'self_link'),
        stack_type=pulumi.get(__ret__, 'stack_type'),
        vpn_interfaces=pulumi.get(__ret__, 'vpn_interfaces'))


@_utilities.lift_output_func(get_hc_vpn_gateway)
def get_hc_vpn_gateway_output(name: Optional[pulumi.Input[str]] = None,
                              project: Optional[pulumi.Input[Optional[str]]] = None,
                              region: Optional[pulumi.Input[Optional[str]]] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetHcVpnGatewayResult]:
    """
    Get a HA VPN Gateway within GCE from its name.

    ## Example Usage


    :param str name: The name of the forwarding rule.
           
           
           - - -
    :param str project: The project in which the resource belongs. If it
           is not provided, the provider project is used.
    :param str region: The region in which the resource belongs. If it
           is not provided, the project region is used.
    """
    ...

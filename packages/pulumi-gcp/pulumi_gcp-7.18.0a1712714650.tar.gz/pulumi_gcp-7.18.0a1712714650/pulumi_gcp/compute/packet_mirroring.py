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
from ._inputs import *

__all__ = ['PacketMirroringArgs', 'PacketMirroring']

@pulumi.input_type
class PacketMirroringArgs:
    def __init__(__self__, *,
                 collector_ilb: pulumi.Input['PacketMirroringCollectorIlbArgs'],
                 mirrored_resources: pulumi.Input['PacketMirroringMirroredResourcesArgs'],
                 network: pulumi.Input['PacketMirroringNetworkArgs'],
                 description: Optional[pulumi.Input[str]] = None,
                 filter: Optional[pulumi.Input['PacketMirroringFilterArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 priority: Optional[pulumi.Input[int]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a PacketMirroring resource.
        :param pulumi.Input['PacketMirroringCollectorIlbArgs'] collector_ilb: The Forwarding Rule resource (of type load_balancing_scheme=INTERNAL)
               that will be used as collector for mirrored traffic. The
               specified forwarding rule must have is_mirroring_collector
               set to true.
               Structure is documented below.
        :param pulumi.Input['PacketMirroringMirroredResourcesArgs'] mirrored_resources: A means of specifying which resources to mirror.
               Structure is documented below.
        :param pulumi.Input['PacketMirroringNetworkArgs'] network: Specifies the mirrored VPC network. Only packets in this network
               will be mirrored. All mirrored VMs should have a NIC in the given
               network. All mirrored subnetworks should belong to the given network.
               Structure is documented below.
        :param pulumi.Input[str] description: A human-readable description of the rule.
        :param pulumi.Input['PacketMirroringFilterArgs'] filter: A filter for mirrored traffic.  If unset, all traffic is mirrored.
               Structure is documented below.
        :param pulumi.Input[str] name: The name of the packet mirroring rule
        :param pulumi.Input[int] priority: Since only one rule can be active at a time, priority is
               used to break ties in the case of two rules that apply to
               the same instances.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] region: The Region in which the created address should reside.
               If it is not provided, the provider region is used.
        """
        pulumi.set(__self__, "collector_ilb", collector_ilb)
        pulumi.set(__self__, "mirrored_resources", mirrored_resources)
        pulumi.set(__self__, "network", network)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if filter is not None:
            pulumi.set(__self__, "filter", filter)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if priority is not None:
            pulumi.set(__self__, "priority", priority)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if region is not None:
            pulumi.set(__self__, "region", region)

    @property
    @pulumi.getter(name="collectorIlb")
    def collector_ilb(self) -> pulumi.Input['PacketMirroringCollectorIlbArgs']:
        """
        The Forwarding Rule resource (of type load_balancing_scheme=INTERNAL)
        that will be used as collector for mirrored traffic. The
        specified forwarding rule must have is_mirroring_collector
        set to true.
        Structure is documented below.
        """
        return pulumi.get(self, "collector_ilb")

    @collector_ilb.setter
    def collector_ilb(self, value: pulumi.Input['PacketMirroringCollectorIlbArgs']):
        pulumi.set(self, "collector_ilb", value)

    @property
    @pulumi.getter(name="mirroredResources")
    def mirrored_resources(self) -> pulumi.Input['PacketMirroringMirroredResourcesArgs']:
        """
        A means of specifying which resources to mirror.
        Structure is documented below.
        """
        return pulumi.get(self, "mirrored_resources")

    @mirrored_resources.setter
    def mirrored_resources(self, value: pulumi.Input['PacketMirroringMirroredResourcesArgs']):
        pulumi.set(self, "mirrored_resources", value)

    @property
    @pulumi.getter
    def network(self) -> pulumi.Input['PacketMirroringNetworkArgs']:
        """
        Specifies the mirrored VPC network. Only packets in this network
        will be mirrored. All mirrored VMs should have a NIC in the given
        network. All mirrored subnetworks should belong to the given network.
        Structure is documented below.
        """
        return pulumi.get(self, "network")

    @network.setter
    def network(self, value: pulumi.Input['PacketMirroringNetworkArgs']):
        pulumi.set(self, "network", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A human-readable description of the rule.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def filter(self) -> Optional[pulumi.Input['PacketMirroringFilterArgs']]:
        """
        A filter for mirrored traffic.  If unset, all traffic is mirrored.
        Structure is documented below.
        """
        return pulumi.get(self, "filter")

    @filter.setter
    def filter(self, value: Optional[pulumi.Input['PacketMirroringFilterArgs']]):
        pulumi.set(self, "filter", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the packet mirroring rule
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def priority(self) -> Optional[pulumi.Input[int]]:
        """
        Since only one rule can be active at a time, priority is
        used to break ties in the case of two rules that apply to
        the same instances.
        """
        return pulumi.get(self, "priority")

    @priority.setter
    def priority(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "priority", value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the project in which the resource belongs.
        If it is not provided, the provider project is used.
        """
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)

    @property
    @pulumi.getter
    def region(self) -> Optional[pulumi.Input[str]]:
        """
        The Region in which the created address should reside.
        If it is not provided, the provider region is used.
        """
        return pulumi.get(self, "region")

    @region.setter
    def region(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "region", value)


@pulumi.input_type
class _PacketMirroringState:
    def __init__(__self__, *,
                 collector_ilb: Optional[pulumi.Input['PacketMirroringCollectorIlbArgs']] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 filter: Optional[pulumi.Input['PacketMirroringFilterArgs']] = None,
                 mirrored_resources: Optional[pulumi.Input['PacketMirroringMirroredResourcesArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network: Optional[pulumi.Input['PacketMirroringNetworkArgs']] = None,
                 priority: Optional[pulumi.Input[int]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering PacketMirroring resources.
        :param pulumi.Input['PacketMirroringCollectorIlbArgs'] collector_ilb: The Forwarding Rule resource (of type load_balancing_scheme=INTERNAL)
               that will be used as collector for mirrored traffic. The
               specified forwarding rule must have is_mirroring_collector
               set to true.
               Structure is documented below.
        :param pulumi.Input[str] description: A human-readable description of the rule.
        :param pulumi.Input['PacketMirroringFilterArgs'] filter: A filter for mirrored traffic.  If unset, all traffic is mirrored.
               Structure is documented below.
        :param pulumi.Input['PacketMirroringMirroredResourcesArgs'] mirrored_resources: A means of specifying which resources to mirror.
               Structure is documented below.
        :param pulumi.Input[str] name: The name of the packet mirroring rule
        :param pulumi.Input['PacketMirroringNetworkArgs'] network: Specifies the mirrored VPC network. Only packets in this network
               will be mirrored. All mirrored VMs should have a NIC in the given
               network. All mirrored subnetworks should belong to the given network.
               Structure is documented below.
        :param pulumi.Input[int] priority: Since only one rule can be active at a time, priority is
               used to break ties in the case of two rules that apply to
               the same instances.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] region: The Region in which the created address should reside.
               If it is not provided, the provider region is used.
        """
        if collector_ilb is not None:
            pulumi.set(__self__, "collector_ilb", collector_ilb)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if filter is not None:
            pulumi.set(__self__, "filter", filter)
        if mirrored_resources is not None:
            pulumi.set(__self__, "mirrored_resources", mirrored_resources)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if network is not None:
            pulumi.set(__self__, "network", network)
        if priority is not None:
            pulumi.set(__self__, "priority", priority)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if region is not None:
            pulumi.set(__self__, "region", region)

    @property
    @pulumi.getter(name="collectorIlb")
    def collector_ilb(self) -> Optional[pulumi.Input['PacketMirroringCollectorIlbArgs']]:
        """
        The Forwarding Rule resource (of type load_balancing_scheme=INTERNAL)
        that will be used as collector for mirrored traffic. The
        specified forwarding rule must have is_mirroring_collector
        set to true.
        Structure is documented below.
        """
        return pulumi.get(self, "collector_ilb")

    @collector_ilb.setter
    def collector_ilb(self, value: Optional[pulumi.Input['PacketMirroringCollectorIlbArgs']]):
        pulumi.set(self, "collector_ilb", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A human-readable description of the rule.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def filter(self) -> Optional[pulumi.Input['PacketMirroringFilterArgs']]:
        """
        A filter for mirrored traffic.  If unset, all traffic is mirrored.
        Structure is documented below.
        """
        return pulumi.get(self, "filter")

    @filter.setter
    def filter(self, value: Optional[pulumi.Input['PacketMirroringFilterArgs']]):
        pulumi.set(self, "filter", value)

    @property
    @pulumi.getter(name="mirroredResources")
    def mirrored_resources(self) -> Optional[pulumi.Input['PacketMirroringMirroredResourcesArgs']]:
        """
        A means of specifying which resources to mirror.
        Structure is documented below.
        """
        return pulumi.get(self, "mirrored_resources")

    @mirrored_resources.setter
    def mirrored_resources(self, value: Optional[pulumi.Input['PacketMirroringMirroredResourcesArgs']]):
        pulumi.set(self, "mirrored_resources", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the packet mirroring rule
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def network(self) -> Optional[pulumi.Input['PacketMirroringNetworkArgs']]:
        """
        Specifies the mirrored VPC network. Only packets in this network
        will be mirrored. All mirrored VMs should have a NIC in the given
        network. All mirrored subnetworks should belong to the given network.
        Structure is documented below.
        """
        return pulumi.get(self, "network")

    @network.setter
    def network(self, value: Optional[pulumi.Input['PacketMirroringNetworkArgs']]):
        pulumi.set(self, "network", value)

    @property
    @pulumi.getter
    def priority(self) -> Optional[pulumi.Input[int]]:
        """
        Since only one rule can be active at a time, priority is
        used to break ties in the case of two rules that apply to
        the same instances.
        """
        return pulumi.get(self, "priority")

    @priority.setter
    def priority(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "priority", value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the project in which the resource belongs.
        If it is not provided, the provider project is used.
        """
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)

    @property
    @pulumi.getter
    def region(self) -> Optional[pulumi.Input[str]]:
        """
        The Region in which the created address should reside.
        If it is not provided, the provider region is used.
        """
        return pulumi.get(self, "region")

    @region.setter
    def region(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "region", value)


class PacketMirroring(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 collector_ilb: Optional[pulumi.Input[pulumi.InputType['PacketMirroringCollectorIlbArgs']]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 filter: Optional[pulumi.Input[pulumi.InputType['PacketMirroringFilterArgs']]] = None,
                 mirrored_resources: Optional[pulumi.Input[pulumi.InputType['PacketMirroringMirroredResourcesArgs']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network: Optional[pulumi.Input[pulumi.InputType['PacketMirroringNetworkArgs']]] = None,
                 priority: Optional[pulumi.Input[int]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Packet Mirroring mirrors traffic to and from particular VM instances.
        You can use the collected traffic to help you detect security threats
        and monitor application performance.

        To get more information about PacketMirroring, see:

        * [API documentation](https://cloud.google.com/compute/docs/reference/rest/v1/packetMirrorings)
        * How-to Guides
            * [Using Packet Mirroring](https://cloud.google.com/vpc/docs/using-packet-mirroring#creating)

        ## Example Usage

        ### Compute Packet Mirroring Full

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        default = gcp.compute.Network("default", name="my-network")
        mirror = gcp.compute.Instance("mirror",
            network_interfaces=[gcp.compute.InstanceNetworkInterfaceArgs(
                access_configs=[gcp.compute.InstanceNetworkInterfaceAccessConfigArgs()],
                network=default.id,
            )],
            name="my-instance",
            machine_type="e2-medium",
            boot_disk=gcp.compute.InstanceBootDiskArgs(
                initialize_params=gcp.compute.InstanceBootDiskInitializeParamsArgs(
                    image="debian-cloud/debian-11",
                ),
            ))
        default_subnetwork = gcp.compute.Subnetwork("default",
            name="my-subnetwork",
            network=default.id,
            ip_cidr_range="10.2.0.0/16")
        default_health_check = gcp.compute.HealthCheck("default",
            name="my-healthcheck",
            check_interval_sec=1,
            timeout_sec=1,
            tcp_health_check=gcp.compute.HealthCheckTcpHealthCheckArgs(
                port=80,
            ))
        default_region_backend_service = gcp.compute.RegionBackendService("default",
            name="my-service",
            health_checks=default_health_check.id)
        default_forwarding_rule = gcp.compute.ForwardingRule("default",
            name="my-ilb",
            is_mirroring_collector=True,
            ip_protocol="TCP",
            load_balancing_scheme="INTERNAL",
            backend_service=default_region_backend_service.id,
            all_ports=True,
            network=default.id,
            subnetwork=default_subnetwork.id,
            network_tier="PREMIUM")
        foobar = gcp.compute.PacketMirroring("foobar",
            name="my-mirroring",
            description="bar",
            network=gcp.compute.PacketMirroringNetworkArgs(
                url=default.id,
            ),
            collector_ilb=gcp.compute.PacketMirroringCollectorIlbArgs(
                url=default_forwarding_rule.id,
            ),
            mirrored_resources=gcp.compute.PacketMirroringMirroredResourcesArgs(
                tags=["foo"],
                instances=[gcp.compute.PacketMirroringMirroredResourcesInstanceArgs(
                    url=mirror.id,
                )],
            ),
            filter=gcp.compute.PacketMirroringFilterArgs(
                ip_protocols=["tcp"],
                cidr_ranges=["0.0.0.0/0"],
                direction="BOTH",
            ))
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        PacketMirroring can be imported using any of these accepted formats:

        * `projects/{{project}}/regions/{{region}}/packetMirrorings/{{name}}`

        * `{{project}}/{{region}}/{{name}}`

        * `{{region}}/{{name}}`

        * `{{name}}`

        When using the `pulumi import` command, PacketMirroring can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:compute/packetMirroring:PacketMirroring default projects/{{project}}/regions/{{region}}/packetMirrorings/{{name}}
        ```

        ```sh
        $ pulumi import gcp:compute/packetMirroring:PacketMirroring default {{project}}/{{region}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:compute/packetMirroring:PacketMirroring default {{region}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:compute/packetMirroring:PacketMirroring default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['PacketMirroringCollectorIlbArgs']] collector_ilb: The Forwarding Rule resource (of type load_balancing_scheme=INTERNAL)
               that will be used as collector for mirrored traffic. The
               specified forwarding rule must have is_mirroring_collector
               set to true.
               Structure is documented below.
        :param pulumi.Input[str] description: A human-readable description of the rule.
        :param pulumi.Input[pulumi.InputType['PacketMirroringFilterArgs']] filter: A filter for mirrored traffic.  If unset, all traffic is mirrored.
               Structure is documented below.
        :param pulumi.Input[pulumi.InputType['PacketMirroringMirroredResourcesArgs']] mirrored_resources: A means of specifying which resources to mirror.
               Structure is documented below.
        :param pulumi.Input[str] name: The name of the packet mirroring rule
        :param pulumi.Input[pulumi.InputType['PacketMirroringNetworkArgs']] network: Specifies the mirrored VPC network. Only packets in this network
               will be mirrored. All mirrored VMs should have a NIC in the given
               network. All mirrored subnetworks should belong to the given network.
               Structure is documented below.
        :param pulumi.Input[int] priority: Since only one rule can be active at a time, priority is
               used to break ties in the case of two rules that apply to
               the same instances.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] region: The Region in which the created address should reside.
               If it is not provided, the provider region is used.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: PacketMirroringArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Packet Mirroring mirrors traffic to and from particular VM instances.
        You can use the collected traffic to help you detect security threats
        and monitor application performance.

        To get more information about PacketMirroring, see:

        * [API documentation](https://cloud.google.com/compute/docs/reference/rest/v1/packetMirrorings)
        * How-to Guides
            * [Using Packet Mirroring](https://cloud.google.com/vpc/docs/using-packet-mirroring#creating)

        ## Example Usage

        ### Compute Packet Mirroring Full

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        default = gcp.compute.Network("default", name="my-network")
        mirror = gcp.compute.Instance("mirror",
            network_interfaces=[gcp.compute.InstanceNetworkInterfaceArgs(
                access_configs=[gcp.compute.InstanceNetworkInterfaceAccessConfigArgs()],
                network=default.id,
            )],
            name="my-instance",
            machine_type="e2-medium",
            boot_disk=gcp.compute.InstanceBootDiskArgs(
                initialize_params=gcp.compute.InstanceBootDiskInitializeParamsArgs(
                    image="debian-cloud/debian-11",
                ),
            ))
        default_subnetwork = gcp.compute.Subnetwork("default",
            name="my-subnetwork",
            network=default.id,
            ip_cidr_range="10.2.0.0/16")
        default_health_check = gcp.compute.HealthCheck("default",
            name="my-healthcheck",
            check_interval_sec=1,
            timeout_sec=1,
            tcp_health_check=gcp.compute.HealthCheckTcpHealthCheckArgs(
                port=80,
            ))
        default_region_backend_service = gcp.compute.RegionBackendService("default",
            name="my-service",
            health_checks=default_health_check.id)
        default_forwarding_rule = gcp.compute.ForwardingRule("default",
            name="my-ilb",
            is_mirroring_collector=True,
            ip_protocol="TCP",
            load_balancing_scheme="INTERNAL",
            backend_service=default_region_backend_service.id,
            all_ports=True,
            network=default.id,
            subnetwork=default_subnetwork.id,
            network_tier="PREMIUM")
        foobar = gcp.compute.PacketMirroring("foobar",
            name="my-mirroring",
            description="bar",
            network=gcp.compute.PacketMirroringNetworkArgs(
                url=default.id,
            ),
            collector_ilb=gcp.compute.PacketMirroringCollectorIlbArgs(
                url=default_forwarding_rule.id,
            ),
            mirrored_resources=gcp.compute.PacketMirroringMirroredResourcesArgs(
                tags=["foo"],
                instances=[gcp.compute.PacketMirroringMirroredResourcesInstanceArgs(
                    url=mirror.id,
                )],
            ),
            filter=gcp.compute.PacketMirroringFilterArgs(
                ip_protocols=["tcp"],
                cidr_ranges=["0.0.0.0/0"],
                direction="BOTH",
            ))
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        PacketMirroring can be imported using any of these accepted formats:

        * `projects/{{project}}/regions/{{region}}/packetMirrorings/{{name}}`

        * `{{project}}/{{region}}/{{name}}`

        * `{{region}}/{{name}}`

        * `{{name}}`

        When using the `pulumi import` command, PacketMirroring can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:compute/packetMirroring:PacketMirroring default projects/{{project}}/regions/{{region}}/packetMirrorings/{{name}}
        ```

        ```sh
        $ pulumi import gcp:compute/packetMirroring:PacketMirroring default {{project}}/{{region}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:compute/packetMirroring:PacketMirroring default {{region}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:compute/packetMirroring:PacketMirroring default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param PacketMirroringArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(PacketMirroringArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 collector_ilb: Optional[pulumi.Input[pulumi.InputType['PacketMirroringCollectorIlbArgs']]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 filter: Optional[pulumi.Input[pulumi.InputType['PacketMirroringFilterArgs']]] = None,
                 mirrored_resources: Optional[pulumi.Input[pulumi.InputType['PacketMirroringMirroredResourcesArgs']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network: Optional[pulumi.Input[pulumi.InputType['PacketMirroringNetworkArgs']]] = None,
                 priority: Optional[pulumi.Input[int]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = PacketMirroringArgs.__new__(PacketMirroringArgs)

            if collector_ilb is None and not opts.urn:
                raise TypeError("Missing required property 'collector_ilb'")
            __props__.__dict__["collector_ilb"] = collector_ilb
            __props__.__dict__["description"] = description
            __props__.__dict__["filter"] = filter
            if mirrored_resources is None and not opts.urn:
                raise TypeError("Missing required property 'mirrored_resources'")
            __props__.__dict__["mirrored_resources"] = mirrored_resources
            __props__.__dict__["name"] = name
            if network is None and not opts.urn:
                raise TypeError("Missing required property 'network'")
            __props__.__dict__["network"] = network
            __props__.__dict__["priority"] = priority
            __props__.__dict__["project"] = project
            __props__.__dict__["region"] = region
        super(PacketMirroring, __self__).__init__(
            'gcp:compute/packetMirroring:PacketMirroring',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            collector_ilb: Optional[pulumi.Input[pulumi.InputType['PacketMirroringCollectorIlbArgs']]] = None,
            description: Optional[pulumi.Input[str]] = None,
            filter: Optional[pulumi.Input[pulumi.InputType['PacketMirroringFilterArgs']]] = None,
            mirrored_resources: Optional[pulumi.Input[pulumi.InputType['PacketMirroringMirroredResourcesArgs']]] = None,
            name: Optional[pulumi.Input[str]] = None,
            network: Optional[pulumi.Input[pulumi.InputType['PacketMirroringNetworkArgs']]] = None,
            priority: Optional[pulumi.Input[int]] = None,
            project: Optional[pulumi.Input[str]] = None,
            region: Optional[pulumi.Input[str]] = None) -> 'PacketMirroring':
        """
        Get an existing PacketMirroring resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['PacketMirroringCollectorIlbArgs']] collector_ilb: The Forwarding Rule resource (of type load_balancing_scheme=INTERNAL)
               that will be used as collector for mirrored traffic. The
               specified forwarding rule must have is_mirroring_collector
               set to true.
               Structure is documented below.
        :param pulumi.Input[str] description: A human-readable description of the rule.
        :param pulumi.Input[pulumi.InputType['PacketMirroringFilterArgs']] filter: A filter for mirrored traffic.  If unset, all traffic is mirrored.
               Structure is documented below.
        :param pulumi.Input[pulumi.InputType['PacketMirroringMirroredResourcesArgs']] mirrored_resources: A means of specifying which resources to mirror.
               Structure is documented below.
        :param pulumi.Input[str] name: The name of the packet mirroring rule
        :param pulumi.Input[pulumi.InputType['PacketMirroringNetworkArgs']] network: Specifies the mirrored VPC network. Only packets in this network
               will be mirrored. All mirrored VMs should have a NIC in the given
               network. All mirrored subnetworks should belong to the given network.
               Structure is documented below.
        :param pulumi.Input[int] priority: Since only one rule can be active at a time, priority is
               used to break ties in the case of two rules that apply to
               the same instances.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] region: The Region in which the created address should reside.
               If it is not provided, the provider region is used.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _PacketMirroringState.__new__(_PacketMirroringState)

        __props__.__dict__["collector_ilb"] = collector_ilb
        __props__.__dict__["description"] = description
        __props__.__dict__["filter"] = filter
        __props__.__dict__["mirrored_resources"] = mirrored_resources
        __props__.__dict__["name"] = name
        __props__.__dict__["network"] = network
        __props__.__dict__["priority"] = priority
        __props__.__dict__["project"] = project
        __props__.__dict__["region"] = region
        return PacketMirroring(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="collectorIlb")
    def collector_ilb(self) -> pulumi.Output['outputs.PacketMirroringCollectorIlb']:
        """
        The Forwarding Rule resource (of type load_balancing_scheme=INTERNAL)
        that will be used as collector for mirrored traffic. The
        specified forwarding rule must have is_mirroring_collector
        set to true.
        Structure is documented below.
        """
        return pulumi.get(self, "collector_ilb")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        A human-readable description of the rule.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def filter(self) -> pulumi.Output[Optional['outputs.PacketMirroringFilter']]:
        """
        A filter for mirrored traffic.  If unset, all traffic is mirrored.
        Structure is documented below.
        """
        return pulumi.get(self, "filter")

    @property
    @pulumi.getter(name="mirroredResources")
    def mirrored_resources(self) -> pulumi.Output['outputs.PacketMirroringMirroredResources']:
        """
        A means of specifying which resources to mirror.
        Structure is documented below.
        """
        return pulumi.get(self, "mirrored_resources")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the packet mirroring rule
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def network(self) -> pulumi.Output['outputs.PacketMirroringNetwork']:
        """
        Specifies the mirrored VPC network. Only packets in this network
        will be mirrored. All mirrored VMs should have a NIC in the given
        network. All mirrored subnetworks should belong to the given network.
        Structure is documented below.
        """
        return pulumi.get(self, "network")

    @property
    @pulumi.getter
    def priority(self) -> pulumi.Output[int]:
        """
        Since only one rule can be active at a time, priority is
        used to break ties in the case of two rules that apply to
        the same instances.
        """
        return pulumi.get(self, "priority")

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        """
        The ID of the project in which the resource belongs.
        If it is not provided, the provider project is used.
        """
        return pulumi.get(self, "project")

    @property
    @pulumi.getter
    def region(self) -> pulumi.Output[str]:
        """
        The Region in which the created address should reside.
        If it is not provided, the provider region is used.
        """
        return pulumi.get(self, "region")


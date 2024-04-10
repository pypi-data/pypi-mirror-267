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

__all__ = ['RouterArgs', 'Router']

@pulumi.input_type
class RouterArgs:
    def __init__(__self__, *,
                 network: pulumi.Input[str],
                 bgp: Optional[pulumi.Input['RouterBgpArgs']] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 encrypted_interconnect_router: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Router resource.
        :param pulumi.Input[str] network: A reference to the network to which this router belongs.
               
               
               - - -
        :param pulumi.Input['RouterBgpArgs'] bgp: BGP information specific to this router.
               Structure is documented below.
        :param pulumi.Input[str] description: An optional description of this resource.
        :param pulumi.Input[bool] encrypted_interconnect_router: Indicates if a router is dedicated for use with encrypted VLAN
               attachments (interconnectAttachments).
        :param pulumi.Input[str] name: Name of the resource. The name must be 1-63 characters long, and
               comply with RFC1035. Specifically, the name must be 1-63 characters
               long and match the regular expression `a-z?`
               which means the first character must be a lowercase letter, and all
               following characters must be a dash, lowercase letter, or digit,
               except the last character, which cannot be a dash.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] region: Region where the router resides.
        """
        pulumi.set(__self__, "network", network)
        if bgp is not None:
            pulumi.set(__self__, "bgp", bgp)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if encrypted_interconnect_router is not None:
            pulumi.set(__self__, "encrypted_interconnect_router", encrypted_interconnect_router)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if region is not None:
            pulumi.set(__self__, "region", region)

    @property
    @pulumi.getter
    def network(self) -> pulumi.Input[str]:
        """
        A reference to the network to which this router belongs.


        - - -
        """
        return pulumi.get(self, "network")

    @network.setter
    def network(self, value: pulumi.Input[str]):
        pulumi.set(self, "network", value)

    @property
    @pulumi.getter
    def bgp(self) -> Optional[pulumi.Input['RouterBgpArgs']]:
        """
        BGP information specific to this router.
        Structure is documented below.
        """
        return pulumi.get(self, "bgp")

    @bgp.setter
    def bgp(self, value: Optional[pulumi.Input['RouterBgpArgs']]):
        pulumi.set(self, "bgp", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        An optional description of this resource.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="encryptedInterconnectRouter")
    def encrypted_interconnect_router(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates if a router is dedicated for use with encrypted VLAN
        attachments (interconnectAttachments).
        """
        return pulumi.get(self, "encrypted_interconnect_router")

    @encrypted_interconnect_router.setter
    def encrypted_interconnect_router(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "encrypted_interconnect_router", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the resource. The name must be 1-63 characters long, and
        comply with RFC1035. Specifically, the name must be 1-63 characters
        long and match the regular expression `a-z?`
        which means the first character must be a lowercase letter, and all
        following characters must be a dash, lowercase letter, or digit,
        except the last character, which cannot be a dash.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

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
        Region where the router resides.
        """
        return pulumi.get(self, "region")

    @region.setter
    def region(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "region", value)


@pulumi.input_type
class _RouterState:
    def __init__(__self__, *,
                 bgp: Optional[pulumi.Input['RouterBgpArgs']] = None,
                 creation_timestamp: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 encrypted_interconnect_router: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 self_link: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Router resources.
        :param pulumi.Input['RouterBgpArgs'] bgp: BGP information specific to this router.
               Structure is documented below.
        :param pulumi.Input[str] creation_timestamp: Creation timestamp in RFC3339 text format.
        :param pulumi.Input[str] description: An optional description of this resource.
        :param pulumi.Input[bool] encrypted_interconnect_router: Indicates if a router is dedicated for use with encrypted VLAN
               attachments (interconnectAttachments).
        :param pulumi.Input[str] name: Name of the resource. The name must be 1-63 characters long, and
               comply with RFC1035. Specifically, the name must be 1-63 characters
               long and match the regular expression `a-z?`
               which means the first character must be a lowercase letter, and all
               following characters must be a dash, lowercase letter, or digit,
               except the last character, which cannot be a dash.
        :param pulumi.Input[str] network: A reference to the network to which this router belongs.
               
               
               - - -
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] region: Region where the router resides.
        :param pulumi.Input[str] self_link: The URI of the created resource.
        """
        if bgp is not None:
            pulumi.set(__self__, "bgp", bgp)
        if creation_timestamp is not None:
            pulumi.set(__self__, "creation_timestamp", creation_timestamp)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if encrypted_interconnect_router is not None:
            pulumi.set(__self__, "encrypted_interconnect_router", encrypted_interconnect_router)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if network is not None:
            pulumi.set(__self__, "network", network)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if region is not None:
            pulumi.set(__self__, "region", region)
        if self_link is not None:
            pulumi.set(__self__, "self_link", self_link)

    @property
    @pulumi.getter
    def bgp(self) -> Optional[pulumi.Input['RouterBgpArgs']]:
        """
        BGP information specific to this router.
        Structure is documented below.
        """
        return pulumi.get(self, "bgp")

    @bgp.setter
    def bgp(self, value: Optional[pulumi.Input['RouterBgpArgs']]):
        pulumi.set(self, "bgp", value)

    @property
    @pulumi.getter(name="creationTimestamp")
    def creation_timestamp(self) -> Optional[pulumi.Input[str]]:
        """
        Creation timestamp in RFC3339 text format.
        """
        return pulumi.get(self, "creation_timestamp")

    @creation_timestamp.setter
    def creation_timestamp(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "creation_timestamp", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        An optional description of this resource.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="encryptedInterconnectRouter")
    def encrypted_interconnect_router(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates if a router is dedicated for use with encrypted VLAN
        attachments (interconnectAttachments).
        """
        return pulumi.get(self, "encrypted_interconnect_router")

    @encrypted_interconnect_router.setter
    def encrypted_interconnect_router(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "encrypted_interconnect_router", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the resource. The name must be 1-63 characters long, and
        comply with RFC1035. Specifically, the name must be 1-63 characters
        long and match the regular expression `a-z?`
        which means the first character must be a lowercase letter, and all
        following characters must be a dash, lowercase letter, or digit,
        except the last character, which cannot be a dash.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def network(self) -> Optional[pulumi.Input[str]]:
        """
        A reference to the network to which this router belongs.


        - - -
        """
        return pulumi.get(self, "network")

    @network.setter
    def network(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "network", value)

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
        Region where the router resides.
        """
        return pulumi.get(self, "region")

    @region.setter
    def region(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "region", value)

    @property
    @pulumi.getter(name="selfLink")
    def self_link(self) -> Optional[pulumi.Input[str]]:
        """
        The URI of the created resource.
        """
        return pulumi.get(self, "self_link")

    @self_link.setter
    def self_link(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "self_link", value)


class Router(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 bgp: Optional[pulumi.Input[pulumi.InputType['RouterBgpArgs']]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 encrypted_interconnect_router: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Represents a Router resource.

        To get more information about Router, see:

        * [API documentation](https://cloud.google.com/compute/docs/reference/rest/v1/routers)
        * How-to Guides
            * [Google Cloud Router](https://cloud.google.com/router/docs/)

        ## Example Usage

        ### Router Basic

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        foobar_network = gcp.compute.Network("foobar",
            name="my-network",
            auto_create_subnetworks=False)
        foobar = gcp.compute.Router("foobar",
            name="my-router",
            network=foobar_network.name,
            bgp=gcp.compute.RouterBgpArgs(
                asn=64514,
                advertise_mode="CUSTOM",
                advertised_groups=["ALL_SUBNETS"],
                advertised_ip_ranges=[
                    gcp.compute.RouterBgpAdvertisedIpRangeArgs(
                        range="1.2.3.4",
                    ),
                    gcp.compute.RouterBgpAdvertisedIpRangeArgs(
                        range="6.7.0.0/16",
                    ),
                ],
            ))
        ```
        <!--End PulumiCodeChooser -->
        ### Compute Router Encrypted Interconnect

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        network = gcp.compute.Network("network",
            name="test-network",
            auto_create_subnetworks=False)
        encrypted_interconnect_router = gcp.compute.Router("encrypted-interconnect-router",
            name="test-router",
            network=network.name,
            encrypted_interconnect_router=True,
            bgp=gcp.compute.RouterBgpArgs(
                asn=64514,
            ))
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Router can be imported using any of these accepted formats:

        * `projects/{{project}}/regions/{{region}}/routers/{{name}}`

        * `{{project}}/{{region}}/{{name}}`

        * `{{region}}/{{name}}`

        * `{{name}}`

        When using the `pulumi import` command, Router can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:compute/router:Router default projects/{{project}}/regions/{{region}}/routers/{{name}}
        ```

        ```sh
        $ pulumi import gcp:compute/router:Router default {{project}}/{{region}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:compute/router:Router default {{region}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:compute/router:Router default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['RouterBgpArgs']] bgp: BGP information specific to this router.
               Structure is documented below.
        :param pulumi.Input[str] description: An optional description of this resource.
        :param pulumi.Input[bool] encrypted_interconnect_router: Indicates if a router is dedicated for use with encrypted VLAN
               attachments (interconnectAttachments).
        :param pulumi.Input[str] name: Name of the resource. The name must be 1-63 characters long, and
               comply with RFC1035. Specifically, the name must be 1-63 characters
               long and match the regular expression `a-z?`
               which means the first character must be a lowercase letter, and all
               following characters must be a dash, lowercase letter, or digit,
               except the last character, which cannot be a dash.
        :param pulumi.Input[str] network: A reference to the network to which this router belongs.
               
               
               - - -
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] region: Region where the router resides.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: RouterArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Represents a Router resource.

        To get more information about Router, see:

        * [API documentation](https://cloud.google.com/compute/docs/reference/rest/v1/routers)
        * How-to Guides
            * [Google Cloud Router](https://cloud.google.com/router/docs/)

        ## Example Usage

        ### Router Basic

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        foobar_network = gcp.compute.Network("foobar",
            name="my-network",
            auto_create_subnetworks=False)
        foobar = gcp.compute.Router("foobar",
            name="my-router",
            network=foobar_network.name,
            bgp=gcp.compute.RouterBgpArgs(
                asn=64514,
                advertise_mode="CUSTOM",
                advertised_groups=["ALL_SUBNETS"],
                advertised_ip_ranges=[
                    gcp.compute.RouterBgpAdvertisedIpRangeArgs(
                        range="1.2.3.4",
                    ),
                    gcp.compute.RouterBgpAdvertisedIpRangeArgs(
                        range="6.7.0.0/16",
                    ),
                ],
            ))
        ```
        <!--End PulumiCodeChooser -->
        ### Compute Router Encrypted Interconnect

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        network = gcp.compute.Network("network",
            name="test-network",
            auto_create_subnetworks=False)
        encrypted_interconnect_router = gcp.compute.Router("encrypted-interconnect-router",
            name="test-router",
            network=network.name,
            encrypted_interconnect_router=True,
            bgp=gcp.compute.RouterBgpArgs(
                asn=64514,
            ))
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Router can be imported using any of these accepted formats:

        * `projects/{{project}}/regions/{{region}}/routers/{{name}}`

        * `{{project}}/{{region}}/{{name}}`

        * `{{region}}/{{name}}`

        * `{{name}}`

        When using the `pulumi import` command, Router can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:compute/router:Router default projects/{{project}}/regions/{{region}}/routers/{{name}}
        ```

        ```sh
        $ pulumi import gcp:compute/router:Router default {{project}}/{{region}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:compute/router:Router default {{region}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:compute/router:Router default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param RouterArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(RouterArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 bgp: Optional[pulumi.Input[pulumi.InputType['RouterBgpArgs']]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 encrypted_interconnect_router: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = RouterArgs.__new__(RouterArgs)

            __props__.__dict__["bgp"] = bgp
            __props__.__dict__["description"] = description
            __props__.__dict__["encrypted_interconnect_router"] = encrypted_interconnect_router
            __props__.__dict__["name"] = name
            if network is None and not opts.urn:
                raise TypeError("Missing required property 'network'")
            __props__.__dict__["network"] = network
            __props__.__dict__["project"] = project
            __props__.__dict__["region"] = region
            __props__.__dict__["creation_timestamp"] = None
            __props__.__dict__["self_link"] = None
        super(Router, __self__).__init__(
            'gcp:compute/router:Router',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            bgp: Optional[pulumi.Input[pulumi.InputType['RouterBgpArgs']]] = None,
            creation_timestamp: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            encrypted_interconnect_router: Optional[pulumi.Input[bool]] = None,
            name: Optional[pulumi.Input[str]] = None,
            network: Optional[pulumi.Input[str]] = None,
            project: Optional[pulumi.Input[str]] = None,
            region: Optional[pulumi.Input[str]] = None,
            self_link: Optional[pulumi.Input[str]] = None) -> 'Router':
        """
        Get an existing Router resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['RouterBgpArgs']] bgp: BGP information specific to this router.
               Structure is documented below.
        :param pulumi.Input[str] creation_timestamp: Creation timestamp in RFC3339 text format.
        :param pulumi.Input[str] description: An optional description of this resource.
        :param pulumi.Input[bool] encrypted_interconnect_router: Indicates if a router is dedicated for use with encrypted VLAN
               attachments (interconnectAttachments).
        :param pulumi.Input[str] name: Name of the resource. The name must be 1-63 characters long, and
               comply with RFC1035. Specifically, the name must be 1-63 characters
               long and match the regular expression `a-z?`
               which means the first character must be a lowercase letter, and all
               following characters must be a dash, lowercase letter, or digit,
               except the last character, which cannot be a dash.
        :param pulumi.Input[str] network: A reference to the network to which this router belongs.
               
               
               - - -
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] region: Region where the router resides.
        :param pulumi.Input[str] self_link: The URI of the created resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _RouterState.__new__(_RouterState)

        __props__.__dict__["bgp"] = bgp
        __props__.__dict__["creation_timestamp"] = creation_timestamp
        __props__.__dict__["description"] = description
        __props__.__dict__["encrypted_interconnect_router"] = encrypted_interconnect_router
        __props__.__dict__["name"] = name
        __props__.__dict__["network"] = network
        __props__.__dict__["project"] = project
        __props__.__dict__["region"] = region
        __props__.__dict__["self_link"] = self_link
        return Router(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def bgp(self) -> pulumi.Output[Optional['outputs.RouterBgp']]:
        """
        BGP information specific to this router.
        Structure is documented below.
        """
        return pulumi.get(self, "bgp")

    @property
    @pulumi.getter(name="creationTimestamp")
    def creation_timestamp(self) -> pulumi.Output[str]:
        """
        Creation timestamp in RFC3339 text format.
        """
        return pulumi.get(self, "creation_timestamp")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        An optional description of this resource.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="encryptedInterconnectRouter")
    def encrypted_interconnect_router(self) -> pulumi.Output[Optional[bool]]:
        """
        Indicates if a router is dedicated for use with encrypted VLAN
        attachments (interconnectAttachments).
        """
        return pulumi.get(self, "encrypted_interconnect_router")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the resource. The name must be 1-63 characters long, and
        comply with RFC1035. Specifically, the name must be 1-63 characters
        long and match the regular expression `a-z?`
        which means the first character must be a lowercase letter, and all
        following characters must be a dash, lowercase letter, or digit,
        except the last character, which cannot be a dash.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def network(self) -> pulumi.Output[str]:
        """
        A reference to the network to which this router belongs.


        - - -
        """
        return pulumi.get(self, "network")

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
        Region where the router resides.
        """
        return pulumi.get(self, "region")

    @property
    @pulumi.getter(name="selfLink")
    def self_link(self) -> pulumi.Output[str]:
        """
        The URI of the created resource.
        """
        return pulumi.get(self, "self_link")


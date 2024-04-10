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

__all__ = ['TlsRouteArgs', 'TlsRoute']

@pulumi.input_type
class TlsRouteArgs:
    def __init__(__self__, *,
                 rules: pulumi.Input[Sequence[pulumi.Input['TlsRouteRuleArgs']]],
                 description: Optional[pulumi.Input[str]] = None,
                 gateways: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 meshes: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a TlsRoute resource.
        :param pulumi.Input[Sequence[pulumi.Input['TlsRouteRuleArgs']]] rules: Rules that define how traffic is routed and handled.
               Structure is documented below.
        :param pulumi.Input[str] description: A free-text description of the resource. Max length 1024 characters.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] gateways: Gateways defines a list of gateways this TlsRoute is attached to, as one of the routing rules to route the requests served by the gateway.
               Each gateway reference should match the pattern: projects/*/locations/global/gateways/<gateway_name>
        :param pulumi.Input[Sequence[pulumi.Input[str]]] meshes: Meshes defines a list of meshes this TlsRoute is attached to, as one of the routing rules to route the requests served by the mesh.
               Each mesh reference should match the pattern: projects/*/locations/global/meshes/<mesh_name>
               The attached Mesh should be of a type SIDECAR
        :param pulumi.Input[str] name: Name of the TlsRoute resource.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        """
        pulumi.set(__self__, "rules", rules)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if gateways is not None:
            pulumi.set(__self__, "gateways", gateways)
        if meshes is not None:
            pulumi.set(__self__, "meshes", meshes)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if project is not None:
            pulumi.set(__self__, "project", project)

    @property
    @pulumi.getter
    def rules(self) -> pulumi.Input[Sequence[pulumi.Input['TlsRouteRuleArgs']]]:
        """
        Rules that define how traffic is routed and handled.
        Structure is documented below.
        """
        return pulumi.get(self, "rules")

    @rules.setter
    def rules(self, value: pulumi.Input[Sequence[pulumi.Input['TlsRouteRuleArgs']]]):
        pulumi.set(self, "rules", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A free-text description of the resource. Max length 1024 characters.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def gateways(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Gateways defines a list of gateways this TlsRoute is attached to, as one of the routing rules to route the requests served by the gateway.
        Each gateway reference should match the pattern: projects/*/locations/global/gateways/<gateway_name>
        """
        return pulumi.get(self, "gateways")

    @gateways.setter
    def gateways(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "gateways", value)

    @property
    @pulumi.getter
    def meshes(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Meshes defines a list of meshes this TlsRoute is attached to, as one of the routing rules to route the requests served by the mesh.
        Each mesh reference should match the pattern: projects/*/locations/global/meshes/<mesh_name>
        The attached Mesh should be of a type SIDECAR
        """
        return pulumi.get(self, "meshes")

    @meshes.setter
    def meshes(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "meshes", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the TlsRoute resource.
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


@pulumi.input_type
class _TlsRouteState:
    def __init__(__self__, *,
                 create_time: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 gateways: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 meshes: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 rules: Optional[pulumi.Input[Sequence[pulumi.Input['TlsRouteRuleArgs']]]] = None,
                 self_link: Optional[pulumi.Input[str]] = None,
                 update_time: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering TlsRoute resources.
        :param pulumi.Input[str] create_time: Time the TlsRoute was created in UTC.
        :param pulumi.Input[str] description: A free-text description of the resource. Max length 1024 characters.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] gateways: Gateways defines a list of gateways this TlsRoute is attached to, as one of the routing rules to route the requests served by the gateway.
               Each gateway reference should match the pattern: projects/*/locations/global/gateways/<gateway_name>
        :param pulumi.Input[Sequence[pulumi.Input[str]]] meshes: Meshes defines a list of meshes this TlsRoute is attached to, as one of the routing rules to route the requests served by the mesh.
               Each mesh reference should match the pattern: projects/*/locations/global/meshes/<mesh_name>
               The attached Mesh should be of a type SIDECAR
        :param pulumi.Input[str] name: Name of the TlsRoute resource.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[Sequence[pulumi.Input['TlsRouteRuleArgs']]] rules: Rules that define how traffic is routed and handled.
               Structure is documented below.
        :param pulumi.Input[str] self_link: Server-defined URL of this resource.
        :param pulumi.Input[str] update_time: Time the TlsRoute was updated in UTC.
        """
        if create_time is not None:
            pulumi.set(__self__, "create_time", create_time)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if gateways is not None:
            pulumi.set(__self__, "gateways", gateways)
        if meshes is not None:
            pulumi.set(__self__, "meshes", meshes)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if rules is not None:
            pulumi.set(__self__, "rules", rules)
        if self_link is not None:
            pulumi.set(__self__, "self_link", self_link)
        if update_time is not None:
            pulumi.set(__self__, "update_time", update_time)

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> Optional[pulumi.Input[str]]:
        """
        Time the TlsRoute was created in UTC.
        """
        return pulumi.get(self, "create_time")

    @create_time.setter
    def create_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "create_time", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A free-text description of the resource. Max length 1024 characters.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def gateways(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Gateways defines a list of gateways this TlsRoute is attached to, as one of the routing rules to route the requests served by the gateway.
        Each gateway reference should match the pattern: projects/*/locations/global/gateways/<gateway_name>
        """
        return pulumi.get(self, "gateways")

    @gateways.setter
    def gateways(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "gateways", value)

    @property
    @pulumi.getter
    def meshes(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Meshes defines a list of meshes this TlsRoute is attached to, as one of the routing rules to route the requests served by the mesh.
        Each mesh reference should match the pattern: projects/*/locations/global/meshes/<mesh_name>
        The attached Mesh should be of a type SIDECAR
        """
        return pulumi.get(self, "meshes")

    @meshes.setter
    def meshes(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "meshes", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the TlsRoute resource.
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
    def rules(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['TlsRouteRuleArgs']]]]:
        """
        Rules that define how traffic is routed and handled.
        Structure is documented below.
        """
        return pulumi.get(self, "rules")

    @rules.setter
    def rules(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['TlsRouteRuleArgs']]]]):
        pulumi.set(self, "rules", value)

    @property
    @pulumi.getter(name="selfLink")
    def self_link(self) -> Optional[pulumi.Input[str]]:
        """
        Server-defined URL of this resource.
        """
        return pulumi.get(self, "self_link")

    @self_link.setter
    def self_link(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "self_link", value)

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> Optional[pulumi.Input[str]]:
        """
        Time the TlsRoute was updated in UTC.
        """
        return pulumi.get(self, "update_time")

    @update_time.setter
    def update_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "update_time", value)


class TlsRoute(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 gateways: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 meshes: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['TlsRouteRuleArgs']]]]] = None,
                 __props__=None):
        """
        ## Example Usage

        ### Network Services Tls Route Basic

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        default_http_health_check = gcp.compute.HttpHealthCheck("default",
            name="backend-service-health-check",
            request_path="/",
            check_interval_sec=1,
            timeout_sec=1)
        default = gcp.compute.BackendService("default",
            name="my-backend-service",
            health_checks=default_http_health_check.id)
        default_tls_route = gcp.networkservices.TlsRoute("default",
            name="my-tls-route",
            description="my description",
            rules=[gcp.networkservices.TlsRouteRuleArgs(
                matches=[gcp.networkservices.TlsRouteRuleMatchArgs(
                    sni_hosts=["example.com"],
                    alpns=["http/1.1"],
                )],
                action=gcp.networkservices.TlsRouteRuleActionArgs(
                    destinations=[gcp.networkservices.TlsRouteRuleActionDestinationArgs(
                        service_name=default.id,
                        weight=1,
                    )],
                ),
            )])
        ```
        <!--End PulumiCodeChooser -->
        ### Network Services Tls Route Mesh Basic

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        default_http_health_check = gcp.compute.HttpHealthCheck("default",
            name="backend-service-health-check",
            request_path="/",
            check_interval_sec=1,
            timeout_sec=1)
        default = gcp.compute.BackendService("default",
            name="my-backend-service",
            health_checks=default_http_health_check.id)
        default_mesh = gcp.networkservices.Mesh("default",
            name="my-tls-route",
            labels={
                "foo": "bar",
            },
            description="my description")
        default_tls_route = gcp.networkservices.TlsRoute("default",
            name="my-tls-route",
            description="my description",
            meshes=[default_mesh.id],
            rules=[gcp.networkservices.TlsRouteRuleArgs(
                matches=[gcp.networkservices.TlsRouteRuleMatchArgs(
                    sni_hosts=["example.com"],
                    alpns=["http/1.1"],
                )],
                action=gcp.networkservices.TlsRouteRuleActionArgs(
                    destinations=[gcp.networkservices.TlsRouteRuleActionDestinationArgs(
                        service_name=default.id,
                        weight=1,
                    )],
                ),
            )])
        ```
        <!--End PulumiCodeChooser -->
        ### Network Services Tls Route Gateway Basic

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        default_http_health_check = gcp.compute.HttpHealthCheck("default",
            name="backend-service-health-check",
            request_path="/",
            check_interval_sec=1,
            timeout_sec=1)
        default = gcp.compute.BackendService("default",
            name="my-backend-service",
            health_checks=default_http_health_check.id)
        default_gateway = gcp.networkservices.Gateway("default",
            name="my-tls-route",
            labels={
                "foo": "bar",
            },
            description="my description",
            scope="my-scope",
            type="OPEN_MESH",
            ports=[443])
        default_tls_route = gcp.networkservices.TlsRoute("default",
            name="my-tls-route",
            description="my description",
            gateways=[default_gateway.id],
            rules=[gcp.networkservices.TlsRouteRuleArgs(
                matches=[gcp.networkservices.TlsRouteRuleMatchArgs(
                    sni_hosts=["example.com"],
                    alpns=["http/1.1"],
                )],
                action=gcp.networkservices.TlsRouteRuleActionArgs(
                    destinations=[gcp.networkservices.TlsRouteRuleActionDestinationArgs(
                        service_name=default.id,
                        weight=1,
                    )],
                ),
            )])
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        TlsRoute can be imported using any of these accepted formats:

        * `projects/{{project}}/locations/global/tlsRoutes/{{name}}`

        * `{{project}}/{{name}}`

        * `{{name}}`

        When using the `pulumi import` command, TlsRoute can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:networkservices/tlsRoute:TlsRoute default projects/{{project}}/locations/global/tlsRoutes/{{name}}
        ```

        ```sh
        $ pulumi import gcp:networkservices/tlsRoute:TlsRoute default {{project}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:networkservices/tlsRoute:TlsRoute default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: A free-text description of the resource. Max length 1024 characters.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] gateways: Gateways defines a list of gateways this TlsRoute is attached to, as one of the routing rules to route the requests served by the gateway.
               Each gateway reference should match the pattern: projects/*/locations/global/gateways/<gateway_name>
        :param pulumi.Input[Sequence[pulumi.Input[str]]] meshes: Meshes defines a list of meshes this TlsRoute is attached to, as one of the routing rules to route the requests served by the mesh.
               Each mesh reference should match the pattern: projects/*/locations/global/meshes/<mesh_name>
               The attached Mesh should be of a type SIDECAR
        :param pulumi.Input[str] name: Name of the TlsRoute resource.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['TlsRouteRuleArgs']]]] rules: Rules that define how traffic is routed and handled.
               Structure is documented below.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: TlsRouteArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## Example Usage

        ### Network Services Tls Route Basic

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        default_http_health_check = gcp.compute.HttpHealthCheck("default",
            name="backend-service-health-check",
            request_path="/",
            check_interval_sec=1,
            timeout_sec=1)
        default = gcp.compute.BackendService("default",
            name="my-backend-service",
            health_checks=default_http_health_check.id)
        default_tls_route = gcp.networkservices.TlsRoute("default",
            name="my-tls-route",
            description="my description",
            rules=[gcp.networkservices.TlsRouteRuleArgs(
                matches=[gcp.networkservices.TlsRouteRuleMatchArgs(
                    sni_hosts=["example.com"],
                    alpns=["http/1.1"],
                )],
                action=gcp.networkservices.TlsRouteRuleActionArgs(
                    destinations=[gcp.networkservices.TlsRouteRuleActionDestinationArgs(
                        service_name=default.id,
                        weight=1,
                    )],
                ),
            )])
        ```
        <!--End PulumiCodeChooser -->
        ### Network Services Tls Route Mesh Basic

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        default_http_health_check = gcp.compute.HttpHealthCheck("default",
            name="backend-service-health-check",
            request_path="/",
            check_interval_sec=1,
            timeout_sec=1)
        default = gcp.compute.BackendService("default",
            name="my-backend-service",
            health_checks=default_http_health_check.id)
        default_mesh = gcp.networkservices.Mesh("default",
            name="my-tls-route",
            labels={
                "foo": "bar",
            },
            description="my description")
        default_tls_route = gcp.networkservices.TlsRoute("default",
            name="my-tls-route",
            description="my description",
            meshes=[default_mesh.id],
            rules=[gcp.networkservices.TlsRouteRuleArgs(
                matches=[gcp.networkservices.TlsRouteRuleMatchArgs(
                    sni_hosts=["example.com"],
                    alpns=["http/1.1"],
                )],
                action=gcp.networkservices.TlsRouteRuleActionArgs(
                    destinations=[gcp.networkservices.TlsRouteRuleActionDestinationArgs(
                        service_name=default.id,
                        weight=1,
                    )],
                ),
            )])
        ```
        <!--End PulumiCodeChooser -->
        ### Network Services Tls Route Gateway Basic

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        default_http_health_check = gcp.compute.HttpHealthCheck("default",
            name="backend-service-health-check",
            request_path="/",
            check_interval_sec=1,
            timeout_sec=1)
        default = gcp.compute.BackendService("default",
            name="my-backend-service",
            health_checks=default_http_health_check.id)
        default_gateway = gcp.networkservices.Gateway("default",
            name="my-tls-route",
            labels={
                "foo": "bar",
            },
            description="my description",
            scope="my-scope",
            type="OPEN_MESH",
            ports=[443])
        default_tls_route = gcp.networkservices.TlsRoute("default",
            name="my-tls-route",
            description="my description",
            gateways=[default_gateway.id],
            rules=[gcp.networkservices.TlsRouteRuleArgs(
                matches=[gcp.networkservices.TlsRouteRuleMatchArgs(
                    sni_hosts=["example.com"],
                    alpns=["http/1.1"],
                )],
                action=gcp.networkservices.TlsRouteRuleActionArgs(
                    destinations=[gcp.networkservices.TlsRouteRuleActionDestinationArgs(
                        service_name=default.id,
                        weight=1,
                    )],
                ),
            )])
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        TlsRoute can be imported using any of these accepted formats:

        * `projects/{{project}}/locations/global/tlsRoutes/{{name}}`

        * `{{project}}/{{name}}`

        * `{{name}}`

        When using the `pulumi import` command, TlsRoute can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:networkservices/tlsRoute:TlsRoute default projects/{{project}}/locations/global/tlsRoutes/{{name}}
        ```

        ```sh
        $ pulumi import gcp:networkservices/tlsRoute:TlsRoute default {{project}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:networkservices/tlsRoute:TlsRoute default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param TlsRouteArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(TlsRouteArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 gateways: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 meshes: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['TlsRouteRuleArgs']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = TlsRouteArgs.__new__(TlsRouteArgs)

            __props__.__dict__["description"] = description
            __props__.__dict__["gateways"] = gateways
            __props__.__dict__["meshes"] = meshes
            __props__.__dict__["name"] = name
            __props__.__dict__["project"] = project
            if rules is None and not opts.urn:
                raise TypeError("Missing required property 'rules'")
            __props__.__dict__["rules"] = rules
            __props__.__dict__["create_time"] = None
            __props__.__dict__["self_link"] = None
            __props__.__dict__["update_time"] = None
        super(TlsRoute, __self__).__init__(
            'gcp:networkservices/tlsRoute:TlsRoute',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            create_time: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            gateways: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            meshes: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            name: Optional[pulumi.Input[str]] = None,
            project: Optional[pulumi.Input[str]] = None,
            rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['TlsRouteRuleArgs']]]]] = None,
            self_link: Optional[pulumi.Input[str]] = None,
            update_time: Optional[pulumi.Input[str]] = None) -> 'TlsRoute':
        """
        Get an existing TlsRoute resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] create_time: Time the TlsRoute was created in UTC.
        :param pulumi.Input[str] description: A free-text description of the resource. Max length 1024 characters.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] gateways: Gateways defines a list of gateways this TlsRoute is attached to, as one of the routing rules to route the requests served by the gateway.
               Each gateway reference should match the pattern: projects/*/locations/global/gateways/<gateway_name>
        :param pulumi.Input[Sequence[pulumi.Input[str]]] meshes: Meshes defines a list of meshes this TlsRoute is attached to, as one of the routing rules to route the requests served by the mesh.
               Each mesh reference should match the pattern: projects/*/locations/global/meshes/<mesh_name>
               The attached Mesh should be of a type SIDECAR
        :param pulumi.Input[str] name: Name of the TlsRoute resource.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['TlsRouteRuleArgs']]]] rules: Rules that define how traffic is routed and handled.
               Structure is documented below.
        :param pulumi.Input[str] self_link: Server-defined URL of this resource.
        :param pulumi.Input[str] update_time: Time the TlsRoute was updated in UTC.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _TlsRouteState.__new__(_TlsRouteState)

        __props__.__dict__["create_time"] = create_time
        __props__.__dict__["description"] = description
        __props__.__dict__["gateways"] = gateways
        __props__.__dict__["meshes"] = meshes
        __props__.__dict__["name"] = name
        __props__.__dict__["project"] = project
        __props__.__dict__["rules"] = rules
        __props__.__dict__["self_link"] = self_link
        __props__.__dict__["update_time"] = update_time
        return TlsRoute(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> pulumi.Output[str]:
        """
        Time the TlsRoute was created in UTC.
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        A free-text description of the resource. Max length 1024 characters.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def gateways(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        Gateways defines a list of gateways this TlsRoute is attached to, as one of the routing rules to route the requests served by the gateway.
        Each gateway reference should match the pattern: projects/*/locations/global/gateways/<gateway_name>
        """
        return pulumi.get(self, "gateways")

    @property
    @pulumi.getter
    def meshes(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        Meshes defines a list of meshes this TlsRoute is attached to, as one of the routing rules to route the requests served by the mesh.
        Each mesh reference should match the pattern: projects/*/locations/global/meshes/<mesh_name>
        The attached Mesh should be of a type SIDECAR
        """
        return pulumi.get(self, "meshes")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the TlsRoute resource.
        """
        return pulumi.get(self, "name")

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
    def rules(self) -> pulumi.Output[Sequence['outputs.TlsRouteRule']]:
        """
        Rules that define how traffic is routed and handled.
        Structure is documented below.
        """
        return pulumi.get(self, "rules")

    @property
    @pulumi.getter(name="selfLink")
    def self_link(self) -> pulumi.Output[str]:
        """
        Server-defined URL of this resource.
        """
        return pulumi.get(self, "self_link")

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> pulumi.Output[str]:
        """
        Time the TlsRoute was updated in UTC.
        """
        return pulumi.get(self, "update_time")


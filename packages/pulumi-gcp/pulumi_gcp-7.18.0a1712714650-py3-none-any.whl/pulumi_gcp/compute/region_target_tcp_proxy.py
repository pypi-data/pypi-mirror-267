# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['RegionTargetTcpProxyArgs', 'RegionTargetTcpProxy']

@pulumi.input_type
class RegionTargetTcpProxyArgs:
    def __init__(__self__, *,
                 backend_service: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 proxy_bind: Optional[pulumi.Input[bool]] = None,
                 proxy_header: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a RegionTargetTcpProxy resource.
        :param pulumi.Input[str] backend_service: A reference to the BackendService resource.
               
               
               - - -
        :param pulumi.Input[str] description: An optional description of this resource.
        :param pulumi.Input[str] name: Name of the resource. Provided by the client when the resource is
               created. The name must be 1-63 characters long, and comply with
               RFC1035. Specifically, the name must be 1-63 characters long and match
               the regular expression `a-z?` which means the
               first character must be a lowercase letter, and all following
               characters must be a dash, lowercase letter, or digit, except the last
               character, which cannot be a dash.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[bool] proxy_bind: This field only applies when the forwarding rule that references
               this target proxy has a loadBalancingScheme set to INTERNAL_SELF_MANAGED.
        :param pulumi.Input[str] proxy_header: Specifies the type of proxy header to append before sending data to
               the backend.
               Default value is `NONE`.
               Possible values are: `NONE`, `PROXY_V1`.
        :param pulumi.Input[str] region: The Region in which the created target TCP proxy should reside.
               If it is not provided, the provider region is used.
        """
        pulumi.set(__self__, "backend_service", backend_service)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if proxy_bind is not None:
            pulumi.set(__self__, "proxy_bind", proxy_bind)
        if proxy_header is not None:
            pulumi.set(__self__, "proxy_header", proxy_header)
        if region is not None:
            pulumi.set(__self__, "region", region)

    @property
    @pulumi.getter(name="backendService")
    def backend_service(self) -> pulumi.Input[str]:
        """
        A reference to the BackendService resource.


        - - -
        """
        return pulumi.get(self, "backend_service")

    @backend_service.setter
    def backend_service(self, value: pulumi.Input[str]):
        pulumi.set(self, "backend_service", value)

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
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the resource. Provided by the client when the resource is
        created. The name must be 1-63 characters long, and comply with
        RFC1035. Specifically, the name must be 1-63 characters long and match
        the regular expression `a-z?` which means the
        first character must be a lowercase letter, and all following
        characters must be a dash, lowercase letter, or digit, except the last
        character, which cannot be a dash.
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
    @pulumi.getter(name="proxyBind")
    def proxy_bind(self) -> Optional[pulumi.Input[bool]]:
        """
        This field only applies when the forwarding rule that references
        this target proxy has a loadBalancingScheme set to INTERNAL_SELF_MANAGED.
        """
        return pulumi.get(self, "proxy_bind")

    @proxy_bind.setter
    def proxy_bind(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "proxy_bind", value)

    @property
    @pulumi.getter(name="proxyHeader")
    def proxy_header(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the type of proxy header to append before sending data to
        the backend.
        Default value is `NONE`.
        Possible values are: `NONE`, `PROXY_V1`.
        """
        return pulumi.get(self, "proxy_header")

    @proxy_header.setter
    def proxy_header(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "proxy_header", value)

    @property
    @pulumi.getter
    def region(self) -> Optional[pulumi.Input[str]]:
        """
        The Region in which the created target TCP proxy should reside.
        If it is not provided, the provider region is used.
        """
        return pulumi.get(self, "region")

    @region.setter
    def region(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "region", value)


@pulumi.input_type
class _RegionTargetTcpProxyState:
    def __init__(__self__, *,
                 backend_service: Optional[pulumi.Input[str]] = None,
                 creation_timestamp: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 proxy_bind: Optional[pulumi.Input[bool]] = None,
                 proxy_header: Optional[pulumi.Input[str]] = None,
                 proxy_id: Optional[pulumi.Input[int]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 self_link: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering RegionTargetTcpProxy resources.
        :param pulumi.Input[str] backend_service: A reference to the BackendService resource.
               
               
               - - -
        :param pulumi.Input[str] creation_timestamp: Creation timestamp in RFC3339 text format.
        :param pulumi.Input[str] description: An optional description of this resource.
        :param pulumi.Input[str] name: Name of the resource. Provided by the client when the resource is
               created. The name must be 1-63 characters long, and comply with
               RFC1035. Specifically, the name must be 1-63 characters long and match
               the regular expression `a-z?` which means the
               first character must be a lowercase letter, and all following
               characters must be a dash, lowercase letter, or digit, except the last
               character, which cannot be a dash.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[bool] proxy_bind: This field only applies when the forwarding rule that references
               this target proxy has a loadBalancingScheme set to INTERNAL_SELF_MANAGED.
        :param pulumi.Input[str] proxy_header: Specifies the type of proxy header to append before sending data to
               the backend.
               Default value is `NONE`.
               Possible values are: `NONE`, `PROXY_V1`.
        :param pulumi.Input[int] proxy_id: The unique identifier for the resource.
        :param pulumi.Input[str] region: The Region in which the created target TCP proxy should reside.
               If it is not provided, the provider region is used.
        :param pulumi.Input[str] self_link: The URI of the created resource.
        """
        if backend_service is not None:
            pulumi.set(__self__, "backend_service", backend_service)
        if creation_timestamp is not None:
            pulumi.set(__self__, "creation_timestamp", creation_timestamp)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if proxy_bind is not None:
            pulumi.set(__self__, "proxy_bind", proxy_bind)
        if proxy_header is not None:
            pulumi.set(__self__, "proxy_header", proxy_header)
        if proxy_id is not None:
            pulumi.set(__self__, "proxy_id", proxy_id)
        if region is not None:
            pulumi.set(__self__, "region", region)
        if self_link is not None:
            pulumi.set(__self__, "self_link", self_link)

    @property
    @pulumi.getter(name="backendService")
    def backend_service(self) -> Optional[pulumi.Input[str]]:
        """
        A reference to the BackendService resource.


        - - -
        """
        return pulumi.get(self, "backend_service")

    @backend_service.setter
    def backend_service(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "backend_service", value)

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
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the resource. Provided by the client when the resource is
        created. The name must be 1-63 characters long, and comply with
        RFC1035. Specifically, the name must be 1-63 characters long and match
        the regular expression `a-z?` which means the
        first character must be a lowercase letter, and all following
        characters must be a dash, lowercase letter, or digit, except the last
        character, which cannot be a dash.
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
    @pulumi.getter(name="proxyBind")
    def proxy_bind(self) -> Optional[pulumi.Input[bool]]:
        """
        This field only applies when the forwarding rule that references
        this target proxy has a loadBalancingScheme set to INTERNAL_SELF_MANAGED.
        """
        return pulumi.get(self, "proxy_bind")

    @proxy_bind.setter
    def proxy_bind(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "proxy_bind", value)

    @property
    @pulumi.getter(name="proxyHeader")
    def proxy_header(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the type of proxy header to append before sending data to
        the backend.
        Default value is `NONE`.
        Possible values are: `NONE`, `PROXY_V1`.
        """
        return pulumi.get(self, "proxy_header")

    @proxy_header.setter
    def proxy_header(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "proxy_header", value)

    @property
    @pulumi.getter(name="proxyId")
    def proxy_id(self) -> Optional[pulumi.Input[int]]:
        """
        The unique identifier for the resource.
        """
        return pulumi.get(self, "proxy_id")

    @proxy_id.setter
    def proxy_id(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "proxy_id", value)

    @property
    @pulumi.getter
    def region(self) -> Optional[pulumi.Input[str]]:
        """
        The Region in which the created target TCP proxy should reside.
        If it is not provided, the provider region is used.
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


class RegionTargetTcpProxy(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 backend_service: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 proxy_bind: Optional[pulumi.Input[bool]] = None,
                 proxy_header: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Represents a RegionTargetTcpProxy resource, which is used by one or more
        forwarding rules to route incoming TCP requests to a regional TCP proxy load
        balancer.

        To get more information about RegionTargetTcpProxy, see:

        * [API documentation](https://cloud.google.com/compute/docs/reference/rest/v1/regionTargetTcpProxies)
        * How-to Guides
            * [Official Documentation](https://cloud.google.com/load-balancing/docs/tcp/internal-proxy)

        ## Example Usage

        ### Region Target Tcp Proxy Basic

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        default_region_health_check = gcp.compute.RegionHealthCheck("default",
            name="health-check",
            region="europe-west4",
            timeout_sec=1,
            check_interval_sec=1,
            tcp_health_check=gcp.compute.RegionHealthCheckTcpHealthCheckArgs(
                port=80,
            ))
        default_region_backend_service = gcp.compute.RegionBackendService("default",
            name="backend-service",
            protocol="TCP",
            timeout_sec=10,
            region="europe-west4",
            health_checks=default_region_health_check.id,
            load_balancing_scheme="INTERNAL_MANAGED")
        default = gcp.compute.RegionTargetTcpProxy("default",
            name="test-proxy",
            region="europe-west4",
            backend_service=default_region_backend_service.id)
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        RegionTargetTcpProxy can be imported using any of these accepted formats:

        * `projects/{{project}}/regions/{{region}}/targetTcpProxies/{{name}}`

        * `{{project}}/{{region}}/{{name}}`

        * `{{region}}/{{name}}`

        * `{{name}}`

        When using the `pulumi import` command, RegionTargetTcpProxy can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:compute/regionTargetTcpProxy:RegionTargetTcpProxy default projects/{{project}}/regions/{{region}}/targetTcpProxies/{{name}}
        ```

        ```sh
        $ pulumi import gcp:compute/regionTargetTcpProxy:RegionTargetTcpProxy default {{project}}/{{region}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:compute/regionTargetTcpProxy:RegionTargetTcpProxy default {{region}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:compute/regionTargetTcpProxy:RegionTargetTcpProxy default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] backend_service: A reference to the BackendService resource.
               
               
               - - -
        :param pulumi.Input[str] description: An optional description of this resource.
        :param pulumi.Input[str] name: Name of the resource. Provided by the client when the resource is
               created. The name must be 1-63 characters long, and comply with
               RFC1035. Specifically, the name must be 1-63 characters long and match
               the regular expression `a-z?` which means the
               first character must be a lowercase letter, and all following
               characters must be a dash, lowercase letter, or digit, except the last
               character, which cannot be a dash.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[bool] proxy_bind: This field only applies when the forwarding rule that references
               this target proxy has a loadBalancingScheme set to INTERNAL_SELF_MANAGED.
        :param pulumi.Input[str] proxy_header: Specifies the type of proxy header to append before sending data to
               the backend.
               Default value is `NONE`.
               Possible values are: `NONE`, `PROXY_V1`.
        :param pulumi.Input[str] region: The Region in which the created target TCP proxy should reside.
               If it is not provided, the provider region is used.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: RegionTargetTcpProxyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Represents a RegionTargetTcpProxy resource, which is used by one or more
        forwarding rules to route incoming TCP requests to a regional TCP proxy load
        balancer.

        To get more information about RegionTargetTcpProxy, see:

        * [API documentation](https://cloud.google.com/compute/docs/reference/rest/v1/regionTargetTcpProxies)
        * How-to Guides
            * [Official Documentation](https://cloud.google.com/load-balancing/docs/tcp/internal-proxy)

        ## Example Usage

        ### Region Target Tcp Proxy Basic

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        default_region_health_check = gcp.compute.RegionHealthCheck("default",
            name="health-check",
            region="europe-west4",
            timeout_sec=1,
            check_interval_sec=1,
            tcp_health_check=gcp.compute.RegionHealthCheckTcpHealthCheckArgs(
                port=80,
            ))
        default_region_backend_service = gcp.compute.RegionBackendService("default",
            name="backend-service",
            protocol="TCP",
            timeout_sec=10,
            region="europe-west4",
            health_checks=default_region_health_check.id,
            load_balancing_scheme="INTERNAL_MANAGED")
        default = gcp.compute.RegionTargetTcpProxy("default",
            name="test-proxy",
            region="europe-west4",
            backend_service=default_region_backend_service.id)
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        RegionTargetTcpProxy can be imported using any of these accepted formats:

        * `projects/{{project}}/regions/{{region}}/targetTcpProxies/{{name}}`

        * `{{project}}/{{region}}/{{name}}`

        * `{{region}}/{{name}}`

        * `{{name}}`

        When using the `pulumi import` command, RegionTargetTcpProxy can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:compute/regionTargetTcpProxy:RegionTargetTcpProxy default projects/{{project}}/regions/{{region}}/targetTcpProxies/{{name}}
        ```

        ```sh
        $ pulumi import gcp:compute/regionTargetTcpProxy:RegionTargetTcpProxy default {{project}}/{{region}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:compute/regionTargetTcpProxy:RegionTargetTcpProxy default {{region}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:compute/regionTargetTcpProxy:RegionTargetTcpProxy default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param RegionTargetTcpProxyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(RegionTargetTcpProxyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 backend_service: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 proxy_bind: Optional[pulumi.Input[bool]] = None,
                 proxy_header: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = RegionTargetTcpProxyArgs.__new__(RegionTargetTcpProxyArgs)

            if backend_service is None and not opts.urn:
                raise TypeError("Missing required property 'backend_service'")
            __props__.__dict__["backend_service"] = backend_service
            __props__.__dict__["description"] = description
            __props__.__dict__["name"] = name
            __props__.__dict__["project"] = project
            __props__.__dict__["proxy_bind"] = proxy_bind
            __props__.__dict__["proxy_header"] = proxy_header
            __props__.__dict__["region"] = region
            __props__.__dict__["creation_timestamp"] = None
            __props__.__dict__["proxy_id"] = None
            __props__.__dict__["self_link"] = None
        super(RegionTargetTcpProxy, __self__).__init__(
            'gcp:compute/regionTargetTcpProxy:RegionTargetTcpProxy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            backend_service: Optional[pulumi.Input[str]] = None,
            creation_timestamp: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            project: Optional[pulumi.Input[str]] = None,
            proxy_bind: Optional[pulumi.Input[bool]] = None,
            proxy_header: Optional[pulumi.Input[str]] = None,
            proxy_id: Optional[pulumi.Input[int]] = None,
            region: Optional[pulumi.Input[str]] = None,
            self_link: Optional[pulumi.Input[str]] = None) -> 'RegionTargetTcpProxy':
        """
        Get an existing RegionTargetTcpProxy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] backend_service: A reference to the BackendService resource.
               
               
               - - -
        :param pulumi.Input[str] creation_timestamp: Creation timestamp in RFC3339 text format.
        :param pulumi.Input[str] description: An optional description of this resource.
        :param pulumi.Input[str] name: Name of the resource. Provided by the client when the resource is
               created. The name must be 1-63 characters long, and comply with
               RFC1035. Specifically, the name must be 1-63 characters long and match
               the regular expression `a-z?` which means the
               first character must be a lowercase letter, and all following
               characters must be a dash, lowercase letter, or digit, except the last
               character, which cannot be a dash.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[bool] proxy_bind: This field only applies when the forwarding rule that references
               this target proxy has a loadBalancingScheme set to INTERNAL_SELF_MANAGED.
        :param pulumi.Input[str] proxy_header: Specifies the type of proxy header to append before sending data to
               the backend.
               Default value is `NONE`.
               Possible values are: `NONE`, `PROXY_V1`.
        :param pulumi.Input[int] proxy_id: The unique identifier for the resource.
        :param pulumi.Input[str] region: The Region in which the created target TCP proxy should reside.
               If it is not provided, the provider region is used.
        :param pulumi.Input[str] self_link: The URI of the created resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _RegionTargetTcpProxyState.__new__(_RegionTargetTcpProxyState)

        __props__.__dict__["backend_service"] = backend_service
        __props__.__dict__["creation_timestamp"] = creation_timestamp
        __props__.__dict__["description"] = description
        __props__.__dict__["name"] = name
        __props__.__dict__["project"] = project
        __props__.__dict__["proxy_bind"] = proxy_bind
        __props__.__dict__["proxy_header"] = proxy_header
        __props__.__dict__["proxy_id"] = proxy_id
        __props__.__dict__["region"] = region
        __props__.__dict__["self_link"] = self_link
        return RegionTargetTcpProxy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="backendService")
    def backend_service(self) -> pulumi.Output[str]:
        """
        A reference to the BackendService resource.


        - - -
        """
        return pulumi.get(self, "backend_service")

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
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the resource. Provided by the client when the resource is
        created. The name must be 1-63 characters long, and comply with
        RFC1035. Specifically, the name must be 1-63 characters long and match
        the regular expression `a-z?` which means the
        first character must be a lowercase letter, and all following
        characters must be a dash, lowercase letter, or digit, except the last
        character, which cannot be a dash.
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
    @pulumi.getter(name="proxyBind")
    def proxy_bind(self) -> pulumi.Output[bool]:
        """
        This field only applies when the forwarding rule that references
        this target proxy has a loadBalancingScheme set to INTERNAL_SELF_MANAGED.
        """
        return pulumi.get(self, "proxy_bind")

    @property
    @pulumi.getter(name="proxyHeader")
    def proxy_header(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the type of proxy header to append before sending data to
        the backend.
        Default value is `NONE`.
        Possible values are: `NONE`, `PROXY_V1`.
        """
        return pulumi.get(self, "proxy_header")

    @property
    @pulumi.getter(name="proxyId")
    def proxy_id(self) -> pulumi.Output[int]:
        """
        The unique identifier for the resource.
        """
        return pulumi.get(self, "proxy_id")

    @property
    @pulumi.getter
    def region(self) -> pulumi.Output[str]:
        """
        The Region in which the created target TCP proxy should reside.
        If it is not provided, the provider region is used.
        """
        return pulumi.get(self, "region")

    @property
    @pulumi.getter(name="selfLink")
    def self_link(self) -> pulumi.Output[str]:
        """
        The URI of the created resource.
        """
        return pulumi.get(self, "self_link")


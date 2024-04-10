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

__all__ = ['EngineSplitTrafficArgs', 'EngineSplitTraffic']

@pulumi.input_type
class EngineSplitTrafficArgs:
    def __init__(__self__, *,
                 service: pulumi.Input[str],
                 split: pulumi.Input['EngineSplitTrafficSplitArgs'],
                 migrate_traffic: Optional[pulumi.Input[bool]] = None,
                 project: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a EngineSplitTraffic resource.
        :param pulumi.Input[str] service: The name of the service these settings apply to.
        :param pulumi.Input['EngineSplitTrafficSplitArgs'] split: Mapping that defines fractional HTTP traffic diversion to different versions within the service.
               Structure is documented below.
        :param pulumi.Input[bool] migrate_traffic: If set to true traffic will be migrated to this version.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        """
        pulumi.set(__self__, "service", service)
        pulumi.set(__self__, "split", split)
        if migrate_traffic is not None:
            pulumi.set(__self__, "migrate_traffic", migrate_traffic)
        if project is not None:
            pulumi.set(__self__, "project", project)

    @property
    @pulumi.getter
    def service(self) -> pulumi.Input[str]:
        """
        The name of the service these settings apply to.
        """
        return pulumi.get(self, "service")

    @service.setter
    def service(self, value: pulumi.Input[str]):
        pulumi.set(self, "service", value)

    @property
    @pulumi.getter
    def split(self) -> pulumi.Input['EngineSplitTrafficSplitArgs']:
        """
        Mapping that defines fractional HTTP traffic diversion to different versions within the service.
        Structure is documented below.
        """
        return pulumi.get(self, "split")

    @split.setter
    def split(self, value: pulumi.Input['EngineSplitTrafficSplitArgs']):
        pulumi.set(self, "split", value)

    @property
    @pulumi.getter(name="migrateTraffic")
    def migrate_traffic(self) -> Optional[pulumi.Input[bool]]:
        """
        If set to true traffic will be migrated to this version.
        """
        return pulumi.get(self, "migrate_traffic")

    @migrate_traffic.setter
    def migrate_traffic(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "migrate_traffic", value)

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
class _EngineSplitTrafficState:
    def __init__(__self__, *,
                 migrate_traffic: Optional[pulumi.Input[bool]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 service: Optional[pulumi.Input[str]] = None,
                 split: Optional[pulumi.Input['EngineSplitTrafficSplitArgs']] = None):
        """
        Input properties used for looking up and filtering EngineSplitTraffic resources.
        :param pulumi.Input[bool] migrate_traffic: If set to true traffic will be migrated to this version.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] service: The name of the service these settings apply to.
        :param pulumi.Input['EngineSplitTrafficSplitArgs'] split: Mapping that defines fractional HTTP traffic diversion to different versions within the service.
               Structure is documented below.
        """
        if migrate_traffic is not None:
            pulumi.set(__self__, "migrate_traffic", migrate_traffic)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if service is not None:
            pulumi.set(__self__, "service", service)
        if split is not None:
            pulumi.set(__self__, "split", split)

    @property
    @pulumi.getter(name="migrateTraffic")
    def migrate_traffic(self) -> Optional[pulumi.Input[bool]]:
        """
        If set to true traffic will be migrated to this version.
        """
        return pulumi.get(self, "migrate_traffic")

    @migrate_traffic.setter
    def migrate_traffic(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "migrate_traffic", value)

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
    def service(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the service these settings apply to.
        """
        return pulumi.get(self, "service")

    @service.setter
    def service(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "service", value)

    @property
    @pulumi.getter
    def split(self) -> Optional[pulumi.Input['EngineSplitTrafficSplitArgs']]:
        """
        Mapping that defines fractional HTTP traffic diversion to different versions within the service.
        Structure is documented below.
        """
        return pulumi.get(self, "split")

    @split.setter
    def split(self, value: Optional[pulumi.Input['EngineSplitTrafficSplitArgs']]):
        pulumi.set(self, "split", value)


class EngineSplitTraffic(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 migrate_traffic: Optional[pulumi.Input[bool]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 service: Optional[pulumi.Input[str]] = None,
                 split: Optional[pulumi.Input[pulumi.InputType['EngineSplitTrafficSplitArgs']]] = None,
                 __props__=None):
        """
        Traffic routing configuration for versions within a single service. Traffic splits define how traffic directed to the service is assigned to versions.

        To get more information about ServiceSplitTraffic, see:

        * [API documentation](https://cloud.google.com/appengine/docs/admin-api/reference/rest/v1/apps.services)

        ## Example Usage

        ### App Engine Service Split Traffic

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        bucket = gcp.storage.Bucket("bucket",
            name="appengine-static-content",
            location="US")
        object = gcp.storage.BucketObject("object",
            name="hello-world.zip",
            bucket=bucket.name,
            source=pulumi.FileAsset("./test-fixtures/hello-world.zip"))
        liveapp_v1 = gcp.appengine.StandardAppVersion("liveapp_v1",
            version_id="v1",
            service="liveapp",
            delete_service_on_destroy=True,
            runtime="nodejs20",
            entrypoint=gcp.appengine.StandardAppVersionEntrypointArgs(
                shell="node ./app.js",
            ),
            deployment=gcp.appengine.StandardAppVersionDeploymentArgs(
                zip=gcp.appengine.StandardAppVersionDeploymentZipArgs(
                    source_url=pulumi.Output.all(bucket.name, object.name).apply(lambda bucketName, objectName: f"https://storage.googleapis.com/{bucket_name}/{object_name}"),
                ),
            ),
            env_variables={
                "port": "8080",
            })
        liveapp_v2 = gcp.appengine.StandardAppVersion("liveapp_v2",
            version_id="v2",
            service="liveapp",
            noop_on_destroy=True,
            runtime="nodejs20",
            entrypoint=gcp.appengine.StandardAppVersionEntrypointArgs(
                shell="node ./app.js",
            ),
            deployment=gcp.appengine.StandardAppVersionDeploymentArgs(
                zip=gcp.appengine.StandardAppVersionDeploymentZipArgs(
                    source_url=pulumi.Output.all(bucket.name, object.name).apply(lambda bucketName, objectName: f"https://storage.googleapis.com/{bucket_name}/{object_name}"),
                ),
            ),
            env_variables={
                "port": "8080",
            })
        liveapp = gcp.appengine.EngineSplitTraffic("liveapp",
            service=liveapp_v2.service,
            migrate_traffic=False,
            split=gcp.appengine.EngineSplitTrafficSplitArgs(
                shard_by="IP",
                allocations=pulumi.Output.all(liveapp_v1.version_id, liveapp_v2.version_id).apply(lambda liveappV1Version_id, liveappV2Version_id: {
                    liveapp_v1_version_id: 0.75,
                    liveapp_v2_version_id: 0.25,
                }),
            ))
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        ServiceSplitTraffic can be imported using any of these accepted formats:

        * `apps/{{project}}/services/{{service}}`

        * `{{project}}/{{service}}`

        * `{{service}}`

        When using the `pulumi import` command, ServiceSplitTraffic can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:appengine/engineSplitTraffic:EngineSplitTraffic default apps/{{project}}/services/{{service}}
        ```

        ```sh
        $ pulumi import gcp:appengine/engineSplitTraffic:EngineSplitTraffic default {{project}}/{{service}}
        ```

        ```sh
        $ pulumi import gcp:appengine/engineSplitTraffic:EngineSplitTraffic default {{service}}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] migrate_traffic: If set to true traffic will be migrated to this version.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] service: The name of the service these settings apply to.
        :param pulumi.Input[pulumi.InputType['EngineSplitTrafficSplitArgs']] split: Mapping that defines fractional HTTP traffic diversion to different versions within the service.
               Structure is documented below.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: EngineSplitTrafficArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Traffic routing configuration for versions within a single service. Traffic splits define how traffic directed to the service is assigned to versions.

        To get more information about ServiceSplitTraffic, see:

        * [API documentation](https://cloud.google.com/appengine/docs/admin-api/reference/rest/v1/apps.services)

        ## Example Usage

        ### App Engine Service Split Traffic

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        bucket = gcp.storage.Bucket("bucket",
            name="appengine-static-content",
            location="US")
        object = gcp.storage.BucketObject("object",
            name="hello-world.zip",
            bucket=bucket.name,
            source=pulumi.FileAsset("./test-fixtures/hello-world.zip"))
        liveapp_v1 = gcp.appengine.StandardAppVersion("liveapp_v1",
            version_id="v1",
            service="liveapp",
            delete_service_on_destroy=True,
            runtime="nodejs20",
            entrypoint=gcp.appengine.StandardAppVersionEntrypointArgs(
                shell="node ./app.js",
            ),
            deployment=gcp.appengine.StandardAppVersionDeploymentArgs(
                zip=gcp.appengine.StandardAppVersionDeploymentZipArgs(
                    source_url=pulumi.Output.all(bucket.name, object.name).apply(lambda bucketName, objectName: f"https://storage.googleapis.com/{bucket_name}/{object_name}"),
                ),
            ),
            env_variables={
                "port": "8080",
            })
        liveapp_v2 = gcp.appengine.StandardAppVersion("liveapp_v2",
            version_id="v2",
            service="liveapp",
            noop_on_destroy=True,
            runtime="nodejs20",
            entrypoint=gcp.appengine.StandardAppVersionEntrypointArgs(
                shell="node ./app.js",
            ),
            deployment=gcp.appengine.StandardAppVersionDeploymentArgs(
                zip=gcp.appengine.StandardAppVersionDeploymentZipArgs(
                    source_url=pulumi.Output.all(bucket.name, object.name).apply(lambda bucketName, objectName: f"https://storage.googleapis.com/{bucket_name}/{object_name}"),
                ),
            ),
            env_variables={
                "port": "8080",
            })
        liveapp = gcp.appengine.EngineSplitTraffic("liveapp",
            service=liveapp_v2.service,
            migrate_traffic=False,
            split=gcp.appengine.EngineSplitTrafficSplitArgs(
                shard_by="IP",
                allocations=pulumi.Output.all(liveapp_v1.version_id, liveapp_v2.version_id).apply(lambda liveappV1Version_id, liveappV2Version_id: {
                    liveapp_v1_version_id: 0.75,
                    liveapp_v2_version_id: 0.25,
                }),
            ))
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        ServiceSplitTraffic can be imported using any of these accepted formats:

        * `apps/{{project}}/services/{{service}}`

        * `{{project}}/{{service}}`

        * `{{service}}`

        When using the `pulumi import` command, ServiceSplitTraffic can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:appengine/engineSplitTraffic:EngineSplitTraffic default apps/{{project}}/services/{{service}}
        ```

        ```sh
        $ pulumi import gcp:appengine/engineSplitTraffic:EngineSplitTraffic default {{project}}/{{service}}
        ```

        ```sh
        $ pulumi import gcp:appengine/engineSplitTraffic:EngineSplitTraffic default {{service}}
        ```

        :param str resource_name: The name of the resource.
        :param EngineSplitTrafficArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(EngineSplitTrafficArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 migrate_traffic: Optional[pulumi.Input[bool]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 service: Optional[pulumi.Input[str]] = None,
                 split: Optional[pulumi.Input[pulumi.InputType['EngineSplitTrafficSplitArgs']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = EngineSplitTrafficArgs.__new__(EngineSplitTrafficArgs)

            __props__.__dict__["migrate_traffic"] = migrate_traffic
            __props__.__dict__["project"] = project
            if service is None and not opts.urn:
                raise TypeError("Missing required property 'service'")
            __props__.__dict__["service"] = service
            if split is None and not opts.urn:
                raise TypeError("Missing required property 'split'")
            __props__.__dict__["split"] = split
        super(EngineSplitTraffic, __self__).__init__(
            'gcp:appengine/engineSplitTraffic:EngineSplitTraffic',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            migrate_traffic: Optional[pulumi.Input[bool]] = None,
            project: Optional[pulumi.Input[str]] = None,
            service: Optional[pulumi.Input[str]] = None,
            split: Optional[pulumi.Input[pulumi.InputType['EngineSplitTrafficSplitArgs']]] = None) -> 'EngineSplitTraffic':
        """
        Get an existing EngineSplitTraffic resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] migrate_traffic: If set to true traffic will be migrated to this version.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] service: The name of the service these settings apply to.
        :param pulumi.Input[pulumi.InputType['EngineSplitTrafficSplitArgs']] split: Mapping that defines fractional HTTP traffic diversion to different versions within the service.
               Structure is documented below.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _EngineSplitTrafficState.__new__(_EngineSplitTrafficState)

        __props__.__dict__["migrate_traffic"] = migrate_traffic
        __props__.__dict__["project"] = project
        __props__.__dict__["service"] = service
        __props__.__dict__["split"] = split
        return EngineSplitTraffic(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="migrateTraffic")
    def migrate_traffic(self) -> pulumi.Output[Optional[bool]]:
        """
        If set to true traffic will be migrated to this version.
        """
        return pulumi.get(self, "migrate_traffic")

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
    def service(self) -> pulumi.Output[str]:
        """
        The name of the service these settings apply to.
        """
        return pulumi.get(self, "service")

    @property
    @pulumi.getter
    def split(self) -> pulumi.Output['outputs.EngineSplitTrafficSplit']:
        """
        Mapping that defines fractional HTTP traffic diversion to different versions within the service.
        Structure is documented below.
        """
        return pulumi.get(self, "split")


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

__all__ = ['ProjectFeedArgs', 'ProjectFeed']

@pulumi.input_type
class ProjectFeedArgs:
    def __init__(__self__, *,
                 feed_id: pulumi.Input[str],
                 feed_output_config: pulumi.Input['ProjectFeedFeedOutputConfigArgs'],
                 asset_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 asset_types: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 billing_project: Optional[pulumi.Input[str]] = None,
                 condition: Optional[pulumi.Input['ProjectFeedConditionArgs']] = None,
                 content_type: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a ProjectFeed resource.
        :param pulumi.Input[str] feed_id: This is the client-assigned asset feed identifier and it needs to be unique under a specific parent.
        :param pulumi.Input['ProjectFeedFeedOutputConfigArgs'] feed_output_config: Output configuration for asset feed destination.
               Structure is documented below.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] asset_names: A list of the full names of the assets to receive updates. You must specify either or both of
               assetNames and assetTypes. Only asset updates matching specified assetNames and assetTypes are
               exported to the feed. For example: //compute.googleapis.com/projects/my_project_123/zones/zone1/instances/instance1.
               See https://cloud.google.com/apis/design/resourceNames#fullResourceName for more info.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] asset_types: A list of types of the assets to receive updates. You must specify either or both of assetNames
               and assetTypes. Only asset updates matching specified assetNames and assetTypes are exported to
               the feed. For example: "compute.googleapis.com/Disk"
               See https://cloud.google.com/asset-inventory/docs/supported-asset-types for a list of all
               supported asset types.
        :param pulumi.Input[str] billing_project: The project whose identity will be used when sending messages to the
               destination pubsub topic. It also specifies the project for API
               enablement check, quota, and billing. If not specified, the resource's
               project will be used.
        :param pulumi.Input['ProjectFeedConditionArgs'] condition: A condition which determines whether an asset update should be published. If specified, an asset
               will be returned only when the expression evaluates to true. When set, expression field
               must be a valid CEL expression on a TemporalAsset with name temporal_asset. Example: a Feed with
               expression "temporal_asset.deleted == true" will only publish Asset deletions. Other fields of
               condition are optional.
               Structure is documented below.
        :param pulumi.Input[str] content_type: Asset content type. If not specified, no content but the asset name and type will be returned.
               Possible values are: `CONTENT_TYPE_UNSPECIFIED`, `RESOURCE`, `IAM_POLICY`, `ORG_POLICY`, `OS_INVENTORY`, `ACCESS_POLICY`.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        """
        pulumi.set(__self__, "feed_id", feed_id)
        pulumi.set(__self__, "feed_output_config", feed_output_config)
        if asset_names is not None:
            pulumi.set(__self__, "asset_names", asset_names)
        if asset_types is not None:
            pulumi.set(__self__, "asset_types", asset_types)
        if billing_project is not None:
            pulumi.set(__self__, "billing_project", billing_project)
        if condition is not None:
            pulumi.set(__self__, "condition", condition)
        if content_type is not None:
            pulumi.set(__self__, "content_type", content_type)
        if project is not None:
            pulumi.set(__self__, "project", project)

    @property
    @pulumi.getter(name="feedId")
    def feed_id(self) -> pulumi.Input[str]:
        """
        This is the client-assigned asset feed identifier and it needs to be unique under a specific parent.
        """
        return pulumi.get(self, "feed_id")

    @feed_id.setter
    def feed_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "feed_id", value)

    @property
    @pulumi.getter(name="feedOutputConfig")
    def feed_output_config(self) -> pulumi.Input['ProjectFeedFeedOutputConfigArgs']:
        """
        Output configuration for asset feed destination.
        Structure is documented below.
        """
        return pulumi.get(self, "feed_output_config")

    @feed_output_config.setter
    def feed_output_config(self, value: pulumi.Input['ProjectFeedFeedOutputConfigArgs']):
        pulumi.set(self, "feed_output_config", value)

    @property
    @pulumi.getter(name="assetNames")
    def asset_names(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of the full names of the assets to receive updates. You must specify either or both of
        assetNames and assetTypes. Only asset updates matching specified assetNames and assetTypes are
        exported to the feed. For example: //compute.googleapis.com/projects/my_project_123/zones/zone1/instances/instance1.
        See https://cloud.google.com/apis/design/resourceNames#fullResourceName for more info.
        """
        return pulumi.get(self, "asset_names")

    @asset_names.setter
    def asset_names(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "asset_names", value)

    @property
    @pulumi.getter(name="assetTypes")
    def asset_types(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of types of the assets to receive updates. You must specify either or both of assetNames
        and assetTypes. Only asset updates matching specified assetNames and assetTypes are exported to
        the feed. For example: "compute.googleapis.com/Disk"
        See https://cloud.google.com/asset-inventory/docs/supported-asset-types for a list of all
        supported asset types.
        """
        return pulumi.get(self, "asset_types")

    @asset_types.setter
    def asset_types(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "asset_types", value)

    @property
    @pulumi.getter(name="billingProject")
    def billing_project(self) -> Optional[pulumi.Input[str]]:
        """
        The project whose identity will be used when sending messages to the
        destination pubsub topic. It also specifies the project for API
        enablement check, quota, and billing. If not specified, the resource's
        project will be used.
        """
        return pulumi.get(self, "billing_project")

    @billing_project.setter
    def billing_project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "billing_project", value)

    @property
    @pulumi.getter
    def condition(self) -> Optional[pulumi.Input['ProjectFeedConditionArgs']]:
        """
        A condition which determines whether an asset update should be published. If specified, an asset
        will be returned only when the expression evaluates to true. When set, expression field
        must be a valid CEL expression on a TemporalAsset with name temporal_asset. Example: a Feed with
        expression "temporal_asset.deleted == true" will only publish Asset deletions. Other fields of
        condition are optional.
        Structure is documented below.
        """
        return pulumi.get(self, "condition")

    @condition.setter
    def condition(self, value: Optional[pulumi.Input['ProjectFeedConditionArgs']]):
        pulumi.set(self, "condition", value)

    @property
    @pulumi.getter(name="contentType")
    def content_type(self) -> Optional[pulumi.Input[str]]:
        """
        Asset content type. If not specified, no content but the asset name and type will be returned.
        Possible values are: `CONTENT_TYPE_UNSPECIFIED`, `RESOURCE`, `IAM_POLICY`, `ORG_POLICY`, `OS_INVENTORY`, `ACCESS_POLICY`.
        """
        return pulumi.get(self, "content_type")

    @content_type.setter
    def content_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "content_type", value)

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
class _ProjectFeedState:
    def __init__(__self__, *,
                 asset_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 asset_types: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 billing_project: Optional[pulumi.Input[str]] = None,
                 condition: Optional[pulumi.Input['ProjectFeedConditionArgs']] = None,
                 content_type: Optional[pulumi.Input[str]] = None,
                 feed_id: Optional[pulumi.Input[str]] = None,
                 feed_output_config: Optional[pulumi.Input['ProjectFeedFeedOutputConfigArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ProjectFeed resources.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] asset_names: A list of the full names of the assets to receive updates. You must specify either or both of
               assetNames and assetTypes. Only asset updates matching specified assetNames and assetTypes are
               exported to the feed. For example: //compute.googleapis.com/projects/my_project_123/zones/zone1/instances/instance1.
               See https://cloud.google.com/apis/design/resourceNames#fullResourceName for more info.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] asset_types: A list of types of the assets to receive updates. You must specify either or both of assetNames
               and assetTypes. Only asset updates matching specified assetNames and assetTypes are exported to
               the feed. For example: "compute.googleapis.com/Disk"
               See https://cloud.google.com/asset-inventory/docs/supported-asset-types for a list of all
               supported asset types.
        :param pulumi.Input[str] billing_project: The project whose identity will be used when sending messages to the
               destination pubsub topic. It also specifies the project for API
               enablement check, quota, and billing. If not specified, the resource's
               project will be used.
        :param pulumi.Input['ProjectFeedConditionArgs'] condition: A condition which determines whether an asset update should be published. If specified, an asset
               will be returned only when the expression evaluates to true. When set, expression field
               must be a valid CEL expression on a TemporalAsset with name temporal_asset. Example: a Feed with
               expression "temporal_asset.deleted == true" will only publish Asset deletions. Other fields of
               condition are optional.
               Structure is documented below.
        :param pulumi.Input[str] content_type: Asset content type. If not specified, no content but the asset name and type will be returned.
               Possible values are: `CONTENT_TYPE_UNSPECIFIED`, `RESOURCE`, `IAM_POLICY`, `ORG_POLICY`, `OS_INVENTORY`, `ACCESS_POLICY`.
        :param pulumi.Input[str] feed_id: This is the client-assigned asset feed identifier and it needs to be unique under a specific parent.
        :param pulumi.Input['ProjectFeedFeedOutputConfigArgs'] feed_output_config: Output configuration for asset feed destination.
               Structure is documented below.
        :param pulumi.Input[str] name: The format will be projects/{projectNumber}/feeds/{client-assigned_feed_identifier}.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        """
        if asset_names is not None:
            pulumi.set(__self__, "asset_names", asset_names)
        if asset_types is not None:
            pulumi.set(__self__, "asset_types", asset_types)
        if billing_project is not None:
            pulumi.set(__self__, "billing_project", billing_project)
        if condition is not None:
            pulumi.set(__self__, "condition", condition)
        if content_type is not None:
            pulumi.set(__self__, "content_type", content_type)
        if feed_id is not None:
            pulumi.set(__self__, "feed_id", feed_id)
        if feed_output_config is not None:
            pulumi.set(__self__, "feed_output_config", feed_output_config)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if project is not None:
            pulumi.set(__self__, "project", project)

    @property
    @pulumi.getter(name="assetNames")
    def asset_names(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of the full names of the assets to receive updates. You must specify either or both of
        assetNames and assetTypes. Only asset updates matching specified assetNames and assetTypes are
        exported to the feed. For example: //compute.googleapis.com/projects/my_project_123/zones/zone1/instances/instance1.
        See https://cloud.google.com/apis/design/resourceNames#fullResourceName for more info.
        """
        return pulumi.get(self, "asset_names")

    @asset_names.setter
    def asset_names(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "asset_names", value)

    @property
    @pulumi.getter(name="assetTypes")
    def asset_types(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of types of the assets to receive updates. You must specify either or both of assetNames
        and assetTypes. Only asset updates matching specified assetNames and assetTypes are exported to
        the feed. For example: "compute.googleapis.com/Disk"
        See https://cloud.google.com/asset-inventory/docs/supported-asset-types for a list of all
        supported asset types.
        """
        return pulumi.get(self, "asset_types")

    @asset_types.setter
    def asset_types(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "asset_types", value)

    @property
    @pulumi.getter(name="billingProject")
    def billing_project(self) -> Optional[pulumi.Input[str]]:
        """
        The project whose identity will be used when sending messages to the
        destination pubsub topic. It also specifies the project for API
        enablement check, quota, and billing. If not specified, the resource's
        project will be used.
        """
        return pulumi.get(self, "billing_project")

    @billing_project.setter
    def billing_project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "billing_project", value)

    @property
    @pulumi.getter
    def condition(self) -> Optional[pulumi.Input['ProjectFeedConditionArgs']]:
        """
        A condition which determines whether an asset update should be published. If specified, an asset
        will be returned only when the expression evaluates to true. When set, expression field
        must be a valid CEL expression on a TemporalAsset with name temporal_asset. Example: a Feed with
        expression "temporal_asset.deleted == true" will only publish Asset deletions. Other fields of
        condition are optional.
        Structure is documented below.
        """
        return pulumi.get(self, "condition")

    @condition.setter
    def condition(self, value: Optional[pulumi.Input['ProjectFeedConditionArgs']]):
        pulumi.set(self, "condition", value)

    @property
    @pulumi.getter(name="contentType")
    def content_type(self) -> Optional[pulumi.Input[str]]:
        """
        Asset content type. If not specified, no content but the asset name and type will be returned.
        Possible values are: `CONTENT_TYPE_UNSPECIFIED`, `RESOURCE`, `IAM_POLICY`, `ORG_POLICY`, `OS_INVENTORY`, `ACCESS_POLICY`.
        """
        return pulumi.get(self, "content_type")

    @content_type.setter
    def content_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "content_type", value)

    @property
    @pulumi.getter(name="feedId")
    def feed_id(self) -> Optional[pulumi.Input[str]]:
        """
        This is the client-assigned asset feed identifier and it needs to be unique under a specific parent.
        """
        return pulumi.get(self, "feed_id")

    @feed_id.setter
    def feed_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "feed_id", value)

    @property
    @pulumi.getter(name="feedOutputConfig")
    def feed_output_config(self) -> Optional[pulumi.Input['ProjectFeedFeedOutputConfigArgs']]:
        """
        Output configuration for asset feed destination.
        Structure is documented below.
        """
        return pulumi.get(self, "feed_output_config")

    @feed_output_config.setter
    def feed_output_config(self, value: Optional[pulumi.Input['ProjectFeedFeedOutputConfigArgs']]):
        pulumi.set(self, "feed_output_config", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The format will be projects/{projectNumber}/feeds/{client-assigned_feed_identifier}.
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


class ProjectFeed(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 asset_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 asset_types: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 billing_project: Optional[pulumi.Input[str]] = None,
                 condition: Optional[pulumi.Input[pulumi.InputType['ProjectFeedConditionArgs']]] = None,
                 content_type: Optional[pulumi.Input[str]] = None,
                 feed_id: Optional[pulumi.Input[str]] = None,
                 feed_output_config: Optional[pulumi.Input[pulumi.InputType['ProjectFeedFeedOutputConfigArgs']]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Describes a Cloud Asset Inventory feed used to to listen to asset updates.

        To get more information about ProjectFeed, see:

        * [API documentation](https://cloud.google.com/asset-inventory/docs/reference/rest/)
        * How-to Guides
            * [Official Documentation](https://cloud.google.com/asset-inventory/docs)

        ## Example Usage

        ### Cloud Asset Project Feed

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        # The topic where the resource change notifications will be sent.
        feed_output = gcp.pubsub.Topic("feed_output",
            project="my-project-name",
            name="network-updates")
        # Create a feed that sends notifications about network resource updates.
        project_feed = gcp.cloudasset.ProjectFeed("project_feed",
            project="my-project-name",
            feed_id="network-updates",
            content_type="RESOURCE",
            asset_types=[
                "compute.googleapis.com/Subnetwork",
                "compute.googleapis.com/Network",
            ],
            feed_output_config=gcp.cloudasset.ProjectFeedFeedOutputConfigArgs(
                pubsub_destination=gcp.cloudasset.ProjectFeedFeedOutputConfigPubsubDestinationArgs(
                    topic=feed_output.id,
                ),
            ),
            condition=gcp.cloudasset.ProjectFeedConditionArgs(
                expression=\"\"\"!temporal_asset.deleted &&
        temporal_asset.prior_asset_state == google.cloud.asset.v1.TemporalAsset.PriorAssetState.DOES_NOT_EXIST
        \"\"\",
                title="created",
                description="Send notifications on creation events",
            ))
        # Find the project number of the project whose identity will be used for sending
        # the asset change notifications.
        project = gcp.organizations.get_project(project_id="my-project-name")
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        ProjectFeed can be imported using any of these accepted formats:

        * `projects/{{project}}/feeds/{{name}}`

        * `{{project}}/{{name}}`

        * `{{name}}`

        When using the `pulumi import` command, ProjectFeed can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:cloudasset/projectFeed:ProjectFeed default projects/{{project}}/feeds/{{name}}
        ```

        ```sh
        $ pulumi import gcp:cloudasset/projectFeed:ProjectFeed default {{project}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:cloudasset/projectFeed:ProjectFeed default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] asset_names: A list of the full names of the assets to receive updates. You must specify either or both of
               assetNames and assetTypes. Only asset updates matching specified assetNames and assetTypes are
               exported to the feed. For example: //compute.googleapis.com/projects/my_project_123/zones/zone1/instances/instance1.
               See https://cloud.google.com/apis/design/resourceNames#fullResourceName for more info.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] asset_types: A list of types of the assets to receive updates. You must specify either or both of assetNames
               and assetTypes. Only asset updates matching specified assetNames and assetTypes are exported to
               the feed. For example: "compute.googleapis.com/Disk"
               See https://cloud.google.com/asset-inventory/docs/supported-asset-types for a list of all
               supported asset types.
        :param pulumi.Input[str] billing_project: The project whose identity will be used when sending messages to the
               destination pubsub topic. It also specifies the project for API
               enablement check, quota, and billing. If not specified, the resource's
               project will be used.
        :param pulumi.Input[pulumi.InputType['ProjectFeedConditionArgs']] condition: A condition which determines whether an asset update should be published. If specified, an asset
               will be returned only when the expression evaluates to true. When set, expression field
               must be a valid CEL expression on a TemporalAsset with name temporal_asset. Example: a Feed with
               expression "temporal_asset.deleted == true" will only publish Asset deletions. Other fields of
               condition are optional.
               Structure is documented below.
        :param pulumi.Input[str] content_type: Asset content type. If not specified, no content but the asset name and type will be returned.
               Possible values are: `CONTENT_TYPE_UNSPECIFIED`, `RESOURCE`, `IAM_POLICY`, `ORG_POLICY`, `OS_INVENTORY`, `ACCESS_POLICY`.
        :param pulumi.Input[str] feed_id: This is the client-assigned asset feed identifier and it needs to be unique under a specific parent.
        :param pulumi.Input[pulumi.InputType['ProjectFeedFeedOutputConfigArgs']] feed_output_config: Output configuration for asset feed destination.
               Structure is documented below.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ProjectFeedArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Describes a Cloud Asset Inventory feed used to to listen to asset updates.

        To get more information about ProjectFeed, see:

        * [API documentation](https://cloud.google.com/asset-inventory/docs/reference/rest/)
        * How-to Guides
            * [Official Documentation](https://cloud.google.com/asset-inventory/docs)

        ## Example Usage

        ### Cloud Asset Project Feed

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        # The topic where the resource change notifications will be sent.
        feed_output = gcp.pubsub.Topic("feed_output",
            project="my-project-name",
            name="network-updates")
        # Create a feed that sends notifications about network resource updates.
        project_feed = gcp.cloudasset.ProjectFeed("project_feed",
            project="my-project-name",
            feed_id="network-updates",
            content_type="RESOURCE",
            asset_types=[
                "compute.googleapis.com/Subnetwork",
                "compute.googleapis.com/Network",
            ],
            feed_output_config=gcp.cloudasset.ProjectFeedFeedOutputConfigArgs(
                pubsub_destination=gcp.cloudasset.ProjectFeedFeedOutputConfigPubsubDestinationArgs(
                    topic=feed_output.id,
                ),
            ),
            condition=gcp.cloudasset.ProjectFeedConditionArgs(
                expression=\"\"\"!temporal_asset.deleted &&
        temporal_asset.prior_asset_state == google.cloud.asset.v1.TemporalAsset.PriorAssetState.DOES_NOT_EXIST
        \"\"\",
                title="created",
                description="Send notifications on creation events",
            ))
        # Find the project number of the project whose identity will be used for sending
        # the asset change notifications.
        project = gcp.organizations.get_project(project_id="my-project-name")
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        ProjectFeed can be imported using any of these accepted formats:

        * `projects/{{project}}/feeds/{{name}}`

        * `{{project}}/{{name}}`

        * `{{name}}`

        When using the `pulumi import` command, ProjectFeed can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:cloudasset/projectFeed:ProjectFeed default projects/{{project}}/feeds/{{name}}
        ```

        ```sh
        $ pulumi import gcp:cloudasset/projectFeed:ProjectFeed default {{project}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:cloudasset/projectFeed:ProjectFeed default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param ProjectFeedArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ProjectFeedArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 asset_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 asset_types: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 billing_project: Optional[pulumi.Input[str]] = None,
                 condition: Optional[pulumi.Input[pulumi.InputType['ProjectFeedConditionArgs']]] = None,
                 content_type: Optional[pulumi.Input[str]] = None,
                 feed_id: Optional[pulumi.Input[str]] = None,
                 feed_output_config: Optional[pulumi.Input[pulumi.InputType['ProjectFeedFeedOutputConfigArgs']]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ProjectFeedArgs.__new__(ProjectFeedArgs)

            __props__.__dict__["asset_names"] = asset_names
            __props__.__dict__["asset_types"] = asset_types
            __props__.__dict__["billing_project"] = billing_project
            __props__.__dict__["condition"] = condition
            __props__.__dict__["content_type"] = content_type
            if feed_id is None and not opts.urn:
                raise TypeError("Missing required property 'feed_id'")
            __props__.__dict__["feed_id"] = feed_id
            if feed_output_config is None and not opts.urn:
                raise TypeError("Missing required property 'feed_output_config'")
            __props__.__dict__["feed_output_config"] = feed_output_config
            __props__.__dict__["project"] = project
            __props__.__dict__["name"] = None
        super(ProjectFeed, __self__).__init__(
            'gcp:cloudasset/projectFeed:ProjectFeed',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            asset_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            asset_types: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            billing_project: Optional[pulumi.Input[str]] = None,
            condition: Optional[pulumi.Input[pulumi.InputType['ProjectFeedConditionArgs']]] = None,
            content_type: Optional[pulumi.Input[str]] = None,
            feed_id: Optional[pulumi.Input[str]] = None,
            feed_output_config: Optional[pulumi.Input[pulumi.InputType['ProjectFeedFeedOutputConfigArgs']]] = None,
            name: Optional[pulumi.Input[str]] = None,
            project: Optional[pulumi.Input[str]] = None) -> 'ProjectFeed':
        """
        Get an existing ProjectFeed resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] asset_names: A list of the full names of the assets to receive updates. You must specify either or both of
               assetNames and assetTypes. Only asset updates matching specified assetNames and assetTypes are
               exported to the feed. For example: //compute.googleapis.com/projects/my_project_123/zones/zone1/instances/instance1.
               See https://cloud.google.com/apis/design/resourceNames#fullResourceName for more info.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] asset_types: A list of types of the assets to receive updates. You must specify either or both of assetNames
               and assetTypes. Only asset updates matching specified assetNames and assetTypes are exported to
               the feed. For example: "compute.googleapis.com/Disk"
               See https://cloud.google.com/asset-inventory/docs/supported-asset-types for a list of all
               supported asset types.
        :param pulumi.Input[str] billing_project: The project whose identity will be used when sending messages to the
               destination pubsub topic. It also specifies the project for API
               enablement check, quota, and billing. If not specified, the resource's
               project will be used.
        :param pulumi.Input[pulumi.InputType['ProjectFeedConditionArgs']] condition: A condition which determines whether an asset update should be published. If specified, an asset
               will be returned only when the expression evaluates to true. When set, expression field
               must be a valid CEL expression on a TemporalAsset with name temporal_asset. Example: a Feed with
               expression "temporal_asset.deleted == true" will only publish Asset deletions. Other fields of
               condition are optional.
               Structure is documented below.
        :param pulumi.Input[str] content_type: Asset content type. If not specified, no content but the asset name and type will be returned.
               Possible values are: `CONTENT_TYPE_UNSPECIFIED`, `RESOURCE`, `IAM_POLICY`, `ORG_POLICY`, `OS_INVENTORY`, `ACCESS_POLICY`.
        :param pulumi.Input[str] feed_id: This is the client-assigned asset feed identifier and it needs to be unique under a specific parent.
        :param pulumi.Input[pulumi.InputType['ProjectFeedFeedOutputConfigArgs']] feed_output_config: Output configuration for asset feed destination.
               Structure is documented below.
        :param pulumi.Input[str] name: The format will be projects/{projectNumber}/feeds/{client-assigned_feed_identifier}.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ProjectFeedState.__new__(_ProjectFeedState)

        __props__.__dict__["asset_names"] = asset_names
        __props__.__dict__["asset_types"] = asset_types
        __props__.__dict__["billing_project"] = billing_project
        __props__.__dict__["condition"] = condition
        __props__.__dict__["content_type"] = content_type
        __props__.__dict__["feed_id"] = feed_id
        __props__.__dict__["feed_output_config"] = feed_output_config
        __props__.__dict__["name"] = name
        __props__.__dict__["project"] = project
        return ProjectFeed(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="assetNames")
    def asset_names(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        A list of the full names of the assets to receive updates. You must specify either or both of
        assetNames and assetTypes. Only asset updates matching specified assetNames and assetTypes are
        exported to the feed. For example: //compute.googleapis.com/projects/my_project_123/zones/zone1/instances/instance1.
        See https://cloud.google.com/apis/design/resourceNames#fullResourceName for more info.
        """
        return pulumi.get(self, "asset_names")

    @property
    @pulumi.getter(name="assetTypes")
    def asset_types(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        A list of types of the assets to receive updates. You must specify either or both of assetNames
        and assetTypes. Only asset updates matching specified assetNames and assetTypes are exported to
        the feed. For example: "compute.googleapis.com/Disk"
        See https://cloud.google.com/asset-inventory/docs/supported-asset-types for a list of all
        supported asset types.
        """
        return pulumi.get(self, "asset_types")

    @property
    @pulumi.getter(name="billingProject")
    def billing_project(self) -> pulumi.Output[Optional[str]]:
        """
        The project whose identity will be used when sending messages to the
        destination pubsub topic. It also specifies the project for API
        enablement check, quota, and billing. If not specified, the resource's
        project will be used.
        """
        return pulumi.get(self, "billing_project")

    @property
    @pulumi.getter
    def condition(self) -> pulumi.Output[Optional['outputs.ProjectFeedCondition']]:
        """
        A condition which determines whether an asset update should be published. If specified, an asset
        will be returned only when the expression evaluates to true. When set, expression field
        must be a valid CEL expression on a TemporalAsset with name temporal_asset. Example: a Feed with
        expression "temporal_asset.deleted == true" will only publish Asset deletions. Other fields of
        condition are optional.
        Structure is documented below.
        """
        return pulumi.get(self, "condition")

    @property
    @pulumi.getter(name="contentType")
    def content_type(self) -> pulumi.Output[Optional[str]]:
        """
        Asset content type. If not specified, no content but the asset name and type will be returned.
        Possible values are: `CONTENT_TYPE_UNSPECIFIED`, `RESOURCE`, `IAM_POLICY`, `ORG_POLICY`, `OS_INVENTORY`, `ACCESS_POLICY`.
        """
        return pulumi.get(self, "content_type")

    @property
    @pulumi.getter(name="feedId")
    def feed_id(self) -> pulumi.Output[str]:
        """
        This is the client-assigned asset feed identifier and it needs to be unique under a specific parent.
        """
        return pulumi.get(self, "feed_id")

    @property
    @pulumi.getter(name="feedOutputConfig")
    def feed_output_config(self) -> pulumi.Output['outputs.ProjectFeedFeedOutputConfig']:
        """
        Output configuration for asset feed destination.
        Structure is documented below.
        """
        return pulumi.get(self, "feed_output_config")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The format will be projects/{projectNumber}/feeds/{client-assigned_feed_identifier}.
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


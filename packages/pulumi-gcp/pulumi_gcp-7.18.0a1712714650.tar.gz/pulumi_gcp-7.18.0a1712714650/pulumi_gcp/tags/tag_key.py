# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['TagKeyArgs', 'TagKey']

@pulumi.input_type
class TagKeyArgs:
    def __init__(__self__, *,
                 parent: pulumi.Input[str],
                 short_name: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 purpose: Optional[pulumi.Input[str]] = None,
                 purpose_data: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a TagKey resource.
        :param pulumi.Input[str] parent: Input only. The resource name of the new TagKey's parent. Must be of the form organizations/{org_id} or projects/{project_id_or_number}.
        :param pulumi.Input[str] short_name: Input only. The user friendly name for a TagKey. The short name should be unique for TagKeys within the same tag namespace.
               The short name must be 1-63 characters, beginning and ending with an alphanumeric character ([a-z0-9A-Z]) with dashes (-), underscores (_), dots (.), and alphanumerics between.
               
               
               - - -
        :param pulumi.Input[str] description: User-assigned description of the TagKey. Must not exceed 256 characters.
        :param pulumi.Input[str] purpose: Optional. A purpose cannot be changed once set.
               A purpose denotes that this Tag is intended for use in policies of a specific policy engine, and will involve that policy engine in management operations involving this Tag.
               Possible values are: `GCE_FIREWALL`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] purpose_data: Optional. Purpose data cannot be changed once set.
               Purpose data corresponds to the policy system that the tag is intended for. For example, the GCE_FIREWALL purpose expects data in the following format: `network = "<project-name>/<vpc-name>"`.
        """
        pulumi.set(__self__, "parent", parent)
        pulumi.set(__self__, "short_name", short_name)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if purpose is not None:
            pulumi.set(__self__, "purpose", purpose)
        if purpose_data is not None:
            pulumi.set(__self__, "purpose_data", purpose_data)

    @property
    @pulumi.getter
    def parent(self) -> pulumi.Input[str]:
        """
        Input only. The resource name of the new TagKey's parent. Must be of the form organizations/{org_id} or projects/{project_id_or_number}.
        """
        return pulumi.get(self, "parent")

    @parent.setter
    def parent(self, value: pulumi.Input[str]):
        pulumi.set(self, "parent", value)

    @property
    @pulumi.getter(name="shortName")
    def short_name(self) -> pulumi.Input[str]:
        """
        Input only. The user friendly name for a TagKey. The short name should be unique for TagKeys within the same tag namespace.
        The short name must be 1-63 characters, beginning and ending with an alphanumeric character ([a-z0-9A-Z]) with dashes (-), underscores (_), dots (.), and alphanumerics between.


        - - -
        """
        return pulumi.get(self, "short_name")

    @short_name.setter
    def short_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "short_name", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        User-assigned description of the TagKey. Must not exceed 256 characters.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def purpose(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. A purpose cannot be changed once set.
        A purpose denotes that this Tag is intended for use in policies of a specific policy engine, and will involve that policy engine in management operations involving this Tag.
        Possible values are: `GCE_FIREWALL`.
        """
        return pulumi.get(self, "purpose")

    @purpose.setter
    def purpose(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "purpose", value)

    @property
    @pulumi.getter(name="purposeData")
    def purpose_data(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Optional. Purpose data cannot be changed once set.
        Purpose data corresponds to the policy system that the tag is intended for. For example, the GCE_FIREWALL purpose expects data in the following format: `network = "<project-name>/<vpc-name>"`.
        """
        return pulumi.get(self, "purpose_data")

    @purpose_data.setter
    def purpose_data(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "purpose_data", value)


@pulumi.input_type
class _TagKeyState:
    def __init__(__self__, *,
                 create_time: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 namespaced_name: Optional[pulumi.Input[str]] = None,
                 parent: Optional[pulumi.Input[str]] = None,
                 purpose: Optional[pulumi.Input[str]] = None,
                 purpose_data: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 short_name: Optional[pulumi.Input[str]] = None,
                 update_time: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering TagKey resources.
        :param pulumi.Input[str] create_time: Output only. Creation time.
               A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z".
        :param pulumi.Input[str] description: User-assigned description of the TagKey. Must not exceed 256 characters.
        :param pulumi.Input[str] name: The generated numeric id for the TagKey.
        :param pulumi.Input[str] namespaced_name: Output only. Namespaced name of the TagKey.
        :param pulumi.Input[str] parent: Input only. The resource name of the new TagKey's parent. Must be of the form organizations/{org_id} or projects/{project_id_or_number}.
        :param pulumi.Input[str] purpose: Optional. A purpose cannot be changed once set.
               A purpose denotes that this Tag is intended for use in policies of a specific policy engine, and will involve that policy engine in management operations involving this Tag.
               Possible values are: `GCE_FIREWALL`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] purpose_data: Optional. Purpose data cannot be changed once set.
               Purpose data corresponds to the policy system that the tag is intended for. For example, the GCE_FIREWALL purpose expects data in the following format: `network = "<project-name>/<vpc-name>"`.
        :param pulumi.Input[str] short_name: Input only. The user friendly name for a TagKey. The short name should be unique for TagKeys within the same tag namespace.
               The short name must be 1-63 characters, beginning and ending with an alphanumeric character ([a-z0-9A-Z]) with dashes (-), underscores (_), dots (.), and alphanumerics between.
               
               
               - - -
        :param pulumi.Input[str] update_time: Output only. Update time.
               A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z".
        """
        if create_time is not None:
            pulumi.set(__self__, "create_time", create_time)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if namespaced_name is not None:
            pulumi.set(__self__, "namespaced_name", namespaced_name)
        if parent is not None:
            pulumi.set(__self__, "parent", parent)
        if purpose is not None:
            pulumi.set(__self__, "purpose", purpose)
        if purpose_data is not None:
            pulumi.set(__self__, "purpose_data", purpose_data)
        if short_name is not None:
            pulumi.set(__self__, "short_name", short_name)
        if update_time is not None:
            pulumi.set(__self__, "update_time", update_time)

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> Optional[pulumi.Input[str]]:
        """
        Output only. Creation time.
        A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z".
        """
        return pulumi.get(self, "create_time")

    @create_time.setter
    def create_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "create_time", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        User-assigned description of the TagKey. Must not exceed 256 characters.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The generated numeric id for the TagKey.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="namespacedName")
    def namespaced_name(self) -> Optional[pulumi.Input[str]]:
        """
        Output only. Namespaced name of the TagKey.
        """
        return pulumi.get(self, "namespaced_name")

    @namespaced_name.setter
    def namespaced_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "namespaced_name", value)

    @property
    @pulumi.getter
    def parent(self) -> Optional[pulumi.Input[str]]:
        """
        Input only. The resource name of the new TagKey's parent. Must be of the form organizations/{org_id} or projects/{project_id_or_number}.
        """
        return pulumi.get(self, "parent")

    @parent.setter
    def parent(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "parent", value)

    @property
    @pulumi.getter
    def purpose(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. A purpose cannot be changed once set.
        A purpose denotes that this Tag is intended for use in policies of a specific policy engine, and will involve that policy engine in management operations involving this Tag.
        Possible values are: `GCE_FIREWALL`.
        """
        return pulumi.get(self, "purpose")

    @purpose.setter
    def purpose(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "purpose", value)

    @property
    @pulumi.getter(name="purposeData")
    def purpose_data(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Optional. Purpose data cannot be changed once set.
        Purpose data corresponds to the policy system that the tag is intended for. For example, the GCE_FIREWALL purpose expects data in the following format: `network = "<project-name>/<vpc-name>"`.
        """
        return pulumi.get(self, "purpose_data")

    @purpose_data.setter
    def purpose_data(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "purpose_data", value)

    @property
    @pulumi.getter(name="shortName")
    def short_name(self) -> Optional[pulumi.Input[str]]:
        """
        Input only. The user friendly name for a TagKey. The short name should be unique for TagKeys within the same tag namespace.
        The short name must be 1-63 characters, beginning and ending with an alphanumeric character ([a-z0-9A-Z]) with dashes (-), underscores (_), dots (.), and alphanumerics between.


        - - -
        """
        return pulumi.get(self, "short_name")

    @short_name.setter
    def short_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "short_name", value)

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> Optional[pulumi.Input[str]]:
        """
        Output only. Update time.
        A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z".
        """
        return pulumi.get(self, "update_time")

    @update_time.setter
    def update_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "update_time", value)


class TagKey(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 parent: Optional[pulumi.Input[str]] = None,
                 purpose: Optional[pulumi.Input[str]] = None,
                 purpose_data: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 short_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        A TagKey, used to group a set of TagValues.

        To get more information about TagKey, see:

        * [API documentation](https://cloud.google.com/resource-manager/reference/rest/v3/tagKeys)
        * How-to Guides
            * [Official Documentation](https://cloud.google.com/resource-manager/docs/tags/tags-creating-and-managing)

        ## Example Usage

        ### Tag Key Basic

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        key = gcp.tags.TagKey("key",
            parent="organizations/123456789",
            short_name="keyname",
            description="For keyname resources.")
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        TagKey can be imported using any of these accepted formats:

        * `tagKeys/{{name}}`

        * `{{name}}`

        When using the `pulumi import` command, TagKey can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:tags/tagKey:TagKey default tagKeys/{{name}}
        ```

        ```sh
        $ pulumi import gcp:tags/tagKey:TagKey default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: User-assigned description of the TagKey. Must not exceed 256 characters.
        :param pulumi.Input[str] parent: Input only. The resource name of the new TagKey's parent. Must be of the form organizations/{org_id} or projects/{project_id_or_number}.
        :param pulumi.Input[str] purpose: Optional. A purpose cannot be changed once set.
               A purpose denotes that this Tag is intended for use in policies of a specific policy engine, and will involve that policy engine in management operations involving this Tag.
               Possible values are: `GCE_FIREWALL`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] purpose_data: Optional. Purpose data cannot be changed once set.
               Purpose data corresponds to the policy system that the tag is intended for. For example, the GCE_FIREWALL purpose expects data in the following format: `network = "<project-name>/<vpc-name>"`.
        :param pulumi.Input[str] short_name: Input only. The user friendly name for a TagKey. The short name should be unique for TagKeys within the same tag namespace.
               The short name must be 1-63 characters, beginning and ending with an alphanumeric character ([a-z0-9A-Z]) with dashes (-), underscores (_), dots (.), and alphanumerics between.
               
               
               - - -
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: TagKeyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        A TagKey, used to group a set of TagValues.

        To get more information about TagKey, see:

        * [API documentation](https://cloud.google.com/resource-manager/reference/rest/v3/tagKeys)
        * How-to Guides
            * [Official Documentation](https://cloud.google.com/resource-manager/docs/tags/tags-creating-and-managing)

        ## Example Usage

        ### Tag Key Basic

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        key = gcp.tags.TagKey("key",
            parent="organizations/123456789",
            short_name="keyname",
            description="For keyname resources.")
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        TagKey can be imported using any of these accepted formats:

        * `tagKeys/{{name}}`

        * `{{name}}`

        When using the `pulumi import` command, TagKey can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:tags/tagKey:TagKey default tagKeys/{{name}}
        ```

        ```sh
        $ pulumi import gcp:tags/tagKey:TagKey default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param TagKeyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(TagKeyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 parent: Optional[pulumi.Input[str]] = None,
                 purpose: Optional[pulumi.Input[str]] = None,
                 purpose_data: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 short_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = TagKeyArgs.__new__(TagKeyArgs)

            __props__.__dict__["description"] = description
            if parent is None and not opts.urn:
                raise TypeError("Missing required property 'parent'")
            __props__.__dict__["parent"] = parent
            __props__.__dict__["purpose"] = purpose
            __props__.__dict__["purpose_data"] = purpose_data
            if short_name is None and not opts.urn:
                raise TypeError("Missing required property 'short_name'")
            __props__.__dict__["short_name"] = short_name
            __props__.__dict__["create_time"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["namespaced_name"] = None
            __props__.__dict__["update_time"] = None
        super(TagKey, __self__).__init__(
            'gcp:tags/tagKey:TagKey',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            create_time: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            namespaced_name: Optional[pulumi.Input[str]] = None,
            parent: Optional[pulumi.Input[str]] = None,
            purpose: Optional[pulumi.Input[str]] = None,
            purpose_data: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            short_name: Optional[pulumi.Input[str]] = None,
            update_time: Optional[pulumi.Input[str]] = None) -> 'TagKey':
        """
        Get an existing TagKey resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] create_time: Output only. Creation time.
               A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z".
        :param pulumi.Input[str] description: User-assigned description of the TagKey. Must not exceed 256 characters.
        :param pulumi.Input[str] name: The generated numeric id for the TagKey.
        :param pulumi.Input[str] namespaced_name: Output only. Namespaced name of the TagKey.
        :param pulumi.Input[str] parent: Input only. The resource name of the new TagKey's parent. Must be of the form organizations/{org_id} or projects/{project_id_or_number}.
        :param pulumi.Input[str] purpose: Optional. A purpose cannot be changed once set.
               A purpose denotes that this Tag is intended for use in policies of a specific policy engine, and will involve that policy engine in management operations involving this Tag.
               Possible values are: `GCE_FIREWALL`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] purpose_data: Optional. Purpose data cannot be changed once set.
               Purpose data corresponds to the policy system that the tag is intended for. For example, the GCE_FIREWALL purpose expects data in the following format: `network = "<project-name>/<vpc-name>"`.
        :param pulumi.Input[str] short_name: Input only. The user friendly name for a TagKey. The short name should be unique for TagKeys within the same tag namespace.
               The short name must be 1-63 characters, beginning and ending with an alphanumeric character ([a-z0-9A-Z]) with dashes (-), underscores (_), dots (.), and alphanumerics between.
               
               
               - - -
        :param pulumi.Input[str] update_time: Output only. Update time.
               A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z".
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _TagKeyState.__new__(_TagKeyState)

        __props__.__dict__["create_time"] = create_time
        __props__.__dict__["description"] = description
        __props__.__dict__["name"] = name
        __props__.__dict__["namespaced_name"] = namespaced_name
        __props__.__dict__["parent"] = parent
        __props__.__dict__["purpose"] = purpose
        __props__.__dict__["purpose_data"] = purpose_data
        __props__.__dict__["short_name"] = short_name
        __props__.__dict__["update_time"] = update_time
        return TagKey(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> pulumi.Output[str]:
        """
        Output only. Creation time.
        A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z".
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        User-assigned description of the TagKey. Must not exceed 256 characters.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The generated numeric id for the TagKey.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="namespacedName")
    def namespaced_name(self) -> pulumi.Output[str]:
        """
        Output only. Namespaced name of the TagKey.
        """
        return pulumi.get(self, "namespaced_name")

    @property
    @pulumi.getter
    def parent(self) -> pulumi.Output[str]:
        """
        Input only. The resource name of the new TagKey's parent. Must be of the form organizations/{org_id} or projects/{project_id_or_number}.
        """
        return pulumi.get(self, "parent")

    @property
    @pulumi.getter
    def purpose(self) -> pulumi.Output[Optional[str]]:
        """
        Optional. A purpose cannot be changed once set.
        A purpose denotes that this Tag is intended for use in policies of a specific policy engine, and will involve that policy engine in management operations involving this Tag.
        Possible values are: `GCE_FIREWALL`.
        """
        return pulumi.get(self, "purpose")

    @property
    @pulumi.getter(name="purposeData")
    def purpose_data(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Optional. Purpose data cannot be changed once set.
        Purpose data corresponds to the policy system that the tag is intended for. For example, the GCE_FIREWALL purpose expects data in the following format: `network = "<project-name>/<vpc-name>"`.
        """
        return pulumi.get(self, "purpose_data")

    @property
    @pulumi.getter(name="shortName")
    def short_name(self) -> pulumi.Output[str]:
        """
        Input only. The user friendly name for a TagKey. The short name should be unique for TagKeys within the same tag namespace.
        The short name must be 1-63 characters, beginning and ending with an alphanumeric character ([a-z0-9A-Z]) with dashes (-), underscores (_), dots (.), and alphanumerics between.


        - - -
        """
        return pulumi.get(self, "short_name")

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> pulumi.Output[str]:
        """
        Output only. Update time.
        A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z".
        """
        return pulumi.get(self, "update_time")


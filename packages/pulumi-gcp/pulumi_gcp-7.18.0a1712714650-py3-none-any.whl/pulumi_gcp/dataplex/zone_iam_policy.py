# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['ZoneIamPolicyArgs', 'ZoneIamPolicy']

@pulumi.input_type
class ZoneIamPolicyArgs:
    def __init__(__self__, *,
                 dataplex_zone: pulumi.Input[str],
                 lake: pulumi.Input[str],
                 policy_data: pulumi.Input[str],
                 location: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a ZoneIamPolicy resource.
        :param pulumi.Input[str] dataplex_zone: Used to find the parent resource to bind the IAM policy to
        :param pulumi.Input[str] policy_data: The policy data generated by
               a `organizations_get_iam_policy` data source.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the project will be parsed from the identifier of the parent resource. If no project is provided in the parent identifier and no project is specified, the provider project is used.
               
               * `member/members` - (Required) Identities that will be granted the privilege in `role`.
               Each entry can have one of the following values:
               * **allUsers**: A special identifier that represents anyone who is on the internet; with or without a Google account.
               * **allAuthenticatedUsers**: A special identifier that represents anyone who is authenticated with a Google account or a service account.
               * **user:{emailid}**: An email address that represents a specific Google account. For example, alice@gmail.com or joe@example.com.
               * **serviceAccount:{emailid}**: An email address that represents a service account. For example, my-other-app@appspot.gserviceaccount.com.
               * **group:{emailid}**: An email address that represents a Google group. For example, admins@example.com.
               * **domain:{domain}**: A G Suite domain (primary, instead of alias) name that represents all the users of that domain. For example, google.com or example.com.
               * **projectOwner:projectid**: Owners of the given project. For example, "projectOwner:my-example-project"
               * **projectEditor:projectid**: Editors of the given project. For example, "projectEditor:my-example-project"
               * **projectViewer:projectid**: Viewers of the given project. For example, "projectViewer:my-example-project"
        """
        pulumi.set(__self__, "dataplex_zone", dataplex_zone)
        pulumi.set(__self__, "lake", lake)
        pulumi.set(__self__, "policy_data", policy_data)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if project is not None:
            pulumi.set(__self__, "project", project)

    @property
    @pulumi.getter(name="dataplexZone")
    def dataplex_zone(self) -> pulumi.Input[str]:
        """
        Used to find the parent resource to bind the IAM policy to
        """
        return pulumi.get(self, "dataplex_zone")

    @dataplex_zone.setter
    def dataplex_zone(self, value: pulumi.Input[str]):
        pulumi.set(self, "dataplex_zone", value)

    @property
    @pulumi.getter
    def lake(self) -> pulumi.Input[str]:
        return pulumi.get(self, "lake")

    @lake.setter
    def lake(self, value: pulumi.Input[str]):
        pulumi.set(self, "lake", value)

    @property
    @pulumi.getter(name="policyData")
    def policy_data(self) -> pulumi.Input[str]:
        """
        The policy data generated by
        a `organizations_get_iam_policy` data source.
        """
        return pulumi.get(self, "policy_data")

    @policy_data.setter
    def policy_data(self, value: pulumi.Input[str]):
        pulumi.set(self, "policy_data", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the project in which the resource belongs.
        If it is not provided, the project will be parsed from the identifier of the parent resource. If no project is provided in the parent identifier and no project is specified, the provider project is used.

        * `member/members` - (Required) Identities that will be granted the privilege in `role`.
        Each entry can have one of the following values:
        * **allUsers**: A special identifier that represents anyone who is on the internet; with or without a Google account.
        * **allAuthenticatedUsers**: A special identifier that represents anyone who is authenticated with a Google account or a service account.
        * **user:{emailid}**: An email address that represents a specific Google account. For example, alice@gmail.com or joe@example.com.
        * **serviceAccount:{emailid}**: An email address that represents a service account. For example, my-other-app@appspot.gserviceaccount.com.
        * **group:{emailid}**: An email address that represents a Google group. For example, admins@example.com.
        * **domain:{domain}**: A G Suite domain (primary, instead of alias) name that represents all the users of that domain. For example, google.com or example.com.
        * **projectOwner:projectid**: Owners of the given project. For example, "projectOwner:my-example-project"
        * **projectEditor:projectid**: Editors of the given project. For example, "projectEditor:my-example-project"
        * **projectViewer:projectid**: Viewers of the given project. For example, "projectViewer:my-example-project"
        """
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)


@pulumi.input_type
class _ZoneIamPolicyState:
    def __init__(__self__, *,
                 dataplex_zone: Optional[pulumi.Input[str]] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 lake: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 policy_data: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ZoneIamPolicy resources.
        :param pulumi.Input[str] dataplex_zone: Used to find the parent resource to bind the IAM policy to
        :param pulumi.Input[str] etag: (Computed) The etag of the IAM policy.
        :param pulumi.Input[str] policy_data: The policy data generated by
               a `organizations_get_iam_policy` data source.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the project will be parsed from the identifier of the parent resource. If no project is provided in the parent identifier and no project is specified, the provider project is used.
               
               * `member/members` - (Required) Identities that will be granted the privilege in `role`.
               Each entry can have one of the following values:
               * **allUsers**: A special identifier that represents anyone who is on the internet; with or without a Google account.
               * **allAuthenticatedUsers**: A special identifier that represents anyone who is authenticated with a Google account or a service account.
               * **user:{emailid}**: An email address that represents a specific Google account. For example, alice@gmail.com or joe@example.com.
               * **serviceAccount:{emailid}**: An email address that represents a service account. For example, my-other-app@appspot.gserviceaccount.com.
               * **group:{emailid}**: An email address that represents a Google group. For example, admins@example.com.
               * **domain:{domain}**: A G Suite domain (primary, instead of alias) name that represents all the users of that domain. For example, google.com or example.com.
               * **projectOwner:projectid**: Owners of the given project. For example, "projectOwner:my-example-project"
               * **projectEditor:projectid**: Editors of the given project. For example, "projectEditor:my-example-project"
               * **projectViewer:projectid**: Viewers of the given project. For example, "projectViewer:my-example-project"
        """
        if dataplex_zone is not None:
            pulumi.set(__self__, "dataplex_zone", dataplex_zone)
        if etag is not None:
            pulumi.set(__self__, "etag", etag)
        if lake is not None:
            pulumi.set(__self__, "lake", lake)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if policy_data is not None:
            pulumi.set(__self__, "policy_data", policy_data)
        if project is not None:
            pulumi.set(__self__, "project", project)

    @property
    @pulumi.getter(name="dataplexZone")
    def dataplex_zone(self) -> Optional[pulumi.Input[str]]:
        """
        Used to find the parent resource to bind the IAM policy to
        """
        return pulumi.get(self, "dataplex_zone")

    @dataplex_zone.setter
    def dataplex_zone(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "dataplex_zone", value)

    @property
    @pulumi.getter
    def etag(self) -> Optional[pulumi.Input[str]]:
        """
        (Computed) The etag of the IAM policy.
        """
        return pulumi.get(self, "etag")

    @etag.setter
    def etag(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "etag", value)

    @property
    @pulumi.getter
    def lake(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "lake")

    @lake.setter
    def lake(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "lake", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="policyData")
    def policy_data(self) -> Optional[pulumi.Input[str]]:
        """
        The policy data generated by
        a `organizations_get_iam_policy` data source.
        """
        return pulumi.get(self, "policy_data")

    @policy_data.setter
    def policy_data(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "policy_data", value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the project in which the resource belongs.
        If it is not provided, the project will be parsed from the identifier of the parent resource. If no project is provided in the parent identifier and no project is specified, the provider project is used.

        * `member/members` - (Required) Identities that will be granted the privilege in `role`.
        Each entry can have one of the following values:
        * **allUsers**: A special identifier that represents anyone who is on the internet; with or without a Google account.
        * **allAuthenticatedUsers**: A special identifier that represents anyone who is authenticated with a Google account or a service account.
        * **user:{emailid}**: An email address that represents a specific Google account. For example, alice@gmail.com or joe@example.com.
        * **serviceAccount:{emailid}**: An email address that represents a service account. For example, my-other-app@appspot.gserviceaccount.com.
        * **group:{emailid}**: An email address that represents a Google group. For example, admins@example.com.
        * **domain:{domain}**: A G Suite domain (primary, instead of alias) name that represents all the users of that domain. For example, google.com or example.com.
        * **projectOwner:projectid**: Owners of the given project. For example, "projectOwner:my-example-project"
        * **projectEditor:projectid**: Editors of the given project. For example, "projectEditor:my-example-project"
        * **projectViewer:projectid**: Viewers of the given project. For example, "projectViewer:my-example-project"
        """
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)


class ZoneIamPolicy(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 dataplex_zone: Optional[pulumi.Input[str]] = None,
                 lake: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 policy_data: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Three different resources help you manage your IAM policy for Dataplex Zone. Each of these resources serves a different use case:

        * `dataplex.ZoneIamPolicy`: Authoritative. Sets the IAM policy for the zone and replaces any existing policy already attached.
        * `dataplex.ZoneIamBinding`: Authoritative for a given role. Updates the IAM policy to grant a role to a list of members. Other roles within the IAM policy for the zone are preserved.
        * `dataplex.ZoneIamMember`: Non-authoritative. Updates the IAM policy to grant a role to a new member. Other members for the role for the zone are preserved.

        A data source can be used to retrieve policy data in advent you do not need creation

        * `dataplex.ZoneIamPolicy`: Retrieves the IAM policy for the zone

        > **Note:** `dataplex.ZoneIamPolicy` **cannot** be used in conjunction with `dataplex.ZoneIamBinding` and `dataplex.ZoneIamMember` or they will fight over what your policy should be.

        > **Note:** `dataplex.ZoneIamBinding` resources **can be** used in conjunction with `dataplex.ZoneIamMember` resources **only if** they do not grant privilege to the same role.

        ## google\\_dataplex\\_zone\\_iam\\_policy

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        admin = gcp.organizations.get_iam_policy(bindings=[gcp.organizations.GetIAMPolicyBindingArgs(
            role="roles/viewer",
            members=["user:jane@example.com"],
        )])
        policy = gcp.dataplex.ZoneIamPolicy("policy",
            project=example["project"],
            location=example["location"],
            lake=example["lake"],
            dataplex_zone=example["name"],
            policy_data=admin.policy_data)
        ```
        <!--End PulumiCodeChooser -->

        ## google\\_dataplex\\_zone\\_iam\\_binding

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        binding = gcp.dataplex.ZoneIamBinding("binding",
            project=example["project"],
            location=example["location"],
            lake=example["lake"],
            dataplex_zone=example["name"],
            role="roles/viewer",
            members=["user:jane@example.com"])
        ```
        <!--End PulumiCodeChooser -->

        ## google\\_dataplex\\_zone\\_iam\\_member

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        member = gcp.dataplex.ZoneIamMember("member",
            project=example["project"],
            location=example["location"],
            lake=example["lake"],
            dataplex_zone=example["name"],
            role="roles/viewer",
            member="user:jane@example.com")
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        For all import syntaxes, the "resource in question" can take any of the following forms:

        * projects/{{project}}/locations/{{location}}/lakes/{{lake}}/zones/{{name}}

        * {{project}}/{{location}}/{{lake}}/{{name}}

        * {{location}}/{{lake}}/{{name}}

        * {{name}}

        Any variables not passed in the import command will be taken from the provider configuration.

        Dataplex zone IAM resources can be imported using the resource identifiers, role, and member.

        IAM member imports use space-delimited identifiers: the resource in question, the role, and the member identity, e.g.

        ```sh
        $ pulumi import gcp:dataplex/zoneIamPolicy:ZoneIamPolicy editor "projects/{{project}}/locations/{{location}}/lakes/{{lake}}/zones/{{zone}} roles/viewer user:jane@example.com"
        ```

        IAM binding imports use space-delimited identifiers: the resource in question and the role, e.g.

        ```sh
        $ pulumi import gcp:dataplex/zoneIamPolicy:ZoneIamPolicy editor "projects/{{project}}/locations/{{location}}/lakes/{{lake}}/zones/{{zone}} roles/viewer"
        ```

        IAM policy imports use the identifier of the resource in question, e.g.

        ```sh
        $ pulumi import gcp:dataplex/zoneIamPolicy:ZoneIamPolicy editor projects/{{project}}/locations/{{location}}/lakes/{{lake}}/zones/{{zone}}
        ```

        -> **Custom Roles**: If you're importing a IAM resource with a custom role, make sure to use the

         full name of the custom role, e.g. `[projects/my-project|organizations/my-org]/roles/my-custom-role`.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] dataplex_zone: Used to find the parent resource to bind the IAM policy to
        :param pulumi.Input[str] policy_data: The policy data generated by
               a `organizations_get_iam_policy` data source.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the project will be parsed from the identifier of the parent resource. If no project is provided in the parent identifier and no project is specified, the provider project is used.
               
               * `member/members` - (Required) Identities that will be granted the privilege in `role`.
               Each entry can have one of the following values:
               * **allUsers**: A special identifier that represents anyone who is on the internet; with or without a Google account.
               * **allAuthenticatedUsers**: A special identifier that represents anyone who is authenticated with a Google account or a service account.
               * **user:{emailid}**: An email address that represents a specific Google account. For example, alice@gmail.com or joe@example.com.
               * **serviceAccount:{emailid}**: An email address that represents a service account. For example, my-other-app@appspot.gserviceaccount.com.
               * **group:{emailid}**: An email address that represents a Google group. For example, admins@example.com.
               * **domain:{domain}**: A G Suite domain (primary, instead of alias) name that represents all the users of that domain. For example, google.com or example.com.
               * **projectOwner:projectid**: Owners of the given project. For example, "projectOwner:my-example-project"
               * **projectEditor:projectid**: Editors of the given project. For example, "projectEditor:my-example-project"
               * **projectViewer:projectid**: Viewers of the given project. For example, "projectViewer:my-example-project"
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ZoneIamPolicyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Three different resources help you manage your IAM policy for Dataplex Zone. Each of these resources serves a different use case:

        * `dataplex.ZoneIamPolicy`: Authoritative. Sets the IAM policy for the zone and replaces any existing policy already attached.
        * `dataplex.ZoneIamBinding`: Authoritative for a given role. Updates the IAM policy to grant a role to a list of members. Other roles within the IAM policy for the zone are preserved.
        * `dataplex.ZoneIamMember`: Non-authoritative. Updates the IAM policy to grant a role to a new member. Other members for the role for the zone are preserved.

        A data source can be used to retrieve policy data in advent you do not need creation

        * `dataplex.ZoneIamPolicy`: Retrieves the IAM policy for the zone

        > **Note:** `dataplex.ZoneIamPolicy` **cannot** be used in conjunction with `dataplex.ZoneIamBinding` and `dataplex.ZoneIamMember` or they will fight over what your policy should be.

        > **Note:** `dataplex.ZoneIamBinding` resources **can be** used in conjunction with `dataplex.ZoneIamMember` resources **only if** they do not grant privilege to the same role.

        ## google\\_dataplex\\_zone\\_iam\\_policy

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        admin = gcp.organizations.get_iam_policy(bindings=[gcp.organizations.GetIAMPolicyBindingArgs(
            role="roles/viewer",
            members=["user:jane@example.com"],
        )])
        policy = gcp.dataplex.ZoneIamPolicy("policy",
            project=example["project"],
            location=example["location"],
            lake=example["lake"],
            dataplex_zone=example["name"],
            policy_data=admin.policy_data)
        ```
        <!--End PulumiCodeChooser -->

        ## google\\_dataplex\\_zone\\_iam\\_binding

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        binding = gcp.dataplex.ZoneIamBinding("binding",
            project=example["project"],
            location=example["location"],
            lake=example["lake"],
            dataplex_zone=example["name"],
            role="roles/viewer",
            members=["user:jane@example.com"])
        ```
        <!--End PulumiCodeChooser -->

        ## google\\_dataplex\\_zone\\_iam\\_member

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        member = gcp.dataplex.ZoneIamMember("member",
            project=example["project"],
            location=example["location"],
            lake=example["lake"],
            dataplex_zone=example["name"],
            role="roles/viewer",
            member="user:jane@example.com")
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        For all import syntaxes, the "resource in question" can take any of the following forms:

        * projects/{{project}}/locations/{{location}}/lakes/{{lake}}/zones/{{name}}

        * {{project}}/{{location}}/{{lake}}/{{name}}

        * {{location}}/{{lake}}/{{name}}

        * {{name}}

        Any variables not passed in the import command will be taken from the provider configuration.

        Dataplex zone IAM resources can be imported using the resource identifiers, role, and member.

        IAM member imports use space-delimited identifiers: the resource in question, the role, and the member identity, e.g.

        ```sh
        $ pulumi import gcp:dataplex/zoneIamPolicy:ZoneIamPolicy editor "projects/{{project}}/locations/{{location}}/lakes/{{lake}}/zones/{{zone}} roles/viewer user:jane@example.com"
        ```

        IAM binding imports use space-delimited identifiers: the resource in question and the role, e.g.

        ```sh
        $ pulumi import gcp:dataplex/zoneIamPolicy:ZoneIamPolicy editor "projects/{{project}}/locations/{{location}}/lakes/{{lake}}/zones/{{zone}} roles/viewer"
        ```

        IAM policy imports use the identifier of the resource in question, e.g.

        ```sh
        $ pulumi import gcp:dataplex/zoneIamPolicy:ZoneIamPolicy editor projects/{{project}}/locations/{{location}}/lakes/{{lake}}/zones/{{zone}}
        ```

        -> **Custom Roles**: If you're importing a IAM resource with a custom role, make sure to use the

         full name of the custom role, e.g. `[projects/my-project|organizations/my-org]/roles/my-custom-role`.

        :param str resource_name: The name of the resource.
        :param ZoneIamPolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ZoneIamPolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 dataplex_zone: Optional[pulumi.Input[str]] = None,
                 lake: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 policy_data: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ZoneIamPolicyArgs.__new__(ZoneIamPolicyArgs)

            if dataplex_zone is None and not opts.urn:
                raise TypeError("Missing required property 'dataplex_zone'")
            __props__.__dict__["dataplex_zone"] = dataplex_zone
            if lake is None and not opts.urn:
                raise TypeError("Missing required property 'lake'")
            __props__.__dict__["lake"] = lake
            __props__.__dict__["location"] = location
            if policy_data is None and not opts.urn:
                raise TypeError("Missing required property 'policy_data'")
            __props__.__dict__["policy_data"] = policy_data
            __props__.__dict__["project"] = project
            __props__.__dict__["etag"] = None
        super(ZoneIamPolicy, __self__).__init__(
            'gcp:dataplex/zoneIamPolicy:ZoneIamPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            dataplex_zone: Optional[pulumi.Input[str]] = None,
            etag: Optional[pulumi.Input[str]] = None,
            lake: Optional[pulumi.Input[str]] = None,
            location: Optional[pulumi.Input[str]] = None,
            policy_data: Optional[pulumi.Input[str]] = None,
            project: Optional[pulumi.Input[str]] = None) -> 'ZoneIamPolicy':
        """
        Get an existing ZoneIamPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] dataplex_zone: Used to find the parent resource to bind the IAM policy to
        :param pulumi.Input[str] etag: (Computed) The etag of the IAM policy.
        :param pulumi.Input[str] policy_data: The policy data generated by
               a `organizations_get_iam_policy` data source.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the project will be parsed from the identifier of the parent resource. If no project is provided in the parent identifier and no project is specified, the provider project is used.
               
               * `member/members` - (Required) Identities that will be granted the privilege in `role`.
               Each entry can have one of the following values:
               * **allUsers**: A special identifier that represents anyone who is on the internet; with or without a Google account.
               * **allAuthenticatedUsers**: A special identifier that represents anyone who is authenticated with a Google account or a service account.
               * **user:{emailid}**: An email address that represents a specific Google account. For example, alice@gmail.com or joe@example.com.
               * **serviceAccount:{emailid}**: An email address that represents a service account. For example, my-other-app@appspot.gserviceaccount.com.
               * **group:{emailid}**: An email address that represents a Google group. For example, admins@example.com.
               * **domain:{domain}**: A G Suite domain (primary, instead of alias) name that represents all the users of that domain. For example, google.com or example.com.
               * **projectOwner:projectid**: Owners of the given project. For example, "projectOwner:my-example-project"
               * **projectEditor:projectid**: Editors of the given project. For example, "projectEditor:my-example-project"
               * **projectViewer:projectid**: Viewers of the given project. For example, "projectViewer:my-example-project"
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ZoneIamPolicyState.__new__(_ZoneIamPolicyState)

        __props__.__dict__["dataplex_zone"] = dataplex_zone
        __props__.__dict__["etag"] = etag
        __props__.__dict__["lake"] = lake
        __props__.__dict__["location"] = location
        __props__.__dict__["policy_data"] = policy_data
        __props__.__dict__["project"] = project
        return ZoneIamPolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="dataplexZone")
    def dataplex_zone(self) -> pulumi.Output[str]:
        """
        Used to find the parent resource to bind the IAM policy to
        """
        return pulumi.get(self, "dataplex_zone")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        (Computed) The etag of the IAM policy.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def lake(self) -> pulumi.Output[str]:
        return pulumi.get(self, "lake")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="policyData")
    def policy_data(self) -> pulumi.Output[str]:
        """
        The policy data generated by
        a `organizations_get_iam_policy` data source.
        """
        return pulumi.get(self, "policy_data")

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        """
        The ID of the project in which the resource belongs.
        If it is not provided, the project will be parsed from the identifier of the parent resource. If no project is provided in the parent identifier and no project is specified, the provider project is used.

        * `member/members` - (Required) Identities that will be granted the privilege in `role`.
        Each entry can have one of the following values:
        * **allUsers**: A special identifier that represents anyone who is on the internet; with or without a Google account.
        * **allAuthenticatedUsers**: A special identifier that represents anyone who is authenticated with a Google account or a service account.
        * **user:{emailid}**: An email address that represents a specific Google account. For example, alice@gmail.com or joe@example.com.
        * **serviceAccount:{emailid}**: An email address that represents a service account. For example, my-other-app@appspot.gserviceaccount.com.
        * **group:{emailid}**: An email address that represents a Google group. For example, admins@example.com.
        * **domain:{domain}**: A G Suite domain (primary, instead of alias) name that represents all the users of that domain. For example, google.com or example.com.
        * **projectOwner:projectid**: Owners of the given project. For example, "projectOwner:my-example-project"
        * **projectEditor:projectid**: Editors of the given project. For example, "projectEditor:my-example-project"
        * **projectViewer:projectid**: Viewers of the given project. For example, "projectViewer:my-example-project"
        """
        return pulumi.get(self, "project")


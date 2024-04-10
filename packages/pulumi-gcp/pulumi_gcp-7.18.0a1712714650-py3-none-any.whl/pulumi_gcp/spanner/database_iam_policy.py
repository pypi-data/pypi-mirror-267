# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['DatabaseIAMPolicyArgs', 'DatabaseIAMPolicy']

@pulumi.input_type
class DatabaseIAMPolicyArgs:
    def __init__(__self__, *,
                 database: pulumi.Input[str],
                 instance: pulumi.Input[str],
                 policy_data: pulumi.Input[str],
                 project: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a DatabaseIAMPolicy resource.
        :param pulumi.Input[str] database: The name of the Spanner database.
        :param pulumi.Input[str] instance: The name of the Spanner instance the database belongs to.
               
               * `member/members` - (Required) Identities that will be granted the privilege in `role`.
               Each entry can have one of the following values:
               * **allUsers**: A special identifier that represents anyone who is on the internet; with or without a Google account.
               * **allAuthenticatedUsers**: A special identifier that represents anyone who is authenticated with a Google account or a service account.
               * **user:{emailid}**: An email address that represents a specific Google account. For example, alice@gmail.com or joe@example.com.
               * **serviceAccount:{emailid}**: An email address that represents a service account. For example, my-other-app@appspot.gserviceaccount.com.
               * **group:{emailid}**: An email address that represents a Google group. For example, admins@example.com.
               * **domain:{domain}**: A G Suite domain (primary, instead of alias) name that represents all the users of that domain. For example, google.com or example.com.
        :param pulumi.Input[str] policy_data: The policy data generated by
               a `organizations_get_iam_policy` data source.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs. If it
               is not provided, the provider project is used.
        """
        pulumi.set(__self__, "database", database)
        pulumi.set(__self__, "instance", instance)
        pulumi.set(__self__, "policy_data", policy_data)
        if project is not None:
            pulumi.set(__self__, "project", project)

    @property
    @pulumi.getter
    def database(self) -> pulumi.Input[str]:
        """
        The name of the Spanner database.
        """
        return pulumi.get(self, "database")

    @database.setter
    def database(self, value: pulumi.Input[str]):
        pulumi.set(self, "database", value)

    @property
    @pulumi.getter
    def instance(self) -> pulumi.Input[str]:
        """
        The name of the Spanner instance the database belongs to.

        * `member/members` - (Required) Identities that will be granted the privilege in `role`.
        Each entry can have one of the following values:
        * **allUsers**: A special identifier that represents anyone who is on the internet; with or without a Google account.
        * **allAuthenticatedUsers**: A special identifier that represents anyone who is authenticated with a Google account or a service account.
        * **user:{emailid}**: An email address that represents a specific Google account. For example, alice@gmail.com or joe@example.com.
        * **serviceAccount:{emailid}**: An email address that represents a service account. For example, my-other-app@appspot.gserviceaccount.com.
        * **group:{emailid}**: An email address that represents a Google group. For example, admins@example.com.
        * **domain:{domain}**: A G Suite domain (primary, instead of alias) name that represents all the users of that domain. For example, google.com or example.com.
        """
        return pulumi.get(self, "instance")

    @instance.setter
    def instance(self, value: pulumi.Input[str]):
        pulumi.set(self, "instance", value)

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
    def project(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the project in which the resource belongs. If it
        is not provided, the provider project is used.
        """
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)


@pulumi.input_type
class _DatabaseIAMPolicyState:
    def __init__(__self__, *,
                 database: Optional[pulumi.Input[str]] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 instance: Optional[pulumi.Input[str]] = None,
                 policy_data: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering DatabaseIAMPolicy resources.
        :param pulumi.Input[str] database: The name of the Spanner database.
        :param pulumi.Input[str] etag: (Computed) The etag of the database's IAM policy.
        :param pulumi.Input[str] instance: The name of the Spanner instance the database belongs to.
               
               * `member/members` - (Required) Identities that will be granted the privilege in `role`.
               Each entry can have one of the following values:
               * **allUsers**: A special identifier that represents anyone who is on the internet; with or without a Google account.
               * **allAuthenticatedUsers**: A special identifier that represents anyone who is authenticated with a Google account or a service account.
               * **user:{emailid}**: An email address that represents a specific Google account. For example, alice@gmail.com or joe@example.com.
               * **serviceAccount:{emailid}**: An email address that represents a service account. For example, my-other-app@appspot.gserviceaccount.com.
               * **group:{emailid}**: An email address that represents a Google group. For example, admins@example.com.
               * **domain:{domain}**: A G Suite domain (primary, instead of alias) name that represents all the users of that domain. For example, google.com or example.com.
        :param pulumi.Input[str] policy_data: The policy data generated by
               a `organizations_get_iam_policy` data source.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs. If it
               is not provided, the provider project is used.
        """
        if database is not None:
            pulumi.set(__self__, "database", database)
        if etag is not None:
            pulumi.set(__self__, "etag", etag)
        if instance is not None:
            pulumi.set(__self__, "instance", instance)
        if policy_data is not None:
            pulumi.set(__self__, "policy_data", policy_data)
        if project is not None:
            pulumi.set(__self__, "project", project)

    @property
    @pulumi.getter
    def database(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Spanner database.
        """
        return pulumi.get(self, "database")

    @database.setter
    def database(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "database", value)

    @property
    @pulumi.getter
    def etag(self) -> Optional[pulumi.Input[str]]:
        """
        (Computed) The etag of the database's IAM policy.
        """
        return pulumi.get(self, "etag")

    @etag.setter
    def etag(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "etag", value)

    @property
    @pulumi.getter
    def instance(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Spanner instance the database belongs to.

        * `member/members` - (Required) Identities that will be granted the privilege in `role`.
        Each entry can have one of the following values:
        * **allUsers**: A special identifier that represents anyone who is on the internet; with or without a Google account.
        * **allAuthenticatedUsers**: A special identifier that represents anyone who is authenticated with a Google account or a service account.
        * **user:{emailid}**: An email address that represents a specific Google account. For example, alice@gmail.com or joe@example.com.
        * **serviceAccount:{emailid}**: An email address that represents a service account. For example, my-other-app@appspot.gserviceaccount.com.
        * **group:{emailid}**: An email address that represents a Google group. For example, admins@example.com.
        * **domain:{domain}**: A G Suite domain (primary, instead of alias) name that represents all the users of that domain. For example, google.com or example.com.
        """
        return pulumi.get(self, "instance")

    @instance.setter
    def instance(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "instance", value)

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
        The ID of the project in which the resource belongs. If it
        is not provided, the provider project is used.
        """
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)


class DatabaseIAMPolicy(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 database: Optional[pulumi.Input[str]] = None,
                 instance: Optional[pulumi.Input[str]] = None,
                 policy_data: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Three different resources help you manage your IAM policy for a Spanner database. Each of these resources serves a different use case:

        * `spanner.DatabaseIAMPolicy`: Authoritative. Sets the IAM policy for the database and replaces any existing policy already attached.

        > **Warning:** It's entirely possibly to lock yourself out of your database using `spanner.DatabaseIAMPolicy`. Any permissions granted by default will be removed unless you include them in your config.

        * `spanner.DatabaseIAMBinding`: Authoritative for a given role. Updates the IAM policy to grant a role to a list of members. Other roles within the IAM policy for the database are preserved.
        * `spanner.DatabaseIAMMember`: Non-authoritative. Updates the IAM policy to grant a role to a new member. Other members for the role for the database are preserved.

        > **Note:** `spanner.DatabaseIAMPolicy` **cannot** be used in conjunction with `spanner.DatabaseIAMBinding` and `spanner.DatabaseIAMMember` or they will fight over what your policy should be.

        > **Note:** `spanner.DatabaseIAMBinding` resources **can be** used in conjunction with `spanner.DatabaseIAMMember` resources **only if** they do not grant privilege to the same role.

        ## google\\_spanner\\_database\\_iam\\_policy

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        admin = gcp.organizations.get_iam_policy(bindings=[gcp.organizations.GetIAMPolicyBindingArgs(
            role="roles/editor",
            members=["user:jane@example.com"],
        )])
        database = gcp.spanner.DatabaseIAMPolicy("database",
            instance="your-instance-name",
            database="your-database-name",
            policy_data=admin.policy_data)
        ```
        <!--End PulumiCodeChooser -->

        With IAM Conditions:

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        admin = gcp.organizations.get_iam_policy(bindings=[gcp.organizations.GetIAMPolicyBindingArgs(
            role="roles/editor",
            members=["user:jane@example.com"],
            condition=gcp.organizations.GetIAMPolicyBindingConditionArgs(
                title="My Role",
                description="Grant permissions on my_role",
                expression="(resource.type == \\"spanner.googleapis.com/DatabaseRole\\" && (resource.name.endsWith(\\"/myrole\\")))",
            ),
        )])
        database = gcp.spanner.DatabaseIAMPolicy("database",
            instance="your-instance-name",
            database="your-database-name",
            policy_data=admin.policy_data)
        ```
        <!--End PulumiCodeChooser -->

        ## google\\_spanner\\_database\\_iam\\_binding

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        database = gcp.spanner.DatabaseIAMBinding("database",
            instance="your-instance-name",
            database="your-database-name",
            role="roles/compute.networkUser",
            members=["user:jane@example.com"])
        ```
        <!--End PulumiCodeChooser -->

        With IAM Conditions:

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        database = gcp.spanner.DatabaseIAMBinding("database",
            instance="your-instance-name",
            database="your-database-name",
            role="roles/compute.networkUser",
            members=["user:jane@example.com"],
            condition=gcp.spanner.DatabaseIAMBindingConditionArgs(
                title="My Role",
                description="Grant permissions on my_role",
                expression="(resource.type == \\"spanner.googleapis.com/DatabaseRole\\" && (resource.name.endsWith(\\"/myrole\\")))",
            ))
        ```
        <!--End PulumiCodeChooser -->

        ## google\\_spanner\\_database\\_iam\\_member

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        database = gcp.spanner.DatabaseIAMMember("database",
            instance="your-instance-name",
            database="your-database-name",
            role="roles/compute.networkUser",
            member="user:jane@example.com")
        ```
        <!--End PulumiCodeChooser -->

        With IAM Conditions:

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        database = gcp.spanner.DatabaseIAMMember("database",
            instance="your-instance-name",
            database="your-database-name",
            role="roles/compute.networkUser",
            member="user:jane@example.com",
            condition=gcp.spanner.DatabaseIAMMemberConditionArgs(
                title="My Role",
                description="Grant permissions on my_role",
                expression="(resource.type == \\"spanner.googleapis.com/DatabaseRole\\" && (resource.name.endsWith(\\"/myrole\\")))",
            ))
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        ### Importing IAM policies

        IAM policy imports use the identifier of the Spanner Database resource in question. For example:

        * `{{project}}/{{instance}}/{{database}}`

        An `import` block (Terraform v1.5.0 and later) can be used to import IAM policies:

        tf

        import {

          id = {{project}}/{{instance}}/{{database}}

          to = google_spanner_database_iam_policy.default

        }

        The `pulumi import` command can also be used:

        ```sh
        $ pulumi import gcp:spanner/databaseIAMPolicy:DatabaseIAMPolicy default {{project}}/{{instance}}/{{database}}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] database: The name of the Spanner database.
        :param pulumi.Input[str] instance: The name of the Spanner instance the database belongs to.
               
               * `member/members` - (Required) Identities that will be granted the privilege in `role`.
               Each entry can have one of the following values:
               * **allUsers**: A special identifier that represents anyone who is on the internet; with or without a Google account.
               * **allAuthenticatedUsers**: A special identifier that represents anyone who is authenticated with a Google account or a service account.
               * **user:{emailid}**: An email address that represents a specific Google account. For example, alice@gmail.com or joe@example.com.
               * **serviceAccount:{emailid}**: An email address that represents a service account. For example, my-other-app@appspot.gserviceaccount.com.
               * **group:{emailid}**: An email address that represents a Google group. For example, admins@example.com.
               * **domain:{domain}**: A G Suite domain (primary, instead of alias) name that represents all the users of that domain. For example, google.com or example.com.
        :param pulumi.Input[str] policy_data: The policy data generated by
               a `organizations_get_iam_policy` data source.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs. If it
               is not provided, the provider project is used.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DatabaseIAMPolicyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Three different resources help you manage your IAM policy for a Spanner database. Each of these resources serves a different use case:

        * `spanner.DatabaseIAMPolicy`: Authoritative. Sets the IAM policy for the database and replaces any existing policy already attached.

        > **Warning:** It's entirely possibly to lock yourself out of your database using `spanner.DatabaseIAMPolicy`. Any permissions granted by default will be removed unless you include them in your config.

        * `spanner.DatabaseIAMBinding`: Authoritative for a given role. Updates the IAM policy to grant a role to a list of members. Other roles within the IAM policy for the database are preserved.
        * `spanner.DatabaseIAMMember`: Non-authoritative. Updates the IAM policy to grant a role to a new member. Other members for the role for the database are preserved.

        > **Note:** `spanner.DatabaseIAMPolicy` **cannot** be used in conjunction with `spanner.DatabaseIAMBinding` and `spanner.DatabaseIAMMember` or they will fight over what your policy should be.

        > **Note:** `spanner.DatabaseIAMBinding` resources **can be** used in conjunction with `spanner.DatabaseIAMMember` resources **only if** they do not grant privilege to the same role.

        ## google\\_spanner\\_database\\_iam\\_policy

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        admin = gcp.organizations.get_iam_policy(bindings=[gcp.organizations.GetIAMPolicyBindingArgs(
            role="roles/editor",
            members=["user:jane@example.com"],
        )])
        database = gcp.spanner.DatabaseIAMPolicy("database",
            instance="your-instance-name",
            database="your-database-name",
            policy_data=admin.policy_data)
        ```
        <!--End PulumiCodeChooser -->

        With IAM Conditions:

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        admin = gcp.organizations.get_iam_policy(bindings=[gcp.organizations.GetIAMPolicyBindingArgs(
            role="roles/editor",
            members=["user:jane@example.com"],
            condition=gcp.organizations.GetIAMPolicyBindingConditionArgs(
                title="My Role",
                description="Grant permissions on my_role",
                expression="(resource.type == \\"spanner.googleapis.com/DatabaseRole\\" && (resource.name.endsWith(\\"/myrole\\")))",
            ),
        )])
        database = gcp.spanner.DatabaseIAMPolicy("database",
            instance="your-instance-name",
            database="your-database-name",
            policy_data=admin.policy_data)
        ```
        <!--End PulumiCodeChooser -->

        ## google\\_spanner\\_database\\_iam\\_binding

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        database = gcp.spanner.DatabaseIAMBinding("database",
            instance="your-instance-name",
            database="your-database-name",
            role="roles/compute.networkUser",
            members=["user:jane@example.com"])
        ```
        <!--End PulumiCodeChooser -->

        With IAM Conditions:

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        database = gcp.spanner.DatabaseIAMBinding("database",
            instance="your-instance-name",
            database="your-database-name",
            role="roles/compute.networkUser",
            members=["user:jane@example.com"],
            condition=gcp.spanner.DatabaseIAMBindingConditionArgs(
                title="My Role",
                description="Grant permissions on my_role",
                expression="(resource.type == \\"spanner.googleapis.com/DatabaseRole\\" && (resource.name.endsWith(\\"/myrole\\")))",
            ))
        ```
        <!--End PulumiCodeChooser -->

        ## google\\_spanner\\_database\\_iam\\_member

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        database = gcp.spanner.DatabaseIAMMember("database",
            instance="your-instance-name",
            database="your-database-name",
            role="roles/compute.networkUser",
            member="user:jane@example.com")
        ```
        <!--End PulumiCodeChooser -->

        With IAM Conditions:

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        database = gcp.spanner.DatabaseIAMMember("database",
            instance="your-instance-name",
            database="your-database-name",
            role="roles/compute.networkUser",
            member="user:jane@example.com",
            condition=gcp.spanner.DatabaseIAMMemberConditionArgs(
                title="My Role",
                description="Grant permissions on my_role",
                expression="(resource.type == \\"spanner.googleapis.com/DatabaseRole\\" && (resource.name.endsWith(\\"/myrole\\")))",
            ))
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        ### Importing IAM policies

        IAM policy imports use the identifier of the Spanner Database resource in question. For example:

        * `{{project}}/{{instance}}/{{database}}`

        An `import` block (Terraform v1.5.0 and later) can be used to import IAM policies:

        tf

        import {

          id = {{project}}/{{instance}}/{{database}}

          to = google_spanner_database_iam_policy.default

        }

        The `pulumi import` command can also be used:

        ```sh
        $ pulumi import gcp:spanner/databaseIAMPolicy:DatabaseIAMPolicy default {{project}}/{{instance}}/{{database}}
        ```

        :param str resource_name: The name of the resource.
        :param DatabaseIAMPolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DatabaseIAMPolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 database: Optional[pulumi.Input[str]] = None,
                 instance: Optional[pulumi.Input[str]] = None,
                 policy_data: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DatabaseIAMPolicyArgs.__new__(DatabaseIAMPolicyArgs)

            if database is None and not opts.urn:
                raise TypeError("Missing required property 'database'")
            __props__.__dict__["database"] = database
            if instance is None and not opts.urn:
                raise TypeError("Missing required property 'instance'")
            __props__.__dict__["instance"] = instance
            if policy_data is None and not opts.urn:
                raise TypeError("Missing required property 'policy_data'")
            __props__.__dict__["policy_data"] = policy_data
            __props__.__dict__["project"] = project
            __props__.__dict__["etag"] = None
        super(DatabaseIAMPolicy, __self__).__init__(
            'gcp:spanner/databaseIAMPolicy:DatabaseIAMPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            database: Optional[pulumi.Input[str]] = None,
            etag: Optional[pulumi.Input[str]] = None,
            instance: Optional[pulumi.Input[str]] = None,
            policy_data: Optional[pulumi.Input[str]] = None,
            project: Optional[pulumi.Input[str]] = None) -> 'DatabaseIAMPolicy':
        """
        Get an existing DatabaseIAMPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] database: The name of the Spanner database.
        :param pulumi.Input[str] etag: (Computed) The etag of the database's IAM policy.
        :param pulumi.Input[str] instance: The name of the Spanner instance the database belongs to.
               
               * `member/members` - (Required) Identities that will be granted the privilege in `role`.
               Each entry can have one of the following values:
               * **allUsers**: A special identifier that represents anyone who is on the internet; with or without a Google account.
               * **allAuthenticatedUsers**: A special identifier that represents anyone who is authenticated with a Google account or a service account.
               * **user:{emailid}**: An email address that represents a specific Google account. For example, alice@gmail.com or joe@example.com.
               * **serviceAccount:{emailid}**: An email address that represents a service account. For example, my-other-app@appspot.gserviceaccount.com.
               * **group:{emailid}**: An email address that represents a Google group. For example, admins@example.com.
               * **domain:{domain}**: A G Suite domain (primary, instead of alias) name that represents all the users of that domain. For example, google.com or example.com.
        :param pulumi.Input[str] policy_data: The policy data generated by
               a `organizations_get_iam_policy` data source.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs. If it
               is not provided, the provider project is used.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _DatabaseIAMPolicyState.__new__(_DatabaseIAMPolicyState)

        __props__.__dict__["database"] = database
        __props__.__dict__["etag"] = etag
        __props__.__dict__["instance"] = instance
        __props__.__dict__["policy_data"] = policy_data
        __props__.__dict__["project"] = project
        return DatabaseIAMPolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def database(self) -> pulumi.Output[str]:
        """
        The name of the Spanner database.
        """
        return pulumi.get(self, "database")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        (Computed) The etag of the database's IAM policy.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def instance(self) -> pulumi.Output[str]:
        """
        The name of the Spanner instance the database belongs to.

        * `member/members` - (Required) Identities that will be granted the privilege in `role`.
        Each entry can have one of the following values:
        * **allUsers**: A special identifier that represents anyone who is on the internet; with or without a Google account.
        * **allAuthenticatedUsers**: A special identifier that represents anyone who is authenticated with a Google account or a service account.
        * **user:{emailid}**: An email address that represents a specific Google account. For example, alice@gmail.com or joe@example.com.
        * **serviceAccount:{emailid}**: An email address that represents a service account. For example, my-other-app@appspot.gserviceaccount.com.
        * **group:{emailid}**: An email address that represents a Google group. For example, admins@example.com.
        * **domain:{domain}**: A G Suite domain (primary, instead of alias) name that represents all the users of that domain. For example, google.com or example.com.
        """
        return pulumi.get(self, "instance")

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
        The ID of the project in which the resource belongs. If it
        is not provided, the provider project is used.
        """
        return pulumi.get(self, "project")


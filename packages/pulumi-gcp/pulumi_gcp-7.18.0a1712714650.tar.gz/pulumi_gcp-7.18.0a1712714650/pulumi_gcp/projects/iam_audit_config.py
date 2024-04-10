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

__all__ = ['IAMAuditConfigArgs', 'IAMAuditConfig']

@pulumi.input_type
class IAMAuditConfigArgs:
    def __init__(__self__, *,
                 audit_log_configs: pulumi.Input[Sequence[pulumi.Input['IAMAuditConfigAuditLogConfigArgs']]],
                 project: pulumi.Input[str],
                 service: pulumi.Input[str]):
        """
        The set of arguments for constructing a IAMAuditConfig resource.
        :param pulumi.Input[Sequence[pulumi.Input['IAMAuditConfigAuditLogConfigArgs']]] audit_log_configs: The configuration for logging of each type of permission.  This can be specified multiple times.  Structure is documented below.
        :param pulumi.Input[str] project: The project id of the target project. This is not
               inferred from the provider.
        :param pulumi.Input[str] service: Service which will be enabled for audit logging.  The special value `allServices` covers all services.  Note that if there are google\\_project\\_iam\\_audit\\_config resources covering both `allServices` and a specific service then the union of the two AuditConfigs is used for that service: the `log_types` specified in each `audit_log_config` are enabled, and the `exempted_members` in each `audit_log_config` are exempted.
        """
        pulumi.set(__self__, "audit_log_configs", audit_log_configs)
        pulumi.set(__self__, "project", project)
        pulumi.set(__self__, "service", service)

    @property
    @pulumi.getter(name="auditLogConfigs")
    def audit_log_configs(self) -> pulumi.Input[Sequence[pulumi.Input['IAMAuditConfigAuditLogConfigArgs']]]:
        """
        The configuration for logging of each type of permission.  This can be specified multiple times.  Structure is documented below.
        """
        return pulumi.get(self, "audit_log_configs")

    @audit_log_configs.setter
    def audit_log_configs(self, value: pulumi.Input[Sequence[pulumi.Input['IAMAuditConfigAuditLogConfigArgs']]]):
        pulumi.set(self, "audit_log_configs", value)

    @property
    @pulumi.getter
    def project(self) -> pulumi.Input[str]:
        """
        The project id of the target project. This is not
        inferred from the provider.
        """
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: pulumi.Input[str]):
        pulumi.set(self, "project", value)

    @property
    @pulumi.getter
    def service(self) -> pulumi.Input[str]:
        """
        Service which will be enabled for audit logging.  The special value `allServices` covers all services.  Note that if there are google\\_project\\_iam\\_audit\\_config resources covering both `allServices` and a specific service then the union of the two AuditConfigs is used for that service: the `log_types` specified in each `audit_log_config` are enabled, and the `exempted_members` in each `audit_log_config` are exempted.
        """
        return pulumi.get(self, "service")

    @service.setter
    def service(self, value: pulumi.Input[str]):
        pulumi.set(self, "service", value)


@pulumi.input_type
class _IAMAuditConfigState:
    def __init__(__self__, *,
                 audit_log_configs: Optional[pulumi.Input[Sequence[pulumi.Input['IAMAuditConfigAuditLogConfigArgs']]]] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 service: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering IAMAuditConfig resources.
        :param pulumi.Input[Sequence[pulumi.Input['IAMAuditConfigAuditLogConfigArgs']]] audit_log_configs: The configuration for logging of each type of permission.  This can be specified multiple times.  Structure is documented below.
        :param pulumi.Input[str] etag: (Computed) The etag of the project's IAM policy.
        :param pulumi.Input[str] project: The project id of the target project. This is not
               inferred from the provider.
        :param pulumi.Input[str] service: Service which will be enabled for audit logging.  The special value `allServices` covers all services.  Note that if there are google\\_project\\_iam\\_audit\\_config resources covering both `allServices` and a specific service then the union of the two AuditConfigs is used for that service: the `log_types` specified in each `audit_log_config` are enabled, and the `exempted_members` in each `audit_log_config` are exempted.
        """
        if audit_log_configs is not None:
            pulumi.set(__self__, "audit_log_configs", audit_log_configs)
        if etag is not None:
            pulumi.set(__self__, "etag", etag)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if service is not None:
            pulumi.set(__self__, "service", service)

    @property
    @pulumi.getter(name="auditLogConfigs")
    def audit_log_configs(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['IAMAuditConfigAuditLogConfigArgs']]]]:
        """
        The configuration for logging of each type of permission.  This can be specified multiple times.  Structure is documented below.
        """
        return pulumi.get(self, "audit_log_configs")

    @audit_log_configs.setter
    def audit_log_configs(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['IAMAuditConfigAuditLogConfigArgs']]]]):
        pulumi.set(self, "audit_log_configs", value)

    @property
    @pulumi.getter
    def etag(self) -> Optional[pulumi.Input[str]]:
        """
        (Computed) The etag of the project's IAM policy.
        """
        return pulumi.get(self, "etag")

    @etag.setter
    def etag(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "etag", value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        """
        The project id of the target project. This is not
        inferred from the provider.
        """
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)

    @property
    @pulumi.getter
    def service(self) -> Optional[pulumi.Input[str]]:
        """
        Service which will be enabled for audit logging.  The special value `allServices` covers all services.  Note that if there are google\\_project\\_iam\\_audit\\_config resources covering both `allServices` and a specific service then the union of the two AuditConfigs is used for that service: the `log_types` specified in each `audit_log_config` are enabled, and the `exempted_members` in each `audit_log_config` are exempted.
        """
        return pulumi.get(self, "service")

    @service.setter
    def service(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "service", value)


class IAMAuditConfig(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 audit_log_configs: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['IAMAuditConfigAuditLogConfigArgs']]]]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 service: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Four different resources help you manage your IAM policy for a project. Each of these resources serves a different use case:

        * `projects.IAMPolicy`: Authoritative. Sets the IAM policy for the project and replaces any existing policy already attached.
        * `projects.IAMBinding`: Authoritative for a given role. Updates the IAM policy to grant a role to a list of members. Other roles within the IAM policy for the project are preserved.
        * `projects.IAMMember`: Non-authoritative. Updates the IAM policy to grant a role to a new member. Other members for the role for the project are preserved.
        * `projects.IAMAuditConfig`: Authoritative for a given service. Updates the IAM policy to enable audit logging for the given service.

        > **Note:** `projects.IAMPolicy` **cannot** be used in conjunction with `projects.IAMBinding`, `projects.IAMMember`, or `projects.IAMAuditConfig` or they will fight over what your policy should be.

        > **Note:** `projects.IAMBinding` resources **can be** used in conjunction with `projects.IAMMember` resources **only if** they do not grant privilege to the same role.

        > **Note:** The underlying API method `projects.setIamPolicy` has a lot of constraints which are documented [here](https://cloud.google.com/resource-manager/reference/rest/v1/projects/setIamPolicy). In addition to these constraints,
           IAM Conditions cannot be used with Basic Roles such as Owner. Violating these constraints will result in the API returning 400 error code so please review these if you encounter errors with this resource.

        ## google\\_project\\_iam\\_policy

        !> **Be careful!** You can accidentally lock yourself out of your project
           using this resource. Deleting a `projects.IAMPolicy` removes access
           from anyone without organization-level access to the project. Proceed with caution.
           It's not recommended to use `projects.IAMPolicy` with your provider project
           to avoid locking yourself out, and it should generally only be used with projects
           fully managed by this provider. If you do use this resource, it is recommended to **import** the policy before
           applying the change.

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        admin = gcp.organizations.get_iam_policy(bindings=[gcp.organizations.GetIAMPolicyBindingArgs(
            role="roles/editor",
            members=["user:jane@example.com"],
        )])
        project = gcp.projects.IAMPolicy("project",
            project="your-project-id",
            policy_data=admin.policy_data)
        ```
        <!--End PulumiCodeChooser -->

        With IAM Conditions:

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        admin = gcp.organizations.get_iam_policy(bindings=[gcp.organizations.GetIAMPolicyBindingArgs(
            role="roles/compute.admin",
            members=["user:jane@example.com"],
            condition=gcp.organizations.GetIAMPolicyBindingConditionArgs(
                title="expires_after_2019_12_31",
                description="Expiring at midnight of 2019-12-31",
                expression="request.time < timestamp(\\"2020-01-01T00:00:00Z\\")",
            ),
        )])
        project = gcp.projects.IAMPolicy("project",
            project="your-project-id",
            policy_data=admin.policy_data)
        ```
        <!--End PulumiCodeChooser -->

        ## google\\_project\\_iam\\_binding

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        project = gcp.projects.IAMBinding("project",
            project="your-project-id",
            role="roles/editor",
            members=["user:jane@example.com"])
        ```
        <!--End PulumiCodeChooser -->

        With IAM Conditions:

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        project = gcp.projects.IAMBinding("project",
            project="your-project-id",
            role="roles/container.admin",
            members=["user:jane@example.com"],
            condition=gcp.projects.IAMBindingConditionArgs(
                title="expires_after_2019_12_31",
                description="Expiring at midnight of 2019-12-31",
                expression="request.time < timestamp(\\"2020-01-01T00:00:00Z\\")",
            ))
        ```
        <!--End PulumiCodeChooser -->

        ## google\\_project\\_iam\\_member

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        project = gcp.projects.IAMMember("project",
            project="your-project-id",
            role="roles/editor",
            member="user:jane@example.com")
        ```
        <!--End PulumiCodeChooser -->

        With IAM Conditions:

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        project = gcp.projects.IAMMember("project",
            project="your-project-id",
            role="roles/firebase.admin",
            member="user:jane@example.com",
            condition=gcp.projects.IAMMemberConditionArgs(
                title="expires_after_2019_12_31",
                description="Expiring at midnight of 2019-12-31",
                expression="request.time < timestamp(\\"2020-01-01T00:00:00Z\\")",
            ))
        ```
        <!--End PulumiCodeChooser -->

        ## google\\_project\\_iam\\_audit\\_config

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        project = gcp.projects.IAMAuditConfig("project",
            project="your-project-id",
            service="allServices",
            audit_log_configs=[
                gcp.projects.IAMAuditConfigAuditLogConfigArgs(
                    log_type="ADMIN_READ",
                ),
                gcp.projects.IAMAuditConfigAuditLogConfigArgs(
                    log_type="DATA_READ",
                    exempted_members=["user:joebloggs@example.com"],
                ),
            ])
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        ### Importing Audit Configs

        An audit config can be imported into a `google_project_iam_audit_config` resource using the resource's `project_id` and the `service`, e.g:

        * `"{{project_id}} foo.googleapis.com"`

        An `import` block (Terraform v1.5.0 and later) can be used to import audit configs:

        tf

        import {

          id = "{{project_id}} foo.googleapis.com"

          to = google_project_iam_audit_config.default

        }

        The `pulumi import` command can also be used:

        ```sh
        $ pulumi import gcp:projects/iAMAuditConfig:IAMAuditConfig default "{{project_id}} foo.googleapis.com"
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['IAMAuditConfigAuditLogConfigArgs']]]] audit_log_configs: The configuration for logging of each type of permission.  This can be specified multiple times.  Structure is documented below.
        :param pulumi.Input[str] project: The project id of the target project. This is not
               inferred from the provider.
        :param pulumi.Input[str] service: Service which will be enabled for audit logging.  The special value `allServices` covers all services.  Note that if there are google\\_project\\_iam\\_audit\\_config resources covering both `allServices` and a specific service then the union of the two AuditConfigs is used for that service: the `log_types` specified in each `audit_log_config` are enabled, and the `exempted_members` in each `audit_log_config` are exempted.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: IAMAuditConfigArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Four different resources help you manage your IAM policy for a project. Each of these resources serves a different use case:

        * `projects.IAMPolicy`: Authoritative. Sets the IAM policy for the project and replaces any existing policy already attached.
        * `projects.IAMBinding`: Authoritative for a given role. Updates the IAM policy to grant a role to a list of members. Other roles within the IAM policy for the project are preserved.
        * `projects.IAMMember`: Non-authoritative. Updates the IAM policy to grant a role to a new member. Other members for the role for the project are preserved.
        * `projects.IAMAuditConfig`: Authoritative for a given service. Updates the IAM policy to enable audit logging for the given service.

        > **Note:** `projects.IAMPolicy` **cannot** be used in conjunction with `projects.IAMBinding`, `projects.IAMMember`, or `projects.IAMAuditConfig` or they will fight over what your policy should be.

        > **Note:** `projects.IAMBinding` resources **can be** used in conjunction with `projects.IAMMember` resources **only if** they do not grant privilege to the same role.

        > **Note:** The underlying API method `projects.setIamPolicy` has a lot of constraints which are documented [here](https://cloud.google.com/resource-manager/reference/rest/v1/projects/setIamPolicy). In addition to these constraints,
           IAM Conditions cannot be used with Basic Roles such as Owner. Violating these constraints will result in the API returning 400 error code so please review these if you encounter errors with this resource.

        ## google\\_project\\_iam\\_policy

        !> **Be careful!** You can accidentally lock yourself out of your project
           using this resource. Deleting a `projects.IAMPolicy` removes access
           from anyone without organization-level access to the project. Proceed with caution.
           It's not recommended to use `projects.IAMPolicy` with your provider project
           to avoid locking yourself out, and it should generally only be used with projects
           fully managed by this provider. If you do use this resource, it is recommended to **import** the policy before
           applying the change.

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        admin = gcp.organizations.get_iam_policy(bindings=[gcp.organizations.GetIAMPolicyBindingArgs(
            role="roles/editor",
            members=["user:jane@example.com"],
        )])
        project = gcp.projects.IAMPolicy("project",
            project="your-project-id",
            policy_data=admin.policy_data)
        ```
        <!--End PulumiCodeChooser -->

        With IAM Conditions:

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        admin = gcp.organizations.get_iam_policy(bindings=[gcp.organizations.GetIAMPolicyBindingArgs(
            role="roles/compute.admin",
            members=["user:jane@example.com"],
            condition=gcp.organizations.GetIAMPolicyBindingConditionArgs(
                title="expires_after_2019_12_31",
                description="Expiring at midnight of 2019-12-31",
                expression="request.time < timestamp(\\"2020-01-01T00:00:00Z\\")",
            ),
        )])
        project = gcp.projects.IAMPolicy("project",
            project="your-project-id",
            policy_data=admin.policy_data)
        ```
        <!--End PulumiCodeChooser -->

        ## google\\_project\\_iam\\_binding

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        project = gcp.projects.IAMBinding("project",
            project="your-project-id",
            role="roles/editor",
            members=["user:jane@example.com"])
        ```
        <!--End PulumiCodeChooser -->

        With IAM Conditions:

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        project = gcp.projects.IAMBinding("project",
            project="your-project-id",
            role="roles/container.admin",
            members=["user:jane@example.com"],
            condition=gcp.projects.IAMBindingConditionArgs(
                title="expires_after_2019_12_31",
                description="Expiring at midnight of 2019-12-31",
                expression="request.time < timestamp(\\"2020-01-01T00:00:00Z\\")",
            ))
        ```
        <!--End PulumiCodeChooser -->

        ## google\\_project\\_iam\\_member

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        project = gcp.projects.IAMMember("project",
            project="your-project-id",
            role="roles/editor",
            member="user:jane@example.com")
        ```
        <!--End PulumiCodeChooser -->

        With IAM Conditions:

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        project = gcp.projects.IAMMember("project",
            project="your-project-id",
            role="roles/firebase.admin",
            member="user:jane@example.com",
            condition=gcp.projects.IAMMemberConditionArgs(
                title="expires_after_2019_12_31",
                description="Expiring at midnight of 2019-12-31",
                expression="request.time < timestamp(\\"2020-01-01T00:00:00Z\\")",
            ))
        ```
        <!--End PulumiCodeChooser -->

        ## google\\_project\\_iam\\_audit\\_config

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        project = gcp.projects.IAMAuditConfig("project",
            project="your-project-id",
            service="allServices",
            audit_log_configs=[
                gcp.projects.IAMAuditConfigAuditLogConfigArgs(
                    log_type="ADMIN_READ",
                ),
                gcp.projects.IAMAuditConfigAuditLogConfigArgs(
                    log_type="DATA_READ",
                    exempted_members=["user:joebloggs@example.com"],
                ),
            ])
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        ### Importing Audit Configs

        An audit config can be imported into a `google_project_iam_audit_config` resource using the resource's `project_id` and the `service`, e.g:

        * `"{{project_id}} foo.googleapis.com"`

        An `import` block (Terraform v1.5.0 and later) can be used to import audit configs:

        tf

        import {

          id = "{{project_id}} foo.googleapis.com"

          to = google_project_iam_audit_config.default

        }

        The `pulumi import` command can also be used:

        ```sh
        $ pulumi import gcp:projects/iAMAuditConfig:IAMAuditConfig default "{{project_id}} foo.googleapis.com"
        ```

        :param str resource_name: The name of the resource.
        :param IAMAuditConfigArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(IAMAuditConfigArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 audit_log_configs: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['IAMAuditConfigAuditLogConfigArgs']]]]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 service: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = IAMAuditConfigArgs.__new__(IAMAuditConfigArgs)

            if audit_log_configs is None and not opts.urn:
                raise TypeError("Missing required property 'audit_log_configs'")
            __props__.__dict__["audit_log_configs"] = audit_log_configs
            if project is None and not opts.urn:
                raise TypeError("Missing required property 'project'")
            __props__.__dict__["project"] = project
            if service is None and not opts.urn:
                raise TypeError("Missing required property 'service'")
            __props__.__dict__["service"] = service
            __props__.__dict__["etag"] = None
        super(IAMAuditConfig, __self__).__init__(
            'gcp:projects/iAMAuditConfig:IAMAuditConfig',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            audit_log_configs: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['IAMAuditConfigAuditLogConfigArgs']]]]] = None,
            etag: Optional[pulumi.Input[str]] = None,
            project: Optional[pulumi.Input[str]] = None,
            service: Optional[pulumi.Input[str]] = None) -> 'IAMAuditConfig':
        """
        Get an existing IAMAuditConfig resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['IAMAuditConfigAuditLogConfigArgs']]]] audit_log_configs: The configuration for logging of each type of permission.  This can be specified multiple times.  Structure is documented below.
        :param pulumi.Input[str] etag: (Computed) The etag of the project's IAM policy.
        :param pulumi.Input[str] project: The project id of the target project. This is not
               inferred from the provider.
        :param pulumi.Input[str] service: Service which will be enabled for audit logging.  The special value `allServices` covers all services.  Note that if there are google\\_project\\_iam\\_audit\\_config resources covering both `allServices` and a specific service then the union of the two AuditConfigs is used for that service: the `log_types` specified in each `audit_log_config` are enabled, and the `exempted_members` in each `audit_log_config` are exempted.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _IAMAuditConfigState.__new__(_IAMAuditConfigState)

        __props__.__dict__["audit_log_configs"] = audit_log_configs
        __props__.__dict__["etag"] = etag
        __props__.__dict__["project"] = project
        __props__.__dict__["service"] = service
        return IAMAuditConfig(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="auditLogConfigs")
    def audit_log_configs(self) -> pulumi.Output[Sequence['outputs.IAMAuditConfigAuditLogConfig']]:
        """
        The configuration for logging of each type of permission.  This can be specified multiple times.  Structure is documented below.
        """
        return pulumi.get(self, "audit_log_configs")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        (Computed) The etag of the project's IAM policy.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        """
        The project id of the target project. This is not
        inferred from the provider.
        """
        return pulumi.get(self, "project")

    @property
    @pulumi.getter
    def service(self) -> pulumi.Output[str]:
        """
        Service which will be enabled for audit logging.  The special value `allServices` covers all services.  Note that if there are google\\_project\\_iam\\_audit\\_config resources covering both `allServices` and a specific service then the union of the two AuditConfigs is used for that service: the `log_types` specified in each `audit_log_config` are enabled, and the `exempted_members` in each `audit_log_config` are exempted.
        """
        return pulumi.get(self, "service")


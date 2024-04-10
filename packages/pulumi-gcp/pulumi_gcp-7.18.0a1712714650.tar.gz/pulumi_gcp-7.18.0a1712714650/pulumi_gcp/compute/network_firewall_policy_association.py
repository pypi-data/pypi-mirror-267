# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['NetworkFirewallPolicyAssociationArgs', 'NetworkFirewallPolicyAssociation']

@pulumi.input_type
class NetworkFirewallPolicyAssociationArgs:
    def __init__(__self__, *,
                 attachment_target: pulumi.Input[str],
                 firewall_policy: pulumi.Input[str],
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a NetworkFirewallPolicyAssociation resource.
        :param pulumi.Input[str] attachment_target: The target that the firewall policy is attached to.
        :param pulumi.Input[str] firewall_policy: The firewall policy ID of the association.
        :param pulumi.Input[str] name: The name for an association.
               
               
               
               - - -
        :param pulumi.Input[str] project: The project for the resource
        """
        pulumi.set(__self__, "attachment_target", attachment_target)
        pulumi.set(__self__, "firewall_policy", firewall_policy)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if project is not None:
            pulumi.set(__self__, "project", project)

    @property
    @pulumi.getter(name="attachmentTarget")
    def attachment_target(self) -> pulumi.Input[str]:
        """
        The target that the firewall policy is attached to.
        """
        return pulumi.get(self, "attachment_target")

    @attachment_target.setter
    def attachment_target(self, value: pulumi.Input[str]):
        pulumi.set(self, "attachment_target", value)

    @property
    @pulumi.getter(name="firewallPolicy")
    def firewall_policy(self) -> pulumi.Input[str]:
        """
        The firewall policy ID of the association.
        """
        return pulumi.get(self, "firewall_policy")

    @firewall_policy.setter
    def firewall_policy(self, value: pulumi.Input[str]):
        pulumi.set(self, "firewall_policy", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name for an association.



        - - -
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        """
        The project for the resource
        """
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)


@pulumi.input_type
class _NetworkFirewallPolicyAssociationState:
    def __init__(__self__, *,
                 attachment_target: Optional[pulumi.Input[str]] = None,
                 firewall_policy: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 short_name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering NetworkFirewallPolicyAssociation resources.
        :param pulumi.Input[str] attachment_target: The target that the firewall policy is attached to.
        :param pulumi.Input[str] firewall_policy: The firewall policy ID of the association.
        :param pulumi.Input[str] name: The name for an association.
               
               
               
               - - -
        :param pulumi.Input[str] project: The project for the resource
        :param pulumi.Input[str] short_name: The short name of the firewall policy of the association.
        """
        if attachment_target is not None:
            pulumi.set(__self__, "attachment_target", attachment_target)
        if firewall_policy is not None:
            pulumi.set(__self__, "firewall_policy", firewall_policy)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if short_name is not None:
            pulumi.set(__self__, "short_name", short_name)

    @property
    @pulumi.getter(name="attachmentTarget")
    def attachment_target(self) -> Optional[pulumi.Input[str]]:
        """
        The target that the firewall policy is attached to.
        """
        return pulumi.get(self, "attachment_target")

    @attachment_target.setter
    def attachment_target(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "attachment_target", value)

    @property
    @pulumi.getter(name="firewallPolicy")
    def firewall_policy(self) -> Optional[pulumi.Input[str]]:
        """
        The firewall policy ID of the association.
        """
        return pulumi.get(self, "firewall_policy")

    @firewall_policy.setter
    def firewall_policy(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "firewall_policy", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name for an association.



        - - -
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        """
        The project for the resource
        """
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)

    @property
    @pulumi.getter(name="shortName")
    def short_name(self) -> Optional[pulumi.Input[str]]:
        """
        The short name of the firewall policy of the association.
        """
        return pulumi.get(self, "short_name")

    @short_name.setter
    def short_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "short_name", value)


class NetworkFirewallPolicyAssociation(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 attachment_target: Optional[pulumi.Input[str]] = None,
                 firewall_policy: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        The Compute NetworkFirewallPolicyAssociation resource

        ## Example Usage

        ### Global
        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        network_firewall_policy = gcp.compute.NetworkFirewallPolicy("network_firewall_policy",
            name="policy",
            project="my-project-name",
            description="Sample global network firewall policy")
        network = gcp.compute.Network("network", name="network")
        primary = gcp.compute.NetworkFirewallPolicyAssociation("primary",
            name="association",
            attachment_target=network.id,
            firewall_policy=network_firewall_policy.name,
            project="my-project-name")
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        NetworkFirewallPolicyAssociation can be imported using any of these accepted formats:

        * `projects/{{project}}/global/firewallPolicies/{{firewall_policy}}/associations/{{name}}`

        * `{{project}}/{{firewall_policy}}/{{name}}`

        When using the `pulumi import` command, NetworkFirewallPolicyAssociation can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:compute/networkFirewallPolicyAssociation:NetworkFirewallPolicyAssociation default projects/{{project}}/global/firewallPolicies/{{firewall_policy}}/associations/{{name}}
        ```

        ```sh
        $ pulumi import gcp:compute/networkFirewallPolicyAssociation:NetworkFirewallPolicyAssociation default {{project}}/{{firewall_policy}}/{{name}}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] attachment_target: The target that the firewall policy is attached to.
        :param pulumi.Input[str] firewall_policy: The firewall policy ID of the association.
        :param pulumi.Input[str] name: The name for an association.
               
               
               
               - - -
        :param pulumi.Input[str] project: The project for the resource
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: NetworkFirewallPolicyAssociationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The Compute NetworkFirewallPolicyAssociation resource

        ## Example Usage

        ### Global
        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        network_firewall_policy = gcp.compute.NetworkFirewallPolicy("network_firewall_policy",
            name="policy",
            project="my-project-name",
            description="Sample global network firewall policy")
        network = gcp.compute.Network("network", name="network")
        primary = gcp.compute.NetworkFirewallPolicyAssociation("primary",
            name="association",
            attachment_target=network.id,
            firewall_policy=network_firewall_policy.name,
            project="my-project-name")
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        NetworkFirewallPolicyAssociation can be imported using any of these accepted formats:

        * `projects/{{project}}/global/firewallPolicies/{{firewall_policy}}/associations/{{name}}`

        * `{{project}}/{{firewall_policy}}/{{name}}`

        When using the `pulumi import` command, NetworkFirewallPolicyAssociation can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:compute/networkFirewallPolicyAssociation:NetworkFirewallPolicyAssociation default projects/{{project}}/global/firewallPolicies/{{firewall_policy}}/associations/{{name}}
        ```

        ```sh
        $ pulumi import gcp:compute/networkFirewallPolicyAssociation:NetworkFirewallPolicyAssociation default {{project}}/{{firewall_policy}}/{{name}}
        ```

        :param str resource_name: The name of the resource.
        :param NetworkFirewallPolicyAssociationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(NetworkFirewallPolicyAssociationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 attachment_target: Optional[pulumi.Input[str]] = None,
                 firewall_policy: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = NetworkFirewallPolicyAssociationArgs.__new__(NetworkFirewallPolicyAssociationArgs)

            if attachment_target is None and not opts.urn:
                raise TypeError("Missing required property 'attachment_target'")
            __props__.__dict__["attachment_target"] = attachment_target
            if firewall_policy is None and not opts.urn:
                raise TypeError("Missing required property 'firewall_policy'")
            __props__.__dict__["firewall_policy"] = firewall_policy
            __props__.__dict__["name"] = name
            __props__.__dict__["project"] = project
            __props__.__dict__["short_name"] = None
        super(NetworkFirewallPolicyAssociation, __self__).__init__(
            'gcp:compute/networkFirewallPolicyAssociation:NetworkFirewallPolicyAssociation',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            attachment_target: Optional[pulumi.Input[str]] = None,
            firewall_policy: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            project: Optional[pulumi.Input[str]] = None,
            short_name: Optional[pulumi.Input[str]] = None) -> 'NetworkFirewallPolicyAssociation':
        """
        Get an existing NetworkFirewallPolicyAssociation resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] attachment_target: The target that the firewall policy is attached to.
        :param pulumi.Input[str] firewall_policy: The firewall policy ID of the association.
        :param pulumi.Input[str] name: The name for an association.
               
               
               
               - - -
        :param pulumi.Input[str] project: The project for the resource
        :param pulumi.Input[str] short_name: The short name of the firewall policy of the association.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _NetworkFirewallPolicyAssociationState.__new__(_NetworkFirewallPolicyAssociationState)

        __props__.__dict__["attachment_target"] = attachment_target
        __props__.__dict__["firewall_policy"] = firewall_policy
        __props__.__dict__["name"] = name
        __props__.__dict__["project"] = project
        __props__.__dict__["short_name"] = short_name
        return NetworkFirewallPolicyAssociation(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="attachmentTarget")
    def attachment_target(self) -> pulumi.Output[str]:
        """
        The target that the firewall policy is attached to.
        """
        return pulumi.get(self, "attachment_target")

    @property
    @pulumi.getter(name="firewallPolicy")
    def firewall_policy(self) -> pulumi.Output[str]:
        """
        The firewall policy ID of the association.
        """
        return pulumi.get(self, "firewall_policy")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name for an association.



        - - -
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        """
        The project for the resource
        """
        return pulumi.get(self, "project")

    @property
    @pulumi.getter(name="shortName")
    def short_name(self) -> pulumi.Output[str]:
        """
        The short name of the firewall policy of the association.
        """
        return pulumi.get(self, "short_name")


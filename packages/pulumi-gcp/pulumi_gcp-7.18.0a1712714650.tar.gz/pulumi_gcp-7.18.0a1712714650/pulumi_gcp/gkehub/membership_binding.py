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

__all__ = ['MembershipBindingArgs', 'MembershipBinding']

@pulumi.input_type
class MembershipBindingArgs:
    def __init__(__self__, *,
                 location: pulumi.Input[str],
                 membership_binding_id: pulumi.Input[str],
                 membership_id: pulumi.Input[str],
                 scope: pulumi.Input[str],
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 project: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a MembershipBinding resource.
        :param pulumi.Input[str] location: Location of the membership
               
               
               - - -
        :param pulumi.Input[str] membership_binding_id: The client-provided identifier of the membership binding.
        :param pulumi.Input[str] membership_id: Id of the membership
        :param pulumi.Input[str] scope: A Workspace resource name in the format
               `projects/*/locations/*/scopes/*`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Labels for this Membership binding.
               
               **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
               Please refer to the field `effective_labels` for all of the labels present on the resource.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        """
        pulumi.set(__self__, "location", location)
        pulumi.set(__self__, "membership_binding_id", membership_binding_id)
        pulumi.set(__self__, "membership_id", membership_id)
        pulumi.set(__self__, "scope", scope)
        if labels is not None:
            pulumi.set(__self__, "labels", labels)
        if project is not None:
            pulumi.set(__self__, "project", project)

    @property
    @pulumi.getter
    def location(self) -> pulumi.Input[str]:
        """
        Location of the membership


        - - -
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: pulumi.Input[str]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="membershipBindingId")
    def membership_binding_id(self) -> pulumi.Input[str]:
        """
        The client-provided identifier of the membership binding.
        """
        return pulumi.get(self, "membership_binding_id")

    @membership_binding_id.setter
    def membership_binding_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "membership_binding_id", value)

    @property
    @pulumi.getter(name="membershipId")
    def membership_id(self) -> pulumi.Input[str]:
        """
        Id of the membership
        """
        return pulumi.get(self, "membership_id")

    @membership_id.setter
    def membership_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "membership_id", value)

    @property
    @pulumi.getter
    def scope(self) -> pulumi.Input[str]:
        """
        A Workspace resource name in the format
        `projects/*/locations/*/scopes/*`.
        """
        return pulumi.get(self, "scope")

    @scope.setter
    def scope(self, value: pulumi.Input[str]):
        pulumi.set(self, "scope", value)

    @property
    @pulumi.getter
    def labels(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Labels for this Membership binding.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field `effective_labels` for all of the labels present on the resource.
        """
        return pulumi.get(self, "labels")

    @labels.setter
    def labels(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "labels", value)

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
class _MembershipBindingState:
    def __init__(__self__, *,
                 create_time: Optional[pulumi.Input[str]] = None,
                 delete_time: Optional[pulumi.Input[str]] = None,
                 effective_labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 membership_binding_id: Optional[pulumi.Input[str]] = None,
                 membership_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 pulumi_labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 scope: Optional[pulumi.Input[str]] = None,
                 states: Optional[pulumi.Input[Sequence[pulumi.Input['MembershipBindingStateArgs']]]] = None,
                 uid: Optional[pulumi.Input[str]] = None,
                 update_time: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering MembershipBinding resources.
        :param pulumi.Input[str] create_time: Time the MembershipBinding was created in UTC.
        :param pulumi.Input[str] delete_time: Time the MembershipBinding was deleted in UTC.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] effective_labels: All of labels (key/value pairs) present on the resource in GCP, including the labels configured through Pulumi, other clients and services.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Labels for this Membership binding.
               
               **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
               Please refer to the field `effective_labels` for all of the labels present on the resource.
        :param pulumi.Input[str] location: Location of the membership
               
               
               - - -
        :param pulumi.Input[str] membership_binding_id: The client-provided identifier of the membership binding.
        :param pulumi.Input[str] membership_id: Id of the membership
        :param pulumi.Input[str] name: The resource name for the membershipbinding itself
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] pulumi_labels: The combination of labels configured directly on the resource
               and default labels configured on the provider.
        :param pulumi.Input[str] scope: A Workspace resource name in the format
               `projects/*/locations/*/scopes/*`.
        :param pulumi.Input[Sequence[pulumi.Input['MembershipBindingStateArgs']]] states: State of the membership binding resource.
               Structure is documented below.
        :param pulumi.Input[str] uid: Google-generated UUID for this resource.
        :param pulumi.Input[str] update_time: Time the MembershipBinding was updated in UTC.
        """
        if create_time is not None:
            pulumi.set(__self__, "create_time", create_time)
        if delete_time is not None:
            pulumi.set(__self__, "delete_time", delete_time)
        if effective_labels is not None:
            pulumi.set(__self__, "effective_labels", effective_labels)
        if labels is not None:
            pulumi.set(__self__, "labels", labels)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if membership_binding_id is not None:
            pulumi.set(__self__, "membership_binding_id", membership_binding_id)
        if membership_id is not None:
            pulumi.set(__self__, "membership_id", membership_id)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if pulumi_labels is not None:
            pulumi.set(__self__, "pulumi_labels", pulumi_labels)
        if scope is not None:
            pulumi.set(__self__, "scope", scope)
        if states is not None:
            pulumi.set(__self__, "states", states)
        if uid is not None:
            pulumi.set(__self__, "uid", uid)
        if update_time is not None:
            pulumi.set(__self__, "update_time", update_time)

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> Optional[pulumi.Input[str]]:
        """
        Time the MembershipBinding was created in UTC.
        """
        return pulumi.get(self, "create_time")

    @create_time.setter
    def create_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "create_time", value)

    @property
    @pulumi.getter(name="deleteTime")
    def delete_time(self) -> Optional[pulumi.Input[str]]:
        """
        Time the MembershipBinding was deleted in UTC.
        """
        return pulumi.get(self, "delete_time")

    @delete_time.setter
    def delete_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "delete_time", value)

    @property
    @pulumi.getter(name="effectiveLabels")
    def effective_labels(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        All of labels (key/value pairs) present on the resource in GCP, including the labels configured through Pulumi, other clients and services.
        """
        return pulumi.get(self, "effective_labels")

    @effective_labels.setter
    def effective_labels(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "effective_labels", value)

    @property
    @pulumi.getter
    def labels(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Labels for this Membership binding.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field `effective_labels` for all of the labels present on the resource.
        """
        return pulumi.get(self, "labels")

    @labels.setter
    def labels(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "labels", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Location of the membership


        - - -
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="membershipBindingId")
    def membership_binding_id(self) -> Optional[pulumi.Input[str]]:
        """
        The client-provided identifier of the membership binding.
        """
        return pulumi.get(self, "membership_binding_id")

    @membership_binding_id.setter
    def membership_binding_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "membership_binding_id", value)

    @property
    @pulumi.getter(name="membershipId")
    def membership_id(self) -> Optional[pulumi.Input[str]]:
        """
        Id of the membership
        """
        return pulumi.get(self, "membership_id")

    @membership_id.setter
    def membership_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "membership_id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The resource name for the membershipbinding itself
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
    @pulumi.getter(name="pulumiLabels")
    def pulumi_labels(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        The combination of labels configured directly on the resource
        and default labels configured on the provider.
        """
        return pulumi.get(self, "pulumi_labels")

    @pulumi_labels.setter
    def pulumi_labels(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "pulumi_labels", value)

    @property
    @pulumi.getter
    def scope(self) -> Optional[pulumi.Input[str]]:
        """
        A Workspace resource name in the format
        `projects/*/locations/*/scopes/*`.
        """
        return pulumi.get(self, "scope")

    @scope.setter
    def scope(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "scope", value)

    @property
    @pulumi.getter
    def states(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['MembershipBindingStateArgs']]]]:
        """
        State of the membership binding resource.
        Structure is documented below.
        """
        return pulumi.get(self, "states")

    @states.setter
    def states(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['MembershipBindingStateArgs']]]]):
        pulumi.set(self, "states", value)

    @property
    @pulumi.getter
    def uid(self) -> Optional[pulumi.Input[str]]:
        """
        Google-generated UUID for this resource.
        """
        return pulumi.get(self, "uid")

    @uid.setter
    def uid(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "uid", value)

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> Optional[pulumi.Input[str]]:
        """
        Time the MembershipBinding was updated in UTC.
        """
        return pulumi.get(self, "update_time")

    @update_time.setter
    def update_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "update_time", value)


class MembershipBinding(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 membership_binding_id: Optional[pulumi.Input[str]] = None,
                 membership_id: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 scope: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        MembershipBinding is a subresource of a Membership, representing what Fleet Scopes (or other, future Fleet resources) a Membership is bound to.

        To get more information about MembershipBinding, see:

        * [API documentation](https://cloud.google.com/anthos/fleet-management/docs/reference/rest/v1/projects.locations.memberships.bindings)
        * How-to Guides
            * [Registering a Cluster](https://cloud.google.com/anthos/multicluster-management/connect/registering-a-cluster#register_cluster)

        ## Example Usage

        ### Gkehub Membership Binding Basic

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        primary = gcp.container.Cluster("primary",
            name="basic-cluster",
            location="us-central1-a",
            initial_node_count=1,
            deletion_protection=True,
            network="default",
            subnetwork="default")
        membership = gcp.gkehub.Membership("membership",
            membership_id="tf-test-membership_75125",
            endpoint=gcp.gkehub.MembershipEndpointArgs(
                gke_cluster=gcp.gkehub.MembershipEndpointGkeClusterArgs(
                    resource_link=primary.id.apply(lambda id: f"//container.googleapis.com/{id}"),
                ),
            ))
        scope = gcp.gkehub.Scope("scope", scope_id="tf-test-scope_88722")
        membership_binding = gcp.gkehub.MembershipBinding("membership_binding",
            membership_binding_id="tf-test-membership-binding_39249",
            scope=scope.name,
            membership_id=membership.membership_id,
            location="global",
            labels={
                "keyb": "valueb",
                "keya": "valuea",
                "keyc": "valuec",
            })
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        MembershipBinding can be imported using any of these accepted formats:

        * `projects/{{project}}/locations/{{location}}/memberships/{{membership_id}}/bindings/{{membership_binding_id}}`

        * `{{project}}/{{location}}/{{membership_id}}/{{membership_binding_id}}`

        * `{{location}}/{{membership_id}}/{{membership_binding_id}}`

        When using the `pulumi import` command, MembershipBinding can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:gkehub/membershipBinding:MembershipBinding default projects/{{project}}/locations/{{location}}/memberships/{{membership_id}}/bindings/{{membership_binding_id}}
        ```

        ```sh
        $ pulumi import gcp:gkehub/membershipBinding:MembershipBinding default {{project}}/{{location}}/{{membership_id}}/{{membership_binding_id}}
        ```

        ```sh
        $ pulumi import gcp:gkehub/membershipBinding:MembershipBinding default {{location}}/{{membership_id}}/{{membership_binding_id}}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Labels for this Membership binding.
               
               **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
               Please refer to the field `effective_labels` for all of the labels present on the resource.
        :param pulumi.Input[str] location: Location of the membership
               
               
               - - -
        :param pulumi.Input[str] membership_binding_id: The client-provided identifier of the membership binding.
        :param pulumi.Input[str] membership_id: Id of the membership
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] scope: A Workspace resource name in the format
               `projects/*/locations/*/scopes/*`.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: MembershipBindingArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        MembershipBinding is a subresource of a Membership, representing what Fleet Scopes (or other, future Fleet resources) a Membership is bound to.

        To get more information about MembershipBinding, see:

        * [API documentation](https://cloud.google.com/anthos/fleet-management/docs/reference/rest/v1/projects.locations.memberships.bindings)
        * How-to Guides
            * [Registering a Cluster](https://cloud.google.com/anthos/multicluster-management/connect/registering-a-cluster#register_cluster)

        ## Example Usage

        ### Gkehub Membership Binding Basic

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        primary = gcp.container.Cluster("primary",
            name="basic-cluster",
            location="us-central1-a",
            initial_node_count=1,
            deletion_protection=True,
            network="default",
            subnetwork="default")
        membership = gcp.gkehub.Membership("membership",
            membership_id="tf-test-membership_75125",
            endpoint=gcp.gkehub.MembershipEndpointArgs(
                gke_cluster=gcp.gkehub.MembershipEndpointGkeClusterArgs(
                    resource_link=primary.id.apply(lambda id: f"//container.googleapis.com/{id}"),
                ),
            ))
        scope = gcp.gkehub.Scope("scope", scope_id="tf-test-scope_88722")
        membership_binding = gcp.gkehub.MembershipBinding("membership_binding",
            membership_binding_id="tf-test-membership-binding_39249",
            scope=scope.name,
            membership_id=membership.membership_id,
            location="global",
            labels={
                "keyb": "valueb",
                "keya": "valuea",
                "keyc": "valuec",
            })
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        MembershipBinding can be imported using any of these accepted formats:

        * `projects/{{project}}/locations/{{location}}/memberships/{{membership_id}}/bindings/{{membership_binding_id}}`

        * `{{project}}/{{location}}/{{membership_id}}/{{membership_binding_id}}`

        * `{{location}}/{{membership_id}}/{{membership_binding_id}}`

        When using the `pulumi import` command, MembershipBinding can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:gkehub/membershipBinding:MembershipBinding default projects/{{project}}/locations/{{location}}/memberships/{{membership_id}}/bindings/{{membership_binding_id}}
        ```

        ```sh
        $ pulumi import gcp:gkehub/membershipBinding:MembershipBinding default {{project}}/{{location}}/{{membership_id}}/{{membership_binding_id}}
        ```

        ```sh
        $ pulumi import gcp:gkehub/membershipBinding:MembershipBinding default {{location}}/{{membership_id}}/{{membership_binding_id}}
        ```

        :param str resource_name: The name of the resource.
        :param MembershipBindingArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(MembershipBindingArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 membership_binding_id: Optional[pulumi.Input[str]] = None,
                 membership_id: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 scope: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = MembershipBindingArgs.__new__(MembershipBindingArgs)

            __props__.__dict__["labels"] = labels
            if location is None and not opts.urn:
                raise TypeError("Missing required property 'location'")
            __props__.__dict__["location"] = location
            if membership_binding_id is None and not opts.urn:
                raise TypeError("Missing required property 'membership_binding_id'")
            __props__.__dict__["membership_binding_id"] = membership_binding_id
            if membership_id is None and not opts.urn:
                raise TypeError("Missing required property 'membership_id'")
            __props__.__dict__["membership_id"] = membership_id
            __props__.__dict__["project"] = project
            if scope is None and not opts.urn:
                raise TypeError("Missing required property 'scope'")
            __props__.__dict__["scope"] = scope
            __props__.__dict__["create_time"] = None
            __props__.__dict__["delete_time"] = None
            __props__.__dict__["effective_labels"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["pulumi_labels"] = None
            __props__.__dict__["states"] = None
            __props__.__dict__["uid"] = None
            __props__.__dict__["update_time"] = None
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["effectiveLabels", "pulumiLabels"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(MembershipBinding, __self__).__init__(
            'gcp:gkehub/membershipBinding:MembershipBinding',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            create_time: Optional[pulumi.Input[str]] = None,
            delete_time: Optional[pulumi.Input[str]] = None,
            effective_labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            location: Optional[pulumi.Input[str]] = None,
            membership_binding_id: Optional[pulumi.Input[str]] = None,
            membership_id: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            project: Optional[pulumi.Input[str]] = None,
            pulumi_labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            scope: Optional[pulumi.Input[str]] = None,
            states: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['MembershipBindingStateArgs']]]]] = None,
            uid: Optional[pulumi.Input[str]] = None,
            update_time: Optional[pulumi.Input[str]] = None) -> 'MembershipBinding':
        """
        Get an existing MembershipBinding resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] create_time: Time the MembershipBinding was created in UTC.
        :param pulumi.Input[str] delete_time: Time the MembershipBinding was deleted in UTC.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] effective_labels: All of labels (key/value pairs) present on the resource in GCP, including the labels configured through Pulumi, other clients and services.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Labels for this Membership binding.
               
               **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
               Please refer to the field `effective_labels` for all of the labels present on the resource.
        :param pulumi.Input[str] location: Location of the membership
               
               
               - - -
        :param pulumi.Input[str] membership_binding_id: The client-provided identifier of the membership binding.
        :param pulumi.Input[str] membership_id: Id of the membership
        :param pulumi.Input[str] name: The resource name for the membershipbinding itself
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] pulumi_labels: The combination of labels configured directly on the resource
               and default labels configured on the provider.
        :param pulumi.Input[str] scope: A Workspace resource name in the format
               `projects/*/locations/*/scopes/*`.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['MembershipBindingStateArgs']]]] states: State of the membership binding resource.
               Structure is documented below.
        :param pulumi.Input[str] uid: Google-generated UUID for this resource.
        :param pulumi.Input[str] update_time: Time the MembershipBinding was updated in UTC.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _MembershipBindingState.__new__(_MembershipBindingState)

        __props__.__dict__["create_time"] = create_time
        __props__.__dict__["delete_time"] = delete_time
        __props__.__dict__["effective_labels"] = effective_labels
        __props__.__dict__["labels"] = labels
        __props__.__dict__["location"] = location
        __props__.__dict__["membership_binding_id"] = membership_binding_id
        __props__.__dict__["membership_id"] = membership_id
        __props__.__dict__["name"] = name
        __props__.__dict__["project"] = project
        __props__.__dict__["pulumi_labels"] = pulumi_labels
        __props__.__dict__["scope"] = scope
        __props__.__dict__["states"] = states
        __props__.__dict__["uid"] = uid
        __props__.__dict__["update_time"] = update_time
        return MembershipBinding(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> pulumi.Output[str]:
        """
        Time the MembershipBinding was created in UTC.
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter(name="deleteTime")
    def delete_time(self) -> pulumi.Output[str]:
        """
        Time the MembershipBinding was deleted in UTC.
        """
        return pulumi.get(self, "delete_time")

    @property
    @pulumi.getter(name="effectiveLabels")
    def effective_labels(self) -> pulumi.Output[Mapping[str, str]]:
        """
        All of labels (key/value pairs) present on the resource in GCP, including the labels configured through Pulumi, other clients and services.
        """
        return pulumi.get(self, "effective_labels")

    @property
    @pulumi.getter
    def labels(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Labels for this Membership binding.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field `effective_labels` for all of the labels present on the resource.
        """
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Location of the membership


        - - -
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="membershipBindingId")
    def membership_binding_id(self) -> pulumi.Output[str]:
        """
        The client-provided identifier of the membership binding.
        """
        return pulumi.get(self, "membership_binding_id")

    @property
    @pulumi.getter(name="membershipId")
    def membership_id(self) -> pulumi.Output[str]:
        """
        Id of the membership
        """
        return pulumi.get(self, "membership_id")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The resource name for the membershipbinding itself
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
    @pulumi.getter(name="pulumiLabels")
    def pulumi_labels(self) -> pulumi.Output[Mapping[str, str]]:
        """
        The combination of labels configured directly on the resource
        and default labels configured on the provider.
        """
        return pulumi.get(self, "pulumi_labels")

    @property
    @pulumi.getter
    def scope(self) -> pulumi.Output[str]:
        """
        A Workspace resource name in the format
        `projects/*/locations/*/scopes/*`.
        """
        return pulumi.get(self, "scope")

    @property
    @pulumi.getter
    def states(self) -> pulumi.Output[Sequence['outputs.MembershipBindingState']]:
        """
        State of the membership binding resource.
        Structure is documented below.
        """
        return pulumi.get(self, "states")

    @property
    @pulumi.getter
    def uid(self) -> pulumi.Output[str]:
        """
        Google-generated UUID for this resource.
        """
        return pulumi.get(self, "uid")

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> pulumi.Output[str]:
        """
        Time the MembershipBinding was updated in UTC.
        """
        return pulumi.get(self, "update_time")


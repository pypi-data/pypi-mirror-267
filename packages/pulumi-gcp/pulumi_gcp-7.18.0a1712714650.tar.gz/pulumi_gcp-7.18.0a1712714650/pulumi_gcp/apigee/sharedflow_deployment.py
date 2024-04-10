# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['SharedflowDeploymentArgs', 'SharedflowDeployment']

@pulumi.input_type
class SharedflowDeploymentArgs:
    def __init__(__self__, *,
                 environment: pulumi.Input[str],
                 org_id: pulumi.Input[str],
                 revision: pulumi.Input[str],
                 sharedflow_id: pulumi.Input[str],
                 service_account: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a SharedflowDeployment resource.
        :param pulumi.Input[str] environment: The resource ID of the environment.
        :param pulumi.Input[str] org_id: The Apigee Organization associated with the Sharedflow
        :param pulumi.Input[str] revision: Revision of the Sharedflow to be deployed.
               
               
               - - -
        :param pulumi.Input[str] sharedflow_id: Id of the Sharedflow to be deployed.
        :param pulumi.Input[str] service_account: The service account represents the identity of the deployed proxy, and determines what permissions it has. The format must be {ACCOUNT_ID}@{PROJECT}.iam.gserviceaccount.com.
        """
        pulumi.set(__self__, "environment", environment)
        pulumi.set(__self__, "org_id", org_id)
        pulumi.set(__self__, "revision", revision)
        pulumi.set(__self__, "sharedflow_id", sharedflow_id)
        if service_account is not None:
            pulumi.set(__self__, "service_account", service_account)

    @property
    @pulumi.getter
    def environment(self) -> pulumi.Input[str]:
        """
        The resource ID of the environment.
        """
        return pulumi.get(self, "environment")

    @environment.setter
    def environment(self, value: pulumi.Input[str]):
        pulumi.set(self, "environment", value)

    @property
    @pulumi.getter(name="orgId")
    def org_id(self) -> pulumi.Input[str]:
        """
        The Apigee Organization associated with the Sharedflow
        """
        return pulumi.get(self, "org_id")

    @org_id.setter
    def org_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "org_id", value)

    @property
    @pulumi.getter
    def revision(self) -> pulumi.Input[str]:
        """
        Revision of the Sharedflow to be deployed.


        - - -
        """
        return pulumi.get(self, "revision")

    @revision.setter
    def revision(self, value: pulumi.Input[str]):
        pulumi.set(self, "revision", value)

    @property
    @pulumi.getter(name="sharedflowId")
    def sharedflow_id(self) -> pulumi.Input[str]:
        """
        Id of the Sharedflow to be deployed.
        """
        return pulumi.get(self, "sharedflow_id")

    @sharedflow_id.setter
    def sharedflow_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "sharedflow_id", value)

    @property
    @pulumi.getter(name="serviceAccount")
    def service_account(self) -> Optional[pulumi.Input[str]]:
        """
        The service account represents the identity of the deployed proxy, and determines what permissions it has. The format must be {ACCOUNT_ID}@{PROJECT}.iam.gserviceaccount.com.
        """
        return pulumi.get(self, "service_account")

    @service_account.setter
    def service_account(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "service_account", value)


@pulumi.input_type
class _SharedflowDeploymentState:
    def __init__(__self__, *,
                 environment: Optional[pulumi.Input[str]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 revision: Optional[pulumi.Input[str]] = None,
                 service_account: Optional[pulumi.Input[str]] = None,
                 sharedflow_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering SharedflowDeployment resources.
        :param pulumi.Input[str] environment: The resource ID of the environment.
        :param pulumi.Input[str] org_id: The Apigee Organization associated with the Sharedflow
        :param pulumi.Input[str] revision: Revision of the Sharedflow to be deployed.
               
               
               - - -
        :param pulumi.Input[str] service_account: The service account represents the identity of the deployed proxy, and determines what permissions it has. The format must be {ACCOUNT_ID}@{PROJECT}.iam.gserviceaccount.com.
        :param pulumi.Input[str] sharedflow_id: Id of the Sharedflow to be deployed.
        """
        if environment is not None:
            pulumi.set(__self__, "environment", environment)
        if org_id is not None:
            pulumi.set(__self__, "org_id", org_id)
        if revision is not None:
            pulumi.set(__self__, "revision", revision)
        if service_account is not None:
            pulumi.set(__self__, "service_account", service_account)
        if sharedflow_id is not None:
            pulumi.set(__self__, "sharedflow_id", sharedflow_id)

    @property
    @pulumi.getter
    def environment(self) -> Optional[pulumi.Input[str]]:
        """
        The resource ID of the environment.
        """
        return pulumi.get(self, "environment")

    @environment.setter
    def environment(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "environment", value)

    @property
    @pulumi.getter(name="orgId")
    def org_id(self) -> Optional[pulumi.Input[str]]:
        """
        The Apigee Organization associated with the Sharedflow
        """
        return pulumi.get(self, "org_id")

    @org_id.setter
    def org_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "org_id", value)

    @property
    @pulumi.getter
    def revision(self) -> Optional[pulumi.Input[str]]:
        """
        Revision of the Sharedflow to be deployed.


        - - -
        """
        return pulumi.get(self, "revision")

    @revision.setter
    def revision(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "revision", value)

    @property
    @pulumi.getter(name="serviceAccount")
    def service_account(self) -> Optional[pulumi.Input[str]]:
        """
        The service account represents the identity of the deployed proxy, and determines what permissions it has. The format must be {ACCOUNT_ID}@{PROJECT}.iam.gserviceaccount.com.
        """
        return pulumi.get(self, "service_account")

    @service_account.setter
    def service_account(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "service_account", value)

    @property
    @pulumi.getter(name="sharedflowId")
    def sharedflow_id(self) -> Optional[pulumi.Input[str]]:
        """
        Id of the Sharedflow to be deployed.
        """
        return pulumi.get(self, "sharedflow_id")

    @sharedflow_id.setter
    def sharedflow_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "sharedflow_id", value)


class SharedflowDeployment(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 environment: Optional[pulumi.Input[str]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 revision: Optional[pulumi.Input[str]] = None,
                 service_account: Optional[pulumi.Input[str]] = None,
                 sharedflow_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Deploys a revision of a sharedflow.

        To get more information about SharedflowDeployment, see:

        * [API documentation](https://cloud.google.com/apigee/docs/reference/apis/apigee/rest/v1/organizations.environments.sharedflows.revisions.deployments)
        * How-to Guides
            * [sharedflows.revisions.deployments](https://cloud.google.com/apigee/docs/reference/apis/apigee/rest/v1/organizations.environments.sharedflows.revisions.deployments)

        ## Import

        SharedflowDeployment can be imported using any of these accepted formats:

        * `organizations/{{org_id}}/environments/{{environment}}/sharedflows/{{sharedflow_id}}/revisions/{{revision}}/deployments/{{name}}`

        * `{{org_id}}/{{environment}}/{{sharedflow_id}}/{{revision}}/{{name}}`

        When using the `pulumi import` command, SharedflowDeployment can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:apigee/sharedflowDeployment:SharedflowDeployment default organizations/{{org_id}}/environments/{{environment}}/sharedflows/{{sharedflow_id}}/revisions/{{revision}}/deployments/{{name}}
        ```

        ```sh
        $ pulumi import gcp:apigee/sharedflowDeployment:SharedflowDeployment default {{org_id}}/{{environment}}/{{sharedflow_id}}/{{revision}}/{{name}}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] environment: The resource ID of the environment.
        :param pulumi.Input[str] org_id: The Apigee Organization associated with the Sharedflow
        :param pulumi.Input[str] revision: Revision of the Sharedflow to be deployed.
               
               
               - - -
        :param pulumi.Input[str] service_account: The service account represents the identity of the deployed proxy, and determines what permissions it has. The format must be {ACCOUNT_ID}@{PROJECT}.iam.gserviceaccount.com.
        :param pulumi.Input[str] sharedflow_id: Id of the Sharedflow to be deployed.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SharedflowDeploymentArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Deploys a revision of a sharedflow.

        To get more information about SharedflowDeployment, see:

        * [API documentation](https://cloud.google.com/apigee/docs/reference/apis/apigee/rest/v1/organizations.environments.sharedflows.revisions.deployments)
        * How-to Guides
            * [sharedflows.revisions.deployments](https://cloud.google.com/apigee/docs/reference/apis/apigee/rest/v1/organizations.environments.sharedflows.revisions.deployments)

        ## Import

        SharedflowDeployment can be imported using any of these accepted formats:

        * `organizations/{{org_id}}/environments/{{environment}}/sharedflows/{{sharedflow_id}}/revisions/{{revision}}/deployments/{{name}}`

        * `{{org_id}}/{{environment}}/{{sharedflow_id}}/{{revision}}/{{name}}`

        When using the `pulumi import` command, SharedflowDeployment can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:apigee/sharedflowDeployment:SharedflowDeployment default organizations/{{org_id}}/environments/{{environment}}/sharedflows/{{sharedflow_id}}/revisions/{{revision}}/deployments/{{name}}
        ```

        ```sh
        $ pulumi import gcp:apigee/sharedflowDeployment:SharedflowDeployment default {{org_id}}/{{environment}}/{{sharedflow_id}}/{{revision}}/{{name}}
        ```

        :param str resource_name: The name of the resource.
        :param SharedflowDeploymentArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SharedflowDeploymentArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 environment: Optional[pulumi.Input[str]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 revision: Optional[pulumi.Input[str]] = None,
                 service_account: Optional[pulumi.Input[str]] = None,
                 sharedflow_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = SharedflowDeploymentArgs.__new__(SharedflowDeploymentArgs)

            if environment is None and not opts.urn:
                raise TypeError("Missing required property 'environment'")
            __props__.__dict__["environment"] = environment
            if org_id is None and not opts.urn:
                raise TypeError("Missing required property 'org_id'")
            __props__.__dict__["org_id"] = org_id
            if revision is None and not opts.urn:
                raise TypeError("Missing required property 'revision'")
            __props__.__dict__["revision"] = revision
            __props__.__dict__["service_account"] = service_account
            if sharedflow_id is None and not opts.urn:
                raise TypeError("Missing required property 'sharedflow_id'")
            __props__.__dict__["sharedflow_id"] = sharedflow_id
        super(SharedflowDeployment, __self__).__init__(
            'gcp:apigee/sharedflowDeployment:SharedflowDeployment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            environment: Optional[pulumi.Input[str]] = None,
            org_id: Optional[pulumi.Input[str]] = None,
            revision: Optional[pulumi.Input[str]] = None,
            service_account: Optional[pulumi.Input[str]] = None,
            sharedflow_id: Optional[pulumi.Input[str]] = None) -> 'SharedflowDeployment':
        """
        Get an existing SharedflowDeployment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] environment: The resource ID of the environment.
        :param pulumi.Input[str] org_id: The Apigee Organization associated with the Sharedflow
        :param pulumi.Input[str] revision: Revision of the Sharedflow to be deployed.
               
               
               - - -
        :param pulumi.Input[str] service_account: The service account represents the identity of the deployed proxy, and determines what permissions it has. The format must be {ACCOUNT_ID}@{PROJECT}.iam.gserviceaccount.com.
        :param pulumi.Input[str] sharedflow_id: Id of the Sharedflow to be deployed.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _SharedflowDeploymentState.__new__(_SharedflowDeploymentState)

        __props__.__dict__["environment"] = environment
        __props__.__dict__["org_id"] = org_id
        __props__.__dict__["revision"] = revision
        __props__.__dict__["service_account"] = service_account
        __props__.__dict__["sharedflow_id"] = sharedflow_id
        return SharedflowDeployment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def environment(self) -> pulumi.Output[str]:
        """
        The resource ID of the environment.
        """
        return pulumi.get(self, "environment")

    @property
    @pulumi.getter(name="orgId")
    def org_id(self) -> pulumi.Output[str]:
        """
        The Apigee Organization associated with the Sharedflow
        """
        return pulumi.get(self, "org_id")

    @property
    @pulumi.getter
    def revision(self) -> pulumi.Output[str]:
        """
        Revision of the Sharedflow to be deployed.


        - - -
        """
        return pulumi.get(self, "revision")

    @property
    @pulumi.getter(name="serviceAccount")
    def service_account(self) -> pulumi.Output[Optional[str]]:
        """
        The service account represents the identity of the deployed proxy, and determines what permissions it has. The format must be {ACCOUNT_ID}@{PROJECT}.iam.gserviceaccount.com.
        """
        return pulumi.get(self, "service_account")

    @property
    @pulumi.getter(name="sharedflowId")
    def sharedflow_id(self) -> pulumi.Output[str]:
        """
        Id of the Sharedflow to be deployed.
        """
        return pulumi.get(self, "sharedflow_id")


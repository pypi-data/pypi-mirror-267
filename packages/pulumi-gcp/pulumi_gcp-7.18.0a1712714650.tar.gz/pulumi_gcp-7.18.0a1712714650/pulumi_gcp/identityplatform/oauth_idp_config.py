# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['OauthIdpConfigArgs', 'OauthIdpConfig']

@pulumi.input_type
class OauthIdpConfigArgs:
    def __init__(__self__, *,
                 client_id: pulumi.Input[str],
                 issuer: pulumi.Input[str],
                 client_secret: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a OauthIdpConfig resource.
        :param pulumi.Input[str] client_id: The client id of an OAuth client.
               
               
               - - -
        :param pulumi.Input[str] issuer: For OIDC Idps, the issuer identifier.
        :param pulumi.Input[str] client_secret: The client secret of the OAuth client, to enable OIDC code flow.
        :param pulumi.Input[str] display_name: Human friendly display name.
        :param pulumi.Input[bool] enabled: If this config allows users to sign in with the provider.
        :param pulumi.Input[str] name: The name of the OauthIdpConfig. Must start with `oidc.`.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        """
        pulumi.set(__self__, "client_id", client_id)
        pulumi.set(__self__, "issuer", issuer)
        if client_secret is not None:
            pulumi.set(__self__, "client_secret", client_secret)
        if display_name is not None:
            pulumi.set(__self__, "display_name", display_name)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if project is not None:
            pulumi.set(__self__, "project", project)

    @property
    @pulumi.getter(name="clientId")
    def client_id(self) -> pulumi.Input[str]:
        """
        The client id of an OAuth client.


        - - -
        """
        return pulumi.get(self, "client_id")

    @client_id.setter
    def client_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "client_id", value)

    @property
    @pulumi.getter
    def issuer(self) -> pulumi.Input[str]:
        """
        For OIDC Idps, the issuer identifier.
        """
        return pulumi.get(self, "issuer")

    @issuer.setter
    def issuer(self, value: pulumi.Input[str]):
        pulumi.set(self, "issuer", value)

    @property
    @pulumi.getter(name="clientSecret")
    def client_secret(self) -> Optional[pulumi.Input[str]]:
        """
        The client secret of the OAuth client, to enable OIDC code flow.
        """
        return pulumi.get(self, "client_secret")

    @client_secret.setter
    def client_secret(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "client_secret", value)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[pulumi.Input[str]]:
        """
        Human friendly display name.
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        If this config allows users to sign in with the provider.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the OauthIdpConfig. Must start with `oidc.`.
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


@pulumi.input_type
class _OauthIdpConfigState:
    def __init__(__self__, *,
                 client_id: Optional[pulumi.Input[str]] = None,
                 client_secret: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 issuer: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering OauthIdpConfig resources.
        :param pulumi.Input[str] client_id: The client id of an OAuth client.
               
               
               - - -
        :param pulumi.Input[str] client_secret: The client secret of the OAuth client, to enable OIDC code flow.
        :param pulumi.Input[str] display_name: Human friendly display name.
        :param pulumi.Input[bool] enabled: If this config allows users to sign in with the provider.
        :param pulumi.Input[str] issuer: For OIDC Idps, the issuer identifier.
        :param pulumi.Input[str] name: The name of the OauthIdpConfig. Must start with `oidc.`.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        """
        if client_id is not None:
            pulumi.set(__self__, "client_id", client_id)
        if client_secret is not None:
            pulumi.set(__self__, "client_secret", client_secret)
        if display_name is not None:
            pulumi.set(__self__, "display_name", display_name)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if issuer is not None:
            pulumi.set(__self__, "issuer", issuer)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if project is not None:
            pulumi.set(__self__, "project", project)

    @property
    @pulumi.getter(name="clientId")
    def client_id(self) -> Optional[pulumi.Input[str]]:
        """
        The client id of an OAuth client.


        - - -
        """
        return pulumi.get(self, "client_id")

    @client_id.setter
    def client_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "client_id", value)

    @property
    @pulumi.getter(name="clientSecret")
    def client_secret(self) -> Optional[pulumi.Input[str]]:
        """
        The client secret of the OAuth client, to enable OIDC code flow.
        """
        return pulumi.get(self, "client_secret")

    @client_secret.setter
    def client_secret(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "client_secret", value)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[pulumi.Input[str]]:
        """
        Human friendly display name.
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        If this config allows users to sign in with the provider.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter
    def issuer(self) -> Optional[pulumi.Input[str]]:
        """
        For OIDC Idps, the issuer identifier.
        """
        return pulumi.get(self, "issuer")

    @issuer.setter
    def issuer(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "issuer", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the OauthIdpConfig. Must start with `oidc.`.
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


class OauthIdpConfig(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 client_id: Optional[pulumi.Input[str]] = None,
                 client_secret: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 issuer: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        OIDC IdP configuration for a Identity Toolkit project.

        You must enable the
        [Google Identity Platform](https://console.cloud.google.com/marketplace/details/google-cloud-platform/customer-identity) in
        the marketplace prior to using this resource.

        ## Example Usage

        ### Identity Platform Oauth Idp Config Basic

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        oauth_idp_config = gcp.identityplatform.OauthIdpConfig("oauth_idp_config",
            name="oidc.oauth-idp-config",
            display_name="Display Name",
            client_id="client-id",
            issuer="issuer",
            enabled=True,
            client_secret="secret")
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        OauthIdpConfig can be imported using any of these accepted formats:

        * `projects/{{project}}/oauthIdpConfigs/{{name}}`

        * `{{project}}/{{name}}`

        * `{{name}}`

        When using the `pulumi import` command, OauthIdpConfig can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:identityplatform/oauthIdpConfig:OauthIdpConfig default projects/{{project}}/oauthIdpConfigs/{{name}}
        ```

        ```sh
        $ pulumi import gcp:identityplatform/oauthIdpConfig:OauthIdpConfig default {{project}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:identityplatform/oauthIdpConfig:OauthIdpConfig default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] client_id: The client id of an OAuth client.
               
               
               - - -
        :param pulumi.Input[str] client_secret: The client secret of the OAuth client, to enable OIDC code flow.
        :param pulumi.Input[str] display_name: Human friendly display name.
        :param pulumi.Input[bool] enabled: If this config allows users to sign in with the provider.
        :param pulumi.Input[str] issuer: For OIDC Idps, the issuer identifier.
        :param pulumi.Input[str] name: The name of the OauthIdpConfig. Must start with `oidc.`.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: OauthIdpConfigArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        OIDC IdP configuration for a Identity Toolkit project.

        You must enable the
        [Google Identity Platform](https://console.cloud.google.com/marketplace/details/google-cloud-platform/customer-identity) in
        the marketplace prior to using this resource.

        ## Example Usage

        ### Identity Platform Oauth Idp Config Basic

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        oauth_idp_config = gcp.identityplatform.OauthIdpConfig("oauth_idp_config",
            name="oidc.oauth-idp-config",
            display_name="Display Name",
            client_id="client-id",
            issuer="issuer",
            enabled=True,
            client_secret="secret")
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        OauthIdpConfig can be imported using any of these accepted formats:

        * `projects/{{project}}/oauthIdpConfigs/{{name}}`

        * `{{project}}/{{name}}`

        * `{{name}}`

        When using the `pulumi import` command, OauthIdpConfig can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:identityplatform/oauthIdpConfig:OauthIdpConfig default projects/{{project}}/oauthIdpConfigs/{{name}}
        ```

        ```sh
        $ pulumi import gcp:identityplatform/oauthIdpConfig:OauthIdpConfig default {{project}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:identityplatform/oauthIdpConfig:OauthIdpConfig default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param OauthIdpConfigArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(OauthIdpConfigArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 client_id: Optional[pulumi.Input[str]] = None,
                 client_secret: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 issuer: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = OauthIdpConfigArgs.__new__(OauthIdpConfigArgs)

            if client_id is None and not opts.urn:
                raise TypeError("Missing required property 'client_id'")
            __props__.__dict__["client_id"] = client_id
            __props__.__dict__["client_secret"] = client_secret
            __props__.__dict__["display_name"] = display_name
            __props__.__dict__["enabled"] = enabled
            if issuer is None and not opts.urn:
                raise TypeError("Missing required property 'issuer'")
            __props__.__dict__["issuer"] = issuer
            __props__.__dict__["name"] = name
            __props__.__dict__["project"] = project
        super(OauthIdpConfig, __self__).__init__(
            'gcp:identityplatform/oauthIdpConfig:OauthIdpConfig',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            client_id: Optional[pulumi.Input[str]] = None,
            client_secret: Optional[pulumi.Input[str]] = None,
            display_name: Optional[pulumi.Input[str]] = None,
            enabled: Optional[pulumi.Input[bool]] = None,
            issuer: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            project: Optional[pulumi.Input[str]] = None) -> 'OauthIdpConfig':
        """
        Get an existing OauthIdpConfig resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] client_id: The client id of an OAuth client.
               
               
               - - -
        :param pulumi.Input[str] client_secret: The client secret of the OAuth client, to enable OIDC code flow.
        :param pulumi.Input[str] display_name: Human friendly display name.
        :param pulumi.Input[bool] enabled: If this config allows users to sign in with the provider.
        :param pulumi.Input[str] issuer: For OIDC Idps, the issuer identifier.
        :param pulumi.Input[str] name: The name of the OauthIdpConfig. Must start with `oidc.`.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _OauthIdpConfigState.__new__(_OauthIdpConfigState)

        __props__.__dict__["client_id"] = client_id
        __props__.__dict__["client_secret"] = client_secret
        __props__.__dict__["display_name"] = display_name
        __props__.__dict__["enabled"] = enabled
        __props__.__dict__["issuer"] = issuer
        __props__.__dict__["name"] = name
        __props__.__dict__["project"] = project
        return OauthIdpConfig(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="clientId")
    def client_id(self) -> pulumi.Output[str]:
        """
        The client id of an OAuth client.


        - - -
        """
        return pulumi.get(self, "client_id")

    @property
    @pulumi.getter(name="clientSecret")
    def client_secret(self) -> pulumi.Output[Optional[str]]:
        """
        The client secret of the OAuth client, to enable OIDC code flow.
        """
        return pulumi.get(self, "client_secret")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Output[Optional[str]]:
        """
        Human friendly display name.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        If this config allows users to sign in with the provider.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter
    def issuer(self) -> pulumi.Output[str]:
        """
        For OIDC Idps, the issuer identifier.
        """
        return pulumi.get(self, "issuer")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the OauthIdpConfig. Must start with `oidc.`.
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


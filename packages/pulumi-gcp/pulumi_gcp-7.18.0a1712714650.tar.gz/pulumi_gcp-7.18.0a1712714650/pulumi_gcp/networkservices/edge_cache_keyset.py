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

__all__ = ['EdgeCacheKeysetArgs', 'EdgeCacheKeyset']

@pulumi.input_type
class EdgeCacheKeysetArgs:
    def __init__(__self__, *,
                 description: Optional[pulumi.Input[str]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 public_keys: Optional[pulumi.Input[Sequence[pulumi.Input['EdgeCacheKeysetPublicKeyArgs']]]] = None,
                 validation_shared_keys: Optional[pulumi.Input[Sequence[pulumi.Input['EdgeCacheKeysetValidationSharedKeyArgs']]]] = None):
        """
        The set of arguments for constructing a EdgeCacheKeyset resource.
        :param pulumi.Input[str] description: A human-readable description of the resource.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Set of label tags associated with the EdgeCache resource.
               **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
               Please refer to the field `effective_labels` for all of the labels present on the resource.
        :param pulumi.Input[str] name: Name of the resource; provided by the client when the resource is created.
               The name must be 1-64 characters long, and match the regular expression [a-zA-Z][a-zA-Z0-9_-]* which means the first character must be a letter,
               and all following characters must be a dash, underscore, letter or digit.
               
               
               - - -
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[Sequence[pulumi.Input['EdgeCacheKeysetPublicKeyArgs']]] public_keys: An ordered list of Ed25519 public keys to use for validating signed requests.
               You must specify `public_keys` or `validation_shared_keys` (or both). The keys in `public_keys` are checked first.
               You may specify no more than one Google-managed public key.
               If you specify `public_keys`, you must specify at least one (1) key and may specify up to three (3) keys.
               Ed25519 public keys are not secret, and only allow Google to validate a request was signed by your corresponding private key.
               Ensure that the private key is kept secret, and that only authorized users can add public keys to a keyset.
               Structure is documented below.
        :param pulumi.Input[Sequence[pulumi.Input['EdgeCacheKeysetValidationSharedKeyArgs']]] validation_shared_keys: An ordered list of shared keys to use for validating signed requests.
               Shared keys are secret.  Ensure that only authorized users can add `validation_shared_keys` to a keyset.
               You can rotate keys by appending (pushing) a new key to the list of `validation_shared_keys` and removing any superseded keys.
               You must specify `public_keys` or `validation_shared_keys` (or both). The keys in `public_keys` are checked first.
               Structure is documented below.
        """
        if description is not None:
            pulumi.set(__self__, "description", description)
        if labels is not None:
            pulumi.set(__self__, "labels", labels)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if public_keys is not None:
            pulumi.set(__self__, "public_keys", public_keys)
        if validation_shared_keys is not None:
            pulumi.set(__self__, "validation_shared_keys", validation_shared_keys)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A human-readable description of the resource.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def labels(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Set of label tags associated with the EdgeCache resource.
        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field `effective_labels` for all of the labels present on the resource.
        """
        return pulumi.get(self, "labels")

    @labels.setter
    def labels(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "labels", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the resource; provided by the client when the resource is created.
        The name must be 1-64 characters long, and match the regular expression [a-zA-Z][a-zA-Z0-9_-]* which means the first character must be a letter,
        and all following characters must be a dash, underscore, letter or digit.


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
        The ID of the project in which the resource belongs.
        If it is not provided, the provider project is used.
        """
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)

    @property
    @pulumi.getter(name="publicKeys")
    def public_keys(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['EdgeCacheKeysetPublicKeyArgs']]]]:
        """
        An ordered list of Ed25519 public keys to use for validating signed requests.
        You must specify `public_keys` or `validation_shared_keys` (or both). The keys in `public_keys` are checked first.
        You may specify no more than one Google-managed public key.
        If you specify `public_keys`, you must specify at least one (1) key and may specify up to three (3) keys.
        Ed25519 public keys are not secret, and only allow Google to validate a request was signed by your corresponding private key.
        Ensure that the private key is kept secret, and that only authorized users can add public keys to a keyset.
        Structure is documented below.
        """
        return pulumi.get(self, "public_keys")

    @public_keys.setter
    def public_keys(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['EdgeCacheKeysetPublicKeyArgs']]]]):
        pulumi.set(self, "public_keys", value)

    @property
    @pulumi.getter(name="validationSharedKeys")
    def validation_shared_keys(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['EdgeCacheKeysetValidationSharedKeyArgs']]]]:
        """
        An ordered list of shared keys to use for validating signed requests.
        Shared keys are secret.  Ensure that only authorized users can add `validation_shared_keys` to a keyset.
        You can rotate keys by appending (pushing) a new key to the list of `validation_shared_keys` and removing any superseded keys.
        You must specify `public_keys` or `validation_shared_keys` (or both). The keys in `public_keys` are checked first.
        Structure is documented below.
        """
        return pulumi.get(self, "validation_shared_keys")

    @validation_shared_keys.setter
    def validation_shared_keys(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['EdgeCacheKeysetValidationSharedKeyArgs']]]]):
        pulumi.set(self, "validation_shared_keys", value)


@pulumi.input_type
class _EdgeCacheKeysetState:
    def __init__(__self__, *,
                 description: Optional[pulumi.Input[str]] = None,
                 effective_labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 public_keys: Optional[pulumi.Input[Sequence[pulumi.Input['EdgeCacheKeysetPublicKeyArgs']]]] = None,
                 pulumi_labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 validation_shared_keys: Optional[pulumi.Input[Sequence[pulumi.Input['EdgeCacheKeysetValidationSharedKeyArgs']]]] = None):
        """
        Input properties used for looking up and filtering EdgeCacheKeyset resources.
        :param pulumi.Input[str] description: A human-readable description of the resource.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] effective_labels: All of labels (key/value pairs) present on the resource in GCP, including the labels configured through Pulumi, other clients and services.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Set of label tags associated with the EdgeCache resource.
               **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
               Please refer to the field `effective_labels` for all of the labels present on the resource.
        :param pulumi.Input[str] name: Name of the resource; provided by the client when the resource is created.
               The name must be 1-64 characters long, and match the regular expression [a-zA-Z][a-zA-Z0-9_-]* which means the first character must be a letter,
               and all following characters must be a dash, underscore, letter or digit.
               
               
               - - -
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[Sequence[pulumi.Input['EdgeCacheKeysetPublicKeyArgs']]] public_keys: An ordered list of Ed25519 public keys to use for validating signed requests.
               You must specify `public_keys` or `validation_shared_keys` (or both). The keys in `public_keys` are checked first.
               You may specify no more than one Google-managed public key.
               If you specify `public_keys`, you must specify at least one (1) key and may specify up to three (3) keys.
               Ed25519 public keys are not secret, and only allow Google to validate a request was signed by your corresponding private key.
               Ensure that the private key is kept secret, and that only authorized users can add public keys to a keyset.
               Structure is documented below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] pulumi_labels: The combination of labels configured directly on the resource
               and default labels configured on the provider.
        :param pulumi.Input[Sequence[pulumi.Input['EdgeCacheKeysetValidationSharedKeyArgs']]] validation_shared_keys: An ordered list of shared keys to use for validating signed requests.
               Shared keys are secret.  Ensure that only authorized users can add `validation_shared_keys` to a keyset.
               You can rotate keys by appending (pushing) a new key to the list of `validation_shared_keys` and removing any superseded keys.
               You must specify `public_keys` or `validation_shared_keys` (or both). The keys in `public_keys` are checked first.
               Structure is documented below.
        """
        if description is not None:
            pulumi.set(__self__, "description", description)
        if effective_labels is not None:
            pulumi.set(__self__, "effective_labels", effective_labels)
        if labels is not None:
            pulumi.set(__self__, "labels", labels)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if public_keys is not None:
            pulumi.set(__self__, "public_keys", public_keys)
        if pulumi_labels is not None:
            pulumi.set(__self__, "pulumi_labels", pulumi_labels)
        if validation_shared_keys is not None:
            pulumi.set(__self__, "validation_shared_keys", validation_shared_keys)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A human-readable description of the resource.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

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
        Set of label tags associated with the EdgeCache resource.
        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field `effective_labels` for all of the labels present on the resource.
        """
        return pulumi.get(self, "labels")

    @labels.setter
    def labels(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "labels", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the resource; provided by the client when the resource is created.
        The name must be 1-64 characters long, and match the regular expression [a-zA-Z][a-zA-Z0-9_-]* which means the first character must be a letter,
        and all following characters must be a dash, underscore, letter or digit.


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
        The ID of the project in which the resource belongs.
        If it is not provided, the provider project is used.
        """
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)

    @property
    @pulumi.getter(name="publicKeys")
    def public_keys(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['EdgeCacheKeysetPublicKeyArgs']]]]:
        """
        An ordered list of Ed25519 public keys to use for validating signed requests.
        You must specify `public_keys` or `validation_shared_keys` (or both). The keys in `public_keys` are checked first.
        You may specify no more than one Google-managed public key.
        If you specify `public_keys`, you must specify at least one (1) key and may specify up to three (3) keys.
        Ed25519 public keys are not secret, and only allow Google to validate a request was signed by your corresponding private key.
        Ensure that the private key is kept secret, and that only authorized users can add public keys to a keyset.
        Structure is documented below.
        """
        return pulumi.get(self, "public_keys")

    @public_keys.setter
    def public_keys(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['EdgeCacheKeysetPublicKeyArgs']]]]):
        pulumi.set(self, "public_keys", value)

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
    @pulumi.getter(name="validationSharedKeys")
    def validation_shared_keys(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['EdgeCacheKeysetValidationSharedKeyArgs']]]]:
        """
        An ordered list of shared keys to use for validating signed requests.
        Shared keys are secret.  Ensure that only authorized users can add `validation_shared_keys` to a keyset.
        You can rotate keys by appending (pushing) a new key to the list of `validation_shared_keys` and removing any superseded keys.
        You must specify `public_keys` or `validation_shared_keys` (or both). The keys in `public_keys` are checked first.
        Structure is documented below.
        """
        return pulumi.get(self, "validation_shared_keys")

    @validation_shared_keys.setter
    def validation_shared_keys(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['EdgeCacheKeysetValidationSharedKeyArgs']]]]):
        pulumi.set(self, "validation_shared_keys", value)


class EdgeCacheKeyset(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 public_keys: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['EdgeCacheKeysetPublicKeyArgs']]]]] = None,
                 validation_shared_keys: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['EdgeCacheKeysetValidationSharedKeyArgs']]]]] = None,
                 __props__=None):
        """
        EdgeCacheKeyset represents a collection of public keys used for validating signed requests.

        To get more information about EdgeCacheKeyset, see:

        * [API documentation](https://cloud.google.com/media-cdn/docs/reference/rest/v1/projects.locations.edgeCacheKeysets)
        * How-to Guides
            * [Create keysets](https://cloud.google.com/media-cdn/docs/create-keyset)

        ## Example Usage

        ### Network Services Edge Cache Keyset Basic

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        default = gcp.networkservices.EdgeCacheKeyset("default",
            name="my-keyset",
            description="The default keyset",
            public_keys=[
                gcp.networkservices.EdgeCacheKeysetPublicKeyArgs(
                    id="my-public-key",
                    value="FHsTyFHNmvNpw4o7-rp-M1yqMyBF8vXSBRkZtkQ0RKY",
                ),
                gcp.networkservices.EdgeCacheKeysetPublicKeyArgs(
                    id="my-public-key-2",
                    value="hzd03llxB1u5FOLKFkZ6_wCJqC7jtN0bg7xlBqS6WVM",
                ),
            ])
        ```
        <!--End PulumiCodeChooser -->
        ### Network Services Edge Cache Keyset Dual Token

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        secret_basic = gcp.secretmanager.Secret("secret-basic",
            secret_id="secret-name",
            replication=gcp.secretmanager.SecretReplicationArgs(
                auto=gcp.secretmanager.SecretReplicationAutoArgs(),
            ))
        secret_version_basic = gcp.secretmanager.SecretVersion("secret-version-basic",
            secret=secret_basic.id,
            secret_data="secret-data")
        default = gcp.networkservices.EdgeCacheKeyset("default",
            name="my-keyset",
            description="The default keyset",
            public_keys=[gcp.networkservices.EdgeCacheKeysetPublicKeyArgs(
                id="my-public-key",
                managed=True,
            )],
            validation_shared_keys=[gcp.networkservices.EdgeCacheKeysetValidationSharedKeyArgs(
                secret_version=secret_version_basic.id,
            )])
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        EdgeCacheKeyset can be imported using any of these accepted formats:

        * `projects/{{project}}/locations/global/edgeCacheKeysets/{{name}}`

        * `{{project}}/{{name}}`

        * `{{name}}`

        When using the `pulumi import` command, EdgeCacheKeyset can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:networkservices/edgeCacheKeyset:EdgeCacheKeyset default projects/{{project}}/locations/global/edgeCacheKeysets/{{name}}
        ```

        ```sh
        $ pulumi import gcp:networkservices/edgeCacheKeyset:EdgeCacheKeyset default {{project}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:networkservices/edgeCacheKeyset:EdgeCacheKeyset default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: A human-readable description of the resource.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Set of label tags associated with the EdgeCache resource.
               **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
               Please refer to the field `effective_labels` for all of the labels present on the resource.
        :param pulumi.Input[str] name: Name of the resource; provided by the client when the resource is created.
               The name must be 1-64 characters long, and match the regular expression [a-zA-Z][a-zA-Z0-9_-]* which means the first character must be a letter,
               and all following characters must be a dash, underscore, letter or digit.
               
               
               - - -
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['EdgeCacheKeysetPublicKeyArgs']]]] public_keys: An ordered list of Ed25519 public keys to use for validating signed requests.
               You must specify `public_keys` or `validation_shared_keys` (or both). The keys in `public_keys` are checked first.
               You may specify no more than one Google-managed public key.
               If you specify `public_keys`, you must specify at least one (1) key and may specify up to three (3) keys.
               Ed25519 public keys are not secret, and only allow Google to validate a request was signed by your corresponding private key.
               Ensure that the private key is kept secret, and that only authorized users can add public keys to a keyset.
               Structure is documented below.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['EdgeCacheKeysetValidationSharedKeyArgs']]]] validation_shared_keys: An ordered list of shared keys to use for validating signed requests.
               Shared keys are secret.  Ensure that only authorized users can add `validation_shared_keys` to a keyset.
               You can rotate keys by appending (pushing) a new key to the list of `validation_shared_keys` and removing any superseded keys.
               You must specify `public_keys` or `validation_shared_keys` (or both). The keys in `public_keys` are checked first.
               Structure is documented below.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[EdgeCacheKeysetArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        EdgeCacheKeyset represents a collection of public keys used for validating signed requests.

        To get more information about EdgeCacheKeyset, see:

        * [API documentation](https://cloud.google.com/media-cdn/docs/reference/rest/v1/projects.locations.edgeCacheKeysets)
        * How-to Guides
            * [Create keysets](https://cloud.google.com/media-cdn/docs/create-keyset)

        ## Example Usage

        ### Network Services Edge Cache Keyset Basic

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        default = gcp.networkservices.EdgeCacheKeyset("default",
            name="my-keyset",
            description="The default keyset",
            public_keys=[
                gcp.networkservices.EdgeCacheKeysetPublicKeyArgs(
                    id="my-public-key",
                    value="FHsTyFHNmvNpw4o7-rp-M1yqMyBF8vXSBRkZtkQ0RKY",
                ),
                gcp.networkservices.EdgeCacheKeysetPublicKeyArgs(
                    id="my-public-key-2",
                    value="hzd03llxB1u5FOLKFkZ6_wCJqC7jtN0bg7xlBqS6WVM",
                ),
            ])
        ```
        <!--End PulumiCodeChooser -->
        ### Network Services Edge Cache Keyset Dual Token

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        secret_basic = gcp.secretmanager.Secret("secret-basic",
            secret_id="secret-name",
            replication=gcp.secretmanager.SecretReplicationArgs(
                auto=gcp.secretmanager.SecretReplicationAutoArgs(),
            ))
        secret_version_basic = gcp.secretmanager.SecretVersion("secret-version-basic",
            secret=secret_basic.id,
            secret_data="secret-data")
        default = gcp.networkservices.EdgeCacheKeyset("default",
            name="my-keyset",
            description="The default keyset",
            public_keys=[gcp.networkservices.EdgeCacheKeysetPublicKeyArgs(
                id="my-public-key",
                managed=True,
            )],
            validation_shared_keys=[gcp.networkservices.EdgeCacheKeysetValidationSharedKeyArgs(
                secret_version=secret_version_basic.id,
            )])
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        EdgeCacheKeyset can be imported using any of these accepted formats:

        * `projects/{{project}}/locations/global/edgeCacheKeysets/{{name}}`

        * `{{project}}/{{name}}`

        * `{{name}}`

        When using the `pulumi import` command, EdgeCacheKeyset can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:networkservices/edgeCacheKeyset:EdgeCacheKeyset default projects/{{project}}/locations/global/edgeCacheKeysets/{{name}}
        ```

        ```sh
        $ pulumi import gcp:networkservices/edgeCacheKeyset:EdgeCacheKeyset default {{project}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:networkservices/edgeCacheKeyset:EdgeCacheKeyset default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param EdgeCacheKeysetArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(EdgeCacheKeysetArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 public_keys: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['EdgeCacheKeysetPublicKeyArgs']]]]] = None,
                 validation_shared_keys: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['EdgeCacheKeysetValidationSharedKeyArgs']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = EdgeCacheKeysetArgs.__new__(EdgeCacheKeysetArgs)

            __props__.__dict__["description"] = description
            __props__.__dict__["labels"] = labels
            __props__.__dict__["name"] = name
            __props__.__dict__["project"] = project
            __props__.__dict__["public_keys"] = public_keys
            __props__.__dict__["validation_shared_keys"] = validation_shared_keys
            __props__.__dict__["effective_labels"] = None
            __props__.__dict__["pulumi_labels"] = None
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["effectiveLabels", "pulumiLabels"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(EdgeCacheKeyset, __self__).__init__(
            'gcp:networkservices/edgeCacheKeyset:EdgeCacheKeyset',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            description: Optional[pulumi.Input[str]] = None,
            effective_labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            name: Optional[pulumi.Input[str]] = None,
            project: Optional[pulumi.Input[str]] = None,
            public_keys: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['EdgeCacheKeysetPublicKeyArgs']]]]] = None,
            pulumi_labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            validation_shared_keys: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['EdgeCacheKeysetValidationSharedKeyArgs']]]]] = None) -> 'EdgeCacheKeyset':
        """
        Get an existing EdgeCacheKeyset resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: A human-readable description of the resource.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] effective_labels: All of labels (key/value pairs) present on the resource in GCP, including the labels configured through Pulumi, other clients and services.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Set of label tags associated with the EdgeCache resource.
               **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
               Please refer to the field `effective_labels` for all of the labels present on the resource.
        :param pulumi.Input[str] name: Name of the resource; provided by the client when the resource is created.
               The name must be 1-64 characters long, and match the regular expression [a-zA-Z][a-zA-Z0-9_-]* which means the first character must be a letter,
               and all following characters must be a dash, underscore, letter or digit.
               
               
               - - -
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['EdgeCacheKeysetPublicKeyArgs']]]] public_keys: An ordered list of Ed25519 public keys to use for validating signed requests.
               You must specify `public_keys` or `validation_shared_keys` (or both). The keys in `public_keys` are checked first.
               You may specify no more than one Google-managed public key.
               If you specify `public_keys`, you must specify at least one (1) key and may specify up to three (3) keys.
               Ed25519 public keys are not secret, and only allow Google to validate a request was signed by your corresponding private key.
               Ensure that the private key is kept secret, and that only authorized users can add public keys to a keyset.
               Structure is documented below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] pulumi_labels: The combination of labels configured directly on the resource
               and default labels configured on the provider.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['EdgeCacheKeysetValidationSharedKeyArgs']]]] validation_shared_keys: An ordered list of shared keys to use for validating signed requests.
               Shared keys are secret.  Ensure that only authorized users can add `validation_shared_keys` to a keyset.
               You can rotate keys by appending (pushing) a new key to the list of `validation_shared_keys` and removing any superseded keys.
               You must specify `public_keys` or `validation_shared_keys` (or both). The keys in `public_keys` are checked first.
               Structure is documented below.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _EdgeCacheKeysetState.__new__(_EdgeCacheKeysetState)

        __props__.__dict__["description"] = description
        __props__.__dict__["effective_labels"] = effective_labels
        __props__.__dict__["labels"] = labels
        __props__.__dict__["name"] = name
        __props__.__dict__["project"] = project
        __props__.__dict__["public_keys"] = public_keys
        __props__.__dict__["pulumi_labels"] = pulumi_labels
        __props__.__dict__["validation_shared_keys"] = validation_shared_keys
        return EdgeCacheKeyset(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        A human-readable description of the resource.
        """
        return pulumi.get(self, "description")

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
        Set of label tags associated with the EdgeCache resource.
        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field `effective_labels` for all of the labels present on the resource.
        """
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the resource; provided by the client when the resource is created.
        The name must be 1-64 characters long, and match the regular expression [a-zA-Z][a-zA-Z0-9_-]* which means the first character must be a letter,
        and all following characters must be a dash, underscore, letter or digit.


        - - -
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
    @pulumi.getter(name="publicKeys")
    def public_keys(self) -> pulumi.Output[Optional[Sequence['outputs.EdgeCacheKeysetPublicKey']]]:
        """
        An ordered list of Ed25519 public keys to use for validating signed requests.
        You must specify `public_keys` or `validation_shared_keys` (or both). The keys in `public_keys` are checked first.
        You may specify no more than one Google-managed public key.
        If you specify `public_keys`, you must specify at least one (1) key and may specify up to three (3) keys.
        Ed25519 public keys are not secret, and only allow Google to validate a request was signed by your corresponding private key.
        Ensure that the private key is kept secret, and that only authorized users can add public keys to a keyset.
        Structure is documented below.
        """
        return pulumi.get(self, "public_keys")

    @property
    @pulumi.getter(name="pulumiLabels")
    def pulumi_labels(self) -> pulumi.Output[Mapping[str, str]]:
        """
        The combination of labels configured directly on the resource
        and default labels configured on the provider.
        """
        return pulumi.get(self, "pulumi_labels")

    @property
    @pulumi.getter(name="validationSharedKeys")
    def validation_shared_keys(self) -> pulumi.Output[Optional[Sequence['outputs.EdgeCacheKeysetValidationSharedKey']]]:
        """
        An ordered list of shared keys to use for validating signed requests.
        Shared keys are secret.  Ensure that only authorized users can add `validation_shared_keys` to a keyset.
        You can rotate keys by appending (pushing) a new key to the list of `validation_shared_keys` and removing any superseded keys.
        You must specify `public_keys` or `validation_shared_keys` (or both). The keys in `public_keys` are checked first.
        Structure is documented below.
        """
        return pulumi.get(self, "validation_shared_keys")


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

__all__ = ['RepositoryArgs', 'Repository']

@pulumi.input_type
class RepositoryArgs:
    def __init__(__self__, *,
                 display_name: Optional[pulumi.Input[str]] = None,
                 git_remote_settings: Optional[pulumi.Input['RepositoryGitRemoteSettingsArgs']] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 npmrc_environment_variables_secret_version: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 service_account: Optional[pulumi.Input[str]] = None,
                 workspace_compilation_overrides: Optional[pulumi.Input['RepositoryWorkspaceCompilationOverridesArgs']] = None):
        """
        The set of arguments for constructing a Repository resource.
        :param pulumi.Input[str] display_name: Optional. The repository's user-friendly name.
        :param pulumi.Input['RepositoryGitRemoteSettingsArgs'] git_remote_settings: Optional. If set, configures this repository to be linked to a Git remote.
               Structure is documented below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Optional. Repository user labels.
               An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.
               
               **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
               Please refer to the field `effective_labels` for all of the labels present on the resource.
        :param pulumi.Input[str] name: The repository's name.
               
               
               - - -
        :param pulumi.Input[str] npmrc_environment_variables_secret_version: Optional. The name of the Secret Manager secret version to be used to interpolate variables into the .npmrc file for package installation operations. Must be in the format projects/*/secrets/*/versions/*. The file itself must be in a JSON format.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] region: A reference to the region
        :param pulumi.Input[str] service_account: The service account to run workflow invocations under.
        :param pulumi.Input['RepositoryWorkspaceCompilationOverridesArgs'] workspace_compilation_overrides: If set, fields of workspaceCompilationOverrides override the default compilation settings that are specified in dataform.json when creating workspace-scoped compilation results.
               Structure is documented below.
        """
        if display_name is not None:
            pulumi.set(__self__, "display_name", display_name)
        if git_remote_settings is not None:
            pulumi.set(__self__, "git_remote_settings", git_remote_settings)
        if labels is not None:
            pulumi.set(__self__, "labels", labels)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if npmrc_environment_variables_secret_version is not None:
            pulumi.set(__self__, "npmrc_environment_variables_secret_version", npmrc_environment_variables_secret_version)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if region is not None:
            pulumi.set(__self__, "region", region)
        if service_account is not None:
            pulumi.set(__self__, "service_account", service_account)
        if workspace_compilation_overrides is not None:
            pulumi.set(__self__, "workspace_compilation_overrides", workspace_compilation_overrides)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. The repository's user-friendly name.
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter(name="gitRemoteSettings")
    def git_remote_settings(self) -> Optional[pulumi.Input['RepositoryGitRemoteSettingsArgs']]:
        """
        Optional. If set, configures this repository to be linked to a Git remote.
        Structure is documented below.
        """
        return pulumi.get(self, "git_remote_settings")

    @git_remote_settings.setter
    def git_remote_settings(self, value: Optional[pulumi.Input['RepositoryGitRemoteSettingsArgs']]):
        pulumi.set(self, "git_remote_settings", value)

    @property
    @pulumi.getter
    def labels(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Optional. Repository user labels.
        An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.

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
        The repository's name.


        - - -
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="npmrcEnvironmentVariablesSecretVersion")
    def npmrc_environment_variables_secret_version(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. The name of the Secret Manager secret version to be used to interpolate variables into the .npmrc file for package installation operations. Must be in the format projects/*/secrets/*/versions/*. The file itself must be in a JSON format.
        """
        return pulumi.get(self, "npmrc_environment_variables_secret_version")

    @npmrc_environment_variables_secret_version.setter
    def npmrc_environment_variables_secret_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "npmrc_environment_variables_secret_version", value)

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
    @pulumi.getter
    def region(self) -> Optional[pulumi.Input[str]]:
        """
        A reference to the region
        """
        return pulumi.get(self, "region")

    @region.setter
    def region(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "region", value)

    @property
    @pulumi.getter(name="serviceAccount")
    def service_account(self) -> Optional[pulumi.Input[str]]:
        """
        The service account to run workflow invocations under.
        """
        return pulumi.get(self, "service_account")

    @service_account.setter
    def service_account(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "service_account", value)

    @property
    @pulumi.getter(name="workspaceCompilationOverrides")
    def workspace_compilation_overrides(self) -> Optional[pulumi.Input['RepositoryWorkspaceCompilationOverridesArgs']]:
        """
        If set, fields of workspaceCompilationOverrides override the default compilation settings that are specified in dataform.json when creating workspace-scoped compilation results.
        Structure is documented below.
        """
        return pulumi.get(self, "workspace_compilation_overrides")

    @workspace_compilation_overrides.setter
    def workspace_compilation_overrides(self, value: Optional[pulumi.Input['RepositoryWorkspaceCompilationOverridesArgs']]):
        pulumi.set(self, "workspace_compilation_overrides", value)


@pulumi.input_type
class _RepositoryState:
    def __init__(__self__, *,
                 display_name: Optional[pulumi.Input[str]] = None,
                 effective_labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 git_remote_settings: Optional[pulumi.Input['RepositoryGitRemoteSettingsArgs']] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 npmrc_environment_variables_secret_version: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 pulumi_labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 service_account: Optional[pulumi.Input[str]] = None,
                 workspace_compilation_overrides: Optional[pulumi.Input['RepositoryWorkspaceCompilationOverridesArgs']] = None):
        """
        Input properties used for looking up and filtering Repository resources.
        :param pulumi.Input[str] display_name: Optional. The repository's user-friendly name.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] effective_labels: All of labels (key/value pairs) present on the resource in GCP, including the labels configured through Pulumi, other clients and services.
        :param pulumi.Input['RepositoryGitRemoteSettingsArgs'] git_remote_settings: Optional. If set, configures this repository to be linked to a Git remote.
               Structure is documented below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Optional. Repository user labels.
               An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.
               
               **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
               Please refer to the field `effective_labels` for all of the labels present on the resource.
        :param pulumi.Input[str] name: The repository's name.
               
               
               - - -
        :param pulumi.Input[str] npmrc_environment_variables_secret_version: Optional. The name of the Secret Manager secret version to be used to interpolate variables into the .npmrc file for package installation operations. Must be in the format projects/*/secrets/*/versions/*. The file itself must be in a JSON format.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] pulumi_labels: The combination of labels configured directly on the resource
               and default labels configured on the provider.
        :param pulumi.Input[str] region: A reference to the region
        :param pulumi.Input[str] service_account: The service account to run workflow invocations under.
        :param pulumi.Input['RepositoryWorkspaceCompilationOverridesArgs'] workspace_compilation_overrides: If set, fields of workspaceCompilationOverrides override the default compilation settings that are specified in dataform.json when creating workspace-scoped compilation results.
               Structure is documented below.
        """
        if display_name is not None:
            pulumi.set(__self__, "display_name", display_name)
        if effective_labels is not None:
            pulumi.set(__self__, "effective_labels", effective_labels)
        if git_remote_settings is not None:
            pulumi.set(__self__, "git_remote_settings", git_remote_settings)
        if labels is not None:
            pulumi.set(__self__, "labels", labels)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if npmrc_environment_variables_secret_version is not None:
            pulumi.set(__self__, "npmrc_environment_variables_secret_version", npmrc_environment_variables_secret_version)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if pulumi_labels is not None:
            pulumi.set(__self__, "pulumi_labels", pulumi_labels)
        if region is not None:
            pulumi.set(__self__, "region", region)
        if service_account is not None:
            pulumi.set(__self__, "service_account", service_account)
        if workspace_compilation_overrides is not None:
            pulumi.set(__self__, "workspace_compilation_overrides", workspace_compilation_overrides)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. The repository's user-friendly name.
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "display_name", value)

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
    @pulumi.getter(name="gitRemoteSettings")
    def git_remote_settings(self) -> Optional[pulumi.Input['RepositoryGitRemoteSettingsArgs']]:
        """
        Optional. If set, configures this repository to be linked to a Git remote.
        Structure is documented below.
        """
        return pulumi.get(self, "git_remote_settings")

    @git_remote_settings.setter
    def git_remote_settings(self, value: Optional[pulumi.Input['RepositoryGitRemoteSettingsArgs']]):
        pulumi.set(self, "git_remote_settings", value)

    @property
    @pulumi.getter
    def labels(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Optional. Repository user labels.
        An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.

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
        The repository's name.


        - - -
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="npmrcEnvironmentVariablesSecretVersion")
    def npmrc_environment_variables_secret_version(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. The name of the Secret Manager secret version to be used to interpolate variables into the .npmrc file for package installation operations. Must be in the format projects/*/secrets/*/versions/*. The file itself must be in a JSON format.
        """
        return pulumi.get(self, "npmrc_environment_variables_secret_version")

    @npmrc_environment_variables_secret_version.setter
    def npmrc_environment_variables_secret_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "npmrc_environment_variables_secret_version", value)

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
    def region(self) -> Optional[pulumi.Input[str]]:
        """
        A reference to the region
        """
        return pulumi.get(self, "region")

    @region.setter
    def region(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "region", value)

    @property
    @pulumi.getter(name="serviceAccount")
    def service_account(self) -> Optional[pulumi.Input[str]]:
        """
        The service account to run workflow invocations under.
        """
        return pulumi.get(self, "service_account")

    @service_account.setter
    def service_account(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "service_account", value)

    @property
    @pulumi.getter(name="workspaceCompilationOverrides")
    def workspace_compilation_overrides(self) -> Optional[pulumi.Input['RepositoryWorkspaceCompilationOverridesArgs']]:
        """
        If set, fields of workspaceCompilationOverrides override the default compilation settings that are specified in dataform.json when creating workspace-scoped compilation results.
        Structure is documented below.
        """
        return pulumi.get(self, "workspace_compilation_overrides")

    @workspace_compilation_overrides.setter
    def workspace_compilation_overrides(self, value: Optional[pulumi.Input['RepositoryWorkspaceCompilationOverridesArgs']]):
        pulumi.set(self, "workspace_compilation_overrides", value)


class Repository(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 git_remote_settings: Optional[pulumi.Input[pulumi.InputType['RepositoryGitRemoteSettingsArgs']]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 npmrc_environment_variables_secret_version: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 service_account: Optional[pulumi.Input[str]] = None,
                 workspace_compilation_overrides: Optional[pulumi.Input[pulumi.InputType['RepositoryWorkspaceCompilationOverridesArgs']]] = None,
                 __props__=None):
        """
        ## Example Usage

        ### Dataform Repository

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        secret = gcp.secretmanager.Secret("secret",
            secret_id="my-secret",
            replication=gcp.secretmanager.SecretReplicationArgs(
                auto=gcp.secretmanager.SecretReplicationAutoArgs(),
            ))
        secret_version = gcp.secretmanager.SecretVersion("secret_version",
            secret=secret.id,
            secret_data="secret-data")
        dataform_repository = gcp.dataform.Repository("dataform_repository",
            name="dataform_repository",
            display_name="dataform_repository",
            npmrc_environment_variables_secret_version=secret_version.id,
            labels={
                "label_foo1": "label-bar1",
            },
            git_remote_settings=gcp.dataform.RepositoryGitRemoteSettingsArgs(
                url="https://github.com/OWNER/REPOSITORY.git",
                default_branch="main",
                authentication_token_secret_version=secret_version.id,
            ),
            workspace_compilation_overrides=gcp.dataform.RepositoryWorkspaceCompilationOverridesArgs(
                default_database="database",
                schema_suffix="_suffix",
                table_prefix="prefix_",
            ))
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Repository can be imported using any of these accepted formats:

        * `projects/{{project}}/locations/{{region}}/repositories/{{name}}`

        * `{{project}}/{{region}}/{{name}}`

        * `{{region}}/{{name}}`

        * `{{name}}`

        When using the `pulumi import` command, Repository can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:dataform/repository:Repository default projects/{{project}}/locations/{{region}}/repositories/{{name}}
        ```

        ```sh
        $ pulumi import gcp:dataform/repository:Repository default {{project}}/{{region}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:dataform/repository:Repository default {{region}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:dataform/repository:Repository default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] display_name: Optional. The repository's user-friendly name.
        :param pulumi.Input[pulumi.InputType['RepositoryGitRemoteSettingsArgs']] git_remote_settings: Optional. If set, configures this repository to be linked to a Git remote.
               Structure is documented below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Optional. Repository user labels.
               An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.
               
               **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
               Please refer to the field `effective_labels` for all of the labels present on the resource.
        :param pulumi.Input[str] name: The repository's name.
               
               
               - - -
        :param pulumi.Input[str] npmrc_environment_variables_secret_version: Optional. The name of the Secret Manager secret version to be used to interpolate variables into the .npmrc file for package installation operations. Must be in the format projects/*/secrets/*/versions/*. The file itself must be in a JSON format.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] region: A reference to the region
        :param pulumi.Input[str] service_account: The service account to run workflow invocations under.
        :param pulumi.Input[pulumi.InputType['RepositoryWorkspaceCompilationOverridesArgs']] workspace_compilation_overrides: If set, fields of workspaceCompilationOverrides override the default compilation settings that are specified in dataform.json when creating workspace-scoped compilation results.
               Structure is documented below.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[RepositoryArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## Example Usage

        ### Dataform Repository

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        secret = gcp.secretmanager.Secret("secret",
            secret_id="my-secret",
            replication=gcp.secretmanager.SecretReplicationArgs(
                auto=gcp.secretmanager.SecretReplicationAutoArgs(),
            ))
        secret_version = gcp.secretmanager.SecretVersion("secret_version",
            secret=secret.id,
            secret_data="secret-data")
        dataform_repository = gcp.dataform.Repository("dataform_repository",
            name="dataform_repository",
            display_name="dataform_repository",
            npmrc_environment_variables_secret_version=secret_version.id,
            labels={
                "label_foo1": "label-bar1",
            },
            git_remote_settings=gcp.dataform.RepositoryGitRemoteSettingsArgs(
                url="https://github.com/OWNER/REPOSITORY.git",
                default_branch="main",
                authentication_token_secret_version=secret_version.id,
            ),
            workspace_compilation_overrides=gcp.dataform.RepositoryWorkspaceCompilationOverridesArgs(
                default_database="database",
                schema_suffix="_suffix",
                table_prefix="prefix_",
            ))
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Repository can be imported using any of these accepted formats:

        * `projects/{{project}}/locations/{{region}}/repositories/{{name}}`

        * `{{project}}/{{region}}/{{name}}`

        * `{{region}}/{{name}}`

        * `{{name}}`

        When using the `pulumi import` command, Repository can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:dataform/repository:Repository default projects/{{project}}/locations/{{region}}/repositories/{{name}}
        ```

        ```sh
        $ pulumi import gcp:dataform/repository:Repository default {{project}}/{{region}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:dataform/repository:Repository default {{region}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:dataform/repository:Repository default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param RepositoryArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(RepositoryArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 git_remote_settings: Optional[pulumi.Input[pulumi.InputType['RepositoryGitRemoteSettingsArgs']]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 npmrc_environment_variables_secret_version: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 service_account: Optional[pulumi.Input[str]] = None,
                 workspace_compilation_overrides: Optional[pulumi.Input[pulumi.InputType['RepositoryWorkspaceCompilationOverridesArgs']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = RepositoryArgs.__new__(RepositoryArgs)

            __props__.__dict__["display_name"] = display_name
            __props__.__dict__["git_remote_settings"] = git_remote_settings
            __props__.__dict__["labels"] = labels
            __props__.__dict__["name"] = name
            __props__.__dict__["npmrc_environment_variables_secret_version"] = npmrc_environment_variables_secret_version
            __props__.__dict__["project"] = project
            __props__.__dict__["region"] = region
            __props__.__dict__["service_account"] = service_account
            __props__.__dict__["workspace_compilation_overrides"] = workspace_compilation_overrides
            __props__.__dict__["effective_labels"] = None
            __props__.__dict__["pulumi_labels"] = None
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["effectiveLabels", "pulumiLabels"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(Repository, __self__).__init__(
            'gcp:dataform/repository:Repository',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            display_name: Optional[pulumi.Input[str]] = None,
            effective_labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            git_remote_settings: Optional[pulumi.Input[pulumi.InputType['RepositoryGitRemoteSettingsArgs']]] = None,
            labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            name: Optional[pulumi.Input[str]] = None,
            npmrc_environment_variables_secret_version: Optional[pulumi.Input[str]] = None,
            project: Optional[pulumi.Input[str]] = None,
            pulumi_labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            region: Optional[pulumi.Input[str]] = None,
            service_account: Optional[pulumi.Input[str]] = None,
            workspace_compilation_overrides: Optional[pulumi.Input[pulumi.InputType['RepositoryWorkspaceCompilationOverridesArgs']]] = None) -> 'Repository':
        """
        Get an existing Repository resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] display_name: Optional. The repository's user-friendly name.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] effective_labels: All of labels (key/value pairs) present on the resource in GCP, including the labels configured through Pulumi, other clients and services.
        :param pulumi.Input[pulumi.InputType['RepositoryGitRemoteSettingsArgs']] git_remote_settings: Optional. If set, configures this repository to be linked to a Git remote.
               Structure is documented below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Optional. Repository user labels.
               An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.
               
               **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
               Please refer to the field `effective_labels` for all of the labels present on the resource.
        :param pulumi.Input[str] name: The repository's name.
               
               
               - - -
        :param pulumi.Input[str] npmrc_environment_variables_secret_version: Optional. The name of the Secret Manager secret version to be used to interpolate variables into the .npmrc file for package installation operations. Must be in the format projects/*/secrets/*/versions/*. The file itself must be in a JSON format.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] pulumi_labels: The combination of labels configured directly on the resource
               and default labels configured on the provider.
        :param pulumi.Input[str] region: A reference to the region
        :param pulumi.Input[str] service_account: The service account to run workflow invocations under.
        :param pulumi.Input[pulumi.InputType['RepositoryWorkspaceCompilationOverridesArgs']] workspace_compilation_overrides: If set, fields of workspaceCompilationOverrides override the default compilation settings that are specified in dataform.json when creating workspace-scoped compilation results.
               Structure is documented below.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _RepositoryState.__new__(_RepositoryState)

        __props__.__dict__["display_name"] = display_name
        __props__.__dict__["effective_labels"] = effective_labels
        __props__.__dict__["git_remote_settings"] = git_remote_settings
        __props__.__dict__["labels"] = labels
        __props__.__dict__["name"] = name
        __props__.__dict__["npmrc_environment_variables_secret_version"] = npmrc_environment_variables_secret_version
        __props__.__dict__["project"] = project
        __props__.__dict__["pulumi_labels"] = pulumi_labels
        __props__.__dict__["region"] = region
        __props__.__dict__["service_account"] = service_account
        __props__.__dict__["workspace_compilation_overrides"] = workspace_compilation_overrides
        return Repository(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Output[Optional[str]]:
        """
        Optional. The repository's user-friendly name.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter(name="effectiveLabels")
    def effective_labels(self) -> pulumi.Output[Mapping[str, str]]:
        """
        All of labels (key/value pairs) present on the resource in GCP, including the labels configured through Pulumi, other clients and services.
        """
        return pulumi.get(self, "effective_labels")

    @property
    @pulumi.getter(name="gitRemoteSettings")
    def git_remote_settings(self) -> pulumi.Output[Optional['outputs.RepositoryGitRemoteSettings']]:
        """
        Optional. If set, configures this repository to be linked to a Git remote.
        Structure is documented below.
        """
        return pulumi.get(self, "git_remote_settings")

    @property
    @pulumi.getter
    def labels(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Optional. Repository user labels.
        An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field `effective_labels` for all of the labels present on the resource.
        """
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The repository's name.


        - - -
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="npmrcEnvironmentVariablesSecretVersion")
    def npmrc_environment_variables_secret_version(self) -> pulumi.Output[Optional[str]]:
        """
        Optional. The name of the Secret Manager secret version to be used to interpolate variables into the .npmrc file for package installation operations. Must be in the format projects/*/secrets/*/versions/*. The file itself must be in a JSON format.
        """
        return pulumi.get(self, "npmrc_environment_variables_secret_version")

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
    def region(self) -> pulumi.Output[Optional[str]]:
        """
        A reference to the region
        """
        return pulumi.get(self, "region")

    @property
    @pulumi.getter(name="serviceAccount")
    def service_account(self) -> pulumi.Output[Optional[str]]:
        """
        The service account to run workflow invocations under.
        """
        return pulumi.get(self, "service_account")

    @property
    @pulumi.getter(name="workspaceCompilationOverrides")
    def workspace_compilation_overrides(self) -> pulumi.Output[Optional['outputs.RepositoryWorkspaceCompilationOverrides']]:
        """
        If set, fields of workspaceCompilationOverrides override the default compilation settings that are specified in dataform.json when creating workspace-scoped compilation results.
        Structure is documented below.
        """
        return pulumi.get(self, "workspace_compilation_overrides")


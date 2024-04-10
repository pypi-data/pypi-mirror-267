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

__all__ = [
    'ConnectionGithubConfig',
    'ConnectionGithubConfigAuthorizerCredential',
    'ConnectionGithubEnterpriseConfig',
    'ConnectionGithubEnterpriseConfigServiceDirectoryConfig',
    'ConnectionGitlabConfig',
    'ConnectionGitlabConfigAuthorizerCredential',
    'ConnectionGitlabConfigReadAuthorizerCredential',
    'ConnectionGitlabConfigServiceDirectoryConfig',
    'ConnectionIAMBindingCondition',
    'ConnectionIAMMemberCondition',
    'ConnectionInstallationState',
]

@pulumi.output_type
class ConnectionGithubConfig(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "appInstallationId":
            suggest = "app_installation_id"
        elif key == "authorizerCredential":
            suggest = "authorizer_credential"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ConnectionGithubConfig. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ConnectionGithubConfig.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ConnectionGithubConfig.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 app_installation_id: Optional[int] = None,
                 authorizer_credential: Optional['outputs.ConnectionGithubConfigAuthorizerCredential'] = None):
        """
        :param int app_installation_id: GitHub App installation id.
        :param 'ConnectionGithubConfigAuthorizerCredentialArgs' authorizer_credential: OAuth credential of the account that authorized the Cloud Build GitHub App. It is recommended to use a robot account instead of a human user account. The OAuth token must be tied to the Cloud Build GitHub App.
               Structure is documented below.
        """
        if app_installation_id is not None:
            pulumi.set(__self__, "app_installation_id", app_installation_id)
        if authorizer_credential is not None:
            pulumi.set(__self__, "authorizer_credential", authorizer_credential)

    @property
    @pulumi.getter(name="appInstallationId")
    def app_installation_id(self) -> Optional[int]:
        """
        GitHub App installation id.
        """
        return pulumi.get(self, "app_installation_id")

    @property
    @pulumi.getter(name="authorizerCredential")
    def authorizer_credential(self) -> Optional['outputs.ConnectionGithubConfigAuthorizerCredential']:
        """
        OAuth credential of the account that authorized the Cloud Build GitHub App. It is recommended to use a robot account instead of a human user account. The OAuth token must be tied to the Cloud Build GitHub App.
        Structure is documented below.
        """
        return pulumi.get(self, "authorizer_credential")


@pulumi.output_type
class ConnectionGithubConfigAuthorizerCredential(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "oauthTokenSecretVersion":
            suggest = "oauth_token_secret_version"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ConnectionGithubConfigAuthorizerCredential. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ConnectionGithubConfigAuthorizerCredential.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ConnectionGithubConfigAuthorizerCredential.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 oauth_token_secret_version: Optional[str] = None,
                 username: Optional[str] = None):
        """
        :param str oauth_token_secret_version: A SecretManager resource containing the OAuth token that authorizes the Cloud Build connection. Format: `projects/*/secrets/*/versions/*`.
        :param str username: (Output)
               Output only. The username associated to this token.
        """
        if oauth_token_secret_version is not None:
            pulumi.set(__self__, "oauth_token_secret_version", oauth_token_secret_version)
        if username is not None:
            pulumi.set(__self__, "username", username)

    @property
    @pulumi.getter(name="oauthTokenSecretVersion")
    def oauth_token_secret_version(self) -> Optional[str]:
        """
        A SecretManager resource containing the OAuth token that authorizes the Cloud Build connection. Format: `projects/*/secrets/*/versions/*`.
        """
        return pulumi.get(self, "oauth_token_secret_version")

    @property
    @pulumi.getter
    def username(self) -> Optional[str]:
        """
        (Output)
        Output only. The username associated to this token.
        """
        return pulumi.get(self, "username")


@pulumi.output_type
class ConnectionGithubEnterpriseConfig(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "hostUri":
            suggest = "host_uri"
        elif key == "appId":
            suggest = "app_id"
        elif key == "appInstallationId":
            suggest = "app_installation_id"
        elif key == "appSlug":
            suggest = "app_slug"
        elif key == "privateKeySecretVersion":
            suggest = "private_key_secret_version"
        elif key == "serviceDirectoryConfig":
            suggest = "service_directory_config"
        elif key == "sslCa":
            suggest = "ssl_ca"
        elif key == "webhookSecretSecretVersion":
            suggest = "webhook_secret_secret_version"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ConnectionGithubEnterpriseConfig. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ConnectionGithubEnterpriseConfig.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ConnectionGithubEnterpriseConfig.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 host_uri: str,
                 app_id: Optional[int] = None,
                 app_installation_id: Optional[int] = None,
                 app_slug: Optional[str] = None,
                 private_key_secret_version: Optional[str] = None,
                 service_directory_config: Optional['outputs.ConnectionGithubEnterpriseConfigServiceDirectoryConfig'] = None,
                 ssl_ca: Optional[str] = None,
                 webhook_secret_secret_version: Optional[str] = None):
        """
        :param str host_uri: Required. The URI of the GitHub Enterprise host this connection is for.
        :param int app_id: Id of the GitHub App created from the manifest.
        :param int app_installation_id: ID of the installation of the GitHub App.
        :param str app_slug: The URL-friendly name of the GitHub App.
        :param str private_key_secret_version: SecretManager resource containing the private key of the GitHub App, formatted as `projects/*/secrets/*/versions/*`.
        :param 'ConnectionGithubEnterpriseConfigServiceDirectoryConfigArgs' service_directory_config: Configuration for using Service Directory to privately connect to a GitHub Enterprise server. This should only be set if the GitHub Enterprise server is hosted on-premises and not reachable by public internet. If this field is left empty, calls to the GitHub Enterprise server will be made over the public internet.
               Structure is documented below.
        :param str ssl_ca: SSL certificate to use for requests to GitHub Enterprise.
        :param str webhook_secret_secret_version: SecretManager resource containing the webhook secret of the GitHub App, formatted as `projects/*/secrets/*/versions/*`.
        """
        pulumi.set(__self__, "host_uri", host_uri)
        if app_id is not None:
            pulumi.set(__self__, "app_id", app_id)
        if app_installation_id is not None:
            pulumi.set(__self__, "app_installation_id", app_installation_id)
        if app_slug is not None:
            pulumi.set(__self__, "app_slug", app_slug)
        if private_key_secret_version is not None:
            pulumi.set(__self__, "private_key_secret_version", private_key_secret_version)
        if service_directory_config is not None:
            pulumi.set(__self__, "service_directory_config", service_directory_config)
        if ssl_ca is not None:
            pulumi.set(__self__, "ssl_ca", ssl_ca)
        if webhook_secret_secret_version is not None:
            pulumi.set(__self__, "webhook_secret_secret_version", webhook_secret_secret_version)

    @property
    @pulumi.getter(name="hostUri")
    def host_uri(self) -> str:
        """
        Required. The URI of the GitHub Enterprise host this connection is for.
        """
        return pulumi.get(self, "host_uri")

    @property
    @pulumi.getter(name="appId")
    def app_id(self) -> Optional[int]:
        """
        Id of the GitHub App created from the manifest.
        """
        return pulumi.get(self, "app_id")

    @property
    @pulumi.getter(name="appInstallationId")
    def app_installation_id(self) -> Optional[int]:
        """
        ID of the installation of the GitHub App.
        """
        return pulumi.get(self, "app_installation_id")

    @property
    @pulumi.getter(name="appSlug")
    def app_slug(self) -> Optional[str]:
        """
        The URL-friendly name of the GitHub App.
        """
        return pulumi.get(self, "app_slug")

    @property
    @pulumi.getter(name="privateKeySecretVersion")
    def private_key_secret_version(self) -> Optional[str]:
        """
        SecretManager resource containing the private key of the GitHub App, formatted as `projects/*/secrets/*/versions/*`.
        """
        return pulumi.get(self, "private_key_secret_version")

    @property
    @pulumi.getter(name="serviceDirectoryConfig")
    def service_directory_config(self) -> Optional['outputs.ConnectionGithubEnterpriseConfigServiceDirectoryConfig']:
        """
        Configuration for using Service Directory to privately connect to a GitHub Enterprise server. This should only be set if the GitHub Enterprise server is hosted on-premises and not reachable by public internet. If this field is left empty, calls to the GitHub Enterprise server will be made over the public internet.
        Structure is documented below.
        """
        return pulumi.get(self, "service_directory_config")

    @property
    @pulumi.getter(name="sslCa")
    def ssl_ca(self) -> Optional[str]:
        """
        SSL certificate to use for requests to GitHub Enterprise.
        """
        return pulumi.get(self, "ssl_ca")

    @property
    @pulumi.getter(name="webhookSecretSecretVersion")
    def webhook_secret_secret_version(self) -> Optional[str]:
        """
        SecretManager resource containing the webhook secret of the GitHub App, formatted as `projects/*/secrets/*/versions/*`.
        """
        return pulumi.get(self, "webhook_secret_secret_version")


@pulumi.output_type
class ConnectionGithubEnterpriseConfigServiceDirectoryConfig(dict):
    def __init__(__self__, *,
                 service: str):
        """
        :param str service: Required. The Service Directory service name. Format: projects/{project}/locations/{location}/namespaces/{namespace}/services/{service}.
        """
        pulumi.set(__self__, "service", service)

    @property
    @pulumi.getter
    def service(self) -> str:
        """
        Required. The Service Directory service name. Format: projects/{project}/locations/{location}/namespaces/{namespace}/services/{service}.
        """
        return pulumi.get(self, "service")


@pulumi.output_type
class ConnectionGitlabConfig(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "authorizerCredential":
            suggest = "authorizer_credential"
        elif key == "readAuthorizerCredential":
            suggest = "read_authorizer_credential"
        elif key == "webhookSecretSecretVersion":
            suggest = "webhook_secret_secret_version"
        elif key == "hostUri":
            suggest = "host_uri"
        elif key == "serverVersion":
            suggest = "server_version"
        elif key == "serviceDirectoryConfig":
            suggest = "service_directory_config"
        elif key == "sslCa":
            suggest = "ssl_ca"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ConnectionGitlabConfig. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ConnectionGitlabConfig.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ConnectionGitlabConfig.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 authorizer_credential: 'outputs.ConnectionGitlabConfigAuthorizerCredential',
                 read_authorizer_credential: 'outputs.ConnectionGitlabConfigReadAuthorizerCredential',
                 webhook_secret_secret_version: str,
                 host_uri: Optional[str] = None,
                 server_version: Optional[str] = None,
                 service_directory_config: Optional['outputs.ConnectionGitlabConfigServiceDirectoryConfig'] = None,
                 ssl_ca: Optional[str] = None):
        """
        :param 'ConnectionGitlabConfigAuthorizerCredentialArgs' authorizer_credential: Required. A GitLab personal access token with the `api` scope access.
               Structure is documented below.
        :param 'ConnectionGitlabConfigReadAuthorizerCredentialArgs' read_authorizer_credential: Required. A GitLab personal access token with the minimum `read_api` scope access.
               Structure is documented below.
        :param str webhook_secret_secret_version: Required. Immutable. SecretManager resource containing the webhook secret of a GitLab Enterprise project, formatted as `projects/*/secrets/*/versions/*`.
        :param str host_uri: The URI of the GitLab Enterprise host this connection is for. If not specified, the default value is https://gitlab.com.
        :param str server_version: (Output)
               Output only. Version of the GitLab Enterprise server running on the `host_uri`.
        :param 'ConnectionGitlabConfigServiceDirectoryConfigArgs' service_directory_config: Configuration for using Service Directory to privately connect to a GitLab Enterprise server. This should only be set if the GitLab Enterprise server is hosted on-premises and not reachable by public internet. If this field is left empty, calls to the GitLab Enterprise server will be made over the public internet.
               Structure is documented below.
        :param str ssl_ca: SSL certificate to use for requests to GitLab Enterprise.
        """
        pulumi.set(__self__, "authorizer_credential", authorizer_credential)
        pulumi.set(__self__, "read_authorizer_credential", read_authorizer_credential)
        pulumi.set(__self__, "webhook_secret_secret_version", webhook_secret_secret_version)
        if host_uri is not None:
            pulumi.set(__self__, "host_uri", host_uri)
        if server_version is not None:
            pulumi.set(__self__, "server_version", server_version)
        if service_directory_config is not None:
            pulumi.set(__self__, "service_directory_config", service_directory_config)
        if ssl_ca is not None:
            pulumi.set(__self__, "ssl_ca", ssl_ca)

    @property
    @pulumi.getter(name="authorizerCredential")
    def authorizer_credential(self) -> 'outputs.ConnectionGitlabConfigAuthorizerCredential':
        """
        Required. A GitLab personal access token with the `api` scope access.
        Structure is documented below.
        """
        return pulumi.get(self, "authorizer_credential")

    @property
    @pulumi.getter(name="readAuthorizerCredential")
    def read_authorizer_credential(self) -> 'outputs.ConnectionGitlabConfigReadAuthorizerCredential':
        """
        Required. A GitLab personal access token with the minimum `read_api` scope access.
        Structure is documented below.
        """
        return pulumi.get(self, "read_authorizer_credential")

    @property
    @pulumi.getter(name="webhookSecretSecretVersion")
    def webhook_secret_secret_version(self) -> str:
        """
        Required. Immutable. SecretManager resource containing the webhook secret of a GitLab Enterprise project, formatted as `projects/*/secrets/*/versions/*`.
        """
        return pulumi.get(self, "webhook_secret_secret_version")

    @property
    @pulumi.getter(name="hostUri")
    def host_uri(self) -> Optional[str]:
        """
        The URI of the GitLab Enterprise host this connection is for. If not specified, the default value is https://gitlab.com.
        """
        return pulumi.get(self, "host_uri")

    @property
    @pulumi.getter(name="serverVersion")
    def server_version(self) -> Optional[str]:
        """
        (Output)
        Output only. Version of the GitLab Enterprise server running on the `host_uri`.
        """
        return pulumi.get(self, "server_version")

    @property
    @pulumi.getter(name="serviceDirectoryConfig")
    def service_directory_config(self) -> Optional['outputs.ConnectionGitlabConfigServiceDirectoryConfig']:
        """
        Configuration for using Service Directory to privately connect to a GitLab Enterprise server. This should only be set if the GitLab Enterprise server is hosted on-premises and not reachable by public internet. If this field is left empty, calls to the GitLab Enterprise server will be made over the public internet.
        Structure is documented below.
        """
        return pulumi.get(self, "service_directory_config")

    @property
    @pulumi.getter(name="sslCa")
    def ssl_ca(self) -> Optional[str]:
        """
        SSL certificate to use for requests to GitLab Enterprise.
        """
        return pulumi.get(self, "ssl_ca")


@pulumi.output_type
class ConnectionGitlabConfigAuthorizerCredential(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "userTokenSecretVersion":
            suggest = "user_token_secret_version"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ConnectionGitlabConfigAuthorizerCredential. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ConnectionGitlabConfigAuthorizerCredential.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ConnectionGitlabConfigAuthorizerCredential.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 user_token_secret_version: str,
                 username: Optional[str] = None):
        """
        :param str user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Cloud Build connection. Format: `projects/*/secrets/*/versions/*`.
        :param str username: (Output)
               Output only. The username associated to this token.
        """
        pulumi.set(__self__, "user_token_secret_version", user_token_secret_version)
        if username is not None:
            pulumi.set(__self__, "username", username)

    @property
    @pulumi.getter(name="userTokenSecretVersion")
    def user_token_secret_version(self) -> str:
        """
        Required. A SecretManager resource containing the user token that authorizes the Cloud Build connection. Format: `projects/*/secrets/*/versions/*`.
        """
        return pulumi.get(self, "user_token_secret_version")

    @property
    @pulumi.getter
    def username(self) -> Optional[str]:
        """
        (Output)
        Output only. The username associated to this token.
        """
        return pulumi.get(self, "username")


@pulumi.output_type
class ConnectionGitlabConfigReadAuthorizerCredential(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "userTokenSecretVersion":
            suggest = "user_token_secret_version"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ConnectionGitlabConfigReadAuthorizerCredential. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ConnectionGitlabConfigReadAuthorizerCredential.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ConnectionGitlabConfigReadAuthorizerCredential.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 user_token_secret_version: str,
                 username: Optional[str] = None):
        """
        :param str user_token_secret_version: Required. A SecretManager resource containing the user token that authorizes the Cloud Build connection. Format: `projects/*/secrets/*/versions/*`.
        :param str username: (Output)
               Output only. The username associated to this token.
        """
        pulumi.set(__self__, "user_token_secret_version", user_token_secret_version)
        if username is not None:
            pulumi.set(__self__, "username", username)

    @property
    @pulumi.getter(name="userTokenSecretVersion")
    def user_token_secret_version(self) -> str:
        """
        Required. A SecretManager resource containing the user token that authorizes the Cloud Build connection. Format: `projects/*/secrets/*/versions/*`.
        """
        return pulumi.get(self, "user_token_secret_version")

    @property
    @pulumi.getter
    def username(self) -> Optional[str]:
        """
        (Output)
        Output only. The username associated to this token.
        """
        return pulumi.get(self, "username")


@pulumi.output_type
class ConnectionGitlabConfigServiceDirectoryConfig(dict):
    def __init__(__self__, *,
                 service: str):
        """
        :param str service: Required. The Service Directory service name. Format: projects/{project}/locations/{location}/namespaces/{namespace}/services/{service}.
        """
        pulumi.set(__self__, "service", service)

    @property
    @pulumi.getter
    def service(self) -> str:
        """
        Required. The Service Directory service name. Format: projects/{project}/locations/{location}/namespaces/{namespace}/services/{service}.
        """
        return pulumi.get(self, "service")


@pulumi.output_type
class ConnectionIAMBindingCondition(dict):
    def __init__(__self__, *,
                 expression: str,
                 title: str,
                 description: Optional[str] = None):
        pulumi.set(__self__, "expression", expression)
        pulumi.set(__self__, "title", title)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter
    def expression(self) -> str:
        return pulumi.get(self, "expression")

    @property
    @pulumi.getter
    def title(self) -> str:
        return pulumi.get(self, "title")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        return pulumi.get(self, "description")


@pulumi.output_type
class ConnectionIAMMemberCondition(dict):
    def __init__(__self__, *,
                 expression: str,
                 title: str,
                 description: Optional[str] = None):
        pulumi.set(__self__, "expression", expression)
        pulumi.set(__self__, "title", title)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter
    def expression(self) -> str:
        return pulumi.get(self, "expression")

    @property
    @pulumi.getter
    def title(self) -> str:
        return pulumi.get(self, "title")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        return pulumi.get(self, "description")


@pulumi.output_type
class ConnectionInstallationState(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "actionUri":
            suggest = "action_uri"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ConnectionInstallationState. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ConnectionInstallationState.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ConnectionInstallationState.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 action_uri: Optional[str] = None,
                 message: Optional[str] = None,
                 stage: Optional[str] = None):
        """
        :param str action_uri: (Output)
               Output only. Link to follow for next action. Empty string if the installation is already complete.
        :param str message: (Output)
               Output only. Message of what the user should do next to continue the installation. Empty string if the installation is already complete.
        :param str stage: (Output)
               Output only. Current step of the installation process.
        """
        if action_uri is not None:
            pulumi.set(__self__, "action_uri", action_uri)
        if message is not None:
            pulumi.set(__self__, "message", message)
        if stage is not None:
            pulumi.set(__self__, "stage", stage)

    @property
    @pulumi.getter(name="actionUri")
    def action_uri(self) -> Optional[str]:
        """
        (Output)
        Output only. Link to follow for next action. Empty string if the installation is already complete.
        """
        return pulumi.get(self, "action_uri")

    @property
    @pulumi.getter
    def message(self) -> Optional[str]:
        """
        (Output)
        Output only. Message of what the user should do next to continue the installation. Empty string if the installation is already complete.
        """
        return pulumi.get(self, "message")

    @property
    @pulumi.getter
    def stage(self) -> Optional[str]:
        """
        (Output)
        Output only. Current step of the installation process.
        """
        return pulumi.get(self, "stage")



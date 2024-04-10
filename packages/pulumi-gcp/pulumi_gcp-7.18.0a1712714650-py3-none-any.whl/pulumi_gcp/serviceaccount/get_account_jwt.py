# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'GetAccountJwtResult',
    'AwaitableGetAccountJwtResult',
    'get_account_jwt',
    'get_account_jwt_output',
]

@pulumi.output_type
class GetAccountJwtResult:
    """
    A collection of values returned by getAccountJwt.
    """
    def __init__(__self__, delegates=None, expires_in=None, id=None, jwt=None, payload=None, target_service_account=None):
        if delegates and not isinstance(delegates, list):
            raise TypeError("Expected argument 'delegates' to be a list")
        pulumi.set(__self__, "delegates", delegates)
        if expires_in and not isinstance(expires_in, int):
            raise TypeError("Expected argument 'expires_in' to be a int")
        pulumi.set(__self__, "expires_in", expires_in)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if jwt and not isinstance(jwt, str):
            raise TypeError("Expected argument 'jwt' to be a str")
        pulumi.set(__self__, "jwt", jwt)
        if payload and not isinstance(payload, str):
            raise TypeError("Expected argument 'payload' to be a str")
        pulumi.set(__self__, "payload", payload)
        if target_service_account and not isinstance(target_service_account, str):
            raise TypeError("Expected argument 'target_service_account' to be a str")
        pulumi.set(__self__, "target_service_account", target_service_account)

    @property
    @pulumi.getter
    def delegates(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "delegates")

    @property
    @pulumi.getter(name="expiresIn")
    def expires_in(self) -> Optional[int]:
        return pulumi.get(self, "expires_in")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def jwt(self) -> str:
        """
        The signed JWT containing the JWT Claims Set from the `payload`.
        """
        return pulumi.get(self, "jwt")

    @property
    @pulumi.getter
    def payload(self) -> str:
        return pulumi.get(self, "payload")

    @property
    @pulumi.getter(name="targetServiceAccount")
    def target_service_account(self) -> str:
        return pulumi.get(self, "target_service_account")


class AwaitableGetAccountJwtResult(GetAccountJwtResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAccountJwtResult(
            delegates=self.delegates,
            expires_in=self.expires_in,
            id=self.id,
            jwt=self.jwt,
            payload=self.payload,
            target_service_account=self.target_service_account)


def get_account_jwt(delegates: Optional[Sequence[str]] = None,
                    expires_in: Optional[int] = None,
                    payload: Optional[str] = None,
                    target_service_account: Optional[str] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAccountJwtResult:
    """
    This data source provides a [self-signed JWT](https://cloud.google.com/iam/docs/create-short-lived-credentials-direct#sa-credentials-jwt).  Tokens issued from this data source are typically used to call external services that accept JWTs for authentication.

    ## Example Usage

    Note: in order to use the following, the caller must have _at least_ `roles/iam.serviceAccountTokenCreator` on the `target_service_account`.

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import json
    import pulumi_gcp as gcp

    foo = gcp.serviceaccount.get_account_jwt(target_service_account="impersonated-account@project.iam.gserviceaccount.com",
        payload=json.dumps({
            "foo": "bar",
            "sub": "subject",
        }),
        expires_in=60)
    pulumi.export("jwt", foo.jwt)
    ```
    <!--End PulumiCodeChooser -->


    :param Sequence[str] delegates: Delegate chain of approvals needed to perform full impersonation. Specify the fully qualified service account name.
    :param int expires_in: Number of seconds until the JWT expires. If set and non-zero an `exp` claim will be added to the payload derived from the current timestamp plus expires_in seconds.
    :param str payload: The JSON-encoded JWT claims set to include in the self-signed JWT.
    :param str target_service_account: The email of the service account that will sign the JWT.
    """
    __args__ = dict()
    __args__['delegates'] = delegates
    __args__['expiresIn'] = expires_in
    __args__['payload'] = payload
    __args__['targetServiceAccount'] = target_service_account
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('gcp:serviceaccount/getAccountJwt:getAccountJwt', __args__, opts=opts, typ=GetAccountJwtResult).value

    return AwaitableGetAccountJwtResult(
        delegates=pulumi.get(__ret__, 'delegates'),
        expires_in=pulumi.get(__ret__, 'expires_in'),
        id=pulumi.get(__ret__, 'id'),
        jwt=pulumi.get(__ret__, 'jwt'),
        payload=pulumi.get(__ret__, 'payload'),
        target_service_account=pulumi.get(__ret__, 'target_service_account'))


@_utilities.lift_output_func(get_account_jwt)
def get_account_jwt_output(delegates: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                           expires_in: Optional[pulumi.Input[Optional[int]]] = None,
                           payload: Optional[pulumi.Input[str]] = None,
                           target_service_account: Optional[pulumi.Input[str]] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAccountJwtResult]:
    """
    This data source provides a [self-signed JWT](https://cloud.google.com/iam/docs/create-short-lived-credentials-direct#sa-credentials-jwt).  Tokens issued from this data source are typically used to call external services that accept JWTs for authentication.

    ## Example Usage

    Note: in order to use the following, the caller must have _at least_ `roles/iam.serviceAccountTokenCreator` on the `target_service_account`.

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import json
    import pulumi_gcp as gcp

    foo = gcp.serviceaccount.get_account_jwt(target_service_account="impersonated-account@project.iam.gserviceaccount.com",
        payload=json.dumps({
            "foo": "bar",
            "sub": "subject",
        }),
        expires_in=60)
    pulumi.export("jwt", foo.jwt)
    ```
    <!--End PulumiCodeChooser -->


    :param Sequence[str] delegates: Delegate chain of approvals needed to perform full impersonation. Specify the fully qualified service account name.
    :param int expires_in: Number of seconds until the JWT expires. If set and non-zero an `exp` claim will be added to the payload derived from the current timestamp plus expires_in seconds.
    :param str payload: The JSON-encoded JWT claims set to include in the self-signed JWT.
    :param str target_service_account: The email of the service account that will sign the JWT.
    """
    ...

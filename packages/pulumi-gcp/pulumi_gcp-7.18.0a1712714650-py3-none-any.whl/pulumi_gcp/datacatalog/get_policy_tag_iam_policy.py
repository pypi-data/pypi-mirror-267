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
    'GetPolicyTagIamPolicyResult',
    'AwaitableGetPolicyTagIamPolicyResult',
    'get_policy_tag_iam_policy',
    'get_policy_tag_iam_policy_output',
]

@pulumi.output_type
class GetPolicyTagIamPolicyResult:
    """
    A collection of values returned by getPolicyTagIamPolicy.
    """
    def __init__(__self__, etag=None, id=None, policy_data=None, policy_tag=None):
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if policy_data and not isinstance(policy_data, str):
            raise TypeError("Expected argument 'policy_data' to be a str")
        pulumi.set(__self__, "policy_data", policy_data)
        if policy_tag and not isinstance(policy_tag, str):
            raise TypeError("Expected argument 'policy_tag' to be a str")
        pulumi.set(__self__, "policy_tag", policy_tag)

    @property
    @pulumi.getter
    def etag(self) -> str:
        """
        (Computed) The etag of the IAM policy.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="policyData")
    def policy_data(self) -> str:
        """
        (Required only by `datacatalog.PolicyTagIamPolicy`) The policy data generated by
        a `organizations_get_iam_policy` data source.
        """
        return pulumi.get(self, "policy_data")

    @property
    @pulumi.getter(name="policyTag")
    def policy_tag(self) -> str:
        return pulumi.get(self, "policy_tag")


class AwaitableGetPolicyTagIamPolicyResult(GetPolicyTagIamPolicyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetPolicyTagIamPolicyResult(
            etag=self.etag,
            id=self.id,
            policy_data=self.policy_data,
            policy_tag=self.policy_tag)


def get_policy_tag_iam_policy(policy_tag: Optional[str] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetPolicyTagIamPolicyResult:
    """
    Retrieves the current IAM policy data for policytag

    ## example

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_gcp as gcp

    policy = gcp.datacatalog.get_policy_tag_iam_policy(policy_tag=basic_policy_tag["name"])
    ```
    <!--End PulumiCodeChooser -->


    :param str policy_tag: Used to find the parent resource to bind the IAM policy to
    """
    __args__ = dict()
    __args__['policyTag'] = policy_tag
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('gcp:datacatalog/getPolicyTagIamPolicy:getPolicyTagIamPolicy', __args__, opts=opts, typ=GetPolicyTagIamPolicyResult).value

    return AwaitableGetPolicyTagIamPolicyResult(
        etag=pulumi.get(__ret__, 'etag'),
        id=pulumi.get(__ret__, 'id'),
        policy_data=pulumi.get(__ret__, 'policy_data'),
        policy_tag=pulumi.get(__ret__, 'policy_tag'))


@_utilities.lift_output_func(get_policy_tag_iam_policy)
def get_policy_tag_iam_policy_output(policy_tag: Optional[pulumi.Input[str]] = None,
                                     opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetPolicyTagIamPolicyResult]:
    """
    Retrieves the current IAM policy data for policytag

    ## example

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_gcp as gcp

    policy = gcp.datacatalog.get_policy_tag_iam_policy(policy_tag=basic_policy_tag["name"])
    ```
    <!--End PulumiCodeChooser -->


    :param str policy_tag: Used to find the parent resource to bind the IAM policy to
    """
    ...

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
    'GetAccountIamPolicyResult',
    'AwaitableGetAccountIamPolicyResult',
    'get_account_iam_policy',
    'get_account_iam_policy_output',
]

@pulumi.output_type
class GetAccountIamPolicyResult:
    """
    A collection of values returned by getAccountIamPolicy.
    """
    def __init__(__self__, billing_account_id=None, etag=None, id=None, policy_data=None):
        if billing_account_id and not isinstance(billing_account_id, str):
            raise TypeError("Expected argument 'billing_account_id' to be a str")
        pulumi.set(__self__, "billing_account_id", billing_account_id)
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if policy_data and not isinstance(policy_data, str):
            raise TypeError("Expected argument 'policy_data' to be a str")
        pulumi.set(__self__, "policy_data", policy_data)

    @property
    @pulumi.getter(name="billingAccountId")
    def billing_account_id(self) -> str:
        return pulumi.get(self, "billing_account_id")

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
        (Computed) The policy data
        """
        return pulumi.get(self, "policy_data")


class AwaitableGetAccountIamPolicyResult(GetAccountIamPolicyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAccountIamPolicyResult(
            billing_account_id=self.billing_account_id,
            etag=self.etag,
            id=self.id,
            policy_data=self.policy_data)


def get_account_iam_policy(billing_account_id: Optional[str] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAccountIamPolicyResult:
    """
    Retrieves the current IAM policy data for a Billing Account.

    ## example

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_gcp as gcp

    policy = gcp.billing.get_account_iam_policy(billing_account_id="MEEP-MEEP-MEEP-MEEP-MEEP")
    ```
    <!--End PulumiCodeChooser -->


    :param str billing_account_id: The billing account id.
    """
    __args__ = dict()
    __args__['billingAccountId'] = billing_account_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('gcp:billing/getAccountIamPolicy:getAccountIamPolicy', __args__, opts=opts, typ=GetAccountIamPolicyResult).value

    return AwaitableGetAccountIamPolicyResult(
        billing_account_id=pulumi.get(__ret__, 'billing_account_id'),
        etag=pulumi.get(__ret__, 'etag'),
        id=pulumi.get(__ret__, 'id'),
        policy_data=pulumi.get(__ret__, 'policy_data'))


@_utilities.lift_output_func(get_account_iam_policy)
def get_account_iam_policy_output(billing_account_id: Optional[pulumi.Input[str]] = None,
                                  opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAccountIamPolicyResult]:
    """
    Retrieves the current IAM policy data for a Billing Account.

    ## example

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_gcp as gcp

    policy = gcp.billing.get_account_iam_policy(billing_account_id="MEEP-MEEP-MEEP-MEEP-MEEP")
    ```
    <!--End PulumiCodeChooser -->


    :param str billing_account_id: The billing account id.
    """
    ...

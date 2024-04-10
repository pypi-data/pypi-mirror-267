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
    'GetDicomStoreIamPolicyResult',
    'AwaitableGetDicomStoreIamPolicyResult',
    'get_dicom_store_iam_policy',
    'get_dicom_store_iam_policy_output',
]

@pulumi.output_type
class GetDicomStoreIamPolicyResult:
    """
    A collection of values returned by getDicomStoreIamPolicy.
    """
    def __init__(__self__, dicom_store_id=None, etag=None, id=None, policy_data=None):
        if dicom_store_id and not isinstance(dicom_store_id, str):
            raise TypeError("Expected argument 'dicom_store_id' to be a str")
        pulumi.set(__self__, "dicom_store_id", dicom_store_id)
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
    @pulumi.getter(name="dicomStoreId")
    def dicom_store_id(self) -> str:
        return pulumi.get(self, "dicom_store_id")

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


class AwaitableGetDicomStoreIamPolicyResult(GetDicomStoreIamPolicyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDicomStoreIamPolicyResult(
            dicom_store_id=self.dicom_store_id,
            etag=self.etag,
            id=self.id,
            policy_data=self.policy_data)


def get_dicom_store_iam_policy(dicom_store_id: Optional[str] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDicomStoreIamPolicyResult:
    """
    Retrieves the current IAM policy data for a Google Cloud Healthcare DICOM store.

    ## example

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_gcp as gcp

    foo = gcp.healthcare.get_dicom_store_iam_policy(dicom_store_id=dicom_store["id"])
    ```
    <!--End PulumiCodeChooser -->


    :param str dicom_store_id: The DICOM store ID, in the form
           `{project_id}/{location_name}/{dataset_name}/{dicom_store_name}` or
           `{location_name}/{dataset_name}/{dicom_store_name}`. In the second form, the provider's
           project setting will be used as a fallback.
    """
    __args__ = dict()
    __args__['dicomStoreId'] = dicom_store_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('gcp:healthcare/getDicomStoreIamPolicy:getDicomStoreIamPolicy', __args__, opts=opts, typ=GetDicomStoreIamPolicyResult).value

    return AwaitableGetDicomStoreIamPolicyResult(
        dicom_store_id=pulumi.get(__ret__, 'dicom_store_id'),
        etag=pulumi.get(__ret__, 'etag'),
        id=pulumi.get(__ret__, 'id'),
        policy_data=pulumi.get(__ret__, 'policy_data'))


@_utilities.lift_output_func(get_dicom_store_iam_policy)
def get_dicom_store_iam_policy_output(dicom_store_id: Optional[pulumi.Input[str]] = None,
                                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetDicomStoreIamPolicyResult]:
    """
    Retrieves the current IAM policy data for a Google Cloud Healthcare DICOM store.

    ## example

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_gcp as gcp

    foo = gcp.healthcare.get_dicom_store_iam_policy(dicom_store_id=dicom_store["id"])
    ```
    <!--End PulumiCodeChooser -->


    :param str dicom_store_id: The DICOM store ID, in the form
           `{project_id}/{location_name}/{dataset_name}/{dicom_store_name}` or
           `{location_name}/{dataset_name}/{dicom_store_name}`. In the second form, the provider's
           project setting will be used as a fallback.
    """
    ...

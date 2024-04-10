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
    'GetAttestorIamPolicyResult',
    'AwaitableGetAttestorIamPolicyResult',
    'get_attestor_iam_policy',
    'get_attestor_iam_policy_output',
]

@pulumi.output_type
class GetAttestorIamPolicyResult:
    """
    A collection of values returned by getAttestorIamPolicy.
    """
    def __init__(__self__, attestor=None, etag=None, id=None, policy_data=None, project=None):
        if attestor and not isinstance(attestor, str):
            raise TypeError("Expected argument 'attestor' to be a str")
        pulumi.set(__self__, "attestor", attestor)
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if policy_data and not isinstance(policy_data, str):
            raise TypeError("Expected argument 'policy_data' to be a str")
        pulumi.set(__self__, "policy_data", policy_data)
        if project and not isinstance(project, str):
            raise TypeError("Expected argument 'project' to be a str")
        pulumi.set(__self__, "project", project)

    @property
    @pulumi.getter
    def attestor(self) -> str:
        return pulumi.get(self, "attestor")

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
        (Required only by `binaryauthorization.AttestorIamPolicy`) The policy data generated by
        a `organizations_get_iam_policy` data source.
        """
        return pulumi.get(self, "policy_data")

    @property
    @pulumi.getter
    def project(self) -> str:
        return pulumi.get(self, "project")


class AwaitableGetAttestorIamPolicyResult(GetAttestorIamPolicyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAttestorIamPolicyResult(
            attestor=self.attestor,
            etag=self.etag,
            id=self.id,
            policy_data=self.policy_data,
            project=self.project)


def get_attestor_iam_policy(attestor: Optional[str] = None,
                            project: Optional[str] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAttestorIamPolicyResult:
    """
    Retrieves the current IAM policy data for attestor

    ## example

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_gcp as gcp

    policy = gcp.binaryauthorization.get_attestor_iam_policy(project=attestor["project"],
        attestor=attestor["name"])
    ```
    <!--End PulumiCodeChooser -->


    :param str attestor: Used to find the parent resource to bind the IAM policy to
    :param str project: The ID of the project in which the resource belongs.
           If it is not provided, the project will be parsed from the identifier of the parent resource. If no project is provided in the parent identifier and no project is specified, the provider project is used.
    """
    __args__ = dict()
    __args__['attestor'] = attestor
    __args__['project'] = project
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('gcp:binaryauthorization/getAttestorIamPolicy:getAttestorIamPolicy', __args__, opts=opts, typ=GetAttestorIamPolicyResult).value

    return AwaitableGetAttestorIamPolicyResult(
        attestor=pulumi.get(__ret__, 'attestor'),
        etag=pulumi.get(__ret__, 'etag'),
        id=pulumi.get(__ret__, 'id'),
        policy_data=pulumi.get(__ret__, 'policy_data'),
        project=pulumi.get(__ret__, 'project'))


@_utilities.lift_output_func(get_attestor_iam_policy)
def get_attestor_iam_policy_output(attestor: Optional[pulumi.Input[str]] = None,
                                   project: Optional[pulumi.Input[Optional[str]]] = None,
                                   opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAttestorIamPolicyResult]:
    """
    Retrieves the current IAM policy data for attestor

    ## example

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_gcp as gcp

    policy = gcp.binaryauthorization.get_attestor_iam_policy(project=attestor["project"],
        attestor=attestor["name"])
    ```
    <!--End PulumiCodeChooser -->


    :param str attestor: Used to find the parent resource to bind the IAM policy to
    :param str project: The ID of the project in which the resource belongs.
           If it is not provided, the project will be parsed from the identifier of the parent resource. If no project is provided in the parent identifier and no project is specified, the provider project is used.
    """
    ...

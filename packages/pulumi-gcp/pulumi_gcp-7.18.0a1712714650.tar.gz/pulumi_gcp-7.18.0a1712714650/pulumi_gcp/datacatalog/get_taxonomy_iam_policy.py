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
    'GetTaxonomyIamPolicyResult',
    'AwaitableGetTaxonomyIamPolicyResult',
    'get_taxonomy_iam_policy',
    'get_taxonomy_iam_policy_output',
]

@pulumi.output_type
class GetTaxonomyIamPolicyResult:
    """
    A collection of values returned by getTaxonomyIamPolicy.
    """
    def __init__(__self__, etag=None, id=None, policy_data=None, project=None, region=None, taxonomy=None):
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
        if region and not isinstance(region, str):
            raise TypeError("Expected argument 'region' to be a str")
        pulumi.set(__self__, "region", region)
        if taxonomy and not isinstance(taxonomy, str):
            raise TypeError("Expected argument 'taxonomy' to be a str")
        pulumi.set(__self__, "taxonomy", taxonomy)

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
        (Required only by `datacatalog.TaxonomyIamPolicy`) The policy data generated by
        a `organizations_get_iam_policy` data source.
        """
        return pulumi.get(self, "policy_data")

    @property
    @pulumi.getter
    def project(self) -> str:
        return pulumi.get(self, "project")

    @property
    @pulumi.getter
    def region(self) -> str:
        return pulumi.get(self, "region")

    @property
    @pulumi.getter
    def taxonomy(self) -> str:
        return pulumi.get(self, "taxonomy")


class AwaitableGetTaxonomyIamPolicyResult(GetTaxonomyIamPolicyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetTaxonomyIamPolicyResult(
            etag=self.etag,
            id=self.id,
            policy_data=self.policy_data,
            project=self.project,
            region=self.region,
            taxonomy=self.taxonomy)


def get_taxonomy_iam_policy(project: Optional[str] = None,
                            region: Optional[str] = None,
                            taxonomy: Optional[str] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetTaxonomyIamPolicyResult:
    """
    Retrieves the current IAM policy data for taxonomy

    ## example

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_gcp as gcp

    policy = gcp.datacatalog.get_taxonomy_iam_policy(taxonomy=basic_taxonomy["name"])
    ```
    <!--End PulumiCodeChooser -->


    :param str project: The ID of the project in which the resource belongs.
           If it is not provided, the project will be parsed from the identifier of the parent resource. If no project is provided in the parent identifier and no project is specified, the provider project is used.
    :param str taxonomy: Used to find the parent resource to bind the IAM policy to
    """
    __args__ = dict()
    __args__['project'] = project
    __args__['region'] = region
    __args__['taxonomy'] = taxonomy
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('gcp:datacatalog/getTaxonomyIamPolicy:getTaxonomyIamPolicy', __args__, opts=opts, typ=GetTaxonomyIamPolicyResult).value

    return AwaitableGetTaxonomyIamPolicyResult(
        etag=pulumi.get(__ret__, 'etag'),
        id=pulumi.get(__ret__, 'id'),
        policy_data=pulumi.get(__ret__, 'policy_data'),
        project=pulumi.get(__ret__, 'project'),
        region=pulumi.get(__ret__, 'region'),
        taxonomy=pulumi.get(__ret__, 'taxonomy'))


@_utilities.lift_output_func(get_taxonomy_iam_policy)
def get_taxonomy_iam_policy_output(project: Optional[pulumi.Input[Optional[str]]] = None,
                                   region: Optional[pulumi.Input[Optional[str]]] = None,
                                   taxonomy: Optional[pulumi.Input[str]] = None,
                                   opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetTaxonomyIamPolicyResult]:
    """
    Retrieves the current IAM policy data for taxonomy

    ## example

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_gcp as gcp

    policy = gcp.datacatalog.get_taxonomy_iam_policy(taxonomy=basic_taxonomy["name"])
    ```
    <!--End PulumiCodeChooser -->


    :param str project: The ID of the project in which the resource belongs.
           If it is not provided, the project will be parsed from the identifier of the parent resource. If no project is provided in the parent identifier and no project is specified, the provider project is used.
    :param str taxonomy: Used to find the parent resource to bind the IAM policy to
    """
    ...

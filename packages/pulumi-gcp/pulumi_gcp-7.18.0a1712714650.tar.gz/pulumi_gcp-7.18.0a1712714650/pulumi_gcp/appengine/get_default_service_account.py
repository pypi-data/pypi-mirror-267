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
    'GetDefaultServiceAccountResult',
    'AwaitableGetDefaultServiceAccountResult',
    'get_default_service_account',
    'get_default_service_account_output',
]

@pulumi.output_type
class GetDefaultServiceAccountResult:
    """
    A collection of values returned by getDefaultServiceAccount.
    """
    def __init__(__self__, display_name=None, email=None, id=None, member=None, name=None, project=None, unique_id=None):
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if email and not isinstance(email, str):
            raise TypeError("Expected argument 'email' to be a str")
        pulumi.set(__self__, "email", email)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if member and not isinstance(member, str):
            raise TypeError("Expected argument 'member' to be a str")
        pulumi.set(__self__, "member", member)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if project and not isinstance(project, str):
            raise TypeError("Expected argument 'project' to be a str")
        pulumi.set(__self__, "project", project)
        if unique_id and not isinstance(unique_id, str):
            raise TypeError("Expected argument 'unique_id' to be a str")
        pulumi.set(__self__, "unique_id", unique_id)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> str:
        """
        The display name for the service account.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def email(self) -> str:
        """
        Email address of the default service account used by App Engine in this project.
        """
        return pulumi.get(self, "email")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def member(self) -> str:
        """
        The Identity of the service account in the form `serviceAccount:{email}`. This value is often used to refer to the service account in order to grant IAM permissions.
        """
        return pulumi.get(self, "member")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The fully-qualified name of the service account.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def project(self) -> str:
        return pulumi.get(self, "project")

    @property
    @pulumi.getter(name="uniqueId")
    def unique_id(self) -> str:
        """
        The unique id of the service account.
        """
        return pulumi.get(self, "unique_id")


class AwaitableGetDefaultServiceAccountResult(GetDefaultServiceAccountResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDefaultServiceAccountResult(
            display_name=self.display_name,
            email=self.email,
            id=self.id,
            member=self.member,
            name=self.name,
            project=self.project,
            unique_id=self.unique_id)


def get_default_service_account(project: Optional[str] = None,
                                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDefaultServiceAccountResult:
    """
    Use this data source to retrieve the default App Engine service account for the specified project.

    ## Example Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_gcp as gcp

    default = gcp.appengine.get_default_service_account()
    pulumi.export("defaultAccount", default.email)
    ```
    <!--End PulumiCodeChooser -->


    :param str project: The project ID. If it is not provided, the provider project is used.
    """
    __args__ = dict()
    __args__['project'] = project
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('gcp:appengine/getDefaultServiceAccount:getDefaultServiceAccount', __args__, opts=opts, typ=GetDefaultServiceAccountResult).value

    return AwaitableGetDefaultServiceAccountResult(
        display_name=pulumi.get(__ret__, 'display_name'),
        email=pulumi.get(__ret__, 'email'),
        id=pulumi.get(__ret__, 'id'),
        member=pulumi.get(__ret__, 'member'),
        name=pulumi.get(__ret__, 'name'),
        project=pulumi.get(__ret__, 'project'),
        unique_id=pulumi.get(__ret__, 'unique_id'))


@_utilities.lift_output_func(get_default_service_account)
def get_default_service_account_output(project: Optional[pulumi.Input[Optional[str]]] = None,
                                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetDefaultServiceAccountResult]:
    """
    Use this data source to retrieve the default App Engine service account for the specified project.

    ## Example Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_gcp as gcp

    default = gcp.appengine.get_default_service_account()
    pulumi.export("defaultAccount", default.email)
    ```
    <!--End PulumiCodeChooser -->


    :param str project: The project ID. If it is not provided, the provider project is used.
    """
    ...

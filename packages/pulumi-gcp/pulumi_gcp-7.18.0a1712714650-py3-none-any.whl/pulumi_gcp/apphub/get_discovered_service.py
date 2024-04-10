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
    'GetDiscoveredServiceResult',
    'AwaitableGetDiscoveredServiceResult',
    'get_discovered_service',
    'get_discovered_service_output',
]

@pulumi.output_type
class GetDiscoveredServiceResult:
    """
    A collection of values returned by getDiscoveredService.
    """
    def __init__(__self__, id=None, location=None, name=None, project=None, service_properties=None, service_references=None, service_uri=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if project and not isinstance(project, str):
            raise TypeError("Expected argument 'project' to be a str")
        pulumi.set(__self__, "project", project)
        if service_properties and not isinstance(service_properties, list):
            raise TypeError("Expected argument 'service_properties' to be a list")
        pulumi.set(__self__, "service_properties", service_properties)
        if service_references and not isinstance(service_references, list):
            raise TypeError("Expected argument 'service_references' to be a list")
        pulumi.set(__self__, "service_references", service_references)
        if service_uri and not isinstance(service_uri, str):
            raise TypeError("Expected argument 'service_uri' to be a str")
        pulumi.set(__self__, "service_uri", service_uri)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        The location that the underlying resource resides in.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name of a Service. Format: "projects/{host-project-id}/locations/{location}/applications/{application-id}/services/{service-id}".
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def project(self) -> Optional[str]:
        return pulumi.get(self, "project")

    @property
    @pulumi.getter(name="serviceProperties")
    def service_properties(self) -> Sequence['outputs.GetDiscoveredServiceServicePropertyResult']:
        """
        Properties of an underlying compute resource that can comprise a Service. Structure is documented below
        """
        return pulumi.get(self, "service_properties")

    @property
    @pulumi.getter(name="serviceReferences")
    def service_references(self) -> Sequence['outputs.GetDiscoveredServiceServiceReferenceResult']:
        """
        Reference to an underlying networking resource that can comprise a Service. Structure is documented below
        """
        return pulumi.get(self, "service_references")

    @property
    @pulumi.getter(name="serviceUri")
    def service_uri(self) -> str:
        return pulumi.get(self, "service_uri")


class AwaitableGetDiscoveredServiceResult(GetDiscoveredServiceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDiscoveredServiceResult(
            id=self.id,
            location=self.location,
            name=self.name,
            project=self.project,
            service_properties=self.service_properties,
            service_references=self.service_references,
            service_uri=self.service_uri)


def get_discovered_service(location: Optional[str] = None,
                           project: Optional[str] = None,
                           service_uri: Optional[str] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDiscoveredServiceResult:
    """
    Get information about a discovered service from its uri.

    ## Example Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_gcp as gcp

    my_service = gcp.apphub.get_discovered_service(location="my-location",
        service_uri="my-service-uri")
    ```
    <!--End PulumiCodeChooser -->


    :param str location: The location of the discovered service.
    :param str project: The host project of the discovered service.
    :param str service_uri: The uri of the service.
    """
    __args__ = dict()
    __args__['location'] = location
    __args__['project'] = project
    __args__['serviceUri'] = service_uri
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('gcp:apphub/getDiscoveredService:getDiscoveredService', __args__, opts=opts, typ=GetDiscoveredServiceResult).value

    return AwaitableGetDiscoveredServiceResult(
        id=pulumi.get(__ret__, 'id'),
        location=pulumi.get(__ret__, 'location'),
        name=pulumi.get(__ret__, 'name'),
        project=pulumi.get(__ret__, 'project'),
        service_properties=pulumi.get(__ret__, 'service_properties'),
        service_references=pulumi.get(__ret__, 'service_references'),
        service_uri=pulumi.get(__ret__, 'service_uri'))


@_utilities.lift_output_func(get_discovered_service)
def get_discovered_service_output(location: Optional[pulumi.Input[str]] = None,
                                  project: Optional[pulumi.Input[Optional[str]]] = None,
                                  service_uri: Optional[pulumi.Input[str]] = None,
                                  opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetDiscoveredServiceResult]:
    """
    Get information about a discovered service from its uri.

    ## Example Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_gcp as gcp

    my_service = gcp.apphub.get_discovered_service(location="my-location",
        service_uri="my-service-uri")
    ```
    <!--End PulumiCodeChooser -->


    :param str location: The location of the discovered service.
    :param str project: The host project of the discovered service.
    :param str service_uri: The uri of the service.
    """
    ...

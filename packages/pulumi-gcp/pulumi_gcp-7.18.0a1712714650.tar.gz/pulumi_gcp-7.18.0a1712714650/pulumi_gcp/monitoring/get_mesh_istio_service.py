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
    'GetMeshIstioServiceResult',
    'AwaitableGetMeshIstioServiceResult',
    'get_mesh_istio_service',
    'get_mesh_istio_service_output',
]

@pulumi.output_type
class GetMeshIstioServiceResult:
    """
    A collection of values returned by getMeshIstioService.
    """
    def __init__(__self__, display_name=None, id=None, mesh_uid=None, name=None, project=None, service_id=None, service_name=None, service_namespace=None, telemetries=None, user_labels=None):
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if mesh_uid and not isinstance(mesh_uid, str):
            raise TypeError("Expected argument 'mesh_uid' to be a str")
        pulumi.set(__self__, "mesh_uid", mesh_uid)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if project and not isinstance(project, str):
            raise TypeError("Expected argument 'project' to be a str")
        pulumi.set(__self__, "project", project)
        if service_id and not isinstance(service_id, str):
            raise TypeError("Expected argument 'service_id' to be a str")
        pulumi.set(__self__, "service_id", service_id)
        if service_name and not isinstance(service_name, str):
            raise TypeError("Expected argument 'service_name' to be a str")
        pulumi.set(__self__, "service_name", service_name)
        if service_namespace and not isinstance(service_namespace, str):
            raise TypeError("Expected argument 'service_namespace' to be a str")
        pulumi.set(__self__, "service_namespace", service_namespace)
        if telemetries and not isinstance(telemetries, list):
            raise TypeError("Expected argument 'telemetries' to be a list")
        pulumi.set(__self__, "telemetries", telemetries)
        if user_labels and not isinstance(user_labels, dict):
            raise TypeError("Expected argument 'user_labels' to be a dict")
        pulumi.set(__self__, "user_labels", user_labels)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> str:
        """
        Name used for UI elements listing this (Monitoring) Service.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="meshUid")
    def mesh_uid(self) -> str:
        return pulumi.get(self, "mesh_uid")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The full REST resource name for this channel. The syntax is:
        `projects/[PROJECT_ID]/services/[SERVICE_ID]`.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def project(self) -> Optional[str]:
        return pulumi.get(self, "project")

    @property
    @pulumi.getter(name="serviceId")
    def service_id(self) -> str:
        return pulumi.get(self, "service_id")

    @property
    @pulumi.getter(name="serviceName")
    def service_name(self) -> str:
        return pulumi.get(self, "service_name")

    @property
    @pulumi.getter(name="serviceNamespace")
    def service_namespace(self) -> str:
        return pulumi.get(self, "service_namespace")

    @property
    @pulumi.getter
    def telemetries(self) -> Sequence['outputs.GetMeshIstioServiceTelemetryResult']:
        """
        Configuration for how to query telemetry on the Service. Structure is documented below.
        """
        return pulumi.get(self, "telemetries")

    @property
    @pulumi.getter(name="userLabels")
    def user_labels(self) -> Mapping[str, str]:
        return pulumi.get(self, "user_labels")


class AwaitableGetMeshIstioServiceResult(GetMeshIstioServiceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetMeshIstioServiceResult(
            display_name=self.display_name,
            id=self.id,
            mesh_uid=self.mesh_uid,
            name=self.name,
            project=self.project,
            service_id=self.service_id,
            service_name=self.service_name,
            service_namespace=self.service_namespace,
            telemetries=self.telemetries,
            user_labels=self.user_labels)


def get_mesh_istio_service(mesh_uid: Optional[str] = None,
                           project: Optional[str] = None,
                           service_name: Optional[str] = None,
                           service_namespace: Optional[str] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetMeshIstioServiceResult:
    """
    A Monitoring Service is the root resource under which operational aspects of a
    generic service are accessible. A service is some discrete, autonomous, and
    network-accessible unit, designed to solve an individual concern

    An Mesh Istio monitoring service is automatically created by GCP to monitor
    Mesh Istio services.

    To get more information about Service, see:

    * [API documentation](https://cloud.google.com/monitoring/api/ref_v3/rest/v3/services)
    * How-to Guides
        * [Service Monitoring](https://cloud.google.com/monitoring/service-monitoring)
        * [Monitoring API Documentation](https://cloud.google.com/monitoring/api/v3/)

    ## Example Usage

    ### Monitoring Mesh Istio Service

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_gcp as gcp

    # Monitors the default MeshIstio service
    default = gcp.monitoring.get_mesh_istio_service(mesh_uid="proj-573164786102",
        service_namespace="istio-system",
        service_name="prometheus")
    ```
    <!--End PulumiCodeChooser -->


    :param str mesh_uid: Identifier for the mesh in which this Istio service is defined.
           Corresponds to the meshUid metric label in Istio metrics.
    :param str project: The ID of the project in which the resource belongs.
           If it is not provided, the provider project is used.
    :param str service_name: The name of the Istio service underlying this service.
           Corresponds to the destination_service_name metric label in Istio metrics.
           
           - - -
           
           Other optional fields include:
    :param str service_namespace: The namespace of the Istio service underlying this service.
           Corresponds to the destination_service_namespace metric label in Istio metrics.
    """
    __args__ = dict()
    __args__['meshUid'] = mesh_uid
    __args__['project'] = project
    __args__['serviceName'] = service_name
    __args__['serviceNamespace'] = service_namespace
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('gcp:monitoring/getMeshIstioService:getMeshIstioService', __args__, opts=opts, typ=GetMeshIstioServiceResult).value

    return AwaitableGetMeshIstioServiceResult(
        display_name=pulumi.get(__ret__, 'display_name'),
        id=pulumi.get(__ret__, 'id'),
        mesh_uid=pulumi.get(__ret__, 'mesh_uid'),
        name=pulumi.get(__ret__, 'name'),
        project=pulumi.get(__ret__, 'project'),
        service_id=pulumi.get(__ret__, 'service_id'),
        service_name=pulumi.get(__ret__, 'service_name'),
        service_namespace=pulumi.get(__ret__, 'service_namespace'),
        telemetries=pulumi.get(__ret__, 'telemetries'),
        user_labels=pulumi.get(__ret__, 'user_labels'))


@_utilities.lift_output_func(get_mesh_istio_service)
def get_mesh_istio_service_output(mesh_uid: Optional[pulumi.Input[str]] = None,
                                  project: Optional[pulumi.Input[Optional[str]]] = None,
                                  service_name: Optional[pulumi.Input[str]] = None,
                                  service_namespace: Optional[pulumi.Input[str]] = None,
                                  opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetMeshIstioServiceResult]:
    """
    A Monitoring Service is the root resource under which operational aspects of a
    generic service are accessible. A service is some discrete, autonomous, and
    network-accessible unit, designed to solve an individual concern

    An Mesh Istio monitoring service is automatically created by GCP to monitor
    Mesh Istio services.

    To get more information about Service, see:

    * [API documentation](https://cloud.google.com/monitoring/api/ref_v3/rest/v3/services)
    * How-to Guides
        * [Service Monitoring](https://cloud.google.com/monitoring/service-monitoring)
        * [Monitoring API Documentation](https://cloud.google.com/monitoring/api/v3/)

    ## Example Usage

    ### Monitoring Mesh Istio Service

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_gcp as gcp

    # Monitors the default MeshIstio service
    default = gcp.monitoring.get_mesh_istio_service(mesh_uid="proj-573164786102",
        service_namespace="istio-system",
        service_name="prometheus")
    ```
    <!--End PulumiCodeChooser -->


    :param str mesh_uid: Identifier for the mesh in which this Istio service is defined.
           Corresponds to the meshUid metric label in Istio metrics.
    :param str project: The ID of the project in which the resource belongs.
           If it is not provided, the provider project is used.
    :param str service_name: The name of the Istio service underlying this service.
           Corresponds to the destination_service_name metric label in Istio metrics.
           
           - - -
           
           Other optional fields include:
    :param str service_namespace: The namespace of the Istio service underlying this service.
           Corresponds to the destination_service_namespace metric label in Istio metrics.
    """
    ...

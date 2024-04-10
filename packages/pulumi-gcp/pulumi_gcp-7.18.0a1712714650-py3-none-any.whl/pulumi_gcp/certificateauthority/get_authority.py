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
    'GetAuthorityResult',
    'AwaitableGetAuthorityResult',
    'get_authority',
    'get_authority_output',
]

@pulumi.output_type
class GetAuthorityResult:
    """
    A collection of values returned by getAuthority.
    """
    def __init__(__self__, access_urls=None, certificate_authority_id=None, configs=None, create_time=None, deletion_protection=None, desired_state=None, effective_labels=None, gcs_bucket=None, id=None, ignore_active_certificates_on_deletion=None, key_specs=None, labels=None, lifetime=None, location=None, name=None, pem_ca_certificate=None, pem_ca_certificates=None, pem_csr=None, pool=None, project=None, pulumi_labels=None, skip_grace_period=None, state=None, subordinate_configs=None, type=None, update_time=None):
        if access_urls and not isinstance(access_urls, list):
            raise TypeError("Expected argument 'access_urls' to be a list")
        pulumi.set(__self__, "access_urls", access_urls)
        if certificate_authority_id and not isinstance(certificate_authority_id, str):
            raise TypeError("Expected argument 'certificate_authority_id' to be a str")
        pulumi.set(__self__, "certificate_authority_id", certificate_authority_id)
        if configs and not isinstance(configs, list):
            raise TypeError("Expected argument 'configs' to be a list")
        pulumi.set(__self__, "configs", configs)
        if create_time and not isinstance(create_time, str):
            raise TypeError("Expected argument 'create_time' to be a str")
        pulumi.set(__self__, "create_time", create_time)
        if deletion_protection and not isinstance(deletion_protection, bool):
            raise TypeError("Expected argument 'deletion_protection' to be a bool")
        pulumi.set(__self__, "deletion_protection", deletion_protection)
        if desired_state and not isinstance(desired_state, str):
            raise TypeError("Expected argument 'desired_state' to be a str")
        pulumi.set(__self__, "desired_state", desired_state)
        if effective_labels and not isinstance(effective_labels, dict):
            raise TypeError("Expected argument 'effective_labels' to be a dict")
        pulumi.set(__self__, "effective_labels", effective_labels)
        if gcs_bucket and not isinstance(gcs_bucket, str):
            raise TypeError("Expected argument 'gcs_bucket' to be a str")
        pulumi.set(__self__, "gcs_bucket", gcs_bucket)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ignore_active_certificates_on_deletion and not isinstance(ignore_active_certificates_on_deletion, bool):
            raise TypeError("Expected argument 'ignore_active_certificates_on_deletion' to be a bool")
        pulumi.set(__self__, "ignore_active_certificates_on_deletion", ignore_active_certificates_on_deletion)
        if key_specs and not isinstance(key_specs, list):
            raise TypeError("Expected argument 'key_specs' to be a list")
        pulumi.set(__self__, "key_specs", key_specs)
        if labels and not isinstance(labels, dict):
            raise TypeError("Expected argument 'labels' to be a dict")
        pulumi.set(__self__, "labels", labels)
        if lifetime and not isinstance(lifetime, str):
            raise TypeError("Expected argument 'lifetime' to be a str")
        pulumi.set(__self__, "lifetime", lifetime)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if pem_ca_certificate and not isinstance(pem_ca_certificate, str):
            raise TypeError("Expected argument 'pem_ca_certificate' to be a str")
        pulumi.set(__self__, "pem_ca_certificate", pem_ca_certificate)
        if pem_ca_certificates and not isinstance(pem_ca_certificates, list):
            raise TypeError("Expected argument 'pem_ca_certificates' to be a list")
        pulumi.set(__self__, "pem_ca_certificates", pem_ca_certificates)
        if pem_csr and not isinstance(pem_csr, str):
            raise TypeError("Expected argument 'pem_csr' to be a str")
        pulumi.set(__self__, "pem_csr", pem_csr)
        if pool and not isinstance(pool, str):
            raise TypeError("Expected argument 'pool' to be a str")
        pulumi.set(__self__, "pool", pool)
        if project and not isinstance(project, str):
            raise TypeError("Expected argument 'project' to be a str")
        pulumi.set(__self__, "project", project)
        if pulumi_labels and not isinstance(pulumi_labels, dict):
            raise TypeError("Expected argument 'pulumi_labels' to be a dict")
        pulumi.set(__self__, "pulumi_labels", pulumi_labels)
        if skip_grace_period and not isinstance(skip_grace_period, bool):
            raise TypeError("Expected argument 'skip_grace_period' to be a bool")
        pulumi.set(__self__, "skip_grace_period", skip_grace_period)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)
        if subordinate_configs and not isinstance(subordinate_configs, list):
            raise TypeError("Expected argument 'subordinate_configs' to be a list")
        pulumi.set(__self__, "subordinate_configs", subordinate_configs)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if update_time and not isinstance(update_time, str):
            raise TypeError("Expected argument 'update_time' to be a str")
        pulumi.set(__self__, "update_time", update_time)

    @property
    @pulumi.getter(name="accessUrls")
    def access_urls(self) -> Sequence['outputs.GetAuthorityAccessUrlResult']:
        return pulumi.get(self, "access_urls")

    @property
    @pulumi.getter(name="certificateAuthorityId")
    def certificate_authority_id(self) -> Optional[str]:
        return pulumi.get(self, "certificate_authority_id")

    @property
    @pulumi.getter
    def configs(self) -> Sequence['outputs.GetAuthorityConfigResult']:
        return pulumi.get(self, "configs")

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> str:
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter(name="deletionProtection")
    def deletion_protection(self) -> bool:
        return pulumi.get(self, "deletion_protection")

    @property
    @pulumi.getter(name="desiredState")
    def desired_state(self) -> str:
        return pulumi.get(self, "desired_state")

    @property
    @pulumi.getter(name="effectiveLabels")
    def effective_labels(self) -> Mapping[str, str]:
        return pulumi.get(self, "effective_labels")

    @property
    @pulumi.getter(name="gcsBucket")
    def gcs_bucket(self) -> str:
        return pulumi.get(self, "gcs_bucket")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="ignoreActiveCertificatesOnDeletion")
    def ignore_active_certificates_on_deletion(self) -> bool:
        return pulumi.get(self, "ignore_active_certificates_on_deletion")

    @property
    @pulumi.getter(name="keySpecs")
    def key_specs(self) -> Sequence['outputs.GetAuthorityKeySpecResult']:
        return pulumi.get(self, "key_specs")

    @property
    @pulumi.getter
    def labels(self) -> Mapping[str, str]:
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter
    def lifetime(self) -> str:
        return pulumi.get(self, "lifetime")

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="pemCaCertificate")
    def pem_ca_certificate(self) -> str:
        return pulumi.get(self, "pem_ca_certificate")

    @property
    @pulumi.getter(name="pemCaCertificates")
    def pem_ca_certificates(self) -> Sequence[str]:
        return pulumi.get(self, "pem_ca_certificates")

    @property
    @pulumi.getter(name="pemCsr")
    def pem_csr(self) -> str:
        """
        The PEM-encoded signed certificate signing request (CSR). This is only set on subordinate certificate authorities that are awaiting user activation.
        """
        return pulumi.get(self, "pem_csr")

    @property
    @pulumi.getter
    def pool(self) -> Optional[str]:
        return pulumi.get(self, "pool")

    @property
    @pulumi.getter
    def project(self) -> Optional[str]:
        return pulumi.get(self, "project")

    @property
    @pulumi.getter(name="pulumiLabels")
    def pulumi_labels(self) -> Mapping[str, str]:
        return pulumi.get(self, "pulumi_labels")

    @property
    @pulumi.getter(name="skipGracePeriod")
    def skip_grace_period(self) -> bool:
        return pulumi.get(self, "skip_grace_period")

    @property
    @pulumi.getter
    def state(self) -> str:
        return pulumi.get(self, "state")

    @property
    @pulumi.getter(name="subordinateConfigs")
    def subordinate_configs(self) -> Sequence['outputs.GetAuthoritySubordinateConfigResult']:
        return pulumi.get(self, "subordinate_configs")

    @property
    @pulumi.getter
    def type(self) -> str:
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> str:
        return pulumi.get(self, "update_time")


class AwaitableGetAuthorityResult(GetAuthorityResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAuthorityResult(
            access_urls=self.access_urls,
            certificate_authority_id=self.certificate_authority_id,
            configs=self.configs,
            create_time=self.create_time,
            deletion_protection=self.deletion_protection,
            desired_state=self.desired_state,
            effective_labels=self.effective_labels,
            gcs_bucket=self.gcs_bucket,
            id=self.id,
            ignore_active_certificates_on_deletion=self.ignore_active_certificates_on_deletion,
            key_specs=self.key_specs,
            labels=self.labels,
            lifetime=self.lifetime,
            location=self.location,
            name=self.name,
            pem_ca_certificate=self.pem_ca_certificate,
            pem_ca_certificates=self.pem_ca_certificates,
            pem_csr=self.pem_csr,
            pool=self.pool,
            project=self.project,
            pulumi_labels=self.pulumi_labels,
            skip_grace_period=self.skip_grace_period,
            state=self.state,
            subordinate_configs=self.subordinate_configs,
            type=self.type,
            update_time=self.update_time)


def get_authority(certificate_authority_id: Optional[str] = None,
                  location: Optional[str] = None,
                  pool: Optional[str] = None,
                  project: Optional[str] = None,
                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAuthorityResult:
    """
    Get info about a Google CAS Certificate Authority.

    ## Example Usage


    :param str certificate_authority_id: ID of the certificate authority.
           
           - - -
    :param str location: The location the certificate authority exists in.
    :param str pool: The name of the pool the certificate authority belongs to.
    :param str project: The ID of the project in which the resource belongs. If it
           is not provided, the provider project is used.
    """
    __args__ = dict()
    __args__['certificateAuthorityId'] = certificate_authority_id
    __args__['location'] = location
    __args__['pool'] = pool
    __args__['project'] = project
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('gcp:certificateauthority/getAuthority:getAuthority', __args__, opts=opts, typ=GetAuthorityResult).value

    return AwaitableGetAuthorityResult(
        access_urls=pulumi.get(__ret__, 'access_urls'),
        certificate_authority_id=pulumi.get(__ret__, 'certificate_authority_id'),
        configs=pulumi.get(__ret__, 'configs'),
        create_time=pulumi.get(__ret__, 'create_time'),
        deletion_protection=pulumi.get(__ret__, 'deletion_protection'),
        desired_state=pulumi.get(__ret__, 'desired_state'),
        effective_labels=pulumi.get(__ret__, 'effective_labels'),
        gcs_bucket=pulumi.get(__ret__, 'gcs_bucket'),
        id=pulumi.get(__ret__, 'id'),
        ignore_active_certificates_on_deletion=pulumi.get(__ret__, 'ignore_active_certificates_on_deletion'),
        key_specs=pulumi.get(__ret__, 'key_specs'),
        labels=pulumi.get(__ret__, 'labels'),
        lifetime=pulumi.get(__ret__, 'lifetime'),
        location=pulumi.get(__ret__, 'location'),
        name=pulumi.get(__ret__, 'name'),
        pem_ca_certificate=pulumi.get(__ret__, 'pem_ca_certificate'),
        pem_ca_certificates=pulumi.get(__ret__, 'pem_ca_certificates'),
        pem_csr=pulumi.get(__ret__, 'pem_csr'),
        pool=pulumi.get(__ret__, 'pool'),
        project=pulumi.get(__ret__, 'project'),
        pulumi_labels=pulumi.get(__ret__, 'pulumi_labels'),
        skip_grace_period=pulumi.get(__ret__, 'skip_grace_period'),
        state=pulumi.get(__ret__, 'state'),
        subordinate_configs=pulumi.get(__ret__, 'subordinate_configs'),
        type=pulumi.get(__ret__, 'type'),
        update_time=pulumi.get(__ret__, 'update_time'))


@_utilities.lift_output_func(get_authority)
def get_authority_output(certificate_authority_id: Optional[pulumi.Input[Optional[str]]] = None,
                         location: Optional[pulumi.Input[Optional[str]]] = None,
                         pool: Optional[pulumi.Input[Optional[str]]] = None,
                         project: Optional[pulumi.Input[Optional[str]]] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAuthorityResult]:
    """
    Get info about a Google CAS Certificate Authority.

    ## Example Usage


    :param str certificate_authority_id: ID of the certificate authority.
           
           - - -
    :param str location: The location the certificate authority exists in.
    :param str pool: The name of the pool the certificate authority belongs to.
    :param str project: The ID of the project in which the resource belongs. If it
           is not provided, the provider project is used.
    """
    ...

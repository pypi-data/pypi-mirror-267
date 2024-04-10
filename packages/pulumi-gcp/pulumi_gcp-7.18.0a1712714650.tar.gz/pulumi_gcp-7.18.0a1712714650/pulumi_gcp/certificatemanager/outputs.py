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
    'CertificateIssuanceConfigCertificateAuthorityConfig',
    'CertificateIssuanceConfigCertificateAuthorityConfigCertificateAuthorityServiceConfig',
    'CertificateManaged',
    'CertificateManagedAuthorizationAttemptInfo',
    'CertificateManagedProvisioningIssue',
    'CertificateMapGclbTarget',
    'CertificateMapGclbTargetIpConfig',
    'CertificateSelfManaged',
    'DnsAuthorizationDnsResourceRecord',
    'TrustConfigTrustStore',
    'TrustConfigTrustStoreIntermediateCa',
    'TrustConfigTrustStoreTrustAnchor',
    'GetCertificateMapGclbTargetResult',
    'GetCertificateMapGclbTargetIpConfigResult',
]

@pulumi.output_type
class CertificateIssuanceConfigCertificateAuthorityConfig(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "certificateAuthorityServiceConfig":
            suggest = "certificate_authority_service_config"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CertificateIssuanceConfigCertificateAuthorityConfig. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CertificateIssuanceConfigCertificateAuthorityConfig.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        CertificateIssuanceConfigCertificateAuthorityConfig.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 certificate_authority_service_config: Optional['outputs.CertificateIssuanceConfigCertificateAuthorityConfigCertificateAuthorityServiceConfig'] = None):
        """
        :param 'CertificateIssuanceConfigCertificateAuthorityConfigCertificateAuthorityServiceConfigArgs' certificate_authority_service_config: Defines a CertificateAuthorityServiceConfig.
               Structure is documented below.
        """
        if certificate_authority_service_config is not None:
            pulumi.set(__self__, "certificate_authority_service_config", certificate_authority_service_config)

    @property
    @pulumi.getter(name="certificateAuthorityServiceConfig")
    def certificate_authority_service_config(self) -> Optional['outputs.CertificateIssuanceConfigCertificateAuthorityConfigCertificateAuthorityServiceConfig']:
        """
        Defines a CertificateAuthorityServiceConfig.
        Structure is documented below.
        """
        return pulumi.get(self, "certificate_authority_service_config")


@pulumi.output_type
class CertificateIssuanceConfigCertificateAuthorityConfigCertificateAuthorityServiceConfig(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "caPool":
            suggest = "ca_pool"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CertificateIssuanceConfigCertificateAuthorityConfigCertificateAuthorityServiceConfig. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CertificateIssuanceConfigCertificateAuthorityConfigCertificateAuthorityServiceConfig.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        CertificateIssuanceConfigCertificateAuthorityConfigCertificateAuthorityServiceConfig.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 ca_pool: str):
        """
        :param str ca_pool: A CA pool resource used to issue a certificate.
               The CA pool string has a relative resource path following the form
               "projects/{project}/locations/{location}/caPools/{caPool}".
               
               - - -
        """
        pulumi.set(__self__, "ca_pool", ca_pool)

    @property
    @pulumi.getter(name="caPool")
    def ca_pool(self) -> str:
        """
        A CA pool resource used to issue a certificate.
        The CA pool string has a relative resource path following the form
        "projects/{project}/locations/{location}/caPools/{caPool}".

        - - -
        """
        return pulumi.get(self, "ca_pool")


@pulumi.output_type
class CertificateManaged(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "authorizationAttemptInfos":
            suggest = "authorization_attempt_infos"
        elif key == "dnsAuthorizations":
            suggest = "dns_authorizations"
        elif key == "issuanceConfig":
            suggest = "issuance_config"
        elif key == "provisioningIssues":
            suggest = "provisioning_issues"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CertificateManaged. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CertificateManaged.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        CertificateManaged.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 authorization_attempt_infos: Optional[Sequence['outputs.CertificateManagedAuthorizationAttemptInfo']] = None,
                 dns_authorizations: Optional[Sequence[str]] = None,
                 domains: Optional[Sequence[str]] = None,
                 issuance_config: Optional[str] = None,
                 provisioning_issues: Optional[Sequence['outputs.CertificateManagedProvisioningIssue']] = None,
                 state: Optional[str] = None):
        """
        :param Sequence['CertificateManagedAuthorizationAttemptInfoArgs'] authorization_attempt_infos: (Output)
               Detailed state of the latest authorization attempt for each domain
               specified for this Managed Certificate.
               Structure is documented below.
               
               
               <a name="nested_provisioning_issue"></a>The `provisioning_issue` block contains:
        :param Sequence[str] dns_authorizations: Authorizations that will be used for performing domain authorization. Either issuanceConfig or dnsAuthorizations should be specificed, but not both.
        :param Sequence[str] domains: The domains for which a managed SSL certificate will be generated.
               Wildcard domains are only supported with DNS challenge resolution
        :param str issuance_config: The resource name for a CertificateIssuanceConfig used to configure private PKI certificates in the format projects/*/locations/*/certificateIssuanceConfigs/*.
               If this field is not set, the certificates will instead be publicly signed as documented at https://cloud.google.com/load-balancing/docs/ssl-certificates/google-managed-certs#caa.
               Either issuanceConfig or dnsAuthorizations should be specificed, but not both.
        :param Sequence['CertificateManagedProvisioningIssueArgs'] provisioning_issues: (Output)
               Information about issues with provisioning this Managed Certificate.
               Structure is documented below.
        :param str state: (Output)
               State of the domain for managed certificate issuance.
        """
        if authorization_attempt_infos is not None:
            pulumi.set(__self__, "authorization_attempt_infos", authorization_attempt_infos)
        if dns_authorizations is not None:
            pulumi.set(__self__, "dns_authorizations", dns_authorizations)
        if domains is not None:
            pulumi.set(__self__, "domains", domains)
        if issuance_config is not None:
            pulumi.set(__self__, "issuance_config", issuance_config)
        if provisioning_issues is not None:
            pulumi.set(__self__, "provisioning_issues", provisioning_issues)
        if state is not None:
            pulumi.set(__self__, "state", state)

    @property
    @pulumi.getter(name="authorizationAttemptInfos")
    def authorization_attempt_infos(self) -> Optional[Sequence['outputs.CertificateManagedAuthorizationAttemptInfo']]:
        """
        (Output)
        Detailed state of the latest authorization attempt for each domain
        specified for this Managed Certificate.
        Structure is documented below.


        <a name="nested_provisioning_issue"></a>The `provisioning_issue` block contains:
        """
        return pulumi.get(self, "authorization_attempt_infos")

    @property
    @pulumi.getter(name="dnsAuthorizations")
    def dns_authorizations(self) -> Optional[Sequence[str]]:
        """
        Authorizations that will be used for performing domain authorization. Either issuanceConfig or dnsAuthorizations should be specificed, but not both.
        """
        return pulumi.get(self, "dns_authorizations")

    @property
    @pulumi.getter
    def domains(self) -> Optional[Sequence[str]]:
        """
        The domains for which a managed SSL certificate will be generated.
        Wildcard domains are only supported with DNS challenge resolution
        """
        return pulumi.get(self, "domains")

    @property
    @pulumi.getter(name="issuanceConfig")
    def issuance_config(self) -> Optional[str]:
        """
        The resource name for a CertificateIssuanceConfig used to configure private PKI certificates in the format projects/*/locations/*/certificateIssuanceConfigs/*.
        If this field is not set, the certificates will instead be publicly signed as documented at https://cloud.google.com/load-balancing/docs/ssl-certificates/google-managed-certs#caa.
        Either issuanceConfig or dnsAuthorizations should be specificed, but not both.
        """
        return pulumi.get(self, "issuance_config")

    @property
    @pulumi.getter(name="provisioningIssues")
    def provisioning_issues(self) -> Optional[Sequence['outputs.CertificateManagedProvisioningIssue']]:
        """
        (Output)
        Information about issues with provisioning this Managed Certificate.
        Structure is documented below.
        """
        return pulumi.get(self, "provisioning_issues")

    @property
    @pulumi.getter
    def state(self) -> Optional[str]:
        """
        (Output)
        State of the domain for managed certificate issuance.
        """
        return pulumi.get(self, "state")


@pulumi.output_type
class CertificateManagedAuthorizationAttemptInfo(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "failureReason":
            suggest = "failure_reason"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CertificateManagedAuthorizationAttemptInfo. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CertificateManagedAuthorizationAttemptInfo.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        CertificateManagedAuthorizationAttemptInfo.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 details: Optional[str] = None,
                 domain: Optional[str] = None,
                 failure_reason: Optional[str] = None,
                 state: Optional[str] = None):
        """
        :param str details: (Output)
               Human readable explanation for reaching the state. Provided to help
               address the configuration issues.
               Not guaranteed to be stable. For programmatic access use `failure_reason` field.
        :param str domain: (Output)
               Domain name of the authorization attempt.
        :param str failure_reason: (Output)
               Reason for failure of the authorization attempt for the domain.
        :param str state: (Output)
               State of the domain for managed certificate issuance.
        """
        if details is not None:
            pulumi.set(__self__, "details", details)
        if domain is not None:
            pulumi.set(__self__, "domain", domain)
        if failure_reason is not None:
            pulumi.set(__self__, "failure_reason", failure_reason)
        if state is not None:
            pulumi.set(__self__, "state", state)

    @property
    @pulumi.getter
    def details(self) -> Optional[str]:
        """
        (Output)
        Human readable explanation for reaching the state. Provided to help
        address the configuration issues.
        Not guaranteed to be stable. For programmatic access use `failure_reason` field.
        """
        return pulumi.get(self, "details")

    @property
    @pulumi.getter
    def domain(self) -> Optional[str]:
        """
        (Output)
        Domain name of the authorization attempt.
        """
        return pulumi.get(self, "domain")

    @property
    @pulumi.getter(name="failureReason")
    def failure_reason(self) -> Optional[str]:
        """
        (Output)
        Reason for failure of the authorization attempt for the domain.
        """
        return pulumi.get(self, "failure_reason")

    @property
    @pulumi.getter
    def state(self) -> Optional[str]:
        """
        (Output)
        State of the domain for managed certificate issuance.
        """
        return pulumi.get(self, "state")


@pulumi.output_type
class CertificateManagedProvisioningIssue(dict):
    def __init__(__self__, *,
                 details: Optional[str] = None,
                 reason: Optional[str] = None):
        """
        :param str details: (Output)
               Human readable explanation for reaching the state. Provided to help
               address the configuration issues.
               Not guaranteed to be stable. For programmatic access use `failure_reason` field.
        :param str reason: (Output)
               Reason for provisioning failures.
        """
        if details is not None:
            pulumi.set(__self__, "details", details)
        if reason is not None:
            pulumi.set(__self__, "reason", reason)

    @property
    @pulumi.getter
    def details(self) -> Optional[str]:
        """
        (Output)
        Human readable explanation for reaching the state. Provided to help
        address the configuration issues.
        Not guaranteed to be stable. For programmatic access use `failure_reason` field.
        """
        return pulumi.get(self, "details")

    @property
    @pulumi.getter
    def reason(self) -> Optional[str]:
        """
        (Output)
        Reason for provisioning failures.
        """
        return pulumi.get(self, "reason")


@pulumi.output_type
class CertificateMapGclbTarget(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "ipConfigs":
            suggest = "ip_configs"
        elif key == "targetHttpsProxy":
            suggest = "target_https_proxy"
        elif key == "targetSslProxy":
            suggest = "target_ssl_proxy"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CertificateMapGclbTarget. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CertificateMapGclbTarget.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        CertificateMapGclbTarget.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 ip_configs: Optional[Sequence['outputs.CertificateMapGclbTargetIpConfig']] = None,
                 target_https_proxy: Optional[str] = None,
                 target_ssl_proxy: Optional[str] = None):
        """
        :param Sequence['CertificateMapGclbTargetIpConfigArgs'] ip_configs: An IP configuration where this Certificate Map is serving
               Structure is documented below.
        :param str target_https_proxy: Proxy name must be in the format projects/*/locations/*/targetHttpsProxies/*.
               This field is part of a union field `target_proxy`: Only one of `targetHttpsProxy` or
               `targetSslProxy` may be set.
        :param str target_ssl_proxy: Proxy name must be in the format projects/*/locations/*/targetSslProxies/*.
               This field is part of a union field `target_proxy`: Only one of `targetHttpsProxy` or
               `targetSslProxy` may be set.
        """
        if ip_configs is not None:
            pulumi.set(__self__, "ip_configs", ip_configs)
        if target_https_proxy is not None:
            pulumi.set(__self__, "target_https_proxy", target_https_proxy)
        if target_ssl_proxy is not None:
            pulumi.set(__self__, "target_ssl_proxy", target_ssl_proxy)

    @property
    @pulumi.getter(name="ipConfigs")
    def ip_configs(self) -> Optional[Sequence['outputs.CertificateMapGclbTargetIpConfig']]:
        """
        An IP configuration where this Certificate Map is serving
        Structure is documented below.
        """
        return pulumi.get(self, "ip_configs")

    @property
    @pulumi.getter(name="targetHttpsProxy")
    def target_https_proxy(self) -> Optional[str]:
        """
        Proxy name must be in the format projects/*/locations/*/targetHttpsProxies/*.
        This field is part of a union field `target_proxy`: Only one of `targetHttpsProxy` or
        `targetSslProxy` may be set.
        """
        return pulumi.get(self, "target_https_proxy")

    @property
    @pulumi.getter(name="targetSslProxy")
    def target_ssl_proxy(self) -> Optional[str]:
        """
        Proxy name must be in the format projects/*/locations/*/targetSslProxies/*.
        This field is part of a union field `target_proxy`: Only one of `targetHttpsProxy` or
        `targetSslProxy` may be set.
        """
        return pulumi.get(self, "target_ssl_proxy")


@pulumi.output_type
class CertificateMapGclbTargetIpConfig(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "ipAddress":
            suggest = "ip_address"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CertificateMapGclbTargetIpConfig. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CertificateMapGclbTargetIpConfig.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        CertificateMapGclbTargetIpConfig.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 ip_address: Optional[str] = None,
                 ports: Optional[Sequence[int]] = None):
        """
        :param str ip_address: An external IP address
        :param Sequence[int] ports: A list of ports
        """
        if ip_address is not None:
            pulumi.set(__self__, "ip_address", ip_address)
        if ports is not None:
            pulumi.set(__self__, "ports", ports)

    @property
    @pulumi.getter(name="ipAddress")
    def ip_address(self) -> Optional[str]:
        """
        An external IP address
        """
        return pulumi.get(self, "ip_address")

    @property
    @pulumi.getter
    def ports(self) -> Optional[Sequence[int]]:
        """
        A list of ports
        """
        return pulumi.get(self, "ports")


@pulumi.output_type
class CertificateSelfManaged(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "certificatePem":
            suggest = "certificate_pem"
        elif key == "pemCertificate":
            suggest = "pem_certificate"
        elif key == "pemPrivateKey":
            suggest = "pem_private_key"
        elif key == "privateKeyPem":
            suggest = "private_key_pem"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CertificateSelfManaged. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CertificateSelfManaged.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        CertificateSelfManaged.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 certificate_pem: Optional[str] = None,
                 pem_certificate: Optional[str] = None,
                 pem_private_key: Optional[str] = None,
                 private_key_pem: Optional[str] = None):
        """
        :param str certificate_pem: (Optional, Deprecated)
               The certificate chain in PEM-encoded form.
               Leaf certificate comes first, followed by intermediate ones if any.
               **Note**: This property is sensitive and will not be displayed in the plan.
               
               > **Warning:** `certificate_pem` is deprecated and will be removed in a future major release. Use `pem_certificate` instead.
        :param str pem_certificate: The certificate chain in PEM-encoded form.
               Leaf certificate comes first, followed by intermediate ones if any.
               **Note**: This property is sensitive and will not be displayed in the plan.
        :param str pem_private_key: The private key of the leaf certificate in PEM-encoded form.
               **Note**: This property is sensitive and will not be displayed in the plan.
        :param str private_key_pem: (Optional, Deprecated)
               The private key of the leaf certificate in PEM-encoded form.
               **Note**: This property is sensitive and will not be displayed in the plan.
               
               > **Warning:** `private_key_pem` is deprecated and will be removed in a future major release. Use `pem_private_key` instead.
        """
        if certificate_pem is not None:
            pulumi.set(__self__, "certificate_pem", certificate_pem)
        if pem_certificate is not None:
            pulumi.set(__self__, "pem_certificate", pem_certificate)
        if pem_private_key is not None:
            pulumi.set(__self__, "pem_private_key", pem_private_key)
        if private_key_pem is not None:
            pulumi.set(__self__, "private_key_pem", private_key_pem)

    @property
    @pulumi.getter(name="certificatePem")
    def certificate_pem(self) -> Optional[str]:
        """
        (Optional, Deprecated)
        The certificate chain in PEM-encoded form.
        Leaf certificate comes first, followed by intermediate ones if any.
        **Note**: This property is sensitive and will not be displayed in the plan.

        > **Warning:** `certificate_pem` is deprecated and will be removed in a future major release. Use `pem_certificate` instead.
        """
        warnings.warn("""`certificate_pem` is deprecated and will be removed in a future major release. Use `pem_certificate` instead.""", DeprecationWarning)
        pulumi.log.warn("""certificate_pem is deprecated: `certificate_pem` is deprecated and will be removed in a future major release. Use `pem_certificate` instead.""")

        return pulumi.get(self, "certificate_pem")

    @property
    @pulumi.getter(name="pemCertificate")
    def pem_certificate(self) -> Optional[str]:
        """
        The certificate chain in PEM-encoded form.
        Leaf certificate comes first, followed by intermediate ones if any.
        **Note**: This property is sensitive and will not be displayed in the plan.
        """
        return pulumi.get(self, "pem_certificate")

    @property
    @pulumi.getter(name="pemPrivateKey")
    def pem_private_key(self) -> Optional[str]:
        """
        The private key of the leaf certificate in PEM-encoded form.
        **Note**: This property is sensitive and will not be displayed in the plan.
        """
        return pulumi.get(self, "pem_private_key")

    @property
    @pulumi.getter(name="privateKeyPem")
    def private_key_pem(self) -> Optional[str]:
        """
        (Optional, Deprecated)
        The private key of the leaf certificate in PEM-encoded form.
        **Note**: This property is sensitive and will not be displayed in the plan.

        > **Warning:** `private_key_pem` is deprecated and will be removed in a future major release. Use `pem_private_key` instead.
        """
        warnings.warn("""`private_key_pem` is deprecated and will be removed in a future major release. Use `pem_private_key` instead.""", DeprecationWarning)
        pulumi.log.warn("""private_key_pem is deprecated: `private_key_pem` is deprecated and will be removed in a future major release. Use `pem_private_key` instead.""")

        return pulumi.get(self, "private_key_pem")


@pulumi.output_type
class DnsAuthorizationDnsResourceRecord(dict):
    def __init__(__self__, *,
                 data: Optional[str] = None,
                 name: Optional[str] = None,
                 type: Optional[str] = None):
        """
        :param str data: (Output)
               Data of the DNS Resource Record.
        :param str name: Name of the resource; provided by the client when the resource is created.
               The name must be 1-64 characters long, and match the regular expression [a-zA-Z][a-zA-Z0-9_-]* which means the first character must be a letter,
               and all following characters must be a dash, underscore, letter or digit.
               
               
               - - -
        :param str type: type of DNS authorization. If unset during the resource creation, FIXED_RECORD will
               be used for global resources, and PER_PROJECT_RECORD will be used for other locations.
               FIXED_RECORD DNS authorization uses DNS-01 validation method
               PER_PROJECT_RECORD DNS authorization allows for independent management
               of Google-managed certificates with DNS authorization across multiple
               projects.
               Possible values are: `FIXED_RECORD`, `PER_PROJECT_RECORD`.
        """
        if data is not None:
            pulumi.set(__self__, "data", data)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def data(self) -> Optional[str]:
        """
        (Output)
        Data of the DNS Resource Record.
        """
        return pulumi.get(self, "data")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        Name of the resource; provided by the client when the resource is created.
        The name must be 1-64 characters long, and match the regular expression [a-zA-Z][a-zA-Z0-9_-]* which means the first character must be a letter,
        and all following characters must be a dash, underscore, letter or digit.


        - - -
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        """
        type of DNS authorization. If unset during the resource creation, FIXED_RECORD will
        be used for global resources, and PER_PROJECT_RECORD will be used for other locations.
        FIXED_RECORD DNS authorization uses DNS-01 validation method
        PER_PROJECT_RECORD DNS authorization allows for independent management
        of Google-managed certificates with DNS authorization across multiple
        projects.
        Possible values are: `FIXED_RECORD`, `PER_PROJECT_RECORD`.
        """
        return pulumi.get(self, "type")


@pulumi.output_type
class TrustConfigTrustStore(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "intermediateCas":
            suggest = "intermediate_cas"
        elif key == "trustAnchors":
            suggest = "trust_anchors"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in TrustConfigTrustStore. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        TrustConfigTrustStore.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        TrustConfigTrustStore.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 intermediate_cas: Optional[Sequence['outputs.TrustConfigTrustStoreIntermediateCa']] = None,
                 trust_anchors: Optional[Sequence['outputs.TrustConfigTrustStoreTrustAnchor']] = None):
        """
        :param Sequence['TrustConfigTrustStoreIntermediateCaArgs'] intermediate_cas: Set of intermediate CA certificates used for the path building phase of chain validation.
               The field is currently not supported if trust config is used for the workload certificate feature.
               Structure is documented below.
        :param Sequence['TrustConfigTrustStoreTrustAnchorArgs'] trust_anchors: List of Trust Anchors to be used while performing validation against a given TrustStore.
               Structure is documented below.
        """
        if intermediate_cas is not None:
            pulumi.set(__self__, "intermediate_cas", intermediate_cas)
        if trust_anchors is not None:
            pulumi.set(__self__, "trust_anchors", trust_anchors)

    @property
    @pulumi.getter(name="intermediateCas")
    def intermediate_cas(self) -> Optional[Sequence['outputs.TrustConfigTrustStoreIntermediateCa']]:
        """
        Set of intermediate CA certificates used for the path building phase of chain validation.
        The field is currently not supported if trust config is used for the workload certificate feature.
        Structure is documented below.
        """
        return pulumi.get(self, "intermediate_cas")

    @property
    @pulumi.getter(name="trustAnchors")
    def trust_anchors(self) -> Optional[Sequence['outputs.TrustConfigTrustStoreTrustAnchor']]:
        """
        List of Trust Anchors to be used while performing validation against a given TrustStore.
        Structure is documented below.
        """
        return pulumi.get(self, "trust_anchors")


@pulumi.output_type
class TrustConfigTrustStoreIntermediateCa(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "pemCertificate":
            suggest = "pem_certificate"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in TrustConfigTrustStoreIntermediateCa. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        TrustConfigTrustStoreIntermediateCa.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        TrustConfigTrustStoreIntermediateCa.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 pem_certificate: Optional[str] = None):
        """
        :param str pem_certificate: PEM intermediate certificate used for building up paths for validation.
               Each certificate provided in PEM format may occupy up to 5kB.
               **Note**: This property is sensitive and will not be displayed in the plan.
        """
        if pem_certificate is not None:
            pulumi.set(__self__, "pem_certificate", pem_certificate)

    @property
    @pulumi.getter(name="pemCertificate")
    def pem_certificate(self) -> Optional[str]:
        """
        PEM intermediate certificate used for building up paths for validation.
        Each certificate provided in PEM format may occupy up to 5kB.
        **Note**: This property is sensitive and will not be displayed in the plan.
        """
        return pulumi.get(self, "pem_certificate")


@pulumi.output_type
class TrustConfigTrustStoreTrustAnchor(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "pemCertificate":
            suggest = "pem_certificate"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in TrustConfigTrustStoreTrustAnchor. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        TrustConfigTrustStoreTrustAnchor.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        TrustConfigTrustStoreTrustAnchor.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 pem_certificate: Optional[str] = None):
        """
        :param str pem_certificate: PEM root certificate of the PKI used for validation.
               Each certificate provided in PEM format may occupy up to 5kB.
               **Note**: This property is sensitive and will not be displayed in the plan.
        """
        if pem_certificate is not None:
            pulumi.set(__self__, "pem_certificate", pem_certificate)

    @property
    @pulumi.getter(name="pemCertificate")
    def pem_certificate(self) -> Optional[str]:
        """
        PEM root certificate of the PKI used for validation.
        Each certificate provided in PEM format may occupy up to 5kB.
        **Note**: This property is sensitive and will not be displayed in the plan.
        """
        return pulumi.get(self, "pem_certificate")


@pulumi.output_type
class GetCertificateMapGclbTargetResult(dict):
    def __init__(__self__, *,
                 ip_configs: Sequence['outputs.GetCertificateMapGclbTargetIpConfigResult'],
                 target_https_proxy: str,
                 target_ssl_proxy: str):
        """
        :param Sequence['GetCertificateMapGclbTargetIpConfigArgs'] ip_configs: An IP configuration where this Certificate Map is serving
        :param str target_https_proxy: Proxy name must be in the format projects/*/locations/*/targetHttpsProxies/*.
               This field is part of a union field 'target_proxy': Only one of 'targetHttpsProxy' or
               'targetSslProxy' may be set.
        :param str target_ssl_proxy: Proxy name must be in the format projects/*/locations/*/targetSslProxies/*.
               This field is part of a union field 'target_proxy': Only one of 'targetHttpsProxy' or
               'targetSslProxy' may be set.
        """
        pulumi.set(__self__, "ip_configs", ip_configs)
        pulumi.set(__self__, "target_https_proxy", target_https_proxy)
        pulumi.set(__self__, "target_ssl_proxy", target_ssl_proxy)

    @property
    @pulumi.getter(name="ipConfigs")
    def ip_configs(self) -> Sequence['outputs.GetCertificateMapGclbTargetIpConfigResult']:
        """
        An IP configuration where this Certificate Map is serving
        """
        return pulumi.get(self, "ip_configs")

    @property
    @pulumi.getter(name="targetHttpsProxy")
    def target_https_proxy(self) -> str:
        """
        Proxy name must be in the format projects/*/locations/*/targetHttpsProxies/*.
        This field is part of a union field 'target_proxy': Only one of 'targetHttpsProxy' or
        'targetSslProxy' may be set.
        """
        return pulumi.get(self, "target_https_proxy")

    @property
    @pulumi.getter(name="targetSslProxy")
    def target_ssl_proxy(self) -> str:
        """
        Proxy name must be in the format projects/*/locations/*/targetSslProxies/*.
        This field is part of a union field 'target_proxy': Only one of 'targetHttpsProxy' or
        'targetSslProxy' may be set.
        """
        return pulumi.get(self, "target_ssl_proxy")


@pulumi.output_type
class GetCertificateMapGclbTargetIpConfigResult(dict):
    def __init__(__self__, *,
                 ip_address: str,
                 ports: Sequence[int]):
        """
        :param str ip_address: An external IP address
        :param Sequence[int] ports: A list of ports
        """
        pulumi.set(__self__, "ip_address", ip_address)
        pulumi.set(__self__, "ports", ports)

    @property
    @pulumi.getter(name="ipAddress")
    def ip_address(self) -> str:
        """
        An external IP address
        """
        return pulumi.get(self, "ip_address")

    @property
    @pulumi.getter
    def ports(self) -> Sequence[int]:
        """
        A list of ports
        """
        return pulumi.get(self, "ports")



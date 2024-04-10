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
    'ConsumersIamBindingCondition',
    'ConsumersIamMemberCondition',
    'ServiceApi',
    'ServiceApiMethod',
    'ServiceEndpoint',
    'ServiceIamBindingCondition',
    'ServiceIamMemberCondition',
]

@pulumi.output_type
class ConsumersIamBindingCondition(dict):
    def __init__(__self__, *,
                 expression: str,
                 title: str,
                 description: Optional[str] = None):
        pulumi.set(__self__, "expression", expression)
        pulumi.set(__self__, "title", title)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter
    def expression(self) -> str:
        return pulumi.get(self, "expression")

    @property
    @pulumi.getter
    def title(self) -> str:
        return pulumi.get(self, "title")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        return pulumi.get(self, "description")


@pulumi.output_type
class ConsumersIamMemberCondition(dict):
    def __init__(__self__, *,
                 expression: str,
                 title: str,
                 description: Optional[str] = None):
        pulumi.set(__self__, "expression", expression)
        pulumi.set(__self__, "title", title)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter
    def expression(self) -> str:
        return pulumi.get(self, "expression")

    @property
    @pulumi.getter
    def title(self) -> str:
        return pulumi.get(self, "title")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        return pulumi.get(self, "description")


@pulumi.output_type
class ServiceApi(dict):
    def __init__(__self__, *,
                 methods: Optional[Sequence['outputs.ServiceApiMethod']] = None,
                 name: Optional[str] = None,
                 syntax: Optional[str] = None,
                 version: Optional[str] = None):
        """
        :param Sequence['ServiceApiMethodArgs'] methods: A list of Method objects; structure is documented below.
        :param str name: The simple name of the endpoint as described in the config.
        :param str syntax: `SYNTAX_PROTO2` or `SYNTAX_PROTO3`.
        :param str version: A version string for this api. If specified, will have the form major-version.minor-version, e.g. `1.10`.
        """
        if methods is not None:
            pulumi.set(__self__, "methods", methods)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if syntax is not None:
            pulumi.set(__self__, "syntax", syntax)
        if version is not None:
            pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter
    def methods(self) -> Optional[Sequence['outputs.ServiceApiMethod']]:
        """
        A list of Method objects; structure is documented below.
        """
        return pulumi.get(self, "methods")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The simple name of the endpoint as described in the config.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def syntax(self) -> Optional[str]:
        """
        `SYNTAX_PROTO2` or `SYNTAX_PROTO3`.
        """
        return pulumi.get(self, "syntax")

    @property
    @pulumi.getter
    def version(self) -> Optional[str]:
        """
        A version string for this api. If specified, will have the form major-version.minor-version, e.g. `1.10`.
        """
        return pulumi.get(self, "version")


@pulumi.output_type
class ServiceApiMethod(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "requestType":
            suggest = "request_type"
        elif key == "responseType":
            suggest = "response_type"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ServiceApiMethod. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ServiceApiMethod.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ServiceApiMethod.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 name: Optional[str] = None,
                 request_type: Optional[str] = None,
                 response_type: Optional[str] = None,
                 syntax: Optional[str] = None):
        """
        :param str name: The simple name of the endpoint as described in the config.
        :param str request_type: The type URL for the request to this API.
        :param str response_type: The type URL for the response from this API.
        :param str syntax: `SYNTAX_PROTO2` or `SYNTAX_PROTO3`.
        """
        if name is not None:
            pulumi.set(__self__, "name", name)
        if request_type is not None:
            pulumi.set(__self__, "request_type", request_type)
        if response_type is not None:
            pulumi.set(__self__, "response_type", response_type)
        if syntax is not None:
            pulumi.set(__self__, "syntax", syntax)

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The simple name of the endpoint as described in the config.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="requestType")
    def request_type(self) -> Optional[str]:
        """
        The type URL for the request to this API.
        """
        return pulumi.get(self, "request_type")

    @property
    @pulumi.getter(name="responseType")
    def response_type(self) -> Optional[str]:
        """
        The type URL for the response from this API.
        """
        return pulumi.get(self, "response_type")

    @property
    @pulumi.getter
    def syntax(self) -> Optional[str]:
        """
        `SYNTAX_PROTO2` or `SYNTAX_PROTO3`.
        """
        return pulumi.get(self, "syntax")


@pulumi.output_type
class ServiceEndpoint(dict):
    def __init__(__self__, *,
                 address: Optional[str] = None,
                 name: Optional[str] = None):
        """
        :param str address: The FQDN of the endpoint as described in the config.
        :param str name: The simple name of the endpoint as described in the config.
        """
        if address is not None:
            pulumi.set(__self__, "address", address)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def address(self) -> Optional[str]:
        """
        The FQDN of the endpoint as described in the config.
        """
        return pulumi.get(self, "address")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The simple name of the endpoint as described in the config.
        """
        return pulumi.get(self, "name")


@pulumi.output_type
class ServiceIamBindingCondition(dict):
    def __init__(__self__, *,
                 expression: str,
                 title: str,
                 description: Optional[str] = None):
        pulumi.set(__self__, "expression", expression)
        pulumi.set(__self__, "title", title)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter
    def expression(self) -> str:
        return pulumi.get(self, "expression")

    @property
    @pulumi.getter
    def title(self) -> str:
        return pulumi.get(self, "title")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        return pulumi.get(self, "description")


@pulumi.output_type
class ServiceIamMemberCondition(dict):
    def __init__(__self__, *,
                 expression: str,
                 title: str,
                 description: Optional[str] = None):
        pulumi.set(__self__, "expression", expression)
        pulumi.set(__self__, "title", title)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter
    def expression(self) -> str:
        return pulumi.get(self, "expression")

    @property
    @pulumi.getter
    def title(self) -> str:
        return pulumi.get(self, "title")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        return pulumi.get(self, "description")



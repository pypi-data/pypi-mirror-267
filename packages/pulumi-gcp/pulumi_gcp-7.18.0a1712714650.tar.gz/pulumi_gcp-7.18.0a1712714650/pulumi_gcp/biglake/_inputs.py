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
    'DatabaseHiveOptionsArgs',
    'TableHiveOptionsArgs',
    'TableHiveOptionsStorageDescriptorArgs',
]

@pulumi.input_type
class DatabaseHiveOptionsArgs:
    def __init__(__self__, *,
                 location_uri: Optional[pulumi.Input[str]] = None,
                 parameters: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        :param pulumi.Input[str] location_uri: Cloud Storage folder URI where the database data is stored, starting with "gs://".
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] parameters: Stores user supplied Hive database parameters. An object containing a
               list of"key": value pairs.
               Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.
               
               - - -
        """
        if location_uri is not None:
            pulumi.set(__self__, "location_uri", location_uri)
        if parameters is not None:
            pulumi.set(__self__, "parameters", parameters)

    @property
    @pulumi.getter(name="locationUri")
    def location_uri(self) -> Optional[pulumi.Input[str]]:
        """
        Cloud Storage folder URI where the database data is stored, starting with "gs://".
        """
        return pulumi.get(self, "location_uri")

    @location_uri.setter
    def location_uri(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location_uri", value)

    @property
    @pulumi.getter
    def parameters(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Stores user supplied Hive database parameters. An object containing a
        list of"key": value pairs.
        Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.

        - - -
        """
        return pulumi.get(self, "parameters")

    @parameters.setter
    def parameters(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "parameters", value)


@pulumi.input_type
class TableHiveOptionsArgs:
    def __init__(__self__, *,
                 parameters: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 storage_descriptor: Optional[pulumi.Input['TableHiveOptionsStorageDescriptorArgs']] = None,
                 table_type: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] parameters: Stores user supplied Hive table parameters. An object containing a
               list of "key": value pairs.
               Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.
        :param pulumi.Input['TableHiveOptionsStorageDescriptorArgs'] storage_descriptor: Stores physical storage information on the data.
               Structure is documented below.
        :param pulumi.Input[str] table_type: Hive table type. For example, MANAGED_TABLE, EXTERNAL_TABLE.
        """
        if parameters is not None:
            pulumi.set(__self__, "parameters", parameters)
        if storage_descriptor is not None:
            pulumi.set(__self__, "storage_descriptor", storage_descriptor)
        if table_type is not None:
            pulumi.set(__self__, "table_type", table_type)

    @property
    @pulumi.getter
    def parameters(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Stores user supplied Hive table parameters. An object containing a
        list of "key": value pairs.
        Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.
        """
        return pulumi.get(self, "parameters")

    @parameters.setter
    def parameters(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "parameters", value)

    @property
    @pulumi.getter(name="storageDescriptor")
    def storage_descriptor(self) -> Optional[pulumi.Input['TableHiveOptionsStorageDescriptorArgs']]:
        """
        Stores physical storage information on the data.
        Structure is documented below.
        """
        return pulumi.get(self, "storage_descriptor")

    @storage_descriptor.setter
    def storage_descriptor(self, value: Optional[pulumi.Input['TableHiveOptionsStorageDescriptorArgs']]):
        pulumi.set(self, "storage_descriptor", value)

    @property
    @pulumi.getter(name="tableType")
    def table_type(self) -> Optional[pulumi.Input[str]]:
        """
        Hive table type. For example, MANAGED_TABLE, EXTERNAL_TABLE.
        """
        return pulumi.get(self, "table_type")

    @table_type.setter
    def table_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "table_type", value)


@pulumi.input_type
class TableHiveOptionsStorageDescriptorArgs:
    def __init__(__self__, *,
                 input_format: Optional[pulumi.Input[str]] = None,
                 location_uri: Optional[pulumi.Input[str]] = None,
                 output_format: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] input_format: The fully qualified Java class name of the input format.
        :param pulumi.Input[str] location_uri: Cloud Storage folder URI where the table data is stored, starting with "gs://".
        :param pulumi.Input[str] output_format: The fully qualified Java class name of the output format.
        """
        if input_format is not None:
            pulumi.set(__self__, "input_format", input_format)
        if location_uri is not None:
            pulumi.set(__self__, "location_uri", location_uri)
        if output_format is not None:
            pulumi.set(__self__, "output_format", output_format)

    @property
    @pulumi.getter(name="inputFormat")
    def input_format(self) -> Optional[pulumi.Input[str]]:
        """
        The fully qualified Java class name of the input format.
        """
        return pulumi.get(self, "input_format")

    @input_format.setter
    def input_format(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "input_format", value)

    @property
    @pulumi.getter(name="locationUri")
    def location_uri(self) -> Optional[pulumi.Input[str]]:
        """
        Cloud Storage folder URI where the table data is stored, starting with "gs://".
        """
        return pulumi.get(self, "location_uri")

    @location_uri.setter
    def location_uri(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location_uri", value)

    @property
    @pulumi.getter(name="outputFormat")
    def output_format(self) -> Optional[pulumi.Input[str]]:
        """
        The fully qualified Java class name of the output format.
        """
        return pulumi.get(self, "output_format")

    @output_format.setter
    def output_format(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "output_format", value)



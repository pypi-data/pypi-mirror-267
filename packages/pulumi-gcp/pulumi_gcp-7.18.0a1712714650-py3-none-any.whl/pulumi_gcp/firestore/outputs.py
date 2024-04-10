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
    'BackupScheduleDailyRecurrence',
    'BackupScheduleWeeklyRecurrence',
    'DatabaseCmekConfig',
    'FieldIndexConfig',
    'FieldIndexConfigIndex',
    'FieldTtlConfig',
    'IndexField',
]

@pulumi.output_type
class BackupScheduleDailyRecurrence(dict):
    def __init__(__self__):
        pass


@pulumi.output_type
class BackupScheduleWeeklyRecurrence(dict):
    def __init__(__self__, *,
                 day: Optional[str] = None):
        """
        :param str day: The day of week to run.
               Possible values are: `DAY_OF_WEEK_UNSPECIFIED`, `MONDAY`, `TUESDAY`, `WEDNESDAY`, `THURSDAY`, `FRIDAY`, `SATURDAY`, `SUNDAY`.
        """
        if day is not None:
            pulumi.set(__self__, "day", day)

    @property
    @pulumi.getter
    def day(self) -> Optional[str]:
        """
        The day of week to run.
        Possible values are: `DAY_OF_WEEK_UNSPECIFIED`, `MONDAY`, `TUESDAY`, `WEDNESDAY`, `THURSDAY`, `FRIDAY`, `SATURDAY`, `SUNDAY`.
        """
        return pulumi.get(self, "day")


@pulumi.output_type
class DatabaseCmekConfig(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "kmsKeyName":
            suggest = "kms_key_name"
        elif key == "activeKeyVersions":
            suggest = "active_key_versions"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in DatabaseCmekConfig. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        DatabaseCmekConfig.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        DatabaseCmekConfig.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 kms_key_name: str,
                 active_key_versions: Optional[Sequence[str]] = None):
        """
        :param str kms_key_name: The resource ID of a Cloud KMS key. If set, the database created will
               be a Customer-managed Encryption Key (CMEK) database encrypted with
               this key. This feature is allowlist only in initial launch.
               Only keys in the same location as this database are allowed to be used
               for encryption. For Firestore's nam5 multi-region, this corresponds to Cloud KMS
               multi-region us. For Firestore's eur3 multi-region, this corresponds to
               Cloud KMS multi-region europe. See https://cloud.google.com/kms/docs/locations.
               This value should be the KMS key resource ID in the format of
               `projects/{project_id}/locations/{kms_location}/keyRings/{key_ring}/cryptoKeys/{crypto_key}`.
               How to retrive this resource ID is listed at
               https://cloud.google.com/kms/docs/getting-resource-ids#getting_the_id_for_a_key_and_version.
        :param Sequence[str] active_key_versions: (Output)
               Currently in-use KMS key versions (https://cloud.google.com/kms/docs/resource-hierarchy#key_versions).
               During key rotation (https://cloud.google.com/kms/docs/key-rotation), there can be
               multiple in-use key versions.
               The expected format is
               `projects/{project_id}/locations/{kms_location}/keyRings/{key_ring}/cryptoKeys/{crypto_key}/cryptoKeyVersions/{key_version}`.
        """
        pulumi.set(__self__, "kms_key_name", kms_key_name)
        if active_key_versions is not None:
            pulumi.set(__self__, "active_key_versions", active_key_versions)

    @property
    @pulumi.getter(name="kmsKeyName")
    def kms_key_name(self) -> str:
        """
        The resource ID of a Cloud KMS key. If set, the database created will
        be a Customer-managed Encryption Key (CMEK) database encrypted with
        this key. This feature is allowlist only in initial launch.
        Only keys in the same location as this database are allowed to be used
        for encryption. For Firestore's nam5 multi-region, this corresponds to Cloud KMS
        multi-region us. For Firestore's eur3 multi-region, this corresponds to
        Cloud KMS multi-region europe. See https://cloud.google.com/kms/docs/locations.
        This value should be the KMS key resource ID in the format of
        `projects/{project_id}/locations/{kms_location}/keyRings/{key_ring}/cryptoKeys/{crypto_key}`.
        How to retrive this resource ID is listed at
        https://cloud.google.com/kms/docs/getting-resource-ids#getting_the_id_for_a_key_and_version.
        """
        return pulumi.get(self, "kms_key_name")

    @property
    @pulumi.getter(name="activeKeyVersions")
    def active_key_versions(self) -> Optional[Sequence[str]]:
        """
        (Output)
        Currently in-use KMS key versions (https://cloud.google.com/kms/docs/resource-hierarchy#key_versions).
        During key rotation (https://cloud.google.com/kms/docs/key-rotation), there can be
        multiple in-use key versions.
        The expected format is
        `projects/{project_id}/locations/{kms_location}/keyRings/{key_ring}/cryptoKeys/{crypto_key}/cryptoKeyVersions/{key_version}`.
        """
        return pulumi.get(self, "active_key_versions")


@pulumi.output_type
class FieldIndexConfig(dict):
    def __init__(__self__, *,
                 indexes: Optional[Sequence['outputs.FieldIndexConfigIndex']] = None):
        """
        :param Sequence['FieldIndexConfigIndexArgs'] indexes: The indexes to configure on the field. Order or array contains must be specified.
               Structure is documented below.
        """
        if indexes is not None:
            pulumi.set(__self__, "indexes", indexes)

    @property
    @pulumi.getter
    def indexes(self) -> Optional[Sequence['outputs.FieldIndexConfigIndex']]:
        """
        The indexes to configure on the field. Order or array contains must be specified.
        Structure is documented below.
        """
        return pulumi.get(self, "indexes")


@pulumi.output_type
class FieldIndexConfigIndex(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "arrayConfig":
            suggest = "array_config"
        elif key == "queryScope":
            suggest = "query_scope"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in FieldIndexConfigIndex. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        FieldIndexConfigIndex.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        FieldIndexConfigIndex.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 array_config: Optional[str] = None,
                 order: Optional[str] = None,
                 query_scope: Optional[str] = None):
        """
        :param str array_config: Indicates that this field supports operations on arrayValues. Only one of `order` and `arrayConfig` can
               be specified.
               Possible values are: `CONTAINS`.
        :param str order: Indicates that this field supports ordering by the specified order or comparing using =, <, <=, >, >=, !=.
               Only one of `order` and `arrayConfig` can be specified.
               Possible values are: `ASCENDING`, `DESCENDING`.
        :param str query_scope: The scope at which a query is run. Collection scoped queries require you specify
               the collection at query time. Collection group scope allows queries across all
               collections with the same id.
               Default value is `COLLECTION`.
               Possible values are: `COLLECTION`, `COLLECTION_GROUP`.
        """
        if array_config is not None:
            pulumi.set(__self__, "array_config", array_config)
        if order is not None:
            pulumi.set(__self__, "order", order)
        if query_scope is not None:
            pulumi.set(__self__, "query_scope", query_scope)

    @property
    @pulumi.getter(name="arrayConfig")
    def array_config(self) -> Optional[str]:
        """
        Indicates that this field supports operations on arrayValues. Only one of `order` and `arrayConfig` can
        be specified.
        Possible values are: `CONTAINS`.
        """
        return pulumi.get(self, "array_config")

    @property
    @pulumi.getter
    def order(self) -> Optional[str]:
        """
        Indicates that this field supports ordering by the specified order or comparing using =, <, <=, >, >=, !=.
        Only one of `order` and `arrayConfig` can be specified.
        Possible values are: `ASCENDING`, `DESCENDING`.
        """
        return pulumi.get(self, "order")

    @property
    @pulumi.getter(name="queryScope")
    def query_scope(self) -> Optional[str]:
        """
        The scope at which a query is run. Collection scoped queries require you specify
        the collection at query time. Collection group scope allows queries across all
        collections with the same id.
        Default value is `COLLECTION`.
        Possible values are: `COLLECTION`, `COLLECTION_GROUP`.
        """
        return pulumi.get(self, "query_scope")


@pulumi.output_type
class FieldTtlConfig(dict):
    def __init__(__self__, *,
                 state: Optional[str] = None):
        """
        :param str state: (Output)
               The state of TTL (time-to-live) configuration for documents that have this Field set.
        """
        if state is not None:
            pulumi.set(__self__, "state", state)

    @property
    @pulumi.getter
    def state(self) -> Optional[str]:
        """
        (Output)
        The state of TTL (time-to-live) configuration for documents that have this Field set.
        """
        return pulumi.get(self, "state")


@pulumi.output_type
class IndexField(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "arrayConfig":
            suggest = "array_config"
        elif key == "fieldPath":
            suggest = "field_path"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in IndexField. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        IndexField.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        IndexField.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 array_config: Optional[str] = None,
                 field_path: Optional[str] = None,
                 order: Optional[str] = None):
        """
        :param str array_config: Indicates that this field supports operations on arrayValues. Only one of `order` and `arrayConfig` can
               be specified.
               Possible values are: `CONTAINS`.
               
               - - -
        :param str field_path: Name of the field.
        :param str order: Indicates that this field supports ordering by the specified order or comparing using =, <, <=, >, >=.
               Only one of `order` and `arrayConfig` can be specified.
               Possible values are: `ASCENDING`, `DESCENDING`.
        """
        if array_config is not None:
            pulumi.set(__self__, "array_config", array_config)
        if field_path is not None:
            pulumi.set(__self__, "field_path", field_path)
        if order is not None:
            pulumi.set(__self__, "order", order)

    @property
    @pulumi.getter(name="arrayConfig")
    def array_config(self) -> Optional[str]:
        """
        Indicates that this field supports operations on arrayValues. Only one of `order` and `arrayConfig` can
        be specified.
        Possible values are: `CONTAINS`.

        - - -
        """
        return pulumi.get(self, "array_config")

    @property
    @pulumi.getter(name="fieldPath")
    def field_path(self) -> Optional[str]:
        """
        Name of the field.
        """
        return pulumi.get(self, "field_path")

    @property
    @pulumi.getter
    def order(self) -> Optional[str]:
        """
        Indicates that this field supports ordering by the specified order or comparing using =, <, <=, >, >=.
        Only one of `order` and `arrayConfig` can be specified.
        Possible values are: `ASCENDING`, `DESCENDING`.
        """
        return pulumi.get(self, "order")



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
from ._inputs import *

__all__ = ['TableArgs', 'Table']

@pulumi.input_type
class TableArgs:
    def __init__(__self__, *,
                 instance_name: pulumi.Input[str],
                 change_stream_retention: Optional[pulumi.Input[str]] = None,
                 column_families: Optional[pulumi.Input[Sequence[pulumi.Input['TableColumnFamilyArgs']]]] = None,
                 deletion_protection: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 split_keys: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a Table resource.
        :param pulumi.Input[str] instance_name: The name of the Bigtable instance.
        :param pulumi.Input[str] change_stream_retention: Duration to retain change stream data for the table. Set to 0 to disable. Must be between 1 and 7 days.
               
               -----
        :param pulumi.Input[Sequence[pulumi.Input['TableColumnFamilyArgs']]] column_families: A group of columns within a table which share a common configuration. This can be specified multiple times. Structure is documented below.
        :param pulumi.Input[str] deletion_protection: A field to make the table protected against data loss i.e. when set to PROTECTED, deleting the table, the column families in the table, and the instance containing the table would be prohibited. If not provided, deletion protection will be set to UNPROTECTED.
        :param pulumi.Input[str] name: The name of the table. Must be 1-50 characters and must only contain hyphens, underscores, periods, letters and numbers.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs. If it
               is not provided, the provider project is used.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] split_keys: A list of predefined keys to split the table on.
               !> **Warning:** Modifying the `split_keys` of an existing table will cause the provider
               to delete/recreate the entire `bigtable.Table` resource.
        """
        pulumi.set(__self__, "instance_name", instance_name)
        if change_stream_retention is not None:
            pulumi.set(__self__, "change_stream_retention", change_stream_retention)
        if column_families is not None:
            pulumi.set(__self__, "column_families", column_families)
        if deletion_protection is not None:
            pulumi.set(__self__, "deletion_protection", deletion_protection)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if split_keys is not None:
            pulumi.set(__self__, "split_keys", split_keys)

    @property
    @pulumi.getter(name="instanceName")
    def instance_name(self) -> pulumi.Input[str]:
        """
        The name of the Bigtable instance.
        """
        return pulumi.get(self, "instance_name")

    @instance_name.setter
    def instance_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "instance_name", value)

    @property
    @pulumi.getter(name="changeStreamRetention")
    def change_stream_retention(self) -> Optional[pulumi.Input[str]]:
        """
        Duration to retain change stream data for the table. Set to 0 to disable. Must be between 1 and 7 days.

        -----
        """
        return pulumi.get(self, "change_stream_retention")

    @change_stream_retention.setter
    def change_stream_retention(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "change_stream_retention", value)

    @property
    @pulumi.getter(name="columnFamilies")
    def column_families(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['TableColumnFamilyArgs']]]]:
        """
        A group of columns within a table which share a common configuration. This can be specified multiple times. Structure is documented below.
        """
        return pulumi.get(self, "column_families")

    @column_families.setter
    def column_families(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['TableColumnFamilyArgs']]]]):
        pulumi.set(self, "column_families", value)

    @property
    @pulumi.getter(name="deletionProtection")
    def deletion_protection(self) -> Optional[pulumi.Input[str]]:
        """
        A field to make the table protected against data loss i.e. when set to PROTECTED, deleting the table, the column families in the table, and the instance containing the table would be prohibited. If not provided, deletion protection will be set to UNPROTECTED.
        """
        return pulumi.get(self, "deletion_protection")

    @deletion_protection.setter
    def deletion_protection(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "deletion_protection", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the table. Must be 1-50 characters and must only contain hyphens, underscores, periods, letters and numbers.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the project in which the resource belongs. If it
        is not provided, the provider project is used.
        """
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)

    @property
    @pulumi.getter(name="splitKeys")
    def split_keys(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of predefined keys to split the table on.
        !> **Warning:** Modifying the `split_keys` of an existing table will cause the provider
        to delete/recreate the entire `bigtable.Table` resource.
        """
        return pulumi.get(self, "split_keys")

    @split_keys.setter
    def split_keys(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "split_keys", value)


@pulumi.input_type
class _TableState:
    def __init__(__self__, *,
                 change_stream_retention: Optional[pulumi.Input[str]] = None,
                 column_families: Optional[pulumi.Input[Sequence[pulumi.Input['TableColumnFamilyArgs']]]] = None,
                 deletion_protection: Optional[pulumi.Input[str]] = None,
                 instance_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 split_keys: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering Table resources.
        :param pulumi.Input[str] change_stream_retention: Duration to retain change stream data for the table. Set to 0 to disable. Must be between 1 and 7 days.
               
               -----
        :param pulumi.Input[Sequence[pulumi.Input['TableColumnFamilyArgs']]] column_families: A group of columns within a table which share a common configuration. This can be specified multiple times. Structure is documented below.
        :param pulumi.Input[str] deletion_protection: A field to make the table protected against data loss i.e. when set to PROTECTED, deleting the table, the column families in the table, and the instance containing the table would be prohibited. If not provided, deletion protection will be set to UNPROTECTED.
        :param pulumi.Input[str] instance_name: The name of the Bigtable instance.
        :param pulumi.Input[str] name: The name of the table. Must be 1-50 characters and must only contain hyphens, underscores, periods, letters and numbers.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs. If it
               is not provided, the provider project is used.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] split_keys: A list of predefined keys to split the table on.
               !> **Warning:** Modifying the `split_keys` of an existing table will cause the provider
               to delete/recreate the entire `bigtable.Table` resource.
        """
        if change_stream_retention is not None:
            pulumi.set(__self__, "change_stream_retention", change_stream_retention)
        if column_families is not None:
            pulumi.set(__self__, "column_families", column_families)
        if deletion_protection is not None:
            pulumi.set(__self__, "deletion_protection", deletion_protection)
        if instance_name is not None:
            pulumi.set(__self__, "instance_name", instance_name)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if split_keys is not None:
            pulumi.set(__self__, "split_keys", split_keys)

    @property
    @pulumi.getter(name="changeStreamRetention")
    def change_stream_retention(self) -> Optional[pulumi.Input[str]]:
        """
        Duration to retain change stream data for the table. Set to 0 to disable. Must be between 1 and 7 days.

        -----
        """
        return pulumi.get(self, "change_stream_retention")

    @change_stream_retention.setter
    def change_stream_retention(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "change_stream_retention", value)

    @property
    @pulumi.getter(name="columnFamilies")
    def column_families(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['TableColumnFamilyArgs']]]]:
        """
        A group of columns within a table which share a common configuration. This can be specified multiple times. Structure is documented below.
        """
        return pulumi.get(self, "column_families")

    @column_families.setter
    def column_families(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['TableColumnFamilyArgs']]]]):
        pulumi.set(self, "column_families", value)

    @property
    @pulumi.getter(name="deletionProtection")
    def deletion_protection(self) -> Optional[pulumi.Input[str]]:
        """
        A field to make the table protected against data loss i.e. when set to PROTECTED, deleting the table, the column families in the table, and the instance containing the table would be prohibited. If not provided, deletion protection will be set to UNPROTECTED.
        """
        return pulumi.get(self, "deletion_protection")

    @deletion_protection.setter
    def deletion_protection(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "deletion_protection", value)

    @property
    @pulumi.getter(name="instanceName")
    def instance_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Bigtable instance.
        """
        return pulumi.get(self, "instance_name")

    @instance_name.setter
    def instance_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "instance_name", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the table. Must be 1-50 characters and must only contain hyphens, underscores, periods, letters and numbers.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the project in which the resource belongs. If it
        is not provided, the provider project is used.
        """
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)

    @property
    @pulumi.getter(name="splitKeys")
    def split_keys(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of predefined keys to split the table on.
        !> **Warning:** Modifying the `split_keys` of an existing table will cause the provider
        to delete/recreate the entire `bigtable.Table` resource.
        """
        return pulumi.get(self, "split_keys")

    @split_keys.setter
    def split_keys(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "split_keys", value)


class Table(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 change_stream_retention: Optional[pulumi.Input[str]] = None,
                 column_families: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['TableColumnFamilyArgs']]]]] = None,
                 deletion_protection: Optional[pulumi.Input[str]] = None,
                 instance_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 split_keys: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Creates a Google Cloud Bigtable table inside an instance. For more information see
        [the official documentation](https://cloud.google.com/bigtable/) and
        [API](https://cloud.google.com/bigtable/docs/go/reference).

        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        instance = gcp.bigtable.Instance("instance",
            name="tf-instance",
            clusters=[gcp.bigtable.InstanceClusterArgs(
                cluster_id="tf-instance-cluster",
                zone="us-central1-b",
                num_nodes=3,
                storage_type="HDD",
            )])
        table = gcp.bigtable.Table("table",
            name="tf-table",
            instance_name=instance.name,
            split_keys=[
                "a",
                "b",
                "c",
            ],
            column_families=[
                gcp.bigtable.TableColumnFamilyArgs(
                    family="family-first",
                ),
                gcp.bigtable.TableColumnFamilyArgs(
                    family="family-second",
                ),
            ],
            change_stream_retention="24h0m0s")
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        -> **Fields affected by import** The following fields can't be read and will show diffs if set in config when imported: `split_keys`

        Bigtable Tables can be imported using any of these accepted formats:

        * `projects/{{project}}/instances/{{instance_name}}/tables/{{name}}`

        * `{{project}}/{{instance_name}}/{{name}}`

        * `{{instance_name}}/{{name}}`

        When using the `pulumi import` command, Bigtable Tables can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:bigtable/table:Table default projects/{{project}}/instances/{{instance_name}}/tables/{{name}}
        ```

        ```sh
        $ pulumi import gcp:bigtable/table:Table default {{project}}/{{instance_name}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:bigtable/table:Table default {{instance_name}}/{{name}}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] change_stream_retention: Duration to retain change stream data for the table. Set to 0 to disable. Must be between 1 and 7 days.
               
               -----
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['TableColumnFamilyArgs']]]] column_families: A group of columns within a table which share a common configuration. This can be specified multiple times. Structure is documented below.
        :param pulumi.Input[str] deletion_protection: A field to make the table protected against data loss i.e. when set to PROTECTED, deleting the table, the column families in the table, and the instance containing the table would be prohibited. If not provided, deletion protection will be set to UNPROTECTED.
        :param pulumi.Input[str] instance_name: The name of the Bigtable instance.
        :param pulumi.Input[str] name: The name of the table. Must be 1-50 characters and must only contain hyphens, underscores, periods, letters and numbers.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs. If it
               is not provided, the provider project is used.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] split_keys: A list of predefined keys to split the table on.
               !> **Warning:** Modifying the `split_keys` of an existing table will cause the provider
               to delete/recreate the entire `bigtable.Table` resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: TableArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Creates a Google Cloud Bigtable table inside an instance. For more information see
        [the official documentation](https://cloud.google.com/bigtable/) and
        [API](https://cloud.google.com/bigtable/docs/go/reference).

        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        instance = gcp.bigtable.Instance("instance",
            name="tf-instance",
            clusters=[gcp.bigtable.InstanceClusterArgs(
                cluster_id="tf-instance-cluster",
                zone="us-central1-b",
                num_nodes=3,
                storage_type="HDD",
            )])
        table = gcp.bigtable.Table("table",
            name="tf-table",
            instance_name=instance.name,
            split_keys=[
                "a",
                "b",
                "c",
            ],
            column_families=[
                gcp.bigtable.TableColumnFamilyArgs(
                    family="family-first",
                ),
                gcp.bigtable.TableColumnFamilyArgs(
                    family="family-second",
                ),
            ],
            change_stream_retention="24h0m0s")
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        -> **Fields affected by import** The following fields can't be read and will show diffs if set in config when imported: `split_keys`

        Bigtable Tables can be imported using any of these accepted formats:

        * `projects/{{project}}/instances/{{instance_name}}/tables/{{name}}`

        * `{{project}}/{{instance_name}}/{{name}}`

        * `{{instance_name}}/{{name}}`

        When using the `pulumi import` command, Bigtable Tables can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:bigtable/table:Table default projects/{{project}}/instances/{{instance_name}}/tables/{{name}}
        ```

        ```sh
        $ pulumi import gcp:bigtable/table:Table default {{project}}/{{instance_name}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:bigtable/table:Table default {{instance_name}}/{{name}}
        ```

        :param str resource_name: The name of the resource.
        :param TableArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(TableArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 change_stream_retention: Optional[pulumi.Input[str]] = None,
                 column_families: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['TableColumnFamilyArgs']]]]] = None,
                 deletion_protection: Optional[pulumi.Input[str]] = None,
                 instance_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 split_keys: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = TableArgs.__new__(TableArgs)

            __props__.__dict__["change_stream_retention"] = change_stream_retention
            __props__.__dict__["column_families"] = column_families
            __props__.__dict__["deletion_protection"] = deletion_protection
            if instance_name is None and not opts.urn:
                raise TypeError("Missing required property 'instance_name'")
            __props__.__dict__["instance_name"] = instance_name
            __props__.__dict__["name"] = name
            __props__.__dict__["project"] = project
            __props__.__dict__["split_keys"] = split_keys
        super(Table, __self__).__init__(
            'gcp:bigtable/table:Table',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            change_stream_retention: Optional[pulumi.Input[str]] = None,
            column_families: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['TableColumnFamilyArgs']]]]] = None,
            deletion_protection: Optional[pulumi.Input[str]] = None,
            instance_name: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            project: Optional[pulumi.Input[str]] = None,
            split_keys: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None) -> 'Table':
        """
        Get an existing Table resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] change_stream_retention: Duration to retain change stream data for the table. Set to 0 to disable. Must be between 1 and 7 days.
               
               -----
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['TableColumnFamilyArgs']]]] column_families: A group of columns within a table which share a common configuration. This can be specified multiple times. Structure is documented below.
        :param pulumi.Input[str] deletion_protection: A field to make the table protected against data loss i.e. when set to PROTECTED, deleting the table, the column families in the table, and the instance containing the table would be prohibited. If not provided, deletion protection will be set to UNPROTECTED.
        :param pulumi.Input[str] instance_name: The name of the Bigtable instance.
        :param pulumi.Input[str] name: The name of the table. Must be 1-50 characters and must only contain hyphens, underscores, periods, letters and numbers.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs. If it
               is not provided, the provider project is used.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] split_keys: A list of predefined keys to split the table on.
               !> **Warning:** Modifying the `split_keys` of an existing table will cause the provider
               to delete/recreate the entire `bigtable.Table` resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _TableState.__new__(_TableState)

        __props__.__dict__["change_stream_retention"] = change_stream_retention
        __props__.__dict__["column_families"] = column_families
        __props__.__dict__["deletion_protection"] = deletion_protection
        __props__.__dict__["instance_name"] = instance_name
        __props__.__dict__["name"] = name
        __props__.__dict__["project"] = project
        __props__.__dict__["split_keys"] = split_keys
        return Table(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="changeStreamRetention")
    def change_stream_retention(self) -> pulumi.Output[str]:
        """
        Duration to retain change stream data for the table. Set to 0 to disable. Must be between 1 and 7 days.

        -----
        """
        return pulumi.get(self, "change_stream_retention")

    @property
    @pulumi.getter(name="columnFamilies")
    def column_families(self) -> pulumi.Output[Optional[Sequence['outputs.TableColumnFamily']]]:
        """
        A group of columns within a table which share a common configuration. This can be specified multiple times. Structure is documented below.
        """
        return pulumi.get(self, "column_families")

    @property
    @pulumi.getter(name="deletionProtection")
    def deletion_protection(self) -> pulumi.Output[str]:
        """
        A field to make the table protected against data loss i.e. when set to PROTECTED, deleting the table, the column families in the table, and the instance containing the table would be prohibited. If not provided, deletion protection will be set to UNPROTECTED.
        """
        return pulumi.get(self, "deletion_protection")

    @property
    @pulumi.getter(name="instanceName")
    def instance_name(self) -> pulumi.Output[str]:
        """
        The name of the Bigtable instance.
        """
        return pulumi.get(self, "instance_name")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the table. Must be 1-50 characters and must only contain hyphens, underscores, periods, letters and numbers.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        """
        The ID of the project in which the resource belongs. If it
        is not provided, the provider project is used.
        """
        return pulumi.get(self, "project")

    @property
    @pulumi.getter(name="splitKeys")
    def split_keys(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        A list of predefined keys to split the table on.
        !> **Warning:** Modifying the `split_keys` of an existing table will cause the provider
        to delete/recreate the entire `bigtable.Table` resource.
        """
        return pulumi.get(self, "split_keys")


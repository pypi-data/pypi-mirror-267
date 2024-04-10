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

__all__ = ['BiReservationArgs', 'BiReservation']

@pulumi.input_type
class BiReservationArgs:
    def __init__(__self__, *,
                 location: pulumi.Input[str],
                 preferred_tables: Optional[pulumi.Input[Sequence[pulumi.Input['BiReservationPreferredTableArgs']]]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 size: Optional[pulumi.Input[int]] = None):
        """
        The set of arguments for constructing a BiReservation resource.
        :param pulumi.Input[str] location: LOCATION_DESCRIPTION
               
               
               - - -
        :param pulumi.Input[Sequence[pulumi.Input['BiReservationPreferredTableArgs']]] preferred_tables: Preferred tables to use BI capacity for.
               Structure is documented below.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[int] size: Size of a reservation, in bytes.
        """
        pulumi.set(__self__, "location", location)
        if preferred_tables is not None:
            pulumi.set(__self__, "preferred_tables", preferred_tables)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if size is not None:
            pulumi.set(__self__, "size", size)

    @property
    @pulumi.getter
    def location(self) -> pulumi.Input[str]:
        """
        LOCATION_DESCRIPTION


        - - -
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: pulumi.Input[str]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="preferredTables")
    def preferred_tables(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['BiReservationPreferredTableArgs']]]]:
        """
        Preferred tables to use BI capacity for.
        Structure is documented below.
        """
        return pulumi.get(self, "preferred_tables")

    @preferred_tables.setter
    def preferred_tables(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['BiReservationPreferredTableArgs']]]]):
        pulumi.set(self, "preferred_tables", value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the project in which the resource belongs.
        If it is not provided, the provider project is used.
        """
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)

    @property
    @pulumi.getter
    def size(self) -> Optional[pulumi.Input[int]]:
        """
        Size of a reservation, in bytes.
        """
        return pulumi.get(self, "size")

    @size.setter
    def size(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "size", value)


@pulumi.input_type
class _BiReservationState:
    def __init__(__self__, *,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 preferred_tables: Optional[pulumi.Input[Sequence[pulumi.Input['BiReservationPreferredTableArgs']]]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 size: Optional[pulumi.Input[int]] = None,
                 update_time: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering BiReservation resources.
        :param pulumi.Input[str] location: LOCATION_DESCRIPTION
               
               
               - - -
        :param pulumi.Input[str] name: The resource name of the singleton BI reservation. Reservation names have the form `projects/{projectId}/locations/{locationId}/biReservation`.
        :param pulumi.Input[Sequence[pulumi.Input['BiReservationPreferredTableArgs']]] preferred_tables: Preferred tables to use BI capacity for.
               Structure is documented below.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[int] size: Size of a reservation, in bytes.
        :param pulumi.Input[str] update_time: The last update timestamp of a reservation.
               A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z".
        """
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if preferred_tables is not None:
            pulumi.set(__self__, "preferred_tables", preferred_tables)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if size is not None:
            pulumi.set(__self__, "size", size)
        if update_time is not None:
            pulumi.set(__self__, "update_time", update_time)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        LOCATION_DESCRIPTION


        - - -
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The resource name of the singleton BI reservation. Reservation names have the form `projects/{projectId}/locations/{locationId}/biReservation`.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="preferredTables")
    def preferred_tables(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['BiReservationPreferredTableArgs']]]]:
        """
        Preferred tables to use BI capacity for.
        Structure is documented below.
        """
        return pulumi.get(self, "preferred_tables")

    @preferred_tables.setter
    def preferred_tables(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['BiReservationPreferredTableArgs']]]]):
        pulumi.set(self, "preferred_tables", value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the project in which the resource belongs.
        If it is not provided, the provider project is used.
        """
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)

    @property
    @pulumi.getter
    def size(self) -> Optional[pulumi.Input[int]]:
        """
        Size of a reservation, in bytes.
        """
        return pulumi.get(self, "size")

    @size.setter
    def size(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "size", value)

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> Optional[pulumi.Input[str]]:
        """
        The last update timestamp of a reservation.
        A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z".
        """
        return pulumi.get(self, "update_time")

    @update_time.setter
    def update_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "update_time", value)


class BiReservation(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 preferred_tables: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BiReservationPreferredTableArgs']]]]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 size: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        """
        Represents a BI Reservation.

        To get more information about BiReservation, see:

        * [API documentation](https://cloud.google.com/bigquery/docs/reference/reservations/rest/v1/BiReservation)
        * How-to Guides
            * [Introduction to Reservations](https://cloud.google.com/bigquery/docs/reservations-intro)

        ## Example Usage

        ### Bigquery Reservation Bi Reservation Basic

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        reservation = gcp.bigquery.BiReservation("reservation",
            location="us-west2",
            size=3000000000)
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        BiReservation can be imported using any of these accepted formats:

        * `projects/{{project}}/locations/{{location}}/biReservation`

        * `{{project}}/{{location}}`

        * `{{location}}`

        When using the `pulumi import` command, BiReservation can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:bigquery/biReservation:BiReservation default projects/{{project}}/locations/{{location}}/biReservation
        ```

        ```sh
        $ pulumi import gcp:bigquery/biReservation:BiReservation default {{project}}/{{location}}
        ```

        ```sh
        $ pulumi import gcp:bigquery/biReservation:BiReservation default {{location}}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] location: LOCATION_DESCRIPTION
               
               
               - - -
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BiReservationPreferredTableArgs']]]] preferred_tables: Preferred tables to use BI capacity for.
               Structure is documented below.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[int] size: Size of a reservation, in bytes.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: BiReservationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Represents a BI Reservation.

        To get more information about BiReservation, see:

        * [API documentation](https://cloud.google.com/bigquery/docs/reference/reservations/rest/v1/BiReservation)
        * How-to Guides
            * [Introduction to Reservations](https://cloud.google.com/bigquery/docs/reservations-intro)

        ## Example Usage

        ### Bigquery Reservation Bi Reservation Basic

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        reservation = gcp.bigquery.BiReservation("reservation",
            location="us-west2",
            size=3000000000)
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        BiReservation can be imported using any of these accepted formats:

        * `projects/{{project}}/locations/{{location}}/biReservation`

        * `{{project}}/{{location}}`

        * `{{location}}`

        When using the `pulumi import` command, BiReservation can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:bigquery/biReservation:BiReservation default projects/{{project}}/locations/{{location}}/biReservation
        ```

        ```sh
        $ pulumi import gcp:bigquery/biReservation:BiReservation default {{project}}/{{location}}
        ```

        ```sh
        $ pulumi import gcp:bigquery/biReservation:BiReservation default {{location}}
        ```

        :param str resource_name: The name of the resource.
        :param BiReservationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(BiReservationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 preferred_tables: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BiReservationPreferredTableArgs']]]]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 size: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = BiReservationArgs.__new__(BiReservationArgs)

            if location is None and not opts.urn:
                raise TypeError("Missing required property 'location'")
            __props__.__dict__["location"] = location
            __props__.__dict__["preferred_tables"] = preferred_tables
            __props__.__dict__["project"] = project
            __props__.__dict__["size"] = size
            __props__.__dict__["name"] = None
            __props__.__dict__["update_time"] = None
        super(BiReservation, __self__).__init__(
            'gcp:bigquery/biReservation:BiReservation',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            location: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            preferred_tables: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BiReservationPreferredTableArgs']]]]] = None,
            project: Optional[pulumi.Input[str]] = None,
            size: Optional[pulumi.Input[int]] = None,
            update_time: Optional[pulumi.Input[str]] = None) -> 'BiReservation':
        """
        Get an existing BiReservation resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] location: LOCATION_DESCRIPTION
               
               
               - - -
        :param pulumi.Input[str] name: The resource name of the singleton BI reservation. Reservation names have the form `projects/{projectId}/locations/{locationId}/biReservation`.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BiReservationPreferredTableArgs']]]] preferred_tables: Preferred tables to use BI capacity for.
               Structure is documented below.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[int] size: Size of a reservation, in bytes.
        :param pulumi.Input[str] update_time: The last update timestamp of a reservation.
               A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z".
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _BiReservationState.__new__(_BiReservationState)

        __props__.__dict__["location"] = location
        __props__.__dict__["name"] = name
        __props__.__dict__["preferred_tables"] = preferred_tables
        __props__.__dict__["project"] = project
        __props__.__dict__["size"] = size
        __props__.__dict__["update_time"] = update_time
        return BiReservation(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        LOCATION_DESCRIPTION


        - - -
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The resource name of the singleton BI reservation. Reservation names have the form `projects/{projectId}/locations/{locationId}/biReservation`.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="preferredTables")
    def preferred_tables(self) -> pulumi.Output[Optional[Sequence['outputs.BiReservationPreferredTable']]]:
        """
        Preferred tables to use BI capacity for.
        Structure is documented below.
        """
        return pulumi.get(self, "preferred_tables")

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        """
        The ID of the project in which the resource belongs.
        If it is not provided, the provider project is used.
        """
        return pulumi.get(self, "project")

    @property
    @pulumi.getter
    def size(self) -> pulumi.Output[Optional[int]]:
        """
        Size of a reservation, in bytes.
        """
        return pulumi.get(self, "size")

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> pulumi.Output[str]:
        """
        The last update timestamp of a reservation.
        A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z".
        """
        return pulumi.get(self, "update_time")


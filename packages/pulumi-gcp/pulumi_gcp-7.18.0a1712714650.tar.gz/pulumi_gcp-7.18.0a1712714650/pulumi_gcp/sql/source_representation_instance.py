# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['SourceRepresentationInstanceArgs', 'SourceRepresentationInstance']

@pulumi.input_type
class SourceRepresentationInstanceArgs:
    def __init__(__self__, *,
                 database_version: pulumi.Input[str],
                 host: pulumi.Input[str],
                 ca_certificate: Optional[pulumi.Input[str]] = None,
                 client_certificate: Optional[pulumi.Input[str]] = None,
                 client_key: Optional[pulumi.Input[str]] = None,
                 dump_file_path: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 port: Optional[pulumi.Input[int]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 username: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a SourceRepresentationInstance resource.
        :param pulumi.Input[str] database_version: The MySQL version running on your source database server.
               Possible values are: `MYSQL_5_6`, `MYSQL_5_7`, `MYSQL_8_0`, `POSTGRES_9_6`, `POSTGRES_10`, `POSTGRES_11`, `POSTGRES_12`, `POSTGRES_13`, `POSTGRES_14`.
        :param pulumi.Input[str] host: The IPv4 address and port for the external server, or the the DNS address for the external server. If the external server is hosted on Cloud SQL, the port is 5432.
               
               
               - - -
        :param pulumi.Input[str] ca_certificate: The CA certificate on the external server. Include only if SSL/TLS is used on the external server.
        :param pulumi.Input[str] client_certificate: The client certificate on the external server. Required only for server-client authentication. Include only if SSL/TLS is used on the external server.
        :param pulumi.Input[str] client_key: The private key file for the client certificate on the external server. Required only for server-client authentication. Include only if SSL/TLS is used on the external server.
        :param pulumi.Input[str] dump_file_path: A file in the bucket that contains the data from the external server.
        :param pulumi.Input[str] name: The name of the source representation instance. Use any valid Cloud SQL instance name.
        :param pulumi.Input[str] password: The password for the replication user account.
               **Note**: This property is sensitive and will not be displayed in the plan.
        :param pulumi.Input[int] port: The externally accessible port for the source database server.
               Defaults to 3306.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] region: The Region in which the created instance should reside.
               If it is not provided, the provider region is used.
        :param pulumi.Input[str] username: The replication user account on the external server.
        """
        pulumi.set(__self__, "database_version", database_version)
        pulumi.set(__self__, "host", host)
        if ca_certificate is not None:
            pulumi.set(__self__, "ca_certificate", ca_certificate)
        if client_certificate is not None:
            pulumi.set(__self__, "client_certificate", client_certificate)
        if client_key is not None:
            pulumi.set(__self__, "client_key", client_key)
        if dump_file_path is not None:
            pulumi.set(__self__, "dump_file_path", dump_file_path)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if password is not None:
            pulumi.set(__self__, "password", password)
        if port is not None:
            pulumi.set(__self__, "port", port)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if region is not None:
            pulumi.set(__self__, "region", region)
        if username is not None:
            pulumi.set(__self__, "username", username)

    @property
    @pulumi.getter(name="databaseVersion")
    def database_version(self) -> pulumi.Input[str]:
        """
        The MySQL version running on your source database server.
        Possible values are: `MYSQL_5_6`, `MYSQL_5_7`, `MYSQL_8_0`, `POSTGRES_9_6`, `POSTGRES_10`, `POSTGRES_11`, `POSTGRES_12`, `POSTGRES_13`, `POSTGRES_14`.
        """
        return pulumi.get(self, "database_version")

    @database_version.setter
    def database_version(self, value: pulumi.Input[str]):
        pulumi.set(self, "database_version", value)

    @property
    @pulumi.getter
    def host(self) -> pulumi.Input[str]:
        """
        The IPv4 address and port for the external server, or the the DNS address for the external server. If the external server is hosted on Cloud SQL, the port is 5432.


        - - -
        """
        return pulumi.get(self, "host")

    @host.setter
    def host(self, value: pulumi.Input[str]):
        pulumi.set(self, "host", value)

    @property
    @pulumi.getter(name="caCertificate")
    def ca_certificate(self) -> Optional[pulumi.Input[str]]:
        """
        The CA certificate on the external server. Include only if SSL/TLS is used on the external server.
        """
        return pulumi.get(self, "ca_certificate")

    @ca_certificate.setter
    def ca_certificate(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ca_certificate", value)

    @property
    @pulumi.getter(name="clientCertificate")
    def client_certificate(self) -> Optional[pulumi.Input[str]]:
        """
        The client certificate on the external server. Required only for server-client authentication. Include only if SSL/TLS is used on the external server.
        """
        return pulumi.get(self, "client_certificate")

    @client_certificate.setter
    def client_certificate(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "client_certificate", value)

    @property
    @pulumi.getter(name="clientKey")
    def client_key(self) -> Optional[pulumi.Input[str]]:
        """
        The private key file for the client certificate on the external server. Required only for server-client authentication. Include only if SSL/TLS is used on the external server.
        """
        return pulumi.get(self, "client_key")

    @client_key.setter
    def client_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "client_key", value)

    @property
    @pulumi.getter(name="dumpFilePath")
    def dump_file_path(self) -> Optional[pulumi.Input[str]]:
        """
        A file in the bucket that contains the data from the external server.
        """
        return pulumi.get(self, "dump_file_path")

    @dump_file_path.setter
    def dump_file_path(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "dump_file_path", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the source representation instance. Use any valid Cloud SQL instance name.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def password(self) -> Optional[pulumi.Input[str]]:
        """
        The password for the replication user account.
        **Note**: This property is sensitive and will not be displayed in the plan.
        """
        return pulumi.get(self, "password")

    @password.setter
    def password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "password", value)

    @property
    @pulumi.getter
    def port(self) -> Optional[pulumi.Input[int]]:
        """
        The externally accessible port for the source database server.
        Defaults to 3306.
        """
        return pulumi.get(self, "port")

    @port.setter
    def port(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "port", value)

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
    def region(self) -> Optional[pulumi.Input[str]]:
        """
        The Region in which the created instance should reside.
        If it is not provided, the provider region is used.
        """
        return pulumi.get(self, "region")

    @region.setter
    def region(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "region", value)

    @property
    @pulumi.getter
    def username(self) -> Optional[pulumi.Input[str]]:
        """
        The replication user account on the external server.
        """
        return pulumi.get(self, "username")

    @username.setter
    def username(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "username", value)


@pulumi.input_type
class _SourceRepresentationInstanceState:
    def __init__(__self__, *,
                 ca_certificate: Optional[pulumi.Input[str]] = None,
                 client_certificate: Optional[pulumi.Input[str]] = None,
                 client_key: Optional[pulumi.Input[str]] = None,
                 database_version: Optional[pulumi.Input[str]] = None,
                 dump_file_path: Optional[pulumi.Input[str]] = None,
                 host: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 port: Optional[pulumi.Input[int]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 username: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering SourceRepresentationInstance resources.
        :param pulumi.Input[str] ca_certificate: The CA certificate on the external server. Include only if SSL/TLS is used on the external server.
        :param pulumi.Input[str] client_certificate: The client certificate on the external server. Required only for server-client authentication. Include only if SSL/TLS is used on the external server.
        :param pulumi.Input[str] client_key: The private key file for the client certificate on the external server. Required only for server-client authentication. Include only if SSL/TLS is used on the external server.
        :param pulumi.Input[str] database_version: The MySQL version running on your source database server.
               Possible values are: `MYSQL_5_6`, `MYSQL_5_7`, `MYSQL_8_0`, `POSTGRES_9_6`, `POSTGRES_10`, `POSTGRES_11`, `POSTGRES_12`, `POSTGRES_13`, `POSTGRES_14`.
        :param pulumi.Input[str] dump_file_path: A file in the bucket that contains the data from the external server.
        :param pulumi.Input[str] host: The IPv4 address and port for the external server, or the the DNS address for the external server. If the external server is hosted on Cloud SQL, the port is 5432.
               
               
               - - -
        :param pulumi.Input[str] name: The name of the source representation instance. Use any valid Cloud SQL instance name.
        :param pulumi.Input[str] password: The password for the replication user account.
               **Note**: This property is sensitive and will not be displayed in the plan.
        :param pulumi.Input[int] port: The externally accessible port for the source database server.
               Defaults to 3306.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] region: The Region in which the created instance should reside.
               If it is not provided, the provider region is used.
        :param pulumi.Input[str] username: The replication user account on the external server.
        """
        if ca_certificate is not None:
            pulumi.set(__self__, "ca_certificate", ca_certificate)
        if client_certificate is not None:
            pulumi.set(__self__, "client_certificate", client_certificate)
        if client_key is not None:
            pulumi.set(__self__, "client_key", client_key)
        if database_version is not None:
            pulumi.set(__self__, "database_version", database_version)
        if dump_file_path is not None:
            pulumi.set(__self__, "dump_file_path", dump_file_path)
        if host is not None:
            pulumi.set(__self__, "host", host)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if password is not None:
            pulumi.set(__self__, "password", password)
        if port is not None:
            pulumi.set(__self__, "port", port)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if region is not None:
            pulumi.set(__self__, "region", region)
        if username is not None:
            pulumi.set(__self__, "username", username)

    @property
    @pulumi.getter(name="caCertificate")
    def ca_certificate(self) -> Optional[pulumi.Input[str]]:
        """
        The CA certificate on the external server. Include only if SSL/TLS is used on the external server.
        """
        return pulumi.get(self, "ca_certificate")

    @ca_certificate.setter
    def ca_certificate(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ca_certificate", value)

    @property
    @pulumi.getter(name="clientCertificate")
    def client_certificate(self) -> Optional[pulumi.Input[str]]:
        """
        The client certificate on the external server. Required only for server-client authentication. Include only if SSL/TLS is used on the external server.
        """
        return pulumi.get(self, "client_certificate")

    @client_certificate.setter
    def client_certificate(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "client_certificate", value)

    @property
    @pulumi.getter(name="clientKey")
    def client_key(self) -> Optional[pulumi.Input[str]]:
        """
        The private key file for the client certificate on the external server. Required only for server-client authentication. Include only if SSL/TLS is used on the external server.
        """
        return pulumi.get(self, "client_key")

    @client_key.setter
    def client_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "client_key", value)

    @property
    @pulumi.getter(name="databaseVersion")
    def database_version(self) -> Optional[pulumi.Input[str]]:
        """
        The MySQL version running on your source database server.
        Possible values are: `MYSQL_5_6`, `MYSQL_5_7`, `MYSQL_8_0`, `POSTGRES_9_6`, `POSTGRES_10`, `POSTGRES_11`, `POSTGRES_12`, `POSTGRES_13`, `POSTGRES_14`.
        """
        return pulumi.get(self, "database_version")

    @database_version.setter
    def database_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "database_version", value)

    @property
    @pulumi.getter(name="dumpFilePath")
    def dump_file_path(self) -> Optional[pulumi.Input[str]]:
        """
        A file in the bucket that contains the data from the external server.
        """
        return pulumi.get(self, "dump_file_path")

    @dump_file_path.setter
    def dump_file_path(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "dump_file_path", value)

    @property
    @pulumi.getter
    def host(self) -> Optional[pulumi.Input[str]]:
        """
        The IPv4 address and port for the external server, or the the DNS address for the external server. If the external server is hosted on Cloud SQL, the port is 5432.


        - - -
        """
        return pulumi.get(self, "host")

    @host.setter
    def host(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "host", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the source representation instance. Use any valid Cloud SQL instance name.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def password(self) -> Optional[pulumi.Input[str]]:
        """
        The password for the replication user account.
        **Note**: This property is sensitive and will not be displayed in the plan.
        """
        return pulumi.get(self, "password")

    @password.setter
    def password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "password", value)

    @property
    @pulumi.getter
    def port(self) -> Optional[pulumi.Input[int]]:
        """
        The externally accessible port for the source database server.
        Defaults to 3306.
        """
        return pulumi.get(self, "port")

    @port.setter
    def port(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "port", value)

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
    def region(self) -> Optional[pulumi.Input[str]]:
        """
        The Region in which the created instance should reside.
        If it is not provided, the provider region is used.
        """
        return pulumi.get(self, "region")

    @region.setter
    def region(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "region", value)

    @property
    @pulumi.getter
    def username(self) -> Optional[pulumi.Input[str]]:
        """
        The replication user account on the external server.
        """
        return pulumi.get(self, "username")

    @username.setter
    def username(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "username", value)


class SourceRepresentationInstance(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 ca_certificate: Optional[pulumi.Input[str]] = None,
                 client_certificate: Optional[pulumi.Input[str]] = None,
                 client_key: Optional[pulumi.Input[str]] = None,
                 database_version: Optional[pulumi.Input[str]] = None,
                 dump_file_path: Optional[pulumi.Input[str]] = None,
                 host: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 port: Optional[pulumi.Input[int]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 username: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        A source representation instance is a Cloud SQL instance that represents
        the source database server to the Cloud SQL replica. It is visible in the
        Cloud Console and appears the same as a regular Cloud SQL instance, but it
        contains no data, requires no configuration or maintenance, and does not
        affect billing. You cannot update the source representation instance.

        ## Example Usage

        ### Sql Source Representation Instance Basic

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        instance = gcp.sql.SourceRepresentationInstance("instance",
            name="my-instance",
            region="us-central1",
            database_version="MYSQL_8_0",
            host="10.20.30.40",
            port=3306,
            username="some-user",
            password="password-for-the-user",
            dump_file_path="gs://replica-bucket/source-database.sql.gz")
        ```
        <!--End PulumiCodeChooser -->
        ### Sql Source Representation Instance Postgres

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        instance = gcp.sql.SourceRepresentationInstance("instance",
            name="my-instance",
            region="us-central1",
            database_version="POSTGRES_9_6",
            host="10.20.30.40",
            port=3306,
            username="some-user",
            password="password-for-the-user",
            dump_file_path="gs://replica-bucket/source-database.sql.gz")
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        SourceRepresentationInstance can be imported using any of these accepted formats:

        * `projects/{{project}}/instances/{{name}}`

        * `{{project}}/{{name}}`

        * `{{name}}`

        When using the `pulumi import` command, SourceRepresentationInstance can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:sql/sourceRepresentationInstance:SourceRepresentationInstance default projects/{{project}}/instances/{{name}}
        ```

        ```sh
        $ pulumi import gcp:sql/sourceRepresentationInstance:SourceRepresentationInstance default {{project}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:sql/sourceRepresentationInstance:SourceRepresentationInstance default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] ca_certificate: The CA certificate on the external server. Include only if SSL/TLS is used on the external server.
        :param pulumi.Input[str] client_certificate: The client certificate on the external server. Required only for server-client authentication. Include only if SSL/TLS is used on the external server.
        :param pulumi.Input[str] client_key: The private key file for the client certificate on the external server. Required only for server-client authentication. Include only if SSL/TLS is used on the external server.
        :param pulumi.Input[str] database_version: The MySQL version running on your source database server.
               Possible values are: `MYSQL_5_6`, `MYSQL_5_7`, `MYSQL_8_0`, `POSTGRES_9_6`, `POSTGRES_10`, `POSTGRES_11`, `POSTGRES_12`, `POSTGRES_13`, `POSTGRES_14`.
        :param pulumi.Input[str] dump_file_path: A file in the bucket that contains the data from the external server.
        :param pulumi.Input[str] host: The IPv4 address and port for the external server, or the the DNS address for the external server. If the external server is hosted on Cloud SQL, the port is 5432.
               
               
               - - -
        :param pulumi.Input[str] name: The name of the source representation instance. Use any valid Cloud SQL instance name.
        :param pulumi.Input[str] password: The password for the replication user account.
               **Note**: This property is sensitive and will not be displayed in the plan.
        :param pulumi.Input[int] port: The externally accessible port for the source database server.
               Defaults to 3306.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] region: The Region in which the created instance should reside.
               If it is not provided, the provider region is used.
        :param pulumi.Input[str] username: The replication user account on the external server.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SourceRepresentationInstanceArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        A source representation instance is a Cloud SQL instance that represents
        the source database server to the Cloud SQL replica. It is visible in the
        Cloud Console and appears the same as a regular Cloud SQL instance, but it
        contains no data, requires no configuration or maintenance, and does not
        affect billing. You cannot update the source representation instance.

        ## Example Usage

        ### Sql Source Representation Instance Basic

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        instance = gcp.sql.SourceRepresentationInstance("instance",
            name="my-instance",
            region="us-central1",
            database_version="MYSQL_8_0",
            host="10.20.30.40",
            port=3306,
            username="some-user",
            password="password-for-the-user",
            dump_file_path="gs://replica-bucket/source-database.sql.gz")
        ```
        <!--End PulumiCodeChooser -->
        ### Sql Source Representation Instance Postgres

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_gcp as gcp

        instance = gcp.sql.SourceRepresentationInstance("instance",
            name="my-instance",
            region="us-central1",
            database_version="POSTGRES_9_6",
            host="10.20.30.40",
            port=3306,
            username="some-user",
            password="password-for-the-user",
            dump_file_path="gs://replica-bucket/source-database.sql.gz")
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        SourceRepresentationInstance can be imported using any of these accepted formats:

        * `projects/{{project}}/instances/{{name}}`

        * `{{project}}/{{name}}`

        * `{{name}}`

        When using the `pulumi import` command, SourceRepresentationInstance can be imported using one of the formats above. For example:

        ```sh
        $ pulumi import gcp:sql/sourceRepresentationInstance:SourceRepresentationInstance default projects/{{project}}/instances/{{name}}
        ```

        ```sh
        $ pulumi import gcp:sql/sourceRepresentationInstance:SourceRepresentationInstance default {{project}}/{{name}}
        ```

        ```sh
        $ pulumi import gcp:sql/sourceRepresentationInstance:SourceRepresentationInstance default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param SourceRepresentationInstanceArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SourceRepresentationInstanceArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 ca_certificate: Optional[pulumi.Input[str]] = None,
                 client_certificate: Optional[pulumi.Input[str]] = None,
                 client_key: Optional[pulumi.Input[str]] = None,
                 database_version: Optional[pulumi.Input[str]] = None,
                 dump_file_path: Optional[pulumi.Input[str]] = None,
                 host: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 port: Optional[pulumi.Input[int]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 username: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = SourceRepresentationInstanceArgs.__new__(SourceRepresentationInstanceArgs)

            __props__.__dict__["ca_certificate"] = ca_certificate
            __props__.__dict__["client_certificate"] = client_certificate
            __props__.__dict__["client_key"] = client_key
            if database_version is None and not opts.urn:
                raise TypeError("Missing required property 'database_version'")
            __props__.__dict__["database_version"] = database_version
            __props__.__dict__["dump_file_path"] = dump_file_path
            if host is None and not opts.urn:
                raise TypeError("Missing required property 'host'")
            __props__.__dict__["host"] = host
            __props__.__dict__["name"] = name
            __props__.__dict__["password"] = None if password is None else pulumi.Output.secret(password)
            __props__.__dict__["port"] = port
            __props__.__dict__["project"] = project
            __props__.__dict__["region"] = region
            __props__.__dict__["username"] = username
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["password"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(SourceRepresentationInstance, __self__).__init__(
            'gcp:sql/sourceRepresentationInstance:SourceRepresentationInstance',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            ca_certificate: Optional[pulumi.Input[str]] = None,
            client_certificate: Optional[pulumi.Input[str]] = None,
            client_key: Optional[pulumi.Input[str]] = None,
            database_version: Optional[pulumi.Input[str]] = None,
            dump_file_path: Optional[pulumi.Input[str]] = None,
            host: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            password: Optional[pulumi.Input[str]] = None,
            port: Optional[pulumi.Input[int]] = None,
            project: Optional[pulumi.Input[str]] = None,
            region: Optional[pulumi.Input[str]] = None,
            username: Optional[pulumi.Input[str]] = None) -> 'SourceRepresentationInstance':
        """
        Get an existing SourceRepresentationInstance resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] ca_certificate: The CA certificate on the external server. Include only if SSL/TLS is used on the external server.
        :param pulumi.Input[str] client_certificate: The client certificate on the external server. Required only for server-client authentication. Include only if SSL/TLS is used on the external server.
        :param pulumi.Input[str] client_key: The private key file for the client certificate on the external server. Required only for server-client authentication. Include only if SSL/TLS is used on the external server.
        :param pulumi.Input[str] database_version: The MySQL version running on your source database server.
               Possible values are: `MYSQL_5_6`, `MYSQL_5_7`, `MYSQL_8_0`, `POSTGRES_9_6`, `POSTGRES_10`, `POSTGRES_11`, `POSTGRES_12`, `POSTGRES_13`, `POSTGRES_14`.
        :param pulumi.Input[str] dump_file_path: A file in the bucket that contains the data from the external server.
        :param pulumi.Input[str] host: The IPv4 address and port for the external server, or the the DNS address for the external server. If the external server is hosted on Cloud SQL, the port is 5432.
               
               
               - - -
        :param pulumi.Input[str] name: The name of the source representation instance. Use any valid Cloud SQL instance name.
        :param pulumi.Input[str] password: The password for the replication user account.
               **Note**: This property is sensitive and will not be displayed in the plan.
        :param pulumi.Input[int] port: The externally accessible port for the source database server.
               Defaults to 3306.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] region: The Region in which the created instance should reside.
               If it is not provided, the provider region is used.
        :param pulumi.Input[str] username: The replication user account on the external server.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _SourceRepresentationInstanceState.__new__(_SourceRepresentationInstanceState)

        __props__.__dict__["ca_certificate"] = ca_certificate
        __props__.__dict__["client_certificate"] = client_certificate
        __props__.__dict__["client_key"] = client_key
        __props__.__dict__["database_version"] = database_version
        __props__.__dict__["dump_file_path"] = dump_file_path
        __props__.__dict__["host"] = host
        __props__.__dict__["name"] = name
        __props__.__dict__["password"] = password
        __props__.__dict__["port"] = port
        __props__.__dict__["project"] = project
        __props__.__dict__["region"] = region
        __props__.__dict__["username"] = username
        return SourceRepresentationInstance(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="caCertificate")
    def ca_certificate(self) -> pulumi.Output[Optional[str]]:
        """
        The CA certificate on the external server. Include only if SSL/TLS is used on the external server.
        """
        return pulumi.get(self, "ca_certificate")

    @property
    @pulumi.getter(name="clientCertificate")
    def client_certificate(self) -> pulumi.Output[Optional[str]]:
        """
        The client certificate on the external server. Required only for server-client authentication. Include only if SSL/TLS is used on the external server.
        """
        return pulumi.get(self, "client_certificate")

    @property
    @pulumi.getter(name="clientKey")
    def client_key(self) -> pulumi.Output[Optional[str]]:
        """
        The private key file for the client certificate on the external server. Required only for server-client authentication. Include only if SSL/TLS is used on the external server.
        """
        return pulumi.get(self, "client_key")

    @property
    @pulumi.getter(name="databaseVersion")
    def database_version(self) -> pulumi.Output[str]:
        """
        The MySQL version running on your source database server.
        Possible values are: `MYSQL_5_6`, `MYSQL_5_7`, `MYSQL_8_0`, `POSTGRES_9_6`, `POSTGRES_10`, `POSTGRES_11`, `POSTGRES_12`, `POSTGRES_13`, `POSTGRES_14`.
        """
        return pulumi.get(self, "database_version")

    @property
    @pulumi.getter(name="dumpFilePath")
    def dump_file_path(self) -> pulumi.Output[Optional[str]]:
        """
        A file in the bucket that contains the data from the external server.
        """
        return pulumi.get(self, "dump_file_path")

    @property
    @pulumi.getter
    def host(self) -> pulumi.Output[str]:
        """
        The IPv4 address and port for the external server, or the the DNS address for the external server. If the external server is hosted on Cloud SQL, the port is 5432.


        - - -
        """
        return pulumi.get(self, "host")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the source representation instance. Use any valid Cloud SQL instance name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def password(self) -> pulumi.Output[Optional[str]]:
        """
        The password for the replication user account.
        **Note**: This property is sensitive and will not be displayed in the plan.
        """
        return pulumi.get(self, "password")

    @property
    @pulumi.getter
    def port(self) -> pulumi.Output[Optional[int]]:
        """
        The externally accessible port for the source database server.
        Defaults to 3306.
        """
        return pulumi.get(self, "port")

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
    def region(self) -> pulumi.Output[str]:
        """
        The Region in which the created instance should reside.
        If it is not provided, the provider region is used.
        """
        return pulumi.get(self, "region")

    @property
    @pulumi.getter
    def username(self) -> pulumi.Output[Optional[str]]:
        """
        The replication user account on the external server.
        """
        return pulumi.get(self, "username")


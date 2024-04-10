# coding=utf-8
# *** WARNING: this file was generated by pulumi-language-python. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._enums import *
from ._inputs import *
from .file import File
import pulumi_command

__all__ = ['SystemdServiceArgs', 'SystemdService']

@pulumi.input_type
class SystemdServiceArgs:
    def __init__(__self__, *,
                 connection: pulumi.Input['pulumi_command.remote.ConnectionArgs'],
                 service: pulumi.Input['SystemdServiceSectionArgs'],
                 directory: Optional[pulumi.Input[str]] = None,
                 install: Optional[pulumi.Input['SystemdInstallSectionArgs']] = None,
                 unit: Optional[pulumi.Input['SystemdUnitSectionArgs']] = None):
        """
        The set of arguments for constructing a SystemdService resource.
        :param pulumi.Input['pulumi_command.remote.ConnectionArgs'] connection: The parameters with which to connect to the remote host.
        :param pulumi.Input['SystemdServiceSectionArgs'] service: Describes the [Service] section of a systemd service file.
        :param pulumi.Input[str] directory: The location to create the service file.
        :param pulumi.Input['SystemdInstallSectionArgs'] install: Describes the [Install] section of a systemd service file.
        :param pulumi.Input['SystemdUnitSectionArgs'] unit: Describes the [Unit] section of a systemd service file.
        """
        pulumi.set(__self__, "connection", connection)
        pulumi.set(__self__, "service", service)
        if directory is None:
            directory = '/etc/systemd/system'
        if directory is not None:
            pulumi.set(__self__, "directory", directory)
        if install is not None:
            pulumi.set(__self__, "install", install)
        if unit is not None:
            pulumi.set(__self__, "unit", unit)

    @property
    @pulumi.getter
    def connection(self) -> pulumi.Input['pulumi_command.remote.ConnectionArgs']:
        """
        The parameters with which to connect to the remote host.
        """
        return pulumi.get(self, "connection")

    @connection.setter
    def connection(self, value: pulumi.Input['pulumi_command.remote.ConnectionArgs']):
        pulumi.set(self, "connection", value)

    @property
    @pulumi.getter
    def service(self) -> pulumi.Input['SystemdServiceSectionArgs']:
        """
        Describes the [Service] section of a systemd service file.
        """
        return pulumi.get(self, "service")

    @service.setter
    def service(self, value: pulumi.Input['SystemdServiceSectionArgs']):
        pulumi.set(self, "service", value)

    @property
    @pulumi.getter
    def directory(self) -> Optional[pulumi.Input[str]]:
        """
        The location to create the service file.
        """
        return pulumi.get(self, "directory")

    @directory.setter
    def directory(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "directory", value)

    @property
    @pulumi.getter
    def install(self) -> Optional[pulumi.Input['SystemdInstallSectionArgs']]:
        """
        Describes the [Install] section of a systemd service file.
        """
        return pulumi.get(self, "install")

    @install.setter
    def install(self, value: Optional[pulumi.Input['SystemdInstallSectionArgs']]):
        pulumi.set(self, "install", value)

    @property
    @pulumi.getter
    def unit(self) -> Optional[pulumi.Input['SystemdUnitSectionArgs']]:
        """
        Describes the [Unit] section of a systemd service file.
        """
        return pulumi.get(self, "unit")

    @unit.setter
    def unit(self, value: Optional[pulumi.Input['SystemdUnitSectionArgs']]):
        pulumi.set(self, "unit", value)


class SystemdService(pulumi.ComponentResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 connection: Optional[pulumi.Input[pulumi.InputType['pulumi_command.remote.ConnectionArgs']]] = None,
                 directory: Optional[pulumi.Input[str]] = None,
                 install: Optional[pulumi.Input[pulumi.InputType['SystemdInstallSectionArgs']]] = None,
                 service: Optional[pulumi.Input[pulumi.InputType['SystemdServiceSectionArgs']]] = None,
                 unit: Optional[pulumi.Input[pulumi.InputType['SystemdUnitSectionArgs']]] = None,
                 __props__=None):
        """
        A systemd service on a remote system.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['pulumi_command.remote.ConnectionArgs']] connection: The parameters with which to connect to the remote host.
        :param pulumi.Input[str] directory: The location to create the service file.
        :param pulumi.Input[pulumi.InputType['SystemdInstallSectionArgs']] install: Describes the [Install] section of a systemd service file.
        :param pulumi.Input[pulumi.InputType['SystemdServiceSectionArgs']] service: Describes the [Service] section of a systemd service file.
        :param pulumi.Input[pulumi.InputType['SystemdUnitSectionArgs']] unit: Describes the [Unit] section of a systemd service file.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SystemdServiceArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        A systemd service on a remote system.

        :param str resource_name: The name of the resource.
        :param SystemdServiceArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SystemdServiceArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 connection: Optional[pulumi.Input[pulumi.InputType['pulumi_command.remote.ConnectionArgs']]] = None,
                 directory: Optional[pulumi.Input[str]] = None,
                 install: Optional[pulumi.Input[pulumi.InputType['SystemdInstallSectionArgs']]] = None,
                 service: Optional[pulumi.Input[pulumi.InputType['SystemdServiceSectionArgs']]] = None,
                 unit: Optional[pulumi.Input[pulumi.InputType['SystemdUnitSectionArgs']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is not None:
            raise ValueError('ComponentResource classes do not support opts.id')
        else:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = SystemdServiceArgs.__new__(SystemdServiceArgs)

            if connection is None and not opts.urn:
                raise TypeError("Missing required property 'connection'")
            __props__.__dict__["connection"] = connection
            if directory is None:
                directory = '/etc/systemd/system'
            __props__.__dict__["directory"] = directory
            __props__.__dict__["install"] = install
            if service is None and not opts.urn:
                raise TypeError("Missing required property 'service'")
            __props__.__dict__["service"] = service
            __props__.__dict__["unit"] = unit
            __props__.__dict__["file"] = None
        super(SystemdService, __self__).__init__(
            'kubernetes-the-hard-way:remote:SystemdService',
            resource_name,
            __props__,
            opts,
            remote=True)

    @property
    @pulumi.getter
    def connection(self) -> pulumi.Output['pulumi_command.remote.outputs.Connection']:
        """
        The parameters with which to connect to the remote host.
        """
        return pulumi.get(self, "connection")

    @property
    @pulumi.getter
    def directory(self) -> pulumi.Output[str]:
        """
        The location to create the service file.
        """
        return pulumi.get(self, "directory")

    @property
    @pulumi.getter
    def file(self) -> pulumi.Output['File']:
        """
        The service file on the remote machine.
        """
        return pulumi.get(self, "file")

    @property
    @pulumi.getter
    def install(self) -> pulumi.Output[Optional['outputs.SystemdInstallSection']]:
        """
        Describes the [Install] section of a systemd service file.
        """
        return pulumi.get(self, "install")

    @property
    @pulumi.getter
    def service(self) -> pulumi.Output['outputs.SystemdServiceSection']:
        """
        Describes the [Service] section of a systemd service file.
        """
        return pulumi.get(self, "service")

    @property
    @pulumi.getter
    def unit(self) -> pulumi.Output[Optional['outputs.SystemdUnitSection']]:
        """
        Describes the [Unit] section of a systemd service file.
        """
        return pulumi.get(self, "unit")


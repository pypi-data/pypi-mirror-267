# coding=utf-8
# *** WARNING: this file was generated by pulumi-language-python. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from .. import tools as _tools
from ._enums import *
from .download import Download
import pulumi_command

__all__ = ['KubeletInstallArgs', 'KubeletInstall']

@pulumi.input_type
class KubeletInstallArgs:
    def __init__(__self__, *,
                 connection: pulumi.Input['pulumi_command.remote.ConnectionArgs'],
                 architecture: Optional[pulumi.Input['Architecture']] = None,
                 directory: Optional[pulumi.Input[str]] = None,
                 version: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a KubeletInstall resource.
        :param pulumi.Input['pulumi_command.remote.ConnectionArgs'] connection: The parameters with which to connect to the remote host.
        :param pulumi.Input['Architecture'] architecture: The CPU architecture to install.
        :param pulumi.Input[str] directory: The directory to install the binary to.
        :param pulumi.Input[str] version: The version to install.
        """
        pulumi.set(__self__, "connection", connection)
        if architecture is not None:
            pulumi.set(__self__, "architecture", architecture)
        if directory is None:
            directory = '/usr/local/bin'
        if directory is not None:
            pulumi.set(__self__, "directory", directory)
        if version is not None:
            pulumi.set(__self__, "version", version)

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
    def architecture(self) -> Optional[pulumi.Input['Architecture']]:
        """
        The CPU architecture to install.
        """
        return pulumi.get(self, "architecture")

    @architecture.setter
    def architecture(self, value: Optional[pulumi.Input['Architecture']]):
        pulumi.set(self, "architecture", value)

    @property
    @pulumi.getter
    def directory(self) -> Optional[pulumi.Input[str]]:
        """
        The directory to install the binary to.
        """
        return pulumi.get(self, "directory")

    @directory.setter
    def directory(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "directory", value)

    @property
    @pulumi.getter
    def version(self) -> Optional[pulumi.Input[str]]:
        """
        The version to install.
        """
        return pulumi.get(self, "version")

    @version.setter
    def version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "version", value)


class KubeletInstall(pulumi.ComponentResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 architecture: Optional[pulumi.Input['Architecture']] = None,
                 connection: Optional[pulumi.Input[pulumi.InputType['pulumi_command.remote.ConnectionArgs']]] = None,
                 directory: Optional[pulumi.Input[str]] = None,
                 version: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Installs kubelet on a remote system.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input['Architecture'] architecture: The CPU architecture to install.
        :param pulumi.Input[pulumi.InputType['pulumi_command.remote.ConnectionArgs']] connection: The parameters with which to connect to the remote host.
        :param pulumi.Input[str] directory: The directory to install the binary to.
        :param pulumi.Input[str] version: The version to install.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: KubeletInstallArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Installs kubelet on a remote system.

        :param str resource_name: The name of the resource.
        :param KubeletInstallArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(KubeletInstallArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 architecture: Optional[pulumi.Input['Architecture']] = None,
                 connection: Optional[pulumi.Input[pulumi.InputType['pulumi_command.remote.ConnectionArgs']]] = None,
                 directory: Optional[pulumi.Input[str]] = None,
                 version: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is not None:
            raise ValueError('ComponentResource classes do not support opts.id')
        else:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = KubeletInstallArgs.__new__(KubeletInstallArgs)

            __props__.__dict__["architecture"] = architecture
            if connection is None and not opts.urn:
                raise TypeError("Missing required property 'connection'")
            __props__.__dict__["connection"] = connection
            if directory is None:
                directory = '/usr/local/bin'
            __props__.__dict__["directory"] = directory
            __props__.__dict__["version"] = version
            __props__.__dict__["bin_name"] = None
            __props__.__dict__["download"] = None
            __props__.__dict__["mkdir"] = None
            __props__.__dict__["mktemp"] = None
            __props__.__dict__["mv"] = None
            __props__.__dict__["path"] = None
            __props__.__dict__["rm"] = None
            __props__.__dict__["url"] = None
        super(KubeletInstall, __self__).__init__(
            'kubernetes-the-hard-way:remote:KubeletInstall',
            resource_name,
            __props__,
            opts,
            remote=True)

    @property
    @pulumi.getter
    def architecture(self) -> pulumi.Output['Architecture']:
        """
        The CPU architecture to install.
        """
        return pulumi.get(self, "architecture")

    @property
    @pulumi.getter(name="binName")
    def bin_name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the installed binary.
        """
        return pulumi.get(self, "bin_name")

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
        The directory to install the binary to.
        """
        return pulumi.get(self, "directory")

    @property
    @pulumi.getter
    def download(self) -> pulumi.Output['Download']:
        """
        The download operation.
        """
        return pulumi.get(self, "download")

    @property
    @pulumi.getter
    def mkdir(self) -> pulumi.Output['_tools.Mkdir']:
        """
        The mkdir operation.
        """
        return pulumi.get(self, "mkdir")

    @property
    @pulumi.getter
    def mktemp(self) -> pulumi.Output['_tools.Mktemp']:
        """
        The mktemp operation.
        """
        return pulumi.get(self, "mktemp")

    @property
    @pulumi.getter
    def mv(self) -> pulumi.Output['_tools.Mv']:
        """
        The mv operation.
        """
        return pulumi.get(self, "mv")

    @property
    @pulumi.getter
    def path(self) -> pulumi.Output[str]:
        """
        The path to the installed binary.
        """
        return pulumi.get(self, "path")

    @property
    @pulumi.getter
    def rm(self) -> pulumi.Output['_tools.Rm']:
        """
        The rm operation.
        """
        return pulumi.get(self, "rm")

    @property
    @pulumi.getter
    def url(self) -> pulumi.Output[str]:
        """
        The url used to download the binary.
        """
        return pulumi.get(self, "url")

    @property
    @pulumi.getter
    def version(self) -> pulumi.Output[str]:
        """
        The version to install.
        """
        return pulumi.get(self, "version")


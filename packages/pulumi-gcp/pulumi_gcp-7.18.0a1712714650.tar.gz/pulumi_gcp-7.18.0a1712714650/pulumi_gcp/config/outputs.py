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
    'Batching',
]

@pulumi.output_type
class Batching(dict):
    def __init__(__self__, *,
                 enable_batching: Optional[bool] = None,
                 send_after: Optional[str] = None):
        if enable_batching is not None:
            pulumi.set(__self__, "enable_batching", enable_batching)
        if send_after is not None:
            pulumi.set(__self__, "send_after", send_after)

    @property
    @pulumi.getter(name="enableBatching")
    def enable_batching(self) -> Optional[bool]:
        return pulumi.get(self, "enable_batching")

    @property
    @pulumi.getter(name="sendAfter")
    def send_after(self) -> Optional[str]:
        return pulumi.get(self, "send_after")



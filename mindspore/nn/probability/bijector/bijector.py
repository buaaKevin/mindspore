# Copyright 2020 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""Bijector"""
from mindspore.nn.cell import Cell
from ..distribution import Distribution
from ..distribution import TransformedDistribution

class Bijector(Cell):
    """
    Bijecotr class.

    Args:
        is_constant_jacobian (bool): if the bijector has constant derivative. Default: False.
        is_injective (bool): if the bijector is an one-to-one mapping. Default: True.
        name (str): name of the bijector. Default: None.
        dtype (mstype): type of the distribution the bijector can operate on. Default: None.
        param (dict): parameters used to initialize the bijector. Default: None.
    """
    def __init__(self,
                 is_constant_jacobian=False,
                 is_injective=True,
                 name=None,
                 dtype=None,
                 param=None):

        """
        Constructor of bijector class.
        """
        super(Bijector, self).__init__()
        self._name = name
        self._dtype = dtype
        self._parameters = {}
        # parsing parameters
        for k in param.keys():
            if not(k == 'self' or k.startswith('_')):
                self._parameters[k] = param[k]
        self._is_constant_jacobian = is_constant_jacobian
        self._is_injective = is_injective

    @property
    def name(self):
        return self._name

    @property
    def dtype(self):
        return self._dtype

    @property
    def parameters(self):
        return self._parameters

    @property
    def is_constant_jacobian(self):
        return self._is_constant_jacobian

    @property
    def is_injective(self):
        return self._is_injective

    def forward(self, *args):
        """
        Forward transformation: transform the input value to another distribution.
        """
        return self._forward(*args)

    def inverse(self, *args):
        """
        Inverse transformation: transform the input value back to the original distribution.
        """
        return self._inverse(*args)

    def forward_log_jacobian(self, *args):
        """
        Logarithm of the derivative of forward transformation.
        """
        return self._forward_log_jacobian(*args)

    def inverse_log_jacobian(self, *args):
        """
        Logarithm of the derivative of forward transformation.
        """
        return self._inverse_log_jacobian(*args)

    def __call__(self, *args):
        """
        Call Bijector directly.
        This __call__ may go into two directions:
        If args[0] is a distribution instance, the call will generate a new distribution derived from
        the input distribution.
        Otherwise, input[0] should be the name of a bijector function, e.g. "forward", then this call will
        go in the construct and invoke the correstpoding bijector function.

        Args:
            *args: args[0] shall be either a distribution or the name of a bijector function.
        """
        if isinstance(args[0], Distribution):
            return TransformedDistribution(self, args[0])
        return super(Bijector, self).__call__(*args)

    def construct(self, name, *args):
        """
        Override construct in Cell.

        Args:
            *inputs: inputs[0] is always the name of a function.

        Notes:
            Always raise RuntimeError as Distribution should not be called directly.
        """
        if name == 'forward':
            return self.forward(*args)
        if name == 'inverse':
            return self.inverse(*args)
        if name == 'forward_log_jacobian':
            return self.forward_log_jacobian(*args)
        if name == 'inverse_log_jacobian':
            return self.inverse_log_jacobian(*args)
        return None

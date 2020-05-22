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
""" test_tensor_slice """
import numpy as np
import pytest

from mindspore import Tensor, Parameter
from mindspore import context
from mindspore import dtype as mstype
from mindspore.nn import Cell
from ....mindspore_test_framework.mindspore_test import mindspore_test
from ....mindspore_test_framework.pipeline.forward.compile_forward \
    import pipeline_for_compile_forward_ge_graph_for_case_by_case_config, \
    pipeline_for_compile_forward_ge_graph_for_case_by_case_config_exception


class NetWorkSlicePositive(Cell):
    def __init__(self):
        super(NetWorkSlicePositive, self).__init__()
        self.tensor_ret0 = Tensor(np.ones([1, 2, 2], np.int32))
        self.tensor_ret1 = Tensor(np.ones([4, 7, 4], np.int32))
        self.tensor_ret2 = Tensor(np.ones([6, 8, 10], np.int32))
        self.tensor_ret3 = Tensor(np.ones([3, 8, 10], np.int32))

    def construct(self, tensor):
        ret0 = tensor[3:4:3, 1:5:2, 3:6:2] + self.tensor_ret0
        ret1 = tensor[-6:4:1, 7:-8:-1, ::3] + self.tensor_ret1
        ret2 = tensor[::, ::, ::] + self.tensor_ret2
        ret3 = tensor[::2] + self.tensor_ret3
        return ret0, ret1, ret2, ret3


class NetWorkSliceEllipsis(Cell):
    def __init__(self):
        super(NetWorkSliceEllipsis, self).__init__()
        self.tensor_ret0 = Tensor(np.ones([2, 7, 8], np.int32))
        self.tensor_ret1 = Tensor(np.ones([6, 7, 8, 9], np.int32))
        self.tensor_ret2 = Tensor(np.ones([1, 6, 7, 8, 9], np.int32))

    def construct(self, tensor):
        ret0 = tensor[0:4:2, ..., 1] + self.tensor_ret0
        ret1 = tensor[...] + self.tensor_ret1
        ret2 = tensor[None] + self.tensor_ret2
        ret3 = tensor[True] + self.tensor_ret2
        return ret0, ret1, ret2, ret3


class NetWorkReduceDimension(Cell):
    def __init__(self):
        super(NetWorkReduceDimension, self).__init__()
        self.tensor_ret0 = Tensor(np.ones([2, 4, 1], np.int32))
        self.tensor_ret1 = Tensor(np.ones([3, 4], np.int32))
        self.tensor_ret2 = Tensor(np.ones([6, 8], np.int32))
        self.tensor_ret3 = Tensor(np.array(8, np.int32))
        self.tensor_ret4 = Tensor(np.ones([8, 10], np.int32))

    def construct(self, tensor):
        ret0 = tensor[0:6:3, 1:5:1, 3:5:2] + self.tensor_ret0
        ret1 = tensor[::2, 1, ::3] + self.tensor_ret1
        ret2 = tensor[::, ::, 0] + self.tensor_ret2
        ret3 = tensor[3, 2, 5] + self.tensor_ret3
        ret4 = tensor[1] + self.tensor_ret4
        return ret0, ret1, ret2, ret3, ret4


class NetWorkStepNegative(Cell):
    def __init__(self):
        super(NetWorkStepNegative, self).__init__()
        self.tensor_ret = Tensor(np.ones([6, 5, 10], np.int32))

    def construct(self, tensor):
        ret = tensor[::1, -5::, ::-1] + self.tensor_ret
        return ret


class NetWorkReduceToScalar(Cell):
    def __init__(self):
        super(NetWorkReduceToScalar, self).__init__()
        self.tensor_ret = Tensor(np.array(9, np.int32))

    def construct(self, tensor):
        ret = tensor[2, 3, 4] + self.tensor_ret
        return ret


class TensorAssignWithSliceError1(Cell):
    def __init__(self):
        super(TensorAssignWithSliceError1, self).__init__()

    def construct(self, a, b):
        a[1:3:-1, ::] = b
        return a


class TensorAssignWithSliceError2(Cell):
    def __init__(self):
        super(TensorAssignWithSliceError2, self).__init__()

    def construct(self, a, b):
        a[1:3:-1] = b
        return a


class TensorAssignWithSlice2(Cell):
    def __init__(self):
        super(TensorAssignWithSlice2, self).__init__()

    def construct(self, a, b, ck):
        a[1:5] = b
        a[3:4] = 5
        a[-1:1:-1] = b
        a[-1:3:-1] = 5
        a[::] = b
        a[::] = 9
        z = a + ck
        return z


class TensorAssignWithSlice(Cell):
    def __init__(self):
        super(TensorAssignWithSlice, self).__init__()
        self.c = 2

    def construct(self, a, b, ck):
        a[1:3, ::] = b
        a[2:3:, 3:] = b
        a[::] = b
        a[::] = self.c
        a[::, ::] = b
        a[::, ::] = self.c
        a[2:3:, 0:, 4:1:-1] = b
        a[2:3:, 0:, 4:1:-1] = self.c
        z = a + ck
        return z


class TensorIndexByOneTensor(Cell):
    def __init__(self):
        super(TensorIndexByOneTensor, self).__init__()
        self.const = Tensor(np.ones((5, 4, 7, 8)), mstype.int32)

    def construct(self, x, index):
        ret = x[index] + self.const
        return ret


class TensorIndexByTwoTensors(Cell):
    def __init__(self):
        super(TensorIndexByTwoTensors, self).__init__()
        self.const = Tensor(np.ones((3, 4, 5, 8)), mstype.int32)

    def construct(self, x, index_0, index_1):
        ret = x[index_0, index_1] + self.const
        return ret


class TensorIndexByThreeTensors(Cell):
    def __init__(self):
        super(TensorIndexByThreeTensors, self).__init__()
        self.const = Tensor(np.ones((5, 3, 4, 5)), mstype.int32)

    def construct(self, x, index_0, index_1, index_2):
        ret = x[index_0, index_1, index_2] + self.const
        return ret


class TensorSetItemByOneTensorWithNumber(Cell):
    def __init__(self, value):
        super(TensorSetItemByOneTensorWithNumber, self).__init__()
        self.const = Tensor(np.ones((6, 7, 8)), mstype.float32)
        self.param = Parameter(Tensor(np.arange(6*7*8).reshape((6, 7, 8)), mstype.float32), name="x")
        self.value = value

    def construct(self, index):
        self.param[index] = self.value
        ret = self.param + self.const
        return ret


class TensorSetItemByOneTensorWithTensor(Cell):
    def __init__(self):
        super(TensorSetItemByOneTensorWithTensor, self).__init__()
        self.const = Tensor(np.ones((6, 7, 8)), mstype.float32)
        self.param = Parameter(Tensor(np.arange(6*7*8).reshape((6, 7, 8)), mstype.float32), name="x")

    def construct(self, index, value):
        self.param[index] = value
        ret = self.param + self.const
        return ret


class TensorSetItemByOneTensorWithTupleOfNumber(Cell):
    def __init__(self, value):
        super(TensorSetItemByOneTensorWithTupleOfNumber, self).__init__()
        self.const = Tensor(np.ones((6, 7, 8)), mstype.float32)
        self.param = Parameter(Tensor(np.arange(6*7*8).reshape((6, 7, 8)), mstype.float32), name="x")
        self.value = value

    def construct(self, index):
        self.param[index] = self.value
        ret = self.param + self.const
        return ret


class TensorSetItemByOneTensorWithTupleOfTensor(Cell):
    def __init__(self):
        super(TensorSetItemByOneTensorWithTupleOfTensor, self).__init__()
        self.const = Tensor(np.ones((6, 3, 8)), mstype.float32)
        self.param = Parameter(Tensor(np.arange(6*3*8).reshape((6, 3, 8)), mstype.float32), name="x")

    def construct(self, index, value_0, value_1, value_2):
        self.param[index] = (value_0, value_1, value_2)
        ret = self.param + self.const
        return ret


class TensorSetItemByTensorsWithNumber(Cell):
    def __init__(self, value):
        super(TensorSetItemByTensorsWithNumber, self).__init__()
        self.const = Tensor(np.ones((6, 7, 8)), mstype.float32)
        self.param = Parameter(Tensor(np.arange(6*7*8).reshape((6, 7, 8)), mstype.float32), name="x")
        self.value = value

    def construct(self, index_0, index_1, index_2):
        self.param[index_0, index_1, index_2] = self.value
        ret = self.param + self.const
        return ret


class TensorSetItemByTensorsWithTensor(Cell):
    def __init__(self):
        super(TensorSetItemByTensorsWithTensor, self).__init__()
        self.const = Tensor(np.ones((6, 7, 8)), mstype.float32)
        self.param = Parameter(Tensor(np.arange(6*7*8).reshape((6, 7, 8)), mstype.float32), name="x")

    def construct(self, index_0, index_1, index_2, value):
        self.param[index_0, index_1, index_2] = value
        ret = self.param + self.const
        return ret


class TensorSetItemByTensorsWithTensorNumberError(Cell):
    def __init__(self):
        super(TensorSetItemByTensorsWithTensorNumberError, self).__init__()
        self.const = Tensor(np.ones((6, 7, 8)), mstype.float32)
        self.param = Parameter(Tensor(np.arange(6*7*8).reshape((6, 7, 8)), mstype.float32), name="x")

    def construct(self, index_0, index_1, index_2, index_3, value):
        self.param[index_0, index_1, index_2, index_3] = value
        ret = self.param + self.const
        return ret


class TensorSetItemByTensorsWithTupleOfNumber(Cell):
    def __init__(self, value):
        super(TensorSetItemByTensorsWithTupleOfNumber, self).__init__()
        self.const = Tensor(np.ones((6, 7, 8)), mstype.float32)
        self.param = Parameter(Tensor(np.arange(6*7*8).reshape((6, 7, 8)), mstype.float32), name="x")
        self.value = value

    def construct(self, index_0, index_1, index_2):
        self.param[index_0, index_1, index_2] = self.value
        ret = self.param + self.const
        return ret


class TensorSetItemByTensorsWithTupleOfTensor(Cell):
    def __init__(self):
        super(TensorSetItemByTensorsWithTupleOfTensor, self).__init__()
        self.const = Tensor(np.ones((6, 7, 8)), mstype.float32)
        self.param = Parameter(Tensor(np.arange(6*7*8).reshape((6, 7, 8)), mstype.float32), name="x")

    def construct(self, index_0, index_1, index_2, value_0, value_1, value_2):
        self.param[index_0, index_1, index_2] = (value_0, value_1, value_2)
        ret = self.param + self.const
        return ret


class TensorSetItemByTensorsWithTupleOfTensorNumberError(Cell):
    def __init__(self):
        super(TensorSetItemByTensorsWithTupleOfTensorNumberError, self).__init__()
        self.const = Tensor(np.ones((6, 7, 8)), mstype.float32)
        self.param = Parameter(Tensor(np.arange(6*7*8).reshape((6, 7, 8)), mstype.float32), name="x")

    def construct(self, index_0, index_1, index_2, value_0, value_1):
        self.param[index_0, index_1, index_2] = (value_0, value_1)
        ret = self.param + self.const
        return ret


def test_tensor_assign():
    context.set_context(mode=context.GRAPH_MODE, save_graphs=True)
    net = TensorAssignWithSlice()
    net2 = TensorAssignWithSlice2()
    net_e1 = TensorAssignWithSliceError1()
    net_e2 = TensorAssignWithSliceError2()
    a = np.arange(60).reshape(3, 4, 5)
    ck = np.arange(60).reshape(3, 4, 5)
    b = Tensor([1], dtype=mstype.float32)
    Ta = Tensor(a, dtype=mstype.float32)
    Tck = Tensor(ck, dtype=mstype.float32)
    Ta4d = Tensor(a.reshape(1, 3, 4, 5), dtype=mstype.float32)
    Ta4d_ck = Tensor(ck.reshape(1, 3, 4, 5), dtype=mstype.float32)
    Tb = Tensor([1, 3], dtype=mstype.float32)
    Tc = Tensor([], dtype=mstype.float32)
    t = Tensor([1, 2, 3, 4, 5, 6, 7, 8], dtype=mstype.float32)
    tck = Tensor([1, 2, 3, 4, 5, 6, 7, 8], dtype=mstype.float32)
    net(Ta, b, Tck)
    net2(t, b, tck)
    # Error for A[Slice] = Number
    # 1. A[Slice] = Number,  Slice error
    with pytest.raises(IndexError):
        net_e2(t, 2)

    # Error for A[Slice] = U, U is a Tensor
    # 1. A[Slice] = U,  u.size is error
    with pytest.raises(ValueError):
        net2(t, Tb, tck)
    # 2. A[Slice] = U, U is empty
    with pytest.raises(ValueError):
        net2(t, Tc, tck)
    # 3. A[Slice] = U, U.size error
    with pytest.raises(ValueError):
        net2(t, Tb, tck)

    # Error for A[Tuple(Slice...)] = Tensor
    # 1. A[Tuple(Slice...)] = U, U is empty
    with pytest.raises(ValueError):
        net(Ta, Tc, Tck)
    # 2. A[Tuple(Slice...)] = U, U.size error
    with pytest.raises(ValueError):
        net(Ta, Tb, Tck)
    # 3. A[Tuple(Slice...)] = U,  Slice error
    with pytest.raises(IndexError):
        net_e1(Ta, b)

    # Error for A[Tuple(Slice...)] = Number
    # 1. A[Tuple(Slice...)] = Number,  Slice error
    with pytest.raises(IndexError):
        net_e1(Ta, 2)

    net = TensorAssignWithInteger()
    # Error for A[Number] = scalar/Tensor
    # 1. A[Number] = U, U is a Tensor, u.size not match
    with pytest.raises(ValueError):
        net(Ta, Tb, Tck)
    with pytest.raises(ValueError):
        net(Ta, Tc, Tck)
    # 2. A[Number] = U, the number index error
    with pytest.raises(IndexError):
        net(Ta4d, b, Ta4d_ck)

    # Error for A[(n,m)] = scalar/Tensor
    # 1. A[(n,m)] = U, U is a tensor. u.size not match
    net = TensorAssignWithTupleInteger()
    with pytest.raises(ValueError):
        net(Ta, Tc, Tck)
    with pytest.raises(ValueError):
        net(Ta, Tb, Tck)
    # 2. A[(n,m)] = U, the number index error
    with pytest.raises(IndexError):
        net(Ta4d, b, Ta4d_ck)

    # Error for  A[...] = U or A[1:, ...] = u
    # 1. A[...] = scalar/tensor
    net = TensorAssignWithEllipsis()
    net(Ta, Ta4d)
    with pytest.raises(ValueError):
        net(Ta, Tc)
    with pytest.raises(ValueError):
        net(Ta, Tb)
    # 2. A[::, 1:, ...] = scalar/tensor
    net = TensorAssignWithTupleEllipsis()
    net(Ta, b)
    with pytest.raises(ValueError):
        net(Ta, Tc)
    with pytest.raises(ValueError):
        net(Ta, Tb)


class TensorAssignWithTupleEllipsis2(Cell):
    def __init__(self):
        super(TensorAssignWithTupleEllipsis2, self).__init__()

    def construct(self, a, b):
        a[1:, ..., ::] = b
        return a


class TensorAssignWithTupleEllipsis(Cell):
    def __init__(self):
        super(TensorAssignWithTupleEllipsis, self).__init__()

    def construct(self, a, b):
        a[:2, ...] = 1
        a[1:, ...] = b
        return a


class TensorAssignWithEllipsis(Cell):
    def __init__(self):
        super(TensorAssignWithEllipsis, self).__init__()

    def construct(self, a, b):
        a[...] = 1
        a[...] = b
        return a


class TensorAssignWithInteger(Cell):
    def __init__(self):
        super(TensorAssignWithInteger, self).__init__()

    def construct(self, a, b, ck):
        a[1] = 1
        a[0] = b
        z = a + ck
        return z


class TensorAssignWithTupleInteger(Cell):
    def __init__(self):
        super(TensorAssignWithTupleInteger, self).__init__()

    def construct(self, a, b, ck):
        a[(1)] = 1
        a[(1)] = b
        a[(1, 1)] = b
        a[(1, 1)] = 1
        z = a + ck
        return z


class TensorAssignWithBoolTensorIndex(Cell):
    def __init__(self):
        super(TensorAssignWithBoolTensorIndex, self).__init__()
        self.t = Tensor(np.arange(60).reshape([3, 4, 5]), dtype=mstype.float32)
        self.u_scalar = 5

    def construct(self, a, b, c, u_tensor):
        a[c] = self.u_scalar
        a[b] = u_tensor
        z = a + self.t
        return z


class TensorAssignWithBoolTensorIndexError(Cell):
    def __init__(self):
        super(TensorAssignWithBoolTensorIndexError, self).__init__()

    def construct(self, a, b, c, u_tensor):
        a[b][c] = u_tensor
        return a


class TensorAssignWithBoolTensorIndex2(Cell):
    def __init__(self):
        super(TensorAssignWithBoolTensorIndex2, self).__init__()
        self.t = Tensor(np.arange(6).reshape([2, 3]), dtype=mstype.float32)
        self.t = Tensor(np.arange(60).reshape([3, 4, 5]), dtype=mstype.float32)
        self.u_scalar = 5

    def construct(self, a, u_tensor):
        a[a > 8] = u_tensor
        a[a >= 6] = self.u_scalar
        a[a < 3] = self.u_scalar
        a[a <= 5] = u_tensor
        a[a == 5] = self.u_scalar
        z = a + self.t
        return z


class TensorAssignWithBoolTensorIndex2Error(Cell):
    def __init__(self):
        super(TensorAssignWithBoolTensorIndex2Error, self).__init__()

    def construct(self, a, u_tensor):
        a[a > 8][a > 5] = u_tensor
        return a


a = np.arange(60).reshape(3, 4, 5)
ck = np.arange(60).reshape(3, 4, 5)
a4 = np.arange(60).reshape(3, 2, 2, 5)
b = a > 5
c = a < 3
Ta = Tensor(a, dtype=mstype.float32)
Tck = Tensor(ck, dtype=mstype.float32)
Ta4 = Tensor(a4, dtype=mstype.float32)
Tb = Tensor(b)
Tc = Tensor(c)
Td = Tensor([True, True])
u_tensor = Tensor([1], dtype=mstype.float32)
u_tensor_error = Tensor([1, 2], dtype=mstype.float32)
t_1d = Tensor([1, 2, 3, 4, 5, 6, 7, 8], dtype=mstype.float32)
tck_1d = Tensor([1, 2, 3, 4, 5, 6, 7, 8], dtype=mstype.float32)
u_scalar = 5


def test_tensor_assign_bool_index():
    net1 = TensorAssignWithBoolTensorIndex()
    net2 = TensorAssignWithBoolTensorIndex2()
    net1(Ta, Tb, Tc, u_tensor)
    net1(Ta, Tb, Tc, u_tensor)
    with pytest.raises(ValueError):
        net1(Ta, Td, Tc, u_tensor)
    with pytest.raises(TypeError):
        net1(Ta, u_tensor, Tc, u_tensor)
    with pytest.raises(ValueError):
        net1(Ta, Tb, Td, u_tensor)
    with pytest.raises(TypeError):
        net1(Ta, Tb, Ta, u_tensor)
    with pytest.raises(ValueError):
        net1(Ta, Tb, Tc, u_tensor_error)
    # net1(Ta, u_tensor, Tc, u_tensor_error, u_scalar)
    with pytest.raises(ValueError):
        net2(Ta, u_tensor_error)
    net3 = TensorAssignWithBoolTensorIndexError()
    with pytest.raises(AttributeError):
        net3(Ta, Tb, Tc, u_tensor)
    with pytest.raises(AttributeError):
        net3(Ta, Tb, Tc, u_scalar)
    net4 = TensorAssignWithBoolTensorIndex2Error()
    with pytest.raises(AttributeError):
        net4(Ta, u_tensor)
    with pytest.raises(AttributeError):
        net4(Ta, u_scalar)


test_cases = [
    ('TensorAssignWithTupleEllipsis2', {
        'block': TensorAssignWithTupleEllipsis2(),
        'desc_inputs': [Ta4, u_tensor],
    }),
    ('TensorAssignWithTupleEllipsis', {
        'block': TensorAssignWithTupleEllipsis(),
        'desc_inputs': [Ta, u_tensor],
    }),
    ('TensorAssignWithEllipsis', {
        'block': TensorAssignWithEllipsis(),
        'desc_inputs': [Ta, u_tensor],
    }),
    ('TensorAssignWithTupleInteger', {
        'block': TensorAssignWithTupleInteger(),
        'desc_inputs': [Ta, u_tensor, Tck],
    }),
    ('TensorAssignWithInteger', {
        'block': TensorAssignWithInteger(),
        'desc_inputs': [Ta, u_tensor, Tck],
    }),
    ('TensorAssignWithSlice', {
        'block': TensorAssignWithSlice(),
        'desc_inputs': [Ta, u_tensor, Tck],
    }),
    ('TensorAssignWithSlice2', {
        'block': TensorAssignWithSlice2(),
        'desc_inputs': [t_1d, u_tensor, tck_1d],
    }),
    ('TensorAssignWithBoolTensorIndex', {
        'block': TensorAssignWithBoolTensorIndex(),
        'desc_inputs': [Ta, Tb, Tc, u_tensor],
    }),
    ('TensorAssignWithBoolTensorIndex2', {
        'block': TensorAssignWithBoolTensorIndex2(),
        'desc_inputs': [Ta, u_tensor],
    }),
    ('SlicePositive', {
        'block': NetWorkSlicePositive(),
        'desc_inputs': [Tensor(np.ones([6, 8, 10], np.int32))],
    }),
    ('SliceReduceDimension', {
        'block': NetWorkReduceDimension(),
        'desc_inputs': [Tensor(np.ones([6, 8, 10], np.int32))],
    }),
    ('SliceNegative', {
        'block': NetWorkStepNegative(),
        'desc_inputs': [Tensor(np.ones([6, 8, 10], np.int32))],
    }),
    ('SliceReduceToScalar', {
        'block': NetWorkReduceToScalar(),
        'desc_inputs': [Tensor(np.ones([6, 8, 10], np.int32))],
    }),
    ('TensorSliceEllipsis', {
        'block': NetWorkSliceEllipsis(),
        'desc_inputs': [Tensor(np.ones([6, 7, 8, 9], np.int32))],
    }),
    ('TensorIndexByOneTensor', {
        'block': TensorIndexByOneTensor(),
        'desc_inputs': [Tensor(np.arange(6*7*8).reshape((6, 7, 8)), mstype.int32),
                        Tensor(np.random.randint(6, size=(5, 4)), mstype.int32)],
    }),
    ('TensorIndexByTwoTensors', {
        'block': TensorIndexByTwoTensors(),
        'desc_inputs': [Tensor(np.arange(6*7*8).reshape((6, 7, 8)), mstype.int32),
                        Tensor(np.random.randint(6, size=(3, 4, 5)), mstype.int32),
                        Tensor(np.random.randint(7, size=(4, 5)), mstype.int32)],
    }),
    ('TensorIndexByThreeTensors', {
        'block': TensorIndexByThreeTensors(),
        'desc_inputs': [Tensor(np.arange(6*7*8).reshape((6, 7, 8)), mstype.int32),
                        Tensor(np.random.randint(6, size=(3, 4, 5)), mstype.int32),
                        Tensor(np.random.randint(7, size=(4, 5)), mstype.int32),
                        Tensor(np.random.randint(8, size=(5, 3, 4, 5)), mstype.int32)],
    }),
    ('TensorSetItemByOneTensorWithNumber', {
        'block': TensorSetItemByOneTensorWithNumber(value=0.0),
        'desc_inputs': [Tensor(np.random.randint(4, size=(5, 4)), mstype.int32)],
    }),
    ('TensorSetItemByOneTensorWithTensor', {
        'block': TensorSetItemByOneTensorWithTensor(),
        'desc_inputs': [Tensor(np.random.randint(3, size=(5, 4)), mstype.int32),
                        Tensor(np.zeros((4, 7, 8)), mstype.float32)],
    }),
    ('TensorSetItemByOneTensorWithTupleOfNumber', {
        'block': TensorSetItemByOneTensorWithTupleOfNumber(value=(0.0, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7)),
        'desc_inputs': [Tensor(np.random.randint(5, size=(5, 4)), mstype.int32)],
    }),
    ('TensorSetItemByOneTensorWithTupleOfTensor', {
        'block': TensorSetItemByOneTensorWithTupleOfTensor(),
        'desc_inputs': [Tensor(np.random.randint(6, size=(5, 4)), mstype.int32),
                        Tensor(np.zeros((8,), np.float32)),
                        Tensor(np.ones((8,), np.float32)),
                        Tensor(np.ones((8,), np.float32) * 2)],
    }),
    ('TensorSetItemByTensorsWithNumber', {
        'block': TensorSetItemByTensorsWithNumber(value=0.0),
        'desc_inputs': [Tensor(np.random.randint(6, size=(3, 4, 5)), mstype.int32),
                        Tensor(np.random.randint(7, size=(4, 5)), mstype.int32),
                        Tensor(np.random.randint(8, size=(5, 3, 4, 5)), mstype.int32)],
    }),
    ('TensorSetItemByTensorsWithTensor', {
        'block': TensorSetItemByTensorsWithTensor(),
        'desc_inputs': [Tensor(np.random.randint(6, size=(3, 4, 5)), mstype.int32),
                        Tensor(np.random.randint(7, size=(4, 5)), mstype.int32),
                        Tensor(np.random.randint(8, size=(5, 3, 4, 5)), mstype.int32),
                        Tensor(np.zeros((4, 5)), mstype.float32)],
    }),
    ('TensorSetItemByTensorsWithTupleOfNumber', {
        'block': TensorSetItemByTensorsWithTupleOfNumber(value=(0.0, 1.1, 2.2, 3.3, 4.4)),
        'desc_inputs': [Tensor(np.random.randint(6, size=(3, 4, 5)), mstype.int32),
                        Tensor(np.random.randint(7, size=(4, 5)), mstype.int32),
                        Tensor(np.random.randint(8, size=(5, 3, 4, 5)), mstype.int32)],
    }),
    ('TensorSetItemByTensorsWithTupleOfTensor', {
        'block': TensorSetItemByTensorsWithTupleOfTensor(),
        'desc_inputs': [Tensor(np.random.randint(6, size=(3, 4, 5)), mstype.int32),
                        Tensor(np.random.randint(7, size=(4, 5)), mstype.int32),
                        Tensor(np.random.randint(8, size=(5, 3, 4, 5)), mstype.int32),
                        Tensor(np.zeros((4, 5)), mstype.float32),
                        Tensor(np.ones((4, 5)), mstype.float32),
                        Tensor(np.ones((4, 5)) * 2, mstype.float32)],
    })
]

raise_error_set = [
    ('TensorIndexByOneTensorDtypeError', {
        'block': (TensorIndexByOneTensor(), {'exception': TypeError}),
        'desc_inputs': [Tensor(np.arange(6*7*8).reshape((6, 7, 8)), mstype.int32),
                        Tensor(np.random.randint(6, size=(5, 4)), mstype.int8)],
    }),
    ('TensorIndexByTwoTensorsShapeError', {
        'block': (TensorIndexByTwoTensors(), {'exception': ValueError}),
        'desc_inputs': [Tensor(np.arange(6*7*8).reshape((6, 7, 8)), mstype.int32),
                        Tensor(np.random.randint(6, size=(3, 4, 5)), mstype.int32),
                        Tensor(np.random.randint(7, size=(2, 3, 5)), mstype.int32)],
    }),
    ('TensorIndexByTwoTensorsDtypeError', {
        'block': (TensorIndexByTwoTensors(), {'exception': TypeError}),
        'desc_inputs': [Tensor(np.arange(6*7*8).reshape((6, 7, 8)), mstype.int32),
                        Tensor(np.random.randint(6, size=(3, 4, 5)), mstype.int32),
                        Tensor(np.random.randint(7, size=(4, 5)), mstype.float32)],
    }),
    ('TensorIndexByThreeTensorsShapeError', {
        'block': (TensorIndexByThreeTensors(), {'exception': ValueError}),
        'desc_inputs': [Tensor(np.arange(6*7*8).reshape((6, 7, 8)), mstype.int32),
                        Tensor(np.random.randint(6, size=(3, 4, 5)), mstype.int32),
                        Tensor(np.random.randint(7, size=(3, 4, 5)), mstype.int32),
                        Tensor(np.random.randint(8, size=(5, 2, 4, 5)), mstype.int32)],
    }),
    ('TensorIndexByThreeTensorsDtypeError', {
        'block': (TensorIndexByThreeTensors(), {'exception': TypeError}),
        'desc_inputs': [Tensor(np.arange(6*7*8).reshape((6, 7, 8)), mstype.int32),
                        Tensor(np.random.randint(6, size=(3, 4, 5)), mstype.int32),
                        Tensor(np.random.randint(7, size=(3, 4, 5)), mstype.int64),
                        Tensor(np.random.randint(8, size=(5, 3, 4, 5)), mstype.int32)],
    }),
    ('TensorSetItemByOneTensorWithNumberTypeError', {
        'block': (TensorSetItemByOneTensorWithNumber(value=0), {'exception': TypeError}),
        'desc_inputs': [Tensor(np.random.randint(4, size=(5, 4)), mstype.int32)],
    }),
    ('TensorSetItemByOneTensorWithTensorShapeError', {
        'block': (TensorSetItemByOneTensorWithTensor(), {'exception': ValueError}),
        'desc_inputs': [Tensor(np.random.randint(3, size=(5, 4)), mstype.int32),
                        Tensor(np.zeros((6, 7, 8)), mstype.float32)],
    }),
    ('TensorSetItemByOneTensorWithTensorDtypeError', {
        'block': (TensorSetItemByOneTensorWithTensor(), {'exception': TypeError}),
        'desc_inputs': [Tensor(np.random.randint(3, size=(5, 4)), mstype.int32),
                        Tensor(np.zeros((6, 7, 8)), mstype.int32)],
    }),
    ('TensorSetItemByOneTensorWithTupleOfNumberTypeError', {
        'block': (TensorSetItemByOneTensorWithTupleOfNumber(value=(0, 1, 2, 3, 4, 5, 6, 7)), {'exception': TypeError}),
        'desc_inputs': [Tensor(np.random.randint(5, size=(5, 4)), mstype.int32)],
    }),
    ('TensorSetItemByOneTensorWithTupleOfNumberNumberError', {
        'block': (TensorSetItemByOneTensorWithTupleOfNumber(value=(0.0, 1.1, 2.2)), {'exception': ValueError}),
        'desc_inputs': [Tensor(np.random.randint(5, size=(5, 4)), mstype.int32)],
    }),
    ('TensorSetItemByOneTensorWithTupleOfTensorDtyeError', {
        'block': (TensorSetItemByOneTensorWithTupleOfTensor(), {'exception': TypeError}),
        'desc_inputs': [Tensor(np.random.randint(6, size=(5, 4)), mstype.int32),
                        Tensor(np.zeros((8,), np.int32)),
                        Tensor(np.ones((8,), np.int32)),
                        Tensor(np.ones((8,), np.float32) * 2)],
    }),
    ('TensorSetItemByTensorsWithNumberTypeError', {
        'block': (TensorSetItemByTensorsWithNumber(value=0), {'exception': TypeError}),
        'desc_inputs': [Tensor(np.random.randint(6, size=(3, 4, 5)), mstype.int32),
                        Tensor(np.random.randint(7, size=(4, 5)), mstype.int32),
                        Tensor(np.random.randint(8, size=(5, 3, 4, 5)), mstype.int32)],
    }),
    ('TensorSetItemByTensorsWithTensorShapeError', {
        'block': (TensorSetItemByTensorsWithTensor(),  {'exception': ValueError}),
        'desc_inputs': [Tensor(np.random.randint(6, size=(3, 4, 5)), mstype.int32),
                        Tensor(np.random.randint(7, size=(4, 5)), mstype.int32),
                        Tensor(np.random.randint(8, size=(5, 3, 4, 5)), mstype.int32),
                        Tensor(np.zeros((2, 5)), mstype.float32)],
    }),
    ('TensorSetItemByTensorsWithTensorTypeError', {
        'block': (TensorSetItemByTensorsWithTensor(),  {'exception': TypeError}),
        'desc_inputs': [Tensor(np.random.randint(6, size=(3, 4, 5)), mstype.int32),
                        Tensor(np.random.randint(7, size=(4, 5)), mstype.int32),
                        Tensor(np.random.randint(8, size=(5, 3, 4, 5)), mstype.int32),
                        Tensor(np.zeros((4, 5)), mstype.int32)],
    }),
    ('TensorSetItemByTensorsWithTensorNumberError', {
        'block': (TensorSetItemByTensorsWithTensorNumberError(),  {'exception': IndexError}),
        'desc_inputs': [Tensor(np.random.randint(6, size=(3, 4, 5)), mstype.int32),
                        Tensor(np.random.randint(7, size=(4, 5)), mstype.int32),
                        Tensor(np.random.randint(8, size=(5, 3, 4, 5)), mstype.int32),
                        Tensor(np.random.randint(8, size=(1, 3, 4, 5)), mstype.int32),
                        Tensor(np.zeros((2, 5)), mstype.float32)],
    }),
    ('TensorSetItemByTensorsWithTupleOfNumberTypeError', {
        'block': (TensorSetItemByTensorsWithTupleOfNumber(value=(0, 1, 2, 3, 4)),  {'exception': TypeError}),
        'desc_inputs': [Tensor(np.random.randint(6, size=(3, 4, 5)), mstype.int32),
                        Tensor(np.random.randint(7, size=(4, 5)), mstype.int32),
                        Tensor(np.random.randint(8, size=(5, 3, 4, 5)), mstype.int32)],
    }),
    ('TensorSetItemByTensorsWithTupleOfNumberNumberError', {
        'block': (TensorSetItemByTensorsWithTupleOfNumber(value=(0.0, 1.0, 2.0, 3.0)),  {'exception': ValueError}),
        'desc_inputs': [Tensor(np.random.randint(6, size=(3, 4, 5)), mstype.int32),
                        Tensor(np.random.randint(7, size=(4, 5)), mstype.int32),
                        Tensor(np.random.randint(8, size=(5, 3, 4, 5)), mstype.int32)],
    }),
    ('TensorSetItemByTensorsWithTupleOfTensorNumberError', {
        'block': (TensorSetItemByTensorsWithTupleOfTensorNumberError(),  {'exception': ValueError}),
        'desc_inputs': [Tensor(np.random.randint(6, size=(3, 4, 5)), mstype.int32),
                        Tensor(np.random.randint(7, size=(4, 5)), mstype.int32),
                        Tensor(np.random.randint(8, size=(5, 3, 4, 5)), mstype.int32),
                        Tensor(np.zeros((4, 5)), mstype.float32),
                        Tensor(np.ones((4, 5)), mstype.float32)],
    }),
    ('TensorSetItemByTensorsWithTupleOfTensorTypeError', {
        'block': (TensorSetItemByTensorsWithTupleOfTensor(),  {'exception': TypeError}),
        'desc_inputs': [Tensor(np.random.randint(6, size=(3, 4, 5)), mstype.int32),
                        Tensor(np.random.randint(7, size=(4, 5)), mstype.int32),
                        Tensor(np.random.randint(8, size=(5, 3, 4, 5)), mstype.int32),
                        Tensor(np.zeros((4, 5)), mstype.float32),
                        Tensor(np.ones((4, 5)), mstype.int32),
                        Tensor(np.ones((4, 5)) * 2, mstype.int32)],
    })
]


@mindspore_test(pipeline_for_compile_forward_ge_graph_for_case_by_case_config)
def test_exec():
    context.set_context(mode=context.GRAPH_MODE, save_graphs=True)
    return test_cases


@mindspore_test(pipeline_for_compile_forward_ge_graph_for_case_by_case_config_exception)
def test_check_exception():
    return raise_error_set


def test_tensor_slice_reduce_out_of_bounds_neg():
    class NetWork(Cell):
        def __init__(self):
            super(NetWork, self).__init__()
            self.tensor_ret = Tensor(np.array(9, np.int32))

        def construct(self, tensor):
            ret = tensor[-7, 3, 4]
            return ret

    input_tensor = Tensor(np.ones([6, 8, 10], np.int32))
    net = NetWork()
    with pytest.raises(ValueError) as ex:
        net(input_tensor)
    assert "For 'StridedSlice' the `begin[0]` should be an int and must greater or equal to -6, but got `-7`" in str(
        ex.value)


def test_tensor_slice_reduce_out_of_bounds_positive():
    class NetWork(Cell):
        def __init__(self):
            super(NetWork, self).__init__()
            self.tensor_ret = Tensor(np.array(9, np.int32))

        def construct(self, tensor):
            ret = tensor[6, 3, 4]
            return ret

    input_tensor = Tensor(np.ones([6, 8, 10], np.int32))
    net = NetWork()
    with pytest.raises(ValueError) as ex:
        net(input_tensor)
    assert "For 'StridedSlice' the `begin[0]` should be an int and must less than 6, but got `6`" in str(ex.value)

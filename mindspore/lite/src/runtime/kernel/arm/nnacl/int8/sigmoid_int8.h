/**
 * Copyright 2020 Huawei Technologies Co., Ltd
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
#ifndef MINDSPORE_LITE_SRC_RUNTIME_KERNEL_ARM_OPCLIB_INT8_Sigmoid_INT8_H_
#define MINDSPORE_LITE_SRC_RUNTIME_KERNEL_ARM_OPCLIB_INT8_Sigmoid_INT8_H_

#include <math.h>
#include "src/runtime/kernel/arm/nnacl/op_base.h"
#include "src/runtime/kernel/arm/nnacl/errorcode.h"
#include "src/runtime/kernel/arm/nnacl/quantization/fixed_point.h"

struct SigmoidQuantArg {
  double input_scale;
  int32_t input_zp;
  double output_scale;
  int32_t output_zp;
  int16_t relu6_multiplier_fixedpoint_int16;
  int32_t relu6_multiplier_exponent;
  int16_t output_multiplier_fixedpoint_int16;
  int32_t output_multiplier_exponent;
};

int SigmoidInt8(const int8_t *src, int length, int8_t *dst, SigmoidQuantArg *arg);

#endif  // MINDSPORE_LITE_SRC_RUNTIME_KERNEL_ARM_OPCLIB_INT8_Sigmoid_INT8_H_

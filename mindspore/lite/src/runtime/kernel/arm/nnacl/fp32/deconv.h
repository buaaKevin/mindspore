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
#ifndef MINDSPORE_LITE_SRC_RUNTIME_KERNEL_ARM_NNACL_FP32_DECONV_H_
#define MINDSPORE_LITE_SRC_RUNTIME_KERNEL_ARM_NNACL_FP32_DECONV_H_

#include "src/runtime/kernel/arm/nnacl/pack.h"
#include "src/runtime/kernel/arm/nnacl/op_base.h"
#include "src/runtime/kernel/arm/nnacl/conv_parameter.h"
#include "src/runtime/kernel/arm/nnacl/fp32/strassen_matmul.h"

void PackDeConvWeightFp32(const float *weight, float *dst, int input_channel, int output_channel, int plane);

int DeConvFp32(const float *input, const float *weight, float *output, float *tmp_buffer,
               StrassenMatMulParameter matmul_param);

int DeConvPostFp32C4(const float *src, float *tmp_c4, float *dst, const float *bias, int output_channel,
                     int input_plane, int kernel_plane, int output_plane, ConvParameter *conv_param);
int DeConvPostFp32C8x8(const float *src, float *tmp_out, const float *bias, float *dst, int output_channel,
                       ConvParameter *conv_param);

#endif  // MINDSPORE_LITE_SRC_RUNTIME_KERNEL_ARM_NNACL_FP32_DECONV_H_

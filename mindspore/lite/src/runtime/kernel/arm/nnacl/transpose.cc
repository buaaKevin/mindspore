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

#include "src/runtime/kernel/arm/nnacl/transpose.h"
#include <string.h>
#include "src/runtime/kernel/arm/nnacl/errorcode.h"

void TransposeDim2(float *in_data, float *out_data, int *strides, int *out_strides, int *perm, int *output_shape) {
  const int stride0 = strides[perm[0]];
  const int stride1 = strides[perm[1]];
  const int output0 = output_shape[0];
  const int output1 = output_shape[1];
  for (int i = 0; i < output0; i++) {
    int out_stride0_i = i * output1;
    int stride0_i = i * 1 * stride0;
    for (int j = 0; j < output1; j++) {
      out_data[out_stride0_i + j] = in_data[stride0_i + j * stride1];
    }
  }
}

void TransposeDim3(float *in_data, float *out_data, int *strides, int *out_strides, int *perm, int *output_shape) {
  const int stride0 = strides[perm[0]];
  const int stride1 = strides[perm[1]];
  const int stride2 = strides[perm[2]];
  const int out_stride0 = out_strides[0];
  const int out_stride1 = out_strides[1];
  const int output0 = output_shape[0];
  const int output1 = output_shape[1];
  const int output2 = output_shape[2];
  for (int i = 0; i < output0; i++) {
    int out_stride0_i = i * out_stride0;
    int stride0_i = i * stride0;
    for (int j = 0; j < output1; j++) {
      int out_stride1_j = j * out_stride1;
      int stride1_j = j * stride1;
      for (int k = 0; k < output2; k++) {
        out_data[out_stride0_i + out_stride1_j + k] = in_data[stride0_i + stride1_j + k * stride2];
      }
    }
  }
}

void TransposeDim4(float *in_data, float *out_data, int *strides, int *out_strides, int *perm, int *output_shape) {
  const int stride0 = strides[perm[0]];
  const int stride1 = strides[perm[1]];
  const int stride2 = strides[perm[2]];
  const int stride3 = strides[perm[3]];
  const int out_stride0 = out_strides[0];
  const int out_stride1 = out_strides[1];
  const int out_stride2 = out_strides[2];
  const int output0 = output_shape[0];
  const int output1 = output_shape[1];
  const int output2 = output_shape[2];
  const int output3 = output_shape[3];

  for (int i = 0; i < output0; i++) {
    int out_stride0_i = i * out_stride0;
    int stride0_i = i * stride0;
    for (int j = 0; j < output1; j++) {
      int out_stride1_j = j * out_stride1;
      int stride1_j = j * stride1;
      for (int k = 0; k < output2; k++) {
        int out_stride2_k = k * out_stride2;
        int stride2_k = k * stride2;
        for (int m = 0; m < output3; m++) {
          out_data[out_stride0_i + out_stride1_j + out_stride2_k + m] =
            in_data[stride0_i + stride1_j + stride2_k + m * stride3];
        }
      }
    }
  }
}

int DoTranspose(float *in_data, float *out_data, int *input_shape, int *output_shape,
                TransposeParameter *transpose_param) {
  if (in_data == nullptr || out_data == nullptr) {
    return NNACL_ERR;
  }
  int *perm = transpose_param->perm_;
  int *strides = transpose_param->strides_;
  int *out_strides = transpose_param->out_strides_;
  int data_size = transpose_param->data_size_;
  int num_axes = transpose_param->num_axes_;

  if (num_axes < 2 || num_axes > 4) {
    return NNACL_ERR;
  }

  // check if transpose is needed
  bool needTranspose = false;
  for (int i = 1; i < num_axes; i++) {
    if (perm[i] - perm[i - 1] != 1) {
      needTranspose = true;
      break;
    }
  }

  if (!needTranspose) {
    (void)memcpy(out_data, in_data, data_size);
    return NNACL_OK;
  }
  if (num_axes == 2) {
    TransposeDim2(in_data, out_data, strides, out_strides, perm, output_shape);
  } else if (num_axes == 3) {
    TransposeDim3(in_data, out_data, strides, out_strides, perm, output_shape);
  } else if (num_axes == 4) {
    TransposeDim4(in_data, out_data, strides, out_strides, perm, output_shape);
  }
  return NNACL_OK;
}


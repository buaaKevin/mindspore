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
#include "src/runtime/kernel/arm/fp32/batch_to_space.h"
#include <vector>
#include "schema/model_generated.h"
#include "src/kernel_registry.h"
#include "src/runtime/kernel/arm/nnacl/batch_to_space.h"
#include "include/errorcode.h"

using mindspore::lite::RET_OK;

namespace mindspore::kernel {
int BatchToSpaceCPUKernel::Init() {
  return BatchToSpaceBaseCPUKernel::Init();
}

int BatchToSpaceCPUKernel::Run() {
  auto input = inputs_[0];
  auto output = outputs_[0];
  const float *input_data = reinterpret_cast<const float *>(input->Data());
  float *output_data = reinterpret_cast<float *>(output->Data());
  auto in_shape = input->shape();
  auto out_shape = output->shape();
  BatchToSpaceParameter *param = reinterpret_cast<BatchToSpaceParameter *>(this->opParameter);

  if (IsNoCrop()) {
    BatchToSpaceNoCropForNHWC(input_data, output_data, in_shape.data(), out_shape[0], param->block_shape_,
                              sizeof(float));
  } else {
    BatchToSpaceForNHWC(input_data, output_data, in_shape.data(), out_shape[0], param->block_shape_, param->crops_,
                        sizeof(float));
  }

  return RET_OK;
}
}  // namespace mindspore::kernel

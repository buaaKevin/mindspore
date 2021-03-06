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

#ifndef MINDSPORE_LITE_SRC_RUNTIME_KERNEL_ARM_INT8_ARITHMETIC_INT8_H_
#define MINDSPORE_LITE_SRC_RUNTIME_KERNEL_ARM_INT8_ARITHMETIC_INT8_H_

#include <vector>
#include "src/lite_kernel.h"
#include "schema/model_generated.h"

namespace mindspore::kernel {
class ArithmeticInt8CPUKernel : public LiteKernel {
  typedef int (*ArithmeticRunInt8)(int8_t *input0, int8_t *input1, int8_t *output, int element_size);

 public:
  ArithmeticInt8CPUKernel(OpParameter *parameter, const std::vector<lite::tensor::Tensor *> &inputs,
                          const std::vector<lite::tensor::Tensor *> &outputs, const lite::Context *ctx)
      : LiteKernel(parameter, inputs, outputs), thread_count_(ctx->thread_num_), context_(ctx) {}
  ~ArithmeticInt8CPUKernel();

  int Init() override;
  int ReSize() override;
  int Run() override;
  int DoArithmetic(int thread_id);

 private:
  int thread_count_;
  int8_t *tile_data0_;
  int8_t *tile_data1_;
  const lite::Context *context_;
  ArithmeticRunInt8 arithmetic_run_;
};
}  // namespace mindspore::kernel
#endif  // MINDSPORE_LITE_SRC_RUNTIME_KERNEL_ARM_INT8_ARITHMETIC_INT8_H_

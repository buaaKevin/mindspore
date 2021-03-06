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

#include "tools/converter/parser/tflite/tflite_div_parser.h"
#include <vector>
#include <memory>

namespace mindspore {
namespace lite {
STATUS TfliteDivParser::Parse(const std::unique_ptr<tflite::OperatorT> &tfliteOp,
                              const std::vector<std::unique_ptr<tflite::TensorT>> &tfliteTensors,
                              const std::vector<std::unique_ptr<tflite::BufferT>> &tfliteModelBuffer,
                              const std::vector<std::unique_ptr<tflite::OperatorCodeT>> &tfliteOpSet,
                              schema::CNodeT *op, TensorCache *tensor_cache, bool quantizedModel) {
  MS_LOG(DEBUG) << "parse TfliteDivParser";
  std::unique_ptr<schema::DivT> attr(new schema::DivT());

  const auto &tfliteAttr = tfliteOp->builtin_options.AsDivOptions();
  if (nullptr == tfliteAttr) {
    MS_LOG(ERROR) << "get op: " << op->name.c_str() << " attr failed";
    return RET_NULL_PTR;
  }
  attr->activationType = GetActivationFunctionType(tfliteAttr->fused_activation_function);

  auto x_index = tfliteOp->inputs[0];
  const auto &x_tensor = tfliteTensors[x_index];
  if (x_tensor == nullptr) {
    MS_LOG(ERROR) << "the first input is null";
    return RET_NULL_PTR;
  }
  auto &x_data = tfliteModelBuffer.at(x_tensor->buffer);
  if (x_data == nullptr) {
    MS_LOG(ERROR) << "the data of the first input is null";
    return RET_NULL_PTR;
  }
  if (x_data->data.size() > 0) {
    std::vector<tflite::TensorT *> x_tensors{x_tensor.get()};
    if (RET_OK != ParseTensor(x_tensors, tfliteModelBuffer, tensor_cache, TF_CONST, true)) {
      MS_LOG(ERROR) << "parse the first tensor failed";
      return RET_ERROR;
    }
  }

  auto y_index = tfliteOp->inputs[1];
  const auto &y_tensor = tfliteTensors[y_index];
  if (y_tensor == nullptr) {
    MS_LOG(ERROR) << "the second input is null";
    return RET_NULL_PTR;
  }
  auto &y_data = tfliteModelBuffer.at(y_tensor->buffer);
  if (y_data == nullptr) {
    MS_LOG(ERROR) << "the data of the second input is null";
    return RET_NULL_PTR;
  }
  if (y_data->data.size() > 0) {
    std::vector<tflite::TensorT *> y_tensors{y_tensor.get()};
    if (RET_OK != ParseTensor(y_tensors, tfliteModelBuffer, tensor_cache, TF_CONST, true)) {
      MS_LOG(ERROR) << "parse the second tensor failed";
      return RET_ERROR;
    }
  }

  if (op != nullptr) {
    op->primitive = std::make_unique<schema::PrimitiveT>();
    op->primitive->value.type = schema::PrimitiveType_Div;
    op->primitive->value.value = attr.release();
  }
  return RET_OK;
}

TfliteNodeRegister g_TfliteDivParser("Div", new TfliteDivParser());
}  // namespace lite
}  // namespace mindspore

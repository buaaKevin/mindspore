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

#ifndef MINDSPORE_LITE_SRC_TRAIN_MODEL_IMPL_H_
#define MINDSPORE_LITE_SRC_TRAIN_MODEL_IMPL_H

#include <string>
#include <map>
#include <memory>
#include "schema/model_generated.h"
#include "src/ops/ops.h"
#include "ir/func_graph.h"

namespace mindspore::lite {
namespace train {
class ModelImpl : public FuncGraph {
 public:
  static std::shared_ptr<ModelImpl> Import(const char *model_buf, size_t size);
  ModelImpl() = default;
  explicit ModelImpl(const schema::MetaGraph *graph) : meta_graph(graph) {}
  ~ModelImpl() override = default;
  const lite::Primitive *GetOp(const std::string &name) const;
  const schema::MetaGraph *GetMetaGraph() const;
  void FreeMetaGraph();
  int BuildOps();

 protected:
  lite::Primitive *CopyPrimitive(const schema::Primitive *srcPrim);

 protected:
  const schema::MetaGraph *meta_graph = nullptr;
  std::map<std::string, lite::Primitive *> ops;
};
}  // namespace train
using ModelImpl = mindspore::lite::train::ModelImpl;
}  // namespace mindspore::lite

#endif  // MINDSPORE_LITE_INCLUDE_MODEL_H


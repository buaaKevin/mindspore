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

#include <iostream>
#include <memory>
#include <vector>

#include "utils/log_adapter.h"
#include "common/common_test.h"
#include "src/common/file_utils.h"
#include "src/common/file_utils_ext.h"
#include "mindspore/lite/src/kernel_registry.h"
#include "mindspore/lite/src/ir/tensor.h"
#include "mindspore/lite/src/lite_kernel.h"
#include "mindspore/lite/src/runtime/kernel/arm/fp32/activation_grad.h"

namespace mindspore {
class TestActGradFp32 :  public mindspore::Common {
 public:
  TestActGradFp32() {}
};

TEST_F(TestActGradFp32, ReluGradFp32) {
  // runtime part
  printf("Calculating runtime cost...\n");
  uint64_t time_avg = 0;
  size_t output_data_size = 50;

  size_t input_size;
  std::string input_path = "./test_data/activationGrad/relu_y_50.bin";
  auto input_data = reinterpret_cast<float *>(mindspore::lite::ReadFile(input_path.c_str(), &input_size));
  std::string yt_path = "./test_data/activationGrad/relu_yt_50.bin";
  auto yt_data = reinterpret_cast<float *>(mindspore::lite::ReadFile(yt_path.c_str(), &input_size));

  auto output_data = new float[output_data_size];
  // warm up loop
  for (int i = 0; i < 3; i++) {
    ReluGrad(yt_data, input_data, 50, output_data);
  }

  int loop_count = 100;
  auto time_start = mindspore::lite::GetTimeUs();
  for (int i = 0; i < loop_count; i++) {
    ReluGrad(yt_data, input_data, 50, output_data);
  }
  auto time_end = mindspore::lite::GetTimeUs();
  auto cost = time_end - time_start;
  time_avg = cost / loop_count;
  printf("single thread running time : %f ms\n", time_avg / 1000.0f);

  printf("==================output data=================\n");
  for (int i = 0; i < 20; i++) {
    std::cout << output_data[i] << " ,";
  }
  std::cout << std::endl;

  std::string output_path = "./test_data/activationGrad/relu_out_50.bin";

  int res = lite::CompareRelativeOutput(output_data, output_path);

  EXPECT_EQ(res, 0);

  delete input_data;
  delete[] output_data;
  delete yt_data;

  MS_LOG(INFO) << "ReluGradFp32 passed";
}

TEST_F(TestActGradFp32, Relu6GradFp32) {
  // runtime part
  printf("Calculating runtime cost...\n");
  uint64_t time_avg = 0;
  size_t output_data_size = 50;

  size_t input_size;
  std::string input_path = "./test_data/activationGrad/relu6_y_50.bin";
  auto input_data = reinterpret_cast<float *>(mindspore::lite::ReadFile(input_path.c_str(), &input_size));
  std::string yt_path = "./test_data/activationGrad/relu6_yt_50.bin";
  auto yt_data = reinterpret_cast<float *>(mindspore::lite::ReadFile(yt_path.c_str(), &input_size));

  auto output_data = new float[output_data_size];
  // warm up loop
  for (int i = 0; i < 3; i++) {
    Relu6Grad(yt_data, input_data, 50, output_data);
  }

  int loop_count = 100;
  auto time_start = mindspore::lite::GetTimeUs();
  for (int i = 0; i < loop_count; i++) {
    Relu6Grad(yt_data, input_data, 50, output_data);
  }
  auto time_end = mindspore::lite::GetTimeUs();
  auto cost = time_end - time_start;
  time_avg = cost / loop_count;
  printf("single thread running time : %f ms\n", time_avg / 1000.0f);

  printf("==================output data=================\n");
  for (int i = 0; i < 20; i++) {
    std::cout << output_data[i] << " ,";
  }
  std::cout << std::endl;

  std::string output_path = "./test_data/activationGrad/relu6_out_50.bin";
  int res = lite::CompareRelativeOutput(output_data, output_path);

  EXPECT_EQ(res, 0);

  delete input_data;
  delete[] output_data;
  delete yt_data;

  MS_LOG(INFO) << "Relu6GradFp32 passed";
}

TEST_F(TestActGradFp32, LReluGradFp32) {
  // runtime part
  printf("Calculating runtime cost...\n");
  uint64_t time_avg = 0;
  size_t output_data_size = 50;

  size_t input_size;
  std::string input_path = "./test_data/activationGrad/lrelu_y_50.bin";
  auto input_data = reinterpret_cast<float *>(mindspore::lite::ReadFile(input_path.c_str(), &input_size));
  std::string yt_path = "./test_data/activationGrad/lrelu_yt_50.bin";
  auto yt_data = reinterpret_cast<float *>(mindspore::lite::ReadFile(yt_path.c_str(), &input_size));

  auto output_data = new float[output_data_size];
  // warm up loop
  for (int i = 0; i < 3; i++) {
    LReluGrad(yt_data, input_data, 50, output_data, 0.1);
  }

  int loop_count = 100;
  auto time_start = mindspore::lite::GetTimeUs();
  for (int i = 0; i < loop_count; i++) {
    LReluGrad(yt_data, input_data, 50, output_data, 0.1);
  }
  auto time_end = mindspore::lite::GetTimeUs();
  auto cost = time_end - time_start;
  time_avg = cost / loop_count;
  printf("single thread running time : %f ms\n", time_avg / 1000.0f);

  printf("==================output data=================\n");
  for (int i = 0; i < 20; i++) {
    std::cout << output_data[i] << " ,";
  }
  std::cout << std::endl;

  std::string output_path = "./test_data/activationGrad/lrelu_out_50.bin";
  int res = lite::CompareRelativeOutput(output_data, output_path);

  EXPECT_EQ(res, 0);

  delete input_data;
  delete[] output_data;
  delete yt_data;

  MS_LOG(INFO) << "LReluGradFp32 passed";
}

TEST_F(TestActGradFp32, SigmoidGradFp32) {
  // runtime part
  printf("Calculating runtime cost...\n");
  uint64_t time_avg = 0;
  size_t output_data_size = 50;

  size_t input_size;
  std::string input_path = "./test_data/activationGrad/sigmoid_y_50.bin";
  auto input_data = reinterpret_cast<float *>(mindspore::lite::ReadFile(input_path.c_str(), &input_size));
  std::string yt_path = "./test_data/activationGrad/sigmoid_yt_50.bin";
  auto yt_data = reinterpret_cast<float *>(mindspore::lite::ReadFile(yt_path.c_str(), &input_size));

  auto output_data = new float[output_data_size];
  // warm up loop
  for (int i = 0; i < 3; i++) {
    SigmoidGrad(yt_data, input_data, 50, output_data);
  }

  int loop_count = 100;
  auto time_start = mindspore::lite::GetTimeUs();
  for (int i = 0; i < loop_count; i++) {
    SigmoidGrad(yt_data, input_data, 50, output_data);
  }
  auto time_end = mindspore::lite::GetTimeUs();
  auto cost = time_end - time_start;
  time_avg = cost / loop_count;
  printf("single thread running time : %f ms\n", time_avg / 1000.0f);

  printf("==================output data=================\n");
  for (int i = 0; i < 20; i++) {
    std::cout << output_data[i] << " ,";
  }
  std::cout << std::endl;

  std::string output_path = "./test_data/activationGrad/sigmoid_out_50.bin";
  int res = lite::CompareRelativeOutput(output_data, output_path);

  EXPECT_EQ(res, 0);
  // lite::CompareOutput(output_data, output_path);

  delete input_data;
  delete[] output_data;
  delete yt_data;

  MS_LOG(INFO) << "SigmoidGradFp32 passed";
}

TEST_F(TestActGradFp32, tanhGradFp32) {
  // runtime part
  printf("Calculating runtime cost...\n");
  uint64_t time_avg = 0;
  size_t output_data_size = 50;

  size_t input_size;
  std::string input_path = "./test_data/activationGrad/tanh_y_50.bin";
  auto input_data = reinterpret_cast<float *>(mindspore::lite::ReadFile(input_path.c_str(), &input_size));
  std::string yt_path = "./test_data/activationGrad/tanh_yt_50.bin";
  auto yt_data = reinterpret_cast<float *>(mindspore::lite::ReadFile(yt_path.c_str(), &input_size));

  auto output_data = new float[output_data_size];
  // warm up loop
  for (int i = 0; i < 3; i++) {
    TanhGrad(yt_data, input_data, 50, output_data);
  }

  int loop_count = 100;
  auto time_start = mindspore::lite::GetTimeUs();
  for (int i = 0; i < loop_count; i++) {
    TanhGrad(yt_data, input_data, 50, output_data);
  }
  auto time_end = mindspore::lite::GetTimeUs();
  auto cost = time_end - time_start;
  time_avg = cost / loop_count;
  printf("single thread running time : %f ms\n", time_avg / 1000.0f);

  printf("==================output data=================\n");
  for (int i = 0; i < 20; i++) {
    std::cout << output_data[i] << " ,";
  }
  std::cout << std::endl;

  std::string output_path = "./test_data/activationGrad/tanh_out_50.bin";
  int res = lite::CompareRelativeOutput(output_data, output_path);

  EXPECT_EQ(res, 0);

  delete input_data;
  delete[] output_data;
  delete yt_data;
  MS_LOG(INFO) << "TanhGradFp32 passed";
}

TEST_F(TestActGradFp32, hswishGradFp32) {
  // runtime part
  printf("Calculating runtime cost...\n");
  uint64_t time_avg = 0;
  size_t output_data_size = 50;

  size_t input_size;
  std::string input_path = "./test_data/activationGrad/hswish_x_50.bin";
  auto input_data = reinterpret_cast<float *>(mindspore::lite::ReadFile(input_path.c_str(), &input_size));
  std::string yt_path = "./test_data/activationGrad/hswish_yt_50.bin";
  auto yt_data = reinterpret_cast<float *>(mindspore::lite::ReadFile(yt_path.c_str(), &input_size));

  auto output_data = new float[output_data_size];
  // warm up loop
  for (int i = 0; i < 3; i++) {
    HSwishGrad(yt_data, input_data, 50, output_data);
  }

  int loop_count = 100;
  auto time_start = mindspore::lite::GetTimeUs();
  for (int i = 0; i < loop_count; i++) {
    HSwishGrad(yt_data, input_data, 50, output_data);
  }
  auto time_end = mindspore::lite::GetTimeUs();
  auto cost = time_end - time_start;
  time_avg = cost / loop_count;
  printf("single thread running time : %f ms\n", time_avg / 1000.0f);

  printf("==================output data=================\n");
  for (int i = 0; i < 20; i++) {
    std::cout << output_data[i] << " ,";
  }
  std::cout << std::endl;

  std::string output_path = "./test_data/activationGrad/hswish_out_50.bin";
  int res = lite::CompareRelativeOutput(output_data, output_path);

  EXPECT_EQ(res, 0);

  delete input_data;
  delete[] output_data;
  delete yt_data;
  MS_LOG(INFO) << "hswishGradFp32 passed";
}

}  // namespace mindspore

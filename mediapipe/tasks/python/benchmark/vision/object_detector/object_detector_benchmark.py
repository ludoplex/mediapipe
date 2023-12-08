# Copyright 2023 The MediaPipe Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""MediaPipe object detector benchmark."""

from mediapipe.python._framework_bindings import image
from mediapipe.tasks.python.benchmark import benchmark_utils
from mediapipe.tasks.python.benchmark.vision import benchmark
from mediapipe.tasks.python.benchmark.vision.core import base_vision_benchmark_api
from mediapipe.tasks.python.core import base_options
from mediapipe.tasks.python.vision import object_detector

_MODEL_FILE = 'coco_efficientdet_lite0_v1_1.0_quant_2021_09_06.tflite'
_IMAGE_FILE = 'cats_and_dogs.jpg'


def run(model_path, n_iterations, delegate):
  """Run an object detector benchmark.

  Args:
      model_path: Path to the TFLite model.
      n_iterations: Number of iterations to run the benchmark.
      delegate: CPU or GPU delegate for inference.

  Returns:
      List of inference times.
  """
  # Initialize the object detector
  options = object_detector.ObjectDetectorOptions(
      base_options=base_options.BaseOptions(
          model_asset_path=model_path, delegate=delegate
      )
  )

  with object_detector.ObjectDetector.create_from_options(options) as detector:
    mp_image = image.Image.create_from_file(
        benchmark_utils.get_test_data_path(
            base_vision_benchmark_api.VISION_TEST_DATA_DIR, _IMAGE_FILE
        )
    )
    return base_vision_benchmark_api.benchmark_task(detector.detect, mp_image,
                                                    n_iterations)


if __name__ == '__main__':
  benchmark.benchmarker(run, _MODEL_FILE)

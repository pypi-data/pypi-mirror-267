# Copyright The OpenTelemetry Authors
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

import time
from typing import Mapping, Optional, Sequence

from opentelemetry import trace
from oteltest.common import OtelTest, Telemetry

SERVICE_NAME = "integration-test"
NUM_ADDS = 12

if __name__ == "__main__":
    tracer = trace.get_tracer("my-tracer")
    for i in range(NUM_ADDS):
        with tracer.start_as_current_span("my-span"):
            print(f"simple_loop.py: {i+1}/{NUM_ADDS}")
            time.sleep(0.5)


class MyTest(OtelTest):
    def requirements(self) -> Sequence[str]:
        return "opentelemetry-distro", "opentelemetry-exporter-otlp-proto-grpc"

    def environment_variables(self) -> Mapping[str, str]:
        return {"OTEL_SERVICE_NAME": SERVICE_NAME}

    def wrapper_script(self) -> str:
        return "opentelemetry-instrument"

    def run_client(self) -> None:
        print("run_client()")

    def max_wait(self) -> Optional[float]:
        return 60

    def validate(self, telemetry: Telemetry) -> None:
        assert telemetry.num_spans() == NUM_ADDS

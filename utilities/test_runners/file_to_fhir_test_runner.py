from pathlib import Path
from typing import Optional, Dict, Any, Union

from pyspark.sql.session import SparkSession
from pyspark.sql.types import StructType, DataType

from spark_pipeline_framework.logger.yarn_logger import get_logger

from mockserver_client.mockserver_client import MockServerFriendlyClient
from spark_pipeline_framework_testing.test_runner import clean_spark_session

from spark_pipeline_framework_testing.test_runner_v2 import (
    SparkPipelineFrameworkTestRunnerV2,
)

from spark_pipeline_framework_testing.test_classes import input_types
from spark_pipeline_framework_testing.validators.fhir_validator import FhirValidator

from utilities.test_runners.base_test_runner import BaseTestRunner


class FileToFhirTestRunner(BaseTestRunner):
    def __init__(
        self,
        spark_session: SparkSession,
        data_dir: Path,
        test_name: str,
        extra_params: Optional[Dict[str, Any]] = None,
        input_schema: Optional[
            Union[StructType, Dict[str, StructType], DataType]
        ] = None,
        output_schema: Optional[
            Union[StructType, Dict[str, StructType], DataType]
        ] = None,
    ) -> None:
        assert spark_session
        self.spark_session: SparkSession = spark_session
        assert data_dir
        self.data_dir: Path = data_dir
        assert test_name
        self.test_name: str = test_name
        self.extra_params: Optional[Dict[str, Any]] = extra_params
        self.input_schema: Optional[
            Union[StructType, Dict[str, StructType], DataType]
        ] = input_schema
        self.output_schema: Optional[
            Union[StructType, Dict[str, StructType], DataType]
        ] = output_schema

    def run_test(self) -> None:
        clean_spark_session(self.spark_session)
        test_input = input_types.FileInput(input_schema=self.input_schema)
        test_fhir = input_types.FhirCalls()

        logger = get_logger(__name__)

        mock_server_url = "http://mock-server:1080"
        mock_client = MockServerFriendlyClient(mock_server_url)
        mock_client.clear(f"/{self.test_name}")
        mock_client.clear(f"/{self.test_name}/*")
        mock_client.reset()
        mock_client.expect_default()

        params = {
            "test_name": self.test_name,
            "mock_server_url": mock_server_url,
            "fhir_server_url": f"http://mock-server:1080/{self.test_name}/4_0_0",
        }
        if self.extra_params:
            params.update(self.extra_params)

        test_validator = FhirValidator(
            related_inputs=test_fhir,
            related_file_inputs=test_input,
            mock_server_url=mock_server_url,
            test_name=self.test_name,
            fhir_validation_url="http://fhir:3000/4_0_0",
        )

        # initialize the mock calls
        test_fhir.initialize(
            test_name=self.test_name,
            test_path=self.data_dir,
            logger=logger,
            mock_client=mock_client,
            spark_session=self.spark_session,
        )

        SparkPipelineFrameworkTestRunnerV2(
            spark_session=self.spark_session,
            test_path=self.data_dir,
            test_name=self.test_name,
            test_validators=[
                test_validator,
            ],
            logger=logger,
            test_inputs=[test_input],
            temp_folder="output/temp",
            mock_client=mock_client,
            helix_pipeline_parameters=params,
        ).run_test2()

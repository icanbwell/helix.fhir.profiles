import os
from os import makedirs
from os import mkdir
from pathlib import Path
from shutil import rmtree
from typing import Any, Dict, List, Optional, Type
from pyspark.sql import SparkSession
from spark_pipeline_framework.logger.yarn_logger import get_logger
from spark_pipeline_framework.logger.yarn_logger import Logger  # type: ignore
from spark_pipeline_framework.proxy_generator.proxy_base import ProxyBase

from mockserver_client.mockserver_client import MockServerFriendlyClient
from spark_pipeline_framework_testing.test_classes.input_types import TestInputType
from spark_pipeline_framework_testing.test_classes.validator_types import Validator
from spark_pipeline_framework_testing.test_runner_v2 import (
    SparkPipelineFrameworkTestRunnerV2,
)

from tests_common.path_helpers import get_project_path
from utilities.helix_geolocation.cache import MockCacheHandler
from utilities.helix_geolocation.vendors import MockStandardizingVendor
from utilities.spark_test_helper.spark_test_helper import SparkTestHelper


class SpfTest:
    def __init__(
        self,
        test_name: str,
        # mocked_atc: MagicMock,
        spark_session: SparkSession,
        test_path: Path,
        helix_pipeline_parameters: Optional[Dict[str, Any]] = None,
        temp_dir: str = "./temp",
        clean_spark_session: Optional[bool] = None,
    ):
        """
        This class take some arguments to set the stage for testing. InputTypes and Validators do the rest.
        :param test_name: a unique name for the test e.g. name of the test function
        :param spark_session: pointer to an active spark session to run the pyspark code
        :param test_path: full path to test directory (where the test data and parameters files exist)
        :param helix_pipeline_parameters: the parameters that the pipeline/feature need
        :param temp_dir: name of the temp dir (not full path)
        """
        self.test_name = test_name
        self.data_dir = test_path
        self.spark_session = spark_session
        self.helix_pipeline_parameters = helix_pipeline_parameters
        # self.mocked_atc = mocked_atc
        self.logger = get_logger(__name__)
        self.test_inputs: List[TestInputType] = []
        self.helix_transformers: List[Type[ProxyBase]] = []
        self.test_validator: List[Validator] = []
        self.mock_client_url = "http://mock-server:1080"
        self.mock_client_url_prefix = f"{test_name}/4_0_0"
        self.fhir_validation_url = "http://fhir:3000/4_0_0"
        self.temp_dir = temp_dir
        self.auto_find_helix_transformer = True
        self.clean_spark_session: Optional[bool] = clean_spark_session

    def add_test_input(self, test_input: TestInputType) -> "SpfTest":
        """
        :param test_input: introduce the input data for the test could be csv or fhir
        """
        self.test_inputs.append(test_input)
        return self

    def add_helix_transformer(self, helix_transformer: Type[ProxyBase]) -> "SpfTest":
        """
        :param helix_transformer: if test is not in the same path, please send the transformer subject to test as a class
        """
        self.helix_transformers.append(helix_transformer)
        return self

    def add_test_validator(self, test_validator: Validator) -> "SpfTest":
        """
        :param test_validator: Validator object tells the test framework how to test the output result
        """
        self.test_validator.append(test_validator)
        return self

    def set_auto_find_helix_transformer(self, auto_find: bool) -> "SpfTest":
        """
        :param auto_find: tell the test framework to look for test in the same hierarchy
        """
        self.auto_find_helix_transformer = auto_find
        return self

    def change_fhir_server(
        self,
        server_url: str,
        path_prefix: Optional[str],
        validator_url: Optional[str] = None,
    ) -> "SpfTest":
        """
        url = <server_url>/paht_prefix
        the default values are set in the __init__ function
        :param server_url:
        :param path_prefix:
        :param validator_url:
        :return:
        """
        self.mock_client_url = server_url
        if path_prefix:
            self.mock_client_url_prefix = path_prefix
        if validator_url:
            self.fhir_validation_url = validator_url
        return self

    def run_test(self) -> None:
        # initialize values
        # self.mocked_atc.side_effect = lambda df: df
        self._init_temp_test_dir(self.data_dir)
        logger: Logger = get_logger(__name__)

        # setup servers
        if self.clean_spark_session:
            SparkTestHelper.clean_spark_session(session=self.spark_session)
        mock_client = MockServerFriendlyClient(self.mock_client_url)
        mock_client.clear(f"/{self.test_name}/*.*")

        validation_query_dir = self._get_validation_query_path()
        if self.helix_pipeline_parameters:
            self.helix_pipeline_parameters["validation_query_source_path"] = str(
                validation_query_dir
            )
        else:
            self.helix_pipeline_parameters = {
                "validation_query_source_path": str(validation_query_dir)
            }

        # check up
        if self.auto_find_helix_transformer and self.helix_transformers:
            self.auto_find_helix_transformer = False
            logger.info(
                "helix transformer is provided so ignoring auto_find_helix_transformer=True"
            )

        SparkPipelineFrameworkTestRunnerV2(
            spark_session=self.spark_session,
            mock_client=mock_client,
            test_path=Path(self.data_dir),
            test_name=self.test_name,
            test_inputs=self.test_inputs,
            auto_find_helix_transformer=self.auto_find_helix_transformer,
            helix_transformers=self.helix_transformers,
            helix_pipeline_parameters=self.helix_pipeline_parameters,
            test_validators=self.test_validator,
            temp_folder=os.path.join(self.temp_dir, "spf_test"),
            extra_params={
                "cache_handler": MockCacheHandler(),
                "address_standardization_class": MockStandardizingVendor(),
            },
            fhir_validation_url=self.fhir_validation_url,
            fhir_server_url=f"{self.mock_client_url}/{self.mock_client_url_prefix}",
            logger=logger,
        ).run_test2()

    def _init_temp_test_dir(self, test_dir: Path) -> Path:
        temp_folder = test_dir.joinpath(self.temp_dir)
        if os.path.isdir(temp_folder):
            rmtree(temp_folder)
        makedirs(temp_folder)
        mkdir(temp_folder.joinpath("jsonl"))
        mkdir(temp_folder.joinpath("fhir"))
        return temp_folder

    def _get_validation_query_path(self) -> Path:
        base_dir: Path = get_project_path(self.data_dir)
        return base_dir.joinpath("validation_queries")


def camel_case_to_snake_case(text: str) -> str:
    import re

    str1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", text)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", str1).lower()

import os
from typing import Any, Generator

import boto3
import pytest
from _pytest.fixtures import FixtureFunctionMarker
from botocore.client import BaseClient
from moto import mock_ssm, mock_s3  # type: ignore
from pyspark.sql import SparkSession

# make sure env variables are set correctly
from utilities.spark_test_helper.spark_test_helper import SparkTestHelper

if "SPARK_HOME" not in os.environ:
    os.environ["SPARK_HOME"] = "/usr/local/opt/spark"


def clean_spark_session(session: SparkSession) -> None:
    SparkTestHelper.clean_spark_session(session)


@pytest.fixture(scope="function")
def spark_session(request: Any) -> SparkSession:
    return SparkTestHelper.create_or_reuse_test_spark_session(request=request)


@pytest.fixture(scope="function")
def spark_high_memory_session(request: Any) -> SparkSession:
    return SparkTestHelper.create_or_reuse_test_spark_session(
        request=request, memory="10g"
    )


@pytest.fixture(scope="function")
def spark_session_per_function(request: Any) -> SparkSession:
    return SparkTestHelper.create_test_spark_session(request=request)


@pytest.fixture(scope="function")
def aws_credentials() -> None:
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_REGION"] = "us-east-1"


@pytest.fixture(scope="function")
def ssm_mock(
    aws_credentials: FixtureFunctionMarker,
) -> Generator[BaseClient, None, None]:
    with mock_ssm():
        yield boto3.client("ssm", region_name="us-east-1")


@pytest.fixture(scope="function")
def s3_mock(
    aws_credentials: FixtureFunctionMarker,
) -> Generator[BaseClient, None, None]:
    with mock_s3():
        yield boto3.client("s3", region_name="us-east-1")

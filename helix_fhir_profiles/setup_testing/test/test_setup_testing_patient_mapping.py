from pathlib import Path

from pyspark.sql import SparkSession
from utilities.conftest import clean_spark_session

from utilities.test_runners.file_to_fhir_test_runner import FileToFhirTestRunner


def test_setup_testing_patient_mapping(spark_session: SparkSession) -> None:
    clean_spark_session(session=spark_session)
    data_dir: Path = Path(__file__).parent.joinpath("./")
    test_name = "test_setup_testing_patient_mapping"

    FileToFhirTestRunner(
        spark_session=spark_session, data_dir=data_dir, test_name=test_name
    ).run_test()

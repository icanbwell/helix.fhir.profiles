import logging
import os
import shutil
import random
import string
from pathlib import Path
from typing import Any, Optional, List

from pyspark.sql import SparkSession

# from spark_pipeline_framework.utilities.udf_registrar.v1.udf_registrar import (
#     register_udfs,
# )


class SparkTestHelper:
    current_spark_session: Optional[SparkSession] = None

    @staticmethod
    def quiet_py4j() -> None:
        """turn down spark logging for the test context"""
        logger = logging.getLogger("py4j")
        logger.setLevel(logging.ERROR)

    @staticmethod
    def clean_spark_dir() -> None:
        """

        :return:
        """
        try:
            if os.path.exists("./derby.log") and os.path.isfile("./derby.log"):
                os.remove("./derby.log")
            if os.path.exists("./metastore_db") and os.path.isdir("./metastore_db"):
                shutil.rmtree("./metastore_db")
            if os.path.exists("./spark-warehouse") and os.path.isdir(
                "./spark-warehouse"
            ):
                shutil.rmtree("./spark-warehouse")
        except OSError:
            pass

    @staticmethod
    def clean_spark_session(session: SparkSession) -> None:
        """

        :param session:
        :return:
        """
        tables = session.catalog.listTables("default")

        for table in tables:
            print(f"Dropping table: {table.name}")
            # noinspection SqlDialectInspection,SqlNoDataSourceInspection
            session.sql(f"DROP TABLE IF EXISTS default.{table.name}")
            # noinspection SqlDialectInspection,SqlNoDataSourceInspection
            session.sql(f"DROP VIEW IF EXISTS default.{table.name}")
            # noinspection SqlDialectInspection,SqlNoDataSourceInspection
            session.sql(f"DROP VIEW IF EXISTS {table.name}")

        session.catalog.clearCache()

    @staticmethod
    def clean_close(session: SparkSession) -> None:
        """

        :param session:
        :return:
        """
        SparkTestHelper.clean_spark_session(session)
        SparkTestHelper.clean_spark_dir()
        session.stop()

    @staticmethod
    def get_random_string(length: int) -> str:
        letters = string.ascii_lowercase
        result_str = "".join(random.choice(letters) for _ in range(length))
        return result_str

    @staticmethod
    def create_or_reuse_test_spark_session(
        request: Any, memory: Optional[str] = None
    ) -> SparkSession:
        # check that the working directory is top level or Spark will throw an error:
        # "module transformer was not found"
        current_working_directory = os.getcwd()
        if current_working_directory.startswith("/opt/project"):
            os.chdir("/opt/project")
        elif current_working_directory.startswith("/helix.pipelines"):
            os.chdir("/helix.pipelines")
        current_working_directory = os.getcwd()
        assert current_working_directory in ["/opt/project", "/helix.pipelines"], (
            f"Working directory [{current_working_directory}] must be top level"
            + " (i.e., /opt/project or /helix.pipelines) "
            + "or Spark will complain: 'module transformer not found'."
            + " You can chance in Run/Debug configuration in PyCharm."
        )
        if SparkTestHelper.current_spark_session is None:
            SparkTestHelper.current_spark_session = (
                SparkTestHelper.create_test_spark_session(
                    request=request, memory=memory
                )
            )

        SparkTestHelper.clean_spark_session(SparkTestHelper.current_spark_session)
        return SparkTestHelper.current_spark_session

    @staticmethod
    def _get_bsights_engine_jar_file(lib_dir: Path) -> str:
        bsights_engine_jar_file: str = ""
        bsights_engine_files: List[str] = [
            file for file in os.listdir(lib_dir) if "bsights-engine" in file
        ]
        if not len(bsights_engine_files) > 0:
            raise FileNotFoundError("bsights engine jar library file NOT FOUND!")

        bsights_engine_jar_file = bsights_engine_files[0]

        # debug
        print(f"\nbsights_engine_jar_file: {bsights_engine_jar_file}")

        return bsights_engine_jar_file

    # noinspection PyUnusedLocal
    @staticmethod
    def create_test_spark_session(
        request: Any, memory: Optional[str] = None
    ) -> SparkSession:

        # import better_exceptions
        #
        # better_exceptions.MAX_LENGTH = None
        # # Check if you TERM variable is set to `xterm`, if not set below variable,
        # # See issue: https://github.com/Qix-/better-exceptions/issues/8
        # better_exceptions.SUPPORTS_COLOR = True
        # better_exceptions.hook()

        # make sure env variables are set correctly
        if "SPARK_HOME" not in os.environ:
            os.environ["SPARK_HOME"] = "/usr/local/opt/spark"

        SparkTestHelper.clean_spark_dir()

        lib_dir: Path = Path("/opt/spark/jars/")
        bsights_engine_jar_file: str = SparkTestHelper._get_bsights_engine_jar_file(
            lib_dir
        )
        udf_bsights_engine_jar: Path = lib_dir / bsights_engine_jar_file

        if os.environ.get("SPARK_IN_DOCKER"):
            master: str = "spark://spark:7077"
            print(f"++++++ Running on docker spark: {master} ++++")
        else:
            master = "local[2]"
            print(f"++++++ Running on local spark: {master} ++++")

        spark_event_log_dir: str = "/tmp/spark-events"
        # use a random string to get a different app name every time and not reuse the same app name across tests
        session = (
            SparkSession.builder.appName(
                f"pytest-pyspark-local-testing-{SparkTestHelper.get_random_string(4)}"
            )
            .master(master)
            .config("spark.ui.showConsoleProgress", "false")
            .config("spark.driver.memory", memory or "4g")
            .config("spark.executor.memory", memory or "4g")
            # .config("spark.executor.memoryOverhead", "4096")
            # .config('spark.dynamicAllocation.enabled', True)
            # .config('spark.shuffle.service.enabled', True)
            # .config("spark.sql.shuffle.partitions", "2")
            # .config("spark.default.parallelism", "4")
            .config("spark.sql.broadcastTimeout", "2400")
            .config("spark.executorEnv.AWS_ACCESS_KEY_ID", "testing")
            .config("spark.executorEnv.AWS_SECRET_ACCESS_KEY", "testing")
            .config("spark.executorEnv.AWS_SECURITY_TOKEN", "testing")
            .config("spark.executorEnv.AWS_SESSION_TOKEN", "testing")
            .config("spark.executorEnv.AWS_SESSION_TOKEN", "testing")
            .config("spark.sql.pyspark.inferNestedDictAsStruct.enabled", "true")
            .config(
                "spark.driver.maxResultSize", "1g"
            )  # https://spark.apache.org/docs/latest/sql-performance-tuning.html
            .config(
                "spark.sql.autoBroadcastJoinThreshold", "-1"
            )  # not needed on local tests since we have only one node
            .config(
                "spark.default.parallelism", "1"
            )  # not needed on local tests since we have only one node
            .config(
                "spark.sql.shuffle.partitions", "1"
            )  # not needed on local tests since we have only one node
            .config(f"spark.eventLog.dir", spark_event_log_dir)
            .config(f"spark.eventLog.enabled", "true")
            .config(
                "spark.jars.packages",
                "com.databricks:spark-xml_2.12:0.15.0",
            )
            .config("spark.jars", udf_bsights_engine_jar.as_uri())
            # .config('spark.submit.pyFiles', '/helix.pipelines')
            # .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
            .enableHiveSupport()
            .getOrCreate()
        )

        configurations = session.sparkContext.getConf().getAll()
        for item in configurations:
            print(item)

        register_udfs(session)

        # request.addfinalizer(lambda: SparkTestHelper.clean_close(session))
        SparkTestHelper.quiet_py4j()
        return session

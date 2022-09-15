FROM imranq2/helix.spark:3.3.0.1-slim
# https://github.com/icanbwell/helix.spark
USER root

ENV PYTHONPATH=/helix.fhir.profiles
ENV CLASSPATH=/helix_fhir_profiles/jars:$CLASSPATH

# remove the older version of entrypoints with apt-get because that is how it was installed
RUN apt-get remove python3-entrypoints -y

COPY Pipfile* /helix.fhir.profiles/
WORKDIR /helix.fhir.profiles

RUN df -h # for space monitoring
RUN pipenv sync --dev --system
#RUN python3 -m pip install --upgrade pip && python -m pip install --no-cache-dir pipenv
#RUN pipenv lock && pipenv sync --dev --system && pipenv-setup sync --pipfile


# COPY ./jars/* /opt/bitnami/spark/jars/
# COPY ./conf/* /opt/bitnami/spark/conf/

# override entrypoint to remove extra logging
RUN mv /opt/minimal_entrypoint.sh /opt/entrypoint.sh

COPY . /helix.fhir.profiles

# run pre-commit once so it installs all the hooks and subsequent runs are fast
# RUN pre-commit install
RUN df -h # for space monitoring
RUN mkdir -p /fhir && chmod 777 /fhir
RUN mkdir -p /.local/share/virtualenvs && chmod 777 /.local/share/virtualenvs
# USER 1001
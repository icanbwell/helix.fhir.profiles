from typing import Any, Dict, List

from spark_auto_mapper.helpers.automapper_helpers import AutoMapperHelpers as A
from spark_auto_mapper.automappers.automapper import AutoMapper
from spark_auto_mapper_fhir.complex_types.coding import Coding
from spark_auto_mapper_fhir.fhir_types.id import FhirId
from spark_auto_mapper_fhir.complex_types.meta import Meta
from spark_auto_mapper_fhir.fhir_types.list import FhirList
from spark_auto_mapper_fhir.resources.patient import Patient


def mapping(parameters: Dict[str, Any]) -> List[AutoMapper]:
    mapper = AutoMapper(
        view=parameters["view_patient"],
        source_view=parameters["view_input"],
    ).complex(
        Patient(
            id_=FhirId(A.column("foo")),
            meta=Meta(
                source=A.text("https://www.icanbwell.com"),
                security=FhirList(
                    [
                        Coding(
                            system=A.text("https://www.icanbwell.com/owner"),
                            code=A.text("bwell")
                        ),
                        Coding(
                            system=A.text("https://www.icanbwell.com/access"),
                            code=A.text("bwell")
                        )
                    ]
                ),
            ),
        )
    )

    return [mapper]

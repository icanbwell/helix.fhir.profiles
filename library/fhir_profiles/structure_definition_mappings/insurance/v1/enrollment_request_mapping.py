from typing import Dict, Any, List

from library.fhir_profiles.structure_definition_mappings.eligibility.v1.patient_mapping import (
    ProfilePatient,
)
from spark_auto_mapper.automappers.automapper import AutoMapper
from spark_auto_mapper.data_types.text_like_base import AutoMapperTextLikeBase
from spark_auto_mapper.helpers.automapper_helpers import AutoMapperHelpers as A
from spark_auto_mapper_fhir.backbone_elements.element_definition import (
    ElementDefinition,
)
from spark_auto_mapper_fhir.backbone_elements.element_definition_type import (
    ElementDefinitionType,
)
from spark_auto_mapper_fhir.fhir_types.id import FhirId
from spark_auto_mapper_fhir.fhir_types.list import FhirList

from library.fhir_profiles.data_elements.v1.meta_element import (
    DataElementMeta,
)
from library.fhir_profiles.schema.v1.profile_definition_schema import (
    ProfileDefinition,
)


class ProfileEnrollmentRequest:
    @staticmethod
    def get_profile_id() -> AutoMapperTextLikeBase:
        return A.text("pr-enrollment-request")

    @staticmethod
    def get_profile_url() -> AutoMapperTextLikeBase:
        return A.concat(
            ProfileDefinition.get_url_base(), ProfileEnrollmentRequest.get_profile_id()
        )


def mapping(parameters: Dict[str, Any]) -> List[AutoMapper]:
    resource = A.text("EnrollmentRequest")

    mapper = AutoMapper(
        view=parameters["view_enrollment_request"],
        source_view=parameters["view_profile_config"],
        use_schema=False,
    ).complex(
        ProfileDefinition(
            profile_id=FhirId(ProfileEnrollmentRequest.get_profile_id()),
            profile_name="Enrollment Request",
            computer_friendly_profile_name="EnrollmentRequest",
            fhir_resource_type="EnrollmentRequest",
            description="Enrollment Request",
            differential_elements=FhirList(
                [
                    ElementDefinition(id_=resource, path=resource),
                    ElementDefinition(
                        id_=A.concat(resource, ".id"),
                        path=A.concat(resource, ".id"),
                        short="unique identifier for patient that enrolls in a specific program.",
                        comment="Program Short Name - MBI",
                    ),
                ],
                True,
            )
            # META
            .concat(DataElementMeta.get_meta(resource=resource)).concat(
                FhirList(
                    [
                        # CREATED
                        ElementDefinition(
                            id_=A.concat(resource, ".created"),
                            path=A.concat(resource, ".created"),
                            short="Creation date",
                            definition="date when the request was submitted.",
                            type_=FhirList([ElementDefinitionType(code="dateTime")]),
                            mustSupport=A.boolean(True),
                        ),
                        # CANDIDATE
                        ElementDefinition(
                            id_=A.concat(resource, ".candidate"),
                            path=A.concat(resource, ".candidate"),
                            short="links back to the patient profile",
                            type_=FhirList(
                                [
                                    ElementDefinitionType(
                                        code="Reference",
                                        targetProfile=FhirList(
                                            [ProfilePatient.get_profile_url()]
                                        ),
                                    )
                                ]
                            ),
                            mustSupport=A.boolean(True),
                        ),
                    ],
                    True,
                ),
            ),
        )
    )

    return [mapper]

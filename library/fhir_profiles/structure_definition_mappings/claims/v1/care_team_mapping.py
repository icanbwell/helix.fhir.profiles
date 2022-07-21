from typing import Dict, Any, List

from spark_auto_mapper_fhir.value_sets.generic_type import GenericTypeCode
from spark_auto_mapper_fhir.value_sets.snomed_ct import SNOMED_CTCode

from library.fhir_profiles.schema.v1.file_type_category_codes import (
    FileTypeCategoryCode,
    FileTypeCategoryCodeValues,
)
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
from spark_auto_mapper_fhir.complex_types.codeable_concept import CodeableConcept
from spark_auto_mapper_fhir.complex_types.coding import Coding
from spark_auto_mapper_fhir.fhir_types.id import FhirId
from spark_auto_mapper_fhir.fhir_types.list import FhirList
from spark_auto_mapper_fhir.value_sets.loinc_codes import LOINCCodesCode

from library.fhir_profiles.data_elements.v1.identifier_element import (
    DataElementIdentifier,
)
from library.fhir_profiles.data_elements.v1.meta_element import (
    DataElementMeta,
)
from library.fhir_profiles.structure_definition_mappings.provider_roster.v1.practitioner_mapping import (
    ProfilePractitioner,
)
from library.fhir_profiles.schema.v1.profile_definition_schema import (
    ProfileDefinition,
)


class ProfileCareTeam:
    @staticmethod
    def get_profile_id() -> AutoMapperTextLikeBase:
        return A.text("pr-care-team")

    @staticmethod
    def get_profile_url() -> AutoMapperTextLikeBase:
        return A.concat(
            ProfileDefinition.get_url_base(), ProfileCareTeam.get_profile_id()
        )


def mapping(parameters: Dict[str, Any]) -> List[AutoMapper]:
    resource = A.text("CareTeam")

    mapper = AutoMapper(
        view=parameters["view_care_team"],
        source_view=parameters["view_profile_config"],
        use_schema=False,
    ).complex(
        ProfileDefinition(
            profile_id=FhirId(ProfileCareTeam.get_profile_id()),
            profile_name="Care Team",
            computer_friendly_profile_name="CareTeam",
            fhir_resource_type="CareTeam",
            description="Providers associated to a patient's medical care",
            keyword=FhirList(
                [
                    Coding(
                        system=FileTypeCategoryCode.codeset,
                        code=FileTypeCategoryCodeValues.MedicalClaimsFile,
                    ),
                    Coding(
                        system=FileTypeCategoryCode.codeset,
                        code=FileTypeCategoryCodeValues.ElibilityFile,
                    ),
                ]
            ),
            differential_elements=FhirList(
                [
                    ElementDefinition(id_=resource, path=resource),
                    ElementDefinition(
                        id_=A.concat(resource, ".id"), path=A.concat(resource, ".id")
                    ),
                ],
                True,
            )
            # META
            .concat(DataElementMeta.get_meta(resource=resource))
            # IDENTIFIER
            .concat(DataElementIdentifier.get_identifier_any(resource=resource)).concat(
                FhirList(
                    [
                        # STATUS
                        ElementDefinition(
                            id_=A.concat(resource, ".status"),
                            path=A.concat(resource, ".status"),
                            comment="default to active",
                            min=1,
                            mustSupport=A.boolean(True),
                        ),
                        # CATEGORY
                        ElementDefinition(
                            id_=A.concat(resource, ".category"),
                            path=A.concat(resource, ".category"),
                            min=1,
                            max="1",
                            patternCodeableConcept=CodeableConcept(
                                coding=FhirList(
                                    [
                                        Coding(
                                            system=LOINCCodesCode.codeset,
                                            code=GenericTypeCode("LA28865-6"),
                                            display="Longitudinal care-coordination focused care team",
                                        )
                                    ]
                                )
                            ),
                            mustSupport=A.boolean(True),
                        ),
                        # NAME
                        ElementDefinition(
                            id_=A.concat(resource, ".name"),
                            path=A.concat(resource, ".name"),
                            short="name of the care team",
                            mustSupport=A.boolean(True),
                        ),
                        # SUBJECT
                        ElementDefinition(
                            id_=A.concat(resource, ".subject"),
                            path=A.concat(resource, ".subject"),
                            label="patient",
                            short="The patient",
                            min=1,
                            max="1",
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
                        # encounter = 0
                        ElementDefinition(
                            id_=A.concat(resource, ".encounter"),
                            path=A.concat(resource, ".encounter"),
                            max="0",
                        ),
                        # PARTICIPANT
                        # todo make element definition
                        ElementDefinition(
                            id_=A.concat(resource, ".participant"),
                            path=A.concat(resource, ".participant"),
                            short="providers included in this care team",
                            min=1,
                            max="*",
                            mustSupport=A.boolean(True),
                        ),
                        ElementDefinition(
                            id_=A.concat(resource, ".participant.id"),
                            path=A.concat(resource, ".participant.id"),
                            min=1,
                            mustSupport=A.boolean(True),
                        ),
                        ElementDefinition(
                            id_=A.concat(resource, ".participant.role"),
                            path=A.concat(resource, ".participant.role"),
                            #
                            patternCodeableConcept=CodeableConcept(
                                coding=FhirList(
                                    [
                                        Coding(
                                            system=SNOMED_CTCode.codeset,
                                            code=GenericTypeCode("223366009"),
                                            display="Healthcare Professional",
                                        )
                                    ]
                                )
                            ),
                            mustSupport=A.boolean(True),
                        ),
                        ElementDefinition(
                            id_=A.concat(resource, ".participant.member"),
                            path=A.concat(resource, ".participant.member"),
                            min=1,
                            type_=FhirList(
                                [
                                    ElementDefinitionType(
                                        code="Reference",
                                        targetProfile=FhirList(
                                            [ProfilePractitioner.get_profile_url()]
                                        ),
                                    )
                                ]
                            ),
                            mustSupport=A.boolean(True),
                        ),
                    ]
                )
            ),
        )
    )

    return [mapper]

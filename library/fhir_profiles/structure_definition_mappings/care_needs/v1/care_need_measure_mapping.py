from typing import Dict, Any, List

from spark_auto_mapper.automappers.automapper import AutoMapper
from spark_auto_mapper.data_types.text_like_base import AutoMapperTextLikeBase
from spark_auto_mapper.helpers.automapper_helpers import AutoMapperHelpers as A
from spark_auto_mapper_fhir.backbone_elements.element_definition import (
    ElementDefinition,
)

from spark_auto_mapper_fhir.backbone_elements.element_definition_example import (
    ElementDefinitionExample,
)
from spark_auto_mapper_fhir.backbone_elements.element_definition_type import (
    ElementDefinitionType,
)
from spark_auto_mapper_fhir.complex_types.codeable_concept import CodeableConcept
from spark_auto_mapper_fhir.complex_types.coding import Coding
from spark_auto_mapper_fhir.complex_types.period import Period
from spark_auto_mapper_fhir.fhir_types.id import FhirId
from spark_auto_mapper_fhir.fhir_types.list import FhirList
from spark_auto_mapper_fhir.value_sets.subject_type import (
    SubjectTypeCode,
    SubjectTypeCodeValues,
)

from library.fhir_profiles.data_elements.v1.meta_element import (
    DataElementMeta,
)
from library.fhir_profiles.schema.v1.profile_definition_schema import (
    ProfileDefinition,
)


class ProfileCareNeedMeasure:
    @staticmethod
    def get_profile_id() -> AutoMapperTextLikeBase:
        return A.text("pr-care-need-measure")

    @staticmethod
    def get_profile_url() -> AutoMapperTextLikeBase:
        return A.concat(
            ProfileDefinition.get_url_base(), ProfileCareNeedMeasure.get_profile_id()
        )


def mapping(parameters: Dict[str, Any]) -> List[AutoMapper]:
    resource = A.text("Measure")

    mapper = AutoMapper(
        view=parameters["view_care_need_measure"],
        source_view=parameters["view_profile_config"],
        use_schema=False,
    ).complex(
        ProfileDefinition(
            profile_id=FhirId(ProfileCareNeedMeasure.get_profile_id()),
            profile_name="Care Need Measure",
            computer_friendly_profile_name="CareNeedMeasure",
            fhir_resource_type="Measure",
            description="TBD",
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
            .concat(DataElementMeta.get_meta(resource=resource)).concat(
                FhirList(
                    [
                        ElementDefinition(
                            id_=A.concat(resource, ".url"),
                            path=A.concat(resource, ".url"),
                            mustSupport=A.boolean(True),
                        ),
                        ElementDefinition(
                            id_=A.concat(resource, ".name"),
                            path=A.concat(resource, ".name"),
                            min=1,
                            mustSupport=A.boolean(True),
                        ),
                        ElementDefinition(
                            id_=A.concat(resource, ".title"),
                            path=A.concat(resource, ".title"),
                            min=1,
                            mustSupport=A.boolean(True),
                        ),
                        ElementDefinition(
                            id_=A.concat(resource, ".status"),
                            path=A.concat(resource, ".status"),
                            short="resource status",
                            comment="default to active",
                            mustSupport=A.boolean(True),
                        ),
                        ElementDefinition(
                            id_=A.concat(resource, ".subjectCodeableConcept"),
                            path=A.concat(resource, ".subject[x]"),
                            type_=FhirList(
                                [ElementDefinitionType(code="CodeableConcept")]
                            ),
                            patternCodeableConcept=CodeableConcept(
                                coding=FhirList(
                                    [
                                        Coding(
                                            id_="subject",
                                            system=SubjectTypeCode.codeset,
                                            code=SubjectTypeCodeValues.Patient,
                                        )
                                    ]
                                )
                            ),
                            mustSupport=A.boolean(True),
                        ),
                        ElementDefinition(
                            id_=A.concat(resource, ".effectivePeriod"),
                            path=A.concat(resource, ".effectivePeriod"),
                            min=1,
                            type_=FhirList([ElementDefinitionType(code="Period")]),
                            example=FhirList(
                                [
                                    ElementDefinitionExample(
                                        label="Calendar year 2022",
                                        valuePeriod=Period(start=A.text("2022")),
                                    )
                                ]
                            ),
                            mustSupport=A.boolean(True),
                        ),
                        ElementDefinition(
                            id_=A.concat(resource, ".library"),
                            path=A.concat(resource, ".library"),
                            short="care need identifier",
                            mustSupport=A.boolean(True),
                        ),
                        ElementDefinition(
                            id_=A.concat(resource, ".definition"),
                            path=A.concat(resource, ".definition"),
                            short="measure description",
                            min=1,
                            max="*",
                            mustSupport=A.boolean(True),
                        ),
                    ],
                    True,
                ),
            ),
        )
    )

    return [mapper]

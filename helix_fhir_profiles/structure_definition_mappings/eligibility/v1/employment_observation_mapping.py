from typing import Dict, Any, List

from spark_auto_mapper_fhir.backbone_elements.element_definition_binding import (
    ElementDefinitionBinding,
)
from spark_auto_mapper_fhir.value_sets.binding_strength import BindingStrengthCodeValues
from spark_auto_mapper_fhir.value_sets.generic_type import GenericTypeCode

from helix_fhir_profiles.schema.v1.file_type_category_codes import (
    FileTypeCategoryCode,
    FileTypeCategoryCodeValues,
)
from helix_fhir_profiles.structure_definition_mappings.eligibility.v1.patient_mapping import (
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
from spark_auto_mapper_fhir.value_sets.observation_category_codes import (
    ObservationCategoryCodesCodeValues,
    ObservationCategoryCodesCode,
)

from helix_fhir_profiles.data_elements.v1.extension_element import (
    DataElementExtension,
)
from helix_fhir_profiles.data_elements.v1.identifier_element import (
    DataElementIdentifier,
)
from helix_fhir_profiles.data_elements.v1.meta_element import (
    DataElementMeta,
)
from helix_fhir_profiles.schema.v1.profile_definition_schema import (
    ProfileDefinition,
)


class ProfileEmploymentObservation:
    @staticmethod
    def get_profile_id() -> AutoMapperTextLikeBase:
        return A.text("pr-employment-observation")

    @staticmethod
    def get_profile_url() -> AutoMapperTextLikeBase:
        return A.concat(
            ProfileDefinition.get_url_base(),
            ProfileEmploymentObservation.get_profile_id(),
        )


def mapping(parameters: Dict[str, Any]) -> List[AutoMapper]:
    resource = A.text("Observation")

    mapper = AutoMapper(
        view=parameters["view_employment_observation"],
        source_view=parameters["view_profile_config"],
        use_schema=False,
    ).complex(
        ProfileDefinition(
            profile_id=FhirId(ProfileEmploymentObservation.get_profile_id()),
            profile_name=A.text("Employment Observation"),
            computer_friendly_profile_name=A.text("EmploymentObservation"),
            fhir_resource_type=resource,
            description=A.text("A social-history observation of an employment status"),
            keyword=FhirList(
                [
                    Coding(
                        system=FileTypeCategoryCode.codeset,
                        code=FileTypeCategoryCodeValues.EmployeeFile,
                    )
                ]
            ),
            differential_elements=FhirList(
                [
                    ElementDefinition(id_=resource, path=resource),
                    ElementDefinition(
                        id_=A.concat(resource, ".id"),
                        path=A.concat(resource, ".id"),
                    ),
                ],
                True,
            )
            # META
            .concat(DataElementMeta.get_meta(resource=resource))
            # EXTENSIONS
            .concat(DataElementExtension.get_extension_any(resource=resource)).concat(
                DataElementExtension.get_employer_organization(resource=resource)
            )
            # IDENTIFIERS
            .concat(DataElementIdentifier.get_identifier_any(resource=resource))
            .concat(DataElementIdentifier.get_employee_id(resource=resource))
            .concat(DataElementIdentifier.get_member_number(resource=resource))
            .concat(
                FhirList(
                    [
                        # STATUS
                        ElementDefinition(
                            id_=A.concat(resource, ".status"),
                            path=A.concat(resource, ".status"),
                            short="fixed: final",
                            mustSupport=A.boolean(True),
                        ),
                        # CATEGORY
                        ElementDefinition(
                            id_=A.concat(resource, ".category"),
                            path=A.concat(resource, ".category"),
                            short="fixed: social-history",
                            min=1,
                            type_=FhirList(
                                [ElementDefinitionType(code="CodeableConcept")]
                            ),
                            patternCodeableConcept=CodeableConcept(
                                coding=FhirList(
                                    [
                                        Coding(
                                            system=ObservationCategoryCodesCode.codeset,
                                            code=ObservationCategoryCodesCodeValues.SocialHistory,
                                        )
                                    ]
                                )
                            ),
                            mustSupport=A.boolean(True),
                        ),
                        # CODE
                        ElementDefinition(
                            id_=A.concat(resource, ".code"),
                            path=A.concat(resource, ".code"),
                            short="fixed: 74165-2 History of employment status",
                            definition="the coded value to indicate this record represents an employment status",
                            min=1,
                            type_=FhirList(
                                [ElementDefinitionType(code="CodeableConcept")]
                            ),
                            patternCodeableConcept=CodeableConcept(
                                coding=FhirList(
                                    [
                                        Coding(
                                            system=LOINCCodesCode.codeset,
                                            code=GenericTypeCode("74165-2"),
                                            display="History of employment status",
                                        )
                                    ]
                                )
                            ),
                            mustSupport=A.boolean(True),
                        ),
                        # SUBJECT
                        ElementDefinition(
                            id_=A.concat(resource, ".subject"),
                            path=A.concat(resource, ".subject"),
                            short="Reference to Employee or Beneficiary record",
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
                        ElementDefinition(
                            id_=A.concat(resource, ".focus"),
                            path=A.concat(resource, ".focus"),
                            min=0,
                        ),
                        ElementDefinition(
                            id_=A.concat(resource, ".encounter"),
                            path=A.concat(resource, ".encounter"),
                            min=0,
                        ),
                        # EFFECTIVE
                        ElementDefinition(
                            id_=A.concat(resource, ".effectivePeriod"),
                            path=A.concat(resource, ".effective[x]"),
                            short="employment period (hire date / terminiation date)",
                            type_=FhirList([ElementDefinitionType(code="Period")]),
                            mustSupport=A.boolean(True),
                        ),
                        # VALUE
                        ElementDefinition(
                            id_=A.concat(resource, ".value"),
                            path=A.concat(resource, ".value"),
                            short="coded employment status",
                            min=1,
                            max="1",
                            type_=FhirList(
                                [ElementDefinitionType(code="CodeableConcept")]
                            ),
                            binding=ElementDefinitionBinding(
                                strength=BindingStrengthCodeValues.Extensible,
                                valueSet="https://www.hl7.org/fhir/us/bwell/bwell-vs-employment-status",  # todo move to its own def
                            ),
                            mustSupport=A.boolean(True),
                        ),
                        # Excluded elements
                        ElementDefinition(
                            id_=A.concat(resource, ".dataAbsentReason"),
                            path=A.concat(resource, ".dataAbsentReason"),
                            min=0,
                        ),
                        ElementDefinition(
                            id_=A.concat(resource, ".interpretation"),
                            path=A.concat(resource, ".interpretation"),
                            min=0,
                        ),
                        ElementDefinition(
                            id_=A.concat(resource, ".bodySite"),
                            path=A.concat(resource, ".bodySite"),
                            min=0,
                        ),
                        ElementDefinition(
                            id_=A.concat(resource, ".method"),
                            path=A.concat(resource, ".method"),
                            min=0,
                        ),
                        ElementDefinition(
                            id_=A.concat(resource, ".specimen"),
                            path=A.concat(resource, ".specimen"),
                            min=0,
                        ),
                        ElementDefinition(
                            id_=A.concat(resource, ".device"),
                            path=A.concat(resource, ".device"),
                            min=0,
                        ),
                        ElementDefinition(
                            id_=A.concat(resource, ".referenceRange"),
                            path=A.concat(resource, ".referenceRange"),
                            min=0,
                        ),
                        ElementDefinition(
                            id_=A.concat(resource, ".hasMember"),
                            path=A.concat(resource, ".hasMember"),
                            min=0,
                        ),
                        # COMPONENT
                        # todo make element definition
                        ElementDefinition(
                            id_=A.concat(resource, ".component"),
                            path=A.concat(resource, ".component"),
                            short="other specific details about the employment",
                            min=0,
                            max="*",
                            mustSupport=A.boolean(True),
                        ),
                        ElementDefinition(
                            id_=A.concat(resource, ".component.id"),
                            path=A.concat(resource, ".component.id"),
                            min=1,
                            mustSupport=A.boolean(True),
                        ),
                        ElementDefinition(
                            id_=A.concat(resource, ".component.code"),
                            path=A.concat(resource, ".component.code"),
                            min=1,
                            mustSupport=A.boolean(True),
                        ),
                        ElementDefinition(
                            id_=A.concat(resource, ".component.value[x]"),
                            path=A.concat(resource, ".component.value[x]"),
                            min=1,
                            mustSupport=A.boolean(True),
                        )
                        #                 {
                        #                 "id": "Observation.component:source-detail",
                        #                 "path": "Observation.component",
                        #                 "sliceName": "source-detail",
                        #                 "short": "Includes but isn't limited to: original hire date, rehire date, effective date, line of business, ...",
                        #                 "definition": "Source details are frequently non-standard details received from an employment file. As such, the component.code is frequently defined with `system` = source URL, `code` = column name, & `value[x]` = field contents",
                        #                 "min": 0,
                        #                 "max": "1"
                        #             }
                    ]
                )
            ),
        )
    )

    return [mapper]

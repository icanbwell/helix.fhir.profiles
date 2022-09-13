from spark_auto_mapper.data_types.text_like_base import AutoMapperTextLikeBase
from spark_auto_mapper_fhir.backbone_elements.element_definition import (
    ElementDefinition,
)

from spark_auto_mapper.helpers.automapper_helpers import AutoMapperHelpers as A
from spark_auto_mapper_fhir.backbone_elements.element_definition_example import (
    ElementDefinitionExample,
)
from spark_auto_mapper_fhir.backbone_elements.element_definition_slicing import (
    ElementDefinitionSlicing,
)
from spark_auto_mapper_fhir.backbone_elements.element_definition_type import (
    ElementDefinitionType,
)
from spark_auto_mapper_fhir.complex_types.codeable_concept import CodeableConcept
from spark_auto_mapper_fhir.complex_types.coding import Coding
from spark_auto_mapper_fhir.fhir_types.list import FhirList
from spark_auto_mapper_fhir.value_sets.generic_type import GenericTypeCode
from spark_auto_mapper_fhir.value_sets.practice_setting_code_value_set import (
    PracticeSettingCodeValueSetCode,
    PracticeSettingCodeValueSetCodeValues,
)
from spark_auto_mapper_fhir.value_sets.slicing_rules import SlicingRulesCodeValues

from helix_fhir_profiles.schema.v1.product_feature_codes import (
    ProductFeatureCode,
    ProductFeatureCodeValues,
)


class DataElementPractitionerSpecialty:
    @staticmethod
    def get_practitioner_specialty_any(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "specialty"
        element = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".specialty"),
                    label=label,
                    code=FhirList(
                        [
                            Coding(
                                system=ProductFeatureCode.codeset,
                                code=ProductFeatureCodeValues.ProviderSearch,
                            )
                        ]
                    ),
                    slicing=ElementDefinitionSlicing(
                        description="slice by type", rules=SlicingRulesCodeValues.Open
                    ),
                    short="Practitioner's specialty",
                    definition="Includes: NUCC taxonomy codes, specialty aliases, etc",
                    # comment="",
                    # requirements="",
                    min=0,
                    max="*",
                    type_=FhirList([ElementDefinitionType(code="CodeableConcept")]),
                    example=FhirList(
                        [
                            ElementDefinitionExample(
                                label="Example specialty",
                                valueCodeableConcept=CodeableConcept(
                                    id_="1120",
                                    coding=FhirList(
                                        [
                                            Coding(
                                                id_="1120",
                                                system="https://www.kyruus.com/specialty",
                                                code=GenericTypeCode("1120"),
                                                display="Pediatrics",
                                            )
                                        ]
                                    ),
                                ),
                            )
                        ]
                    ),
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".id"),
                    path=A.concat(resource, ".specialty.id"),
                    label=label,
                    short="set to specialty code",
                    # definition="",
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="string")]),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".coding"),
                    path=A.concat(resource, ".specialty.coding"),
                    label=label,
                    # short="",
                    # definition="",
                    min=1,
                    max="*",
                    type_=FhirList([ElementDefinitionType(code="Coding")]),
                    example=FhirList(
                        [
                            ElementDefinitionExample(
                                label="A cardiology specialty",
                                valueCoding=Coding(
                                    id_="cardio",
                                    system=PracticeSettingCodeValueSetCode.codeset,
                                    code=PracticeSettingCodeValueSetCodeValues.Cardiology,
                                ),
                            )
                        ]
                    ),
                ),
            ],
            True,
        )
        return element

    @staticmethod
    def get_taxonomy_code(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "taxonomy-code"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".specialty"),
                    sliceName=label,
                    label=label,
                    code=FhirList(
                        [
                            Coding(
                                system=ProductFeatureCode.codeset,
                                code=ProductFeatureCodeValues.ProviderSearch,
                            ),
                        ]
                    ),
                    short="NUCC taxonomy code",
                    definition="Healthcare specialty NUCC taxonomy code",
                    comment="set raw value as code, with code.system representing source URL",
                    # requirements="",
                    min=0,
                    max="*",
                    type_=FhirList([ElementDefinitionType(code="CodeableConcept")]),
                    example=FhirList(
                        [
                            ElementDefinitionExample(
                                label="Example specialty taxonomy",
                                valueCodeableConcept=CodeableConcept(
                                    id_="1120-taxonomy",
                                    coding=FhirList(
                                        [
                                            Coding(
                                                id_="1120-taxonomy",
                                                system="http://nucc.org/provider-taxonomy",
                                                code=GenericTypeCode("208000000X"),
                                            )
                                        ]
                                    ),
                                ),
                            )
                        ]
                    ),
                )
            ]
        )

        return elements

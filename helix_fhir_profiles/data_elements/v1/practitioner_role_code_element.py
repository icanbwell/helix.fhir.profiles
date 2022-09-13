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
from spark_auto_mapper_fhir.value_sets.slicing_rules import SlicingRulesCodeValues

from helix_fhir_profiles.schema.v1.product_feature_codes import (
    ProductFeatureCode,
    ProductFeatureCodeValues,
)


class DataElementPractitionerRoleCode:
    @staticmethod
    def get_practitioner_role_code_any(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "practitioner-role-code"
        element = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".code"),
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
                    short="Practitioner role characteristic code",
                    # definition="",
                    # comment="",
                    # requirements="",
                    min=0,
                    max="*",
                    type_=FhirList([ElementDefinitionType(code="CodeableConcept")]),
                    example=FhirList(
                        [
                            ElementDefinitionExample(
                                label="PCP provider",
                                valueCodeableConcept=CodeableConcept(
                                    id_="characteristic",
                                    coding=FhirList(
                                        [
                                            Coding(
                                                id_="primary-care",
                                                system="http://nucc.org/provider-characteristics",
                                                version="5.0",
                                                code=GenericTypeCode("13"),
                                                display="This is a primary care provider",
                                            )
                                        ]
                                    ),
                                ),
                            ),
                            ElementDefinitionExample(
                                label="Not a PCP provider",
                                valueCodeableConcept=CodeableConcept(
                                    id_="characteristic",
                                    coding=FhirList(
                                        [
                                            Coding(
                                                id_="primary-care",
                                                display="This is not a primary care provider",
                                            )
                                        ]
                                    ),
                                ),
                            ),
                        ]
                    ),
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".id"),
                    path=A.concat(resource, ".code.id"),
                    label=label,
                    short="set to role code",
                    # definition="",
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="string")]),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".coding"),
                    path=A.concat(resource, ".code.coding"),
                    label=label,
                    # short="",
                    # definition="",
                    min=1,
                    max="*",
                    type_=FhirList([ElementDefinitionType(code="Coding")]),
                ),
            ],
            True,
        )
        return element

    @staticmethod
    def get_primary_care_characteristic(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "primary-care-characteristic"
        element = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".code"),
                    sliceName=label,
                    label=label,
                    code=FhirList(
                        [
                            Coding(
                                system=ProductFeatureCode.codeset,
                                code=ProductFeatureCodeValues.ProviderSearch,
                            )
                        ]
                    ),
                    short="Practitioner is a primary care provider",
                    definition="NUCC Characteristic code to indicate Primary Care",
                    # comment="",
                    # requirements="",
                    min=0,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="CodeableConcept")]),
                    fixedCodeableConcept=CodeableConcept(
                        id_="characteristic",
                        coding=FhirList(
                            [
                                Coding(
                                    id_="primary-care",
                                    system="http://nucc.org/provider-characteristics",
                                    version="5.0",
                                    code=GenericTypeCode("13"),
                                    display="This is a primary care provider",
                                )
                            ]
                        ),
                    ),
                    mustSupport=A.boolean(True),
                )
            ]
        )

        return element

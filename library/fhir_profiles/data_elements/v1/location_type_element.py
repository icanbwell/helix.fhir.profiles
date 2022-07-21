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
from spark_auto_mapper_fhir.complex_types.coding import Coding
from spark_auto_mapper_fhir.fhir_types.list import FhirList
from spark_auto_mapper_fhir.value_sets.service_delivery_location_role_type import (
    ServiceDeliveryLocationRoleType,
    ServiceDeliveryLocationRoleTypeValues,
)
from spark_auto_mapper_fhir.value_sets.slicing_rules import SlicingRulesCodeValues

from library.fhir_profiles.schema.v1.product_feature_codes import (
    ProductFeatureCode,
    ProductFeatureCodeValues,
)


class DataElementLocationType:
    @staticmethod
    def get_location_type_any(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "location-type"
        element = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".type"),
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
                    short="Type of function performed",
                    definition="Indicates the type of function performed at the location",
                    # comment="",
                    # requirements="",
                    min=1,
                    max="*",
                    type_=FhirList([ElementDefinitionType(code="CodeableConcept")]),
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".type.id"),
                    path=A.concat(resource, ".type.id"),
                    label=label,
                    short="set to type code",
                    # definition="",
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="string")]),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".type.coding"),
                    path=A.concat(resource, ".type.coding"),
                    label=label,
                    # short="",
                    # definition="",
                    min=1,
                    max="*",
                    type_=FhirList([ElementDefinitionType(code="Coding")]),
                    example=FhirList(
                        [
                            ElementDefinitionExample(
                                label="foo",
                                valueCoding=Coding(
                                    id_="bar",
                                    system=ServiceDeliveryLocationRoleType.codeset,
                                    code=ServiceDeliveryLocationRoleTypeValues.Laboratory,
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
    def get_location_specialty(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "specialty"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".type"),
                    sliceName=label,
                    label=label,
                    code=FhirList(
                        [
                            Coding(
                                system=ProductFeatureCode.codeset,
                                code=ProductFeatureCodeValues.IntegratedScheduling,
                            ),
                        ]
                    ),
                    short="location specialty",
                    # definition="",
                    comment="set raw value as code, with code.system representing source URL",
                    # requirements="",
                    min=1,
                    max="*",
                    type_=FhirList([ElementDefinitionType(code="CodeableConcept")]),
                    # exampleCodeableConcept
                )
            ]
        )

        return elements

    @staticmethod
    def get_covid_vaccine(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "covid-vaccine"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".type"),
                    sliceName=label,
                    label=label,
                    code=FhirList(
                        [
                            Coding(
                                system=ProductFeatureCode.codeset,
                                code=ProductFeatureCodeValues.IntegratedScheduling,
                            ),
                        ]
                    ),
                    short="COVID-19 Vaccine Site",
                    definition="Indicates if a location offers COVID-19 vaccines",
                    comment="Needs Review",
                    # requirements="",
                    min=0,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="CodeableConcept")]),
                    # patternCodeableConcept=CodeableConcept(
                    #     id_="",
                    #     coding=FhirList(
                    #         [
                    #             Coding(
                    #                 system="",
                    #                 code=""
                    #             )
                    #         ]
                    #     )
                    # )
                )
            ]
        )

        return elements

    @staticmethod
    def get_covid_testing(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "covid-test"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".type"),
                    sliceName=label,
                    label=label,
                    code=FhirList(
                        [
                            Coding(
                                system=ProductFeatureCode.codeset,
                                code=ProductFeatureCodeValues.IntegratedScheduling,
                            ),
                        ]
                    ),
                    short="COVID-19 Testing Site",
                    definition="Indicates if a location offers COVID-19 testing",
                    comment="Needs Review",
                    # requirements="",
                    min=0,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="CodeableConcept")]),
                    # patternCodeableConcept=CodeableConcept(
                    #     id_="",
                    #     coding=FhirList(
                    #         [
                    #             Coding(
                    #                 system="",
                    #                 code=""
                    #             )
                    #         ]
                    #     )
                    # )
                )
            ]
        )

        return elements

    @staticmethod
    def get_emergency_room(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "er-indicator"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".type"),
                    sliceName=label,
                    label=label,
                    code=FhirList(
                        [
                            Coding(
                                system=ProductFeatureCode.codeset,
                                code=ProductFeatureCodeValues.IntegratedScheduling,
                            ),
                        ]
                    ),
                    short="ER indicator",
                    definition="Indicates if a location is an Emergency Room",
                    comment="Needs Review",
                    # requirements="",
                    min=0,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="CodeableConcept")]),
                    # patternCodeableConcept=CodeableConcept(
                    #     id_="",
                    #     coding=FhirList(
                    #         [
                    #             Coding(
                    #                 system="",
                    #                 code=""
                    #             )
                    #         ]
                    #     )
                    # )
                )
            ]
        )

        return elements

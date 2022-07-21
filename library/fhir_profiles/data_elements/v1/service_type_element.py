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
from spark_auto_mapper_fhir.value_sets.service_type import (
    ServiceTypeCode,
    ServiceTypeCodeValues,
)
from spark_auto_mapper_fhir.value_sets.slicing_rules import SlicingRulesCodeValues

from library.fhir_profiles.schema.v1.product_feature_codes import (
    ProductFeatureCodeValues,
    ProductFeatureCode,
)


class DataElementServiceType:
    @staticmethod
    def get_service_type_any(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "service-type"
        element = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".serviceType"),
                    label=label,
                    slicing=ElementDefinitionSlicing(
                        description="slice by type", rules=SlicingRulesCodeValues.Open
                    ),
                    # short="",
                    # definition="",
                    # comment="",
                    # requirements="",
                    type_=FhirList([ElementDefinitionType(code="CodeableConcept")]),
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".id"),
                    path=A.concat(resource, ".serviceType.id"),
                    label=label,
                    short="set to service type code",
                    # definition="",
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="string")]),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".coding"),
                    path=A.concat(resource, ".serviceType.coding"),
                    label=label,
                    # short="",
                    # definition="",
                    min=1,
                    max="*",
                    type_=FhirList([ElementDefinitionType(code="Coding")]),
                    example=FhirList(
                        [
                            ElementDefinitionExample(
                                label="medical services",
                                valueCoding=Coding(
                                    id_="medical-services",
                                    system=ServiceTypeCode.codeset,
                                    code=ServiceTypeCodeValues.MedicalServices,
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
    def get_medical_services(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "medical-services"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".serviceType"),
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
                    short="medical services type code",
                    type_=FhirList([ElementDefinitionType(code="CodeableConcept")]),
                    patternCodeableConcept=CodeableConcept(
                        coding=FhirList(
                            [
                                Coding(
                                    id_="medical",
                                    system=ServiceTypeCode.codeset,
                                    code=ServiceTypeCodeValues.MedicalServices,
                                )
                            ]
                        )
                    ),
                )
            ]
        )

        return elements

    @staticmethod
    def get_appointment_type(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "appointment-type"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".serviceType"),
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
                    short="appointment types",
                    type_=FhirList([ElementDefinitionType(code="CodeableConcept")]),
                    example=FhirList(
                        [
                            ElementDefinitionExample(
                                label="healthcare appointment slot for an existing patient",
                                valueCodeableConcept=CodeableConcept(
                                    id_="appt-existing",
                                    coding=FhirList(
                                        [
                                            Coding(
                                                id_="existing",
                                                system="https://www.healthsystem.org",
                                                code=GenericTypeCode("existing"),
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

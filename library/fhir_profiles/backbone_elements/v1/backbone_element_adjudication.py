from spark_auto_mapper.data_types.text_like_base import AutoMapperTextLikeBase
from spark_auto_mapper_fhir.backbone_elements.element_definition import (
    ElementDefinition,
)

from spark_auto_mapper.helpers.automapper_helpers import AutoMapperHelpers as A
from spark_auto_mapper_fhir.backbone_elements.element_definition_slicing import (
    ElementDefinitionSlicing,
)
from spark_auto_mapper_fhir.backbone_elements.element_definition_type import (
    ElementDefinitionType,
)
from spark_auto_mapper_fhir.fhir_types.list import FhirList
from spark_auto_mapper_fhir.value_sets.slicing_rules import SlicingRulesCodeValues


class DataBackboneElementAdjudication:
    @staticmethod
    def get_adjudication_any(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "adjudication"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".adjudication"),
                    label=label,
                    slicing=ElementDefinitionSlicing(
                        description="slice by type", rules=SlicingRulesCodeValues.Open
                    ),
                    definition="Monetary figures including: payment, submitted, allowed, copay, deductible, coinsurance, and cob amounts",
                    type_=FhirList([ElementDefinitionType(code="BackboneElement")]),
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".id"),
                    path=A.concat(resource, ".adjudication.id"),
                    label=label,
                    short="set to category code",
                    min=1,
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".category"),
                    path=A.concat(resource, ".adjudication.category"),
                    label=label,
                    short="Amount type category",
                    min=1,
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".reason"),
                    path=A.concat(resource, ".adjudication.reason"),
                    label=label,
                    short="adjudication reason, if provided",
                    min=0,
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".amount"),
                    path=A.concat(resource, ".adjudication.amount"),
                    label=label,
                    short="Financial amount",
                    type_=FhirList([ElementDefinitionType(code="Money")]),
                    mustSupport=A.boolean(True),
                ),
            ],
            True,
        )

        return elements

    @staticmethod
    def get_submitted_amount(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "submitted-amount"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".adjudication"),
                    sliceName=label,
                    label=label,
                    slicing=ElementDefinitionSlicing(
                        description="slice by type", rules=SlicingRulesCodeValues.Open
                    ),
                    # comment="",
                    type_=FhirList([ElementDefinitionType(code="BackboneElement")]),
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".id"),
                    path=A.concat(resource, ".adjudication.id"),
                    label=label,
                    short="submitted",
                    min=1,
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".category"),
                    path=A.concat(resource, ".adjudication.category"),
                    label=label,
                    min=1,
                    type_=FhirList([ElementDefinitionType(code="CodeableConcept")]),
                    # patternCodeableConcept
                    mustSupport=A.boolean(True),
                ),
            ],
            True,
        )

        return elements

    @staticmethod
    def get_allowed_amount(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "allowed-amount"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".adjudication"),
                    sliceName=label,
                    label=label,
                    type_=FhirList([ElementDefinitionType(code="BackboneElement")]),
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".id"),
                    path=A.concat(resource, ".adjudication.id"),
                    label=label,
                    short="allowed",
                    min=1,
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".category"),
                    path=A.concat(resource, ".adjudication.category"),
                    label=label,
                    min=1,
                    type_=FhirList([ElementDefinitionType(code="CodeableConcept")]),
                    # patternCodeableConcept
                    mustSupport=A.boolean(True),
                ),
            ],
            True,
        )

        return elements

    @staticmethod
    def get_copay_amount(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "copay-amount"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".adjudication"),
                    sliceName=label,
                    label=label,
                    type_=FhirList([ElementDefinitionType(code="BackboneElement")]),
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".id"),
                    path=A.concat(resource, ".adjudication.id"),
                    label=label,
                    short="copay",
                    min=1,
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".category"),
                    path=A.concat(resource, ".adjudication.category"),
                    label=label,
                    min=1,
                    type_=FhirList([ElementDefinitionType(code="CodeableConcept")]),
                    # patternCodeableConcept
                    mustSupport=A.boolean(True),
                ),
            ],
            True,
        )

        return elements

    @staticmethod
    def get_payment_amount(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "payment-amount"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".adjudication"),
                    sliceName=label,
                    label=label,
                    # comment="",
                    type_=FhirList([ElementDefinitionType(code="BackboneElement")]),
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".id"),
                    path=A.concat(resource, ".adjudication.id"),
                    label=label,
                    short="payment",
                    min=1,
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".category"),
                    path=A.concat(resource, ".adjudication.category"),
                    label=label,
                    min=1,
                    type_=FhirList([ElementDefinitionType(code="CodeableConcept")]),
                    # patternCodeableConcept
                    mustSupport=A.boolean(True),
                ),
            ],
            True,
        )

        return elements

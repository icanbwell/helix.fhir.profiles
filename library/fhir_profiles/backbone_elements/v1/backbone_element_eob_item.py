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


class DataBackboneElementEOBItem:
    @staticmethod
    def get_eob_item_any(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "eob-item"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".item"),
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
                    path=A.concat(resource, ".item.id"),
                    label=label,
                    short="set to id of the claim line item",
                    comment="usually line number",
                    min=1,
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".sequence"),
                    path=A.concat(resource, ".item.sequence"),
                    label=label,
                    short="claim line number",
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".revenue"),
                    path=A.concat(resource, ".item.revenue"),
                    label=label,
                    short="Revenue center code",
                    requirements="required for institutional claims",
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".productOrService"),
                    path=A.concat(resource, ".item.productOrService"),
                    label=label,
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".modifier"),
                    path=A.concat(resource, ".item.modifier"),
                    label=label,
                    short="modifier to the product code",
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".servicedPeriod"),
                    path=A.concat(resource, ".item.serviced[x]"),
                    label=label,
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".quentity"),
                    path=A.concat(resource, ".item.quantity"),
                    label=label,
                    short="days / units",
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".unitPrice"),
                    path=A.concat(resource, ".item.unitPrice"),
                    label=label,
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".adjudication"),
                    path=A.concat(resource, ".item.adjudication"),
                    label=label,
                    mustSupport=A.boolean(True),
                ),
            ],
            True,
        )

        return elements

    @staticmethod
    def get_eob_drug_ndc(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "drug-ndc"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".item"),
                    sliceName=label,
                    label=label,
                    # comment="",
                    min=0,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="BackboneElement")]),
                ),
            ],
            True,
        )

        return elements

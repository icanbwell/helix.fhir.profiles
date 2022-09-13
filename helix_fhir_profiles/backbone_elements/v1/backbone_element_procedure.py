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
from spark_auto_mapper_fhir.complex_types.codeable_concept import CodeableConcept
from spark_auto_mapper_fhir.complex_types.coding import Coding
from spark_auto_mapper_fhir.fhir_types.list import FhirList
from spark_auto_mapper_fhir.value_sets.icd_10_procedure_codes import (
    ICD_10ProcedureCodesCode,
)
from spark_auto_mapper_fhir.value_sets.slicing_rules import SlicingRulesCodeValues


class DataBackboneElementProcedure:
    @staticmethod
    def get_procedure_any(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "procedure"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".procedure"),
                    label=label,
                    slicing=ElementDefinitionSlicing(
                        description="slice by type", rules=SlicingRulesCodeValues.Open
                    ),
                    min=0,
                    max="*",
                    type_=FhirList([ElementDefinitionType(code="BackboneElement")]),
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".id"),
                    path=A.concat(resource, ".procedure.id"),
                    label=label,
                    short="set to sequence number",
                    min=1,
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".sequence"),
                    path=A.concat(resource, ".procedure.sequence"),
                    label=label,
                    short="Claim line number",
                    min=1,
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".date"),
                    path=A.concat(resource, ".procedure.date"),
                    label=label,
                    short="date of service",
                    comment="When date of service is provided as a date range, use the starting ('from') date",
                    min=1,
                    type_=FhirList([ElementDefinitionType(code="dateTime")]),
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".procedureCodeableConcept"),
                    path=A.concat(resource, ".procedure.procedure[x]"),
                    label=label,
                    short="Procedure code",
                    min=1,
                    type_=FhirList([ElementDefinitionType(code="CodeableConcept")]),
                    # binding=ElementDefinitionBinding(
                    # strength=BindingStrengthCodeValues.Example,
                    # valueSet=ICD_10ProcedureCodesCode.codeset,
                    # ),
                    patternCodeableConcept=CodeableConcept(
                        coding=FhirList(
                            [Coding(system=ICD_10ProcedureCodesCode.codeset)]
                        )
                    ),
                    mustSupport=A.boolean(True),
                ),
            ],
            True,
        )

        return elements

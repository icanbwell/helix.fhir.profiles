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
from spark_auto_mapper_fhir.value_sets.example_diagnosis_type_codes import (
    ExampleDiagnosisTypeCodesCode,
)
from spark_auto_mapper_fhir.value_sets.slicing_rules import SlicingRulesCodeValues


class DataBackboneElementDiagnosis:
    @staticmethod
    def get_diagnosis_any(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "diagnosis"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".diagnosis"),
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
                    path=A.concat(resource, ".diagnosis.id"),
                    label=label,
                    short="set to sequence number",
                    min=1,
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".sequence"),
                    path=A.concat(resource, ".diagnosis.sequence"),
                    label=label,
                    min=1,
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".diagnosisCodeableConcept"),
                    path=A.concat(resource, ".diagnosis.diagnosis[x]"),
                    label=label,
                    short="ICD diagnosis code",
                    min=1,
                    type_=FhirList([ElementDefinitionType(code="CodeableConcept")]),
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".type"),
                    path=A.concat(resource, ".diagnosis.type"),
                    label=label,
                    comment="typically retrospective",
                    min=0,
                    type_=FhirList([ElementDefinitionType(code="CodeableConcept")]),
                    # binding=ElementDefinitionBinding(
                    #     strength=BindingStrengthCodeValues.Extensible,
                    #     valueSet=ExampleDiagnosisTypeCodesCode.codeset,
                    # ),
                    patternCodeableConcept=CodeableConcept(
                        coding=FhirList(
                            [Coding(system=ExampleDiagnosisTypeCodesCode.codeset)]
                        )
                    ),
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".onAdmission"),
                    path=A.concat(resource, ".diagnosis.onAdmission"),
                    label=label,
                    min=0,
                    type_=FhirList([ElementDefinitionType(code="CodeableConcept")]),
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".packageCode"),
                    path=A.concat(resource, ".diagnosis.packageCode"),
                    label="DRG",
                    short="DRG",
                    min=0,
                    type_=FhirList([ElementDefinitionType(code="CodeableConcept")]),
                    mustSupport=A.boolean(True),
                ),
            ],
            True,
        )

        return elements

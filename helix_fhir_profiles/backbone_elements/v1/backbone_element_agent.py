from spark_auto_mapper_fhir.complex_types.codeable_concept import CodeableConcept
from spark_auto_mapper_fhir.complex_types.coding import Coding
from spark_auto_mapper_fhir.value_sets.contract_signer_type_codes import (
    ContractSignerTypeCodesCode,
    ContractSignerTypeCodesCodeValues,
)

from helix_fhir_profiles.structure_definition_mappings.eligibility.v1.patient_mapping import (
    ProfilePatient,
)
from spark_auto_mapper.data_types.text_like_base import AutoMapperTextLikeBase
from spark_auto_mapper_fhir.backbone_elements.element_definition import (
    ElementDefinition,
)

from spark_auto_mapper.helpers.automapper_helpers import AutoMapperHelpers as A
from spark_auto_mapper_fhir.backbone_elements.element_definition_binding import (
    ElementDefinitionBinding,
)
from spark_auto_mapper_fhir.backbone_elements.element_definition_slicing import (
    ElementDefinitionSlicing,
)
from spark_auto_mapper_fhir.backbone_elements.element_definition_type import (
    ElementDefinitionType,
)
from spark_auto_mapper_fhir.fhir_types.list import FhirList
from spark_auto_mapper_fhir.value_sets.binding_strength import BindingStrengthCodeValues
from spark_auto_mapper_fhir.value_sets.slicing_rules import SlicingRulesCodeValues


class DataBackboneElementAgent:
    @staticmethod
    def get_agent_any(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "agent"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat(label),
                    path=A.concat(resource, ".agent"),
                    label=label,
                    slicing=ElementDefinitionSlicing(
                        description="slice by type", rules=SlicingRulesCodeValues.Open
                    ),
                    min=1,
                    max="*",
                    type_=FhirList([ElementDefinitionType(code="BackboneElement")]),
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat(label, ".id"),
                    path=A.concat(resource, ".agent.id"),
                    label=label,
                    short="set to type code",
                    min=1,
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat(label, ".type"),
                    path=A.concat(resource, ".agent.type"),
                    label=label,
                    type_=FhirList([ElementDefinitionType(code="CodeableConcept")]),
                    binding=ElementDefinitionBinding(
                        strength=BindingStrengthCodeValues.Extensible,
                        valueSet=ContractSignerTypeCodesCode.codeset,
                    ),
                    patternCodeableConcept=CodeableConcept(
                        coding=FhirList(
                            [
                                Coding(
                                    system=ContractSignerTypeCodesCode.codeset,
                                    code=ContractSignerTypeCodesCodeValues.Verifier,
                                )
                            ]
                        )
                    ),
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat(label, ".who"),
                    path=A.concat(resource, ".agent.who"),
                    label=label,
                    min=1,
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
            ],
            True,
        )

        return elements

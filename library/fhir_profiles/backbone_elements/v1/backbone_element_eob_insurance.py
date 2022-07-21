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

from library.fhir_profiles.structure_definition_mappings.claims.v1.insurance_coverage_mapping import (
    ProfileInsuranceCoverage,
)


class DataBackboneElementEOBInsurance:
    @staticmethod
    def get_eob_insurance_any(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "eob-insurance"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".insurance"),
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
                    id_=A.concat("de-", label, ".id"),
                    path=A.concat(resource, ".insurance.id"),
                    label=label,
                    short="set to reference id",
                    min=1,
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".focal"),
                    path=A.concat(resource, ".insurance.focal"),
                    label=label,
                    min=1,
                    type_=FhirList([ElementDefinitionType(code="boolean")]),
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".coverage"),
                    path=A.concat(resource, ".insurance.coverage"),
                    label=label,
                    min=1,
                    type_=FhirList(
                        [
                            ElementDefinitionType(
                                code="Reference",
                                targetProfile=FhirList(
                                    [ProfileInsuranceCoverage.get_profile_url()]
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

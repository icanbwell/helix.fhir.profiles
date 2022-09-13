from helix_fhir_profiles.structure_definition_mappings.provider_roster.v1.practitioner_mapping import (
    ProfilePractitioner,
)
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


class DataElementGroupMember:
    @staticmethod
    def get_group_member_any(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "group-member"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".member"),
                    label=label,
                    slicing=ElementDefinitionSlicing(
                        description="slice by types", rules=SlicingRulesCodeValues.Open
                    ),
                    # short="",
                    # definition="",
                    # comment="",
                    # requirements="",
                    type_=FhirList([ElementDefinitionType(code="BackboneElement")]),
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, "-id"),
                    path=A.concat(resource, ".member.id"),
                    label=label,
                    short="set to reference id",
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="string")]),
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, "-entity"),
                    path=A.concat(resource, ".member.entity"),
                    label=label,
                    short="practitioner",
                    min=1,
                    max="1",
                    type_=FhirList(
                        [
                            ElementDefinitionType(
                                code="Reference",
                                targetProfile=FhirList(
                                    [ProfilePractitioner.get_profile_url()]
                                ),
                            )
                        ]
                    ),
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, "-inactive"),
                    path=A.concat(resource, ".member.inactive"),
                    label=label,
                    short="active status",
                    comment="default to false",
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="boolean")]),
                    mustSupport=A.boolean(True),
                ),
            ],
            True,
        )

        return elements

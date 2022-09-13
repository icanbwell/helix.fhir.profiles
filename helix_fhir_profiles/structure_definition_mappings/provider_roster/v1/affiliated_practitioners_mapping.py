from typing import Dict, Any, List

from spark_auto_mapper.automappers.automapper import AutoMapper
from spark_auto_mapper.data_types.text_like_base import AutoMapperTextLikeBase
from spark_auto_mapper.helpers.automapper_helpers import AutoMapperHelpers as A
from spark_auto_mapper_fhir.backbone_elements.element_definition import (
    ElementDefinition,
)
from spark_auto_mapper_fhir.backbone_elements.element_definition_type import (
    ElementDefinitionType,
)
from spark_auto_mapper_fhir.complex_types.coding import Coding
from spark_auto_mapper_fhir.fhir_types.id import FhirId
from spark_auto_mapper_fhir.fhir_types.list import FhirList
from spark_auto_mapper_fhir.value_sets.group_type import GroupTypeCodeValues

from helix_fhir_profiles.backbone_elements.v1.backbone_element_group_member import (
    DataElementGroupMember,
)
from helix_fhir_profiles.data_elements.v1.meta_element import (
    DataElementMeta,
)
from helix_fhir_profiles.schema.v1.file_type_category_codes import (
    FileTypeCategoryCode,
    FileTypeCategoryCodeValues,
)
from helix_fhir_profiles.structure_definition_mappings.provider_roster.v1.healthcare_organization_mapping import (
    ProfileHealthcareOrganization,
)
from helix_fhir_profiles.schema.v1.profile_definition_schema import (
    ProfileDefinition,
)


class ProfileAffiliatedPractitioners:
    @staticmethod
    def get_profile_id() -> AutoMapperTextLikeBase:
        return A.text("pr-affiliated-practitioners")

    @staticmethod
    def get_profile_url() -> AutoMapperTextLikeBase:
        return A.concat(
            ProfileDefinition.get_url_base(),
            ProfileAffiliatedPractitioners.get_profile_id(),
        )


def mapping(parameters: Dict[str, Any]) -> List[AutoMapper]:
    resource = A.text("Group")

    mapper = AutoMapper(
        view=parameters["view_affiliated_practitioners"],
        source_view=parameters["view_profile_config"],
        use_schema=False,
    ).complex(
        ProfileDefinition(
            profile_id=FhirId(ProfileAffiliatedPractitioners.get_profile_id()),
            profile_name="Affiliated Practitioners",
            computer_friendly_profile_name="AffiliatedPractitioners",
            fhir_resource_type="Group",
            description="A group of practitioners that are affiliated with a health system",
            keyword=FhirList(
                [
                    Coding(
                        system=FileTypeCategoryCode.codeset,
                        code=FileTypeCategoryCodeValues.ProviderRoster,
                    )
                ]
            ),
            differential_elements=FhirList(
                [
                    ElementDefinition(id_=resource, path=resource),
                    ElementDefinition(
                        id_=A.concat(resource, ".id"), path=A.concat(resource, ".id")
                    ),
                ],
                True,
            )
            # META
            .concat(DataElementMeta.get_meta(resource=resource)).concat(
                FhirList(
                    [
                        # ACTIVE
                        ElementDefinition(
                            id_=A.concat(resource, ".active"),
                            path=A.concat(resource, ".active"),
                            short="True | False",
                            min=1,
                            type_=FhirList([ElementDefinitionType(code="boolean")]),
                            mustSupport=A.boolean(True),
                        ),
                        # TYPE
                        ElementDefinition(
                            id_=A.concat(resource, ".type"),
                            path=A.concat(resource, ".type"),
                            short="fixed code: 'practitioner'",
                            min=1,
                            type_=FhirList([ElementDefinitionType(code="code")]),
                            fixedCode=GroupTypeCodeValues.Practitioner,
                            mustSupport=A.boolean(True),
                        ),
                        # ACTUAL
                        ElementDefinition(
                            id_=A.concat(resource, ".actual"),
                            path=A.concat(resource, ".actual"),
                            short="fixed: True",
                            min=1,
                            type_=FhirList([ElementDefinitionType(code="boolean")]),
                            fixedBoolean=A.boolean(True),
                            mustSupport=A.boolean(True),
                        ),
                        # NAME
                        ElementDefinition(
                            id_=A.concat(resource, ".name"),
                            path=A.concat(resource, ".name"),
                            short="Name of the Group",
                            definition="The practitioner affiliation group name",
                            min=1,
                            type_=FhirList([ElementDefinitionType(code="string")]),
                            mustSupport=A.boolean(True),
                        ),
                        # MANAGING ENTITY
                        ElementDefinition(
                            id_=A.concat(resource, ".managingEntity"),
                            path=A.concat(resource, ".managingEntity"),
                            short="Organization to which the practitioners belong",
                            min=1,
                            type_=FhirList(
                                [
                                    ElementDefinitionType(
                                        code="Reference",
                                        targetProfile=FhirList(
                                            [
                                                ProfileHealthcareOrganization.get_profile_url()
                                            ]
                                        ),
                                    )
                                ]
                            ),
                            mustSupport=A.boolean(True),
                        ),
                    ],
                    True,
                )
                # MEMBER
                .concat(DataElementGroupMember.get_group_member_any(resource=resource)),
            ),
        )
    )

    return [mapper]

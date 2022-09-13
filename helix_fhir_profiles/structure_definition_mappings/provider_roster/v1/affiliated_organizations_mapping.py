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

from helix_fhir_profiles.data_elements.v1.identifier_element import (
    DataElementIdentifier,
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
from helix_fhir_profiles.structure_definition_mappings.eligibility.v1.partner_organization_mapping import (
    ProfilePartnerOrganization,
)
from helix_fhir_profiles.schema.v1.profile_definition_schema import (
    ProfileDefinition,
)


class ProfileAffiliatedOrganizations:
    @staticmethod
    def get_profile_id() -> AutoMapperTextLikeBase:
        return A.text("pr-affiliated-organizations")

    @staticmethod
    def get_profile_url() -> AutoMapperTextLikeBase:
        return A.concat(
            ProfileDefinition.get_url_base(),
            ProfileAffiliatedOrganizations.get_profile_id(),
        )


def mapping(parameters: Dict[str, Any]) -> List[AutoMapper]:
    resource = A.text("OrganizationAffiliation")

    mapper = AutoMapper(
        view=parameters["view_affiliated_organizations"],
        source_view=parameters["view_profile_config"],
        use_schema=False,
    ).complex(
        ProfileDefinition(
            profile_id=FhirId(ProfileAffiliatedOrganizations.get_profile_id()),
            profile_name="Affiliated Organizations",
            computer_friendly_profile_name="AffiliatedOrganizations",
            fhir_resource_type="OrganizationAffiliation",
            description="A relationship between two organizations",
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
            .concat(DataElementMeta.get_meta(resource=resource))
            # IDENTIFIER
            .concat(DataElementIdentifier.get_identifier_any(resource=resource)).concat(
                FhirList(
                    [
                        # ACTIVE
                        ElementDefinition(
                            id_=A.concat(resource, ".active"),
                            path=A.concat(resource, ".active"),
                            label="active-organization-affiliation",
                            short="Whether this organization affiliation record is in active use",
                            min=1,
                            max="1",
                            type_=FhirList([ElementDefinitionType(code="boolean")]),
                            mustSupport=A.boolean(True),
                        ),
                        # ORGANIZATION
                        ElementDefinition(
                            id_=A.concat(resource, ".organization"),
                            path=A.concat(resource, ".organization"),
                            label="partner-organization",
                            short="Managing organization",
                            min=1,
                            max="1",
                            type_=FhirList(
                                [
                                    ElementDefinitionType(
                                        code="Reference",
                                        targetProfile=FhirList(
                                            [
                                                ProfilePartnerOrganization.get_profile_url()
                                            ]
                                        ),
                                    )
                                ]
                            ),
                            mustSupport=A.boolean(True),
                        ),
                        # PARTICIPATING ORGANIZATION
                        ElementDefinition(
                            id_=A.concat(resource, ".participatingOrganization"),
                            path=A.concat(resource, ".participatingOrganization"),
                            label="healthcare-organization",
                            short="Participating organization, such as a healthcare practice",
                            min=1,
                            max="1",
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
                    ]
                )
            ),
        )
    )

    return [mapper]

from typing import Dict, Any, List

from library.fhir_profiles.data_elements.v1.practitioner_role_code_element import (
    DataElementPractitionerRoleCode,
)
from library.fhir_profiles.schema.v1.file_type_category_codes import (
    FileTypeCategoryCode,
    FileTypeCategoryCodeValues,
)
from library.fhir_profiles.schema.v1.product_feature_codes import (
    ProductFeatureCode,
    ProductFeatureCodeValues,
)
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

from library.fhir_profiles.data_elements.v1.identifier_element import (
    DataElementIdentifier,
)
from library.fhir_profiles.data_elements.v1.meta_element import (
    DataElementMeta,
)
from library.fhir_profiles.data_elements.v1.practitioner_specialty_element import (
    DataElementPractitionerSpecialty,
)
from library.fhir_profiles.data_elements.v1.extension_element import (
    DataElementExtension,
)
from library.fhir_profiles.structure_definition_mappings.provider_roster.v1.healthcare_location_mapping import (
    ProfileHealthcareLocation,
)
from library.fhir_profiles.structure_definition_mappings.provider_roster.v1.healthcare_organization_mapping import (
    ProfileHealthcareOrganization,
)
from library.fhir_profiles.structure_definition_mappings.scheduling.v1.healthcare_service_mapping import (
    ProfileHealthcareService,
)
from library.fhir_profiles.structure_definition_mappings.provider_roster.v1.practitioner_mapping import (
    ProfilePractitioner,
)
from library.fhir_profiles.schema.v1.profile_definition_schema import (
    ProfileDefinition,
)


class ProfilePractitionerRole:
    @staticmethod
    def get_profile_id() -> AutoMapperTextLikeBase:
        return A.text("pr-practitioner-role")

    @staticmethod
    def get_profile_url() -> AutoMapperTextLikeBase:
        return A.concat(
            ProfileDefinition.get_url_base(), ProfilePractitionerRole.get_profile_id()
        )


def mapping(parameters: Dict[str, Any]) -> List[AutoMapper]:
    resource = A.text("PractitionerRole")

    mapper = AutoMapper(
        view=parameters["view_practitioner_role"],
        source_view=parameters["view_profile_config"],
        use_schema=False,
    ).complex(
        ProfileDefinition(
            profile_id=FhirId(ProfilePractitionerRole.get_profile_id()),
            profile_name=A.text("Practitioner Role"),
            computer_friendly_profile_name=A.text("PractitionerRole"),
            fhir_resource_type=resource,
            description=A.text(
                "PractitionerRole resource for bWell's FHIR server. \n \n Included but not limited to: practitioner specialties, practitioner's location, appointment types, healthcare services, accepted insurance. See Implementation Guide for details regarding resource id patterns."
            ),
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
            # EXTENSIONS
            .concat(DataElementExtension.get_extension_any(resource=resource)).concat(
                DataElementExtension.get_accepted_patients(resource=resource)
            )
            # IDENTIFIERS
            .concat(DataElementIdentifier.get_identifier_any(resource=resource))
            .concat(DataElementIdentifier.get_npi(resource=resource))
            .concat(DataElementIdentifier.get_facility_id(resource=resource))
            .concat(DataElementIdentifier.get_provider_location_id(resource=resource))
            .concat(
                FhirList(
                    [
                        # practitioner
                        ElementDefinition(
                            id_=A.concat(resource, ".practitioner"),
                            path=A.concat(resource, ".practitioner"),
                            label="practitioner",
                            code=FhirList(
                                [
                                    Coding(
                                        system=ProductFeatureCode.codeset,
                                        code=ProductFeatureCodeValues.ProviderSearch,
                                    )
                                ]
                            ),
                            alias=FhirList(["provider", "physician"]),
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
                        # organization
                        ElementDefinition(
                            id_=A.concat(resource, ".organization"),
                            path=A.concat(resource, ".organization"),
                            label="organization",
                            code=FhirList(
                                [
                                    Coding(
                                        system=ProductFeatureCode.codeset,
                                        code=ProductFeatureCodeValues.ProviderSearch,
                                    )
                                ]
                            ),
                            short="A healthcare location's managing organization or a claims billing organization",
                            min=0,
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
            )
            # CODE
            .concat(
                DataElementPractitionerRoleCode.get_practitioner_role_code_any(
                    resource=resource
                )
            ).concat(
                DataElementPractitionerRoleCode.get_primary_care_characteristic(
                    resource=resource
                )
            )
            # SPECIALTY
            .concat(
                DataElementPractitionerSpecialty.get_practitioner_specialty_any(
                    resource=resource
                )
            ).concat(
                DataElementPractitionerSpecialty.get_taxonomy_code(resource=resource)
            )
            # LOCATION
            .concat(
                FhirList(
                    [
                        # location
                        ElementDefinition(
                            id_=A.concat(resource, ".location"),
                            path=A.concat(resource, ".location"),
                            label="location",
                            code=FhirList(
                                [
                                    Coding(
                                        system=ProductFeatureCode.codeset,
                                        code=ProductFeatureCodeValues.ProviderSearch,
                                    )
                                ]
                            ),
                            short="The location where this role is performed",
                            min=0,
                            max="1",
                            type_=FhirList(
                                [
                                    ElementDefinitionType(
                                        code="Reference",
                                        targetProfile=FhirList(
                                            [
                                                ProfileHealthcareLocation.get_profile_url()
                                            ]
                                        ),
                                    )
                                ]
                            ),
                            mustSupport=A.boolean(True),
                        ),
                        # healthcareservice
                        ElementDefinition(
                            id_=A.concat(resource, ".healthcareService"),
                            path=A.concat(resource, ".healthcareService"),
                            code=FhirList(
                                [
                                    Coding(
                                        system=ProductFeatureCode.codeset,
                                        code=ProductFeatureCodeValues.ProviderSearch,
                                    )
                                ]
                            ),
                            min=0,
                            max="1",
                            type_=FhirList(
                                [
                                    ElementDefinitionType(
                                        code="Reference",
                                        targetProfile=FhirList(
                                            [ProfileHealthcareService.get_profile_url()]
                                        ),
                                    )
                                ]
                            ),
                            mustSupport=A.boolean(True),
                        ),
                    ],
                )
            ),
        )
    )

    return [mapper]

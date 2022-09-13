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

from helix_fhir_profiles.data_elements.v1.address_element import (
    DataElementAddress,
)
from helix_fhir_profiles.data_elements.v1.contact_point_element import (
    DataElementContactPoint,
)
from helix_fhir_profiles.data_elements.v1.identifier_element import (
    DataElementIdentifier,
)
from helix_fhir_profiles.data_elements.v1.meta_element import (
    DataElementMeta,
)
from helix_fhir_profiles.data_elements.v1.organization_type_element import (
    DataElementOrganizationType,
)
from helix_fhir_profiles.schema.v1.file_type_category_codes import (
    FileTypeCategoryCode,
    FileTypeCategoryCodeValues,
)
from helix_fhir_profiles.schema.v1.product_feature_codes import (
    ProductFeatureCodeValues,
    ProductFeatureCode,
)
from helix_fhir_profiles.schema.v1.profile_definition_schema import (
    ProfileDefinition,
)


class ProfileHealthcareOrganization:
    @staticmethod
    def get_profile_id() -> AutoMapperTextLikeBase:
        return A.text("pr-healthcare-organization")

    @staticmethod
    def get_profile_url() -> AutoMapperTextLikeBase:
        return A.concat(
            ProfileDefinition.get_url_base(),
            ProfileHealthcareOrganization.get_profile_id(),
        )


def mapping(parameters: Dict[str, Any]) -> List[AutoMapper]:
    resource = A.text("Organization")

    mapper = AutoMapper(
        view=parameters["view_healthcare_organization"],
        source_view=parameters["view_profile_config"],
        use_schema=False,
    ).complex(
        ProfileDefinition(
            profile_id=FhirId(ProfileHealthcareOrganization.get_profile_id()),
            profile_name=A.text("Healthcare Organization"),
            computer_friendly_profile_name=A.text("HealthcareOrganization"),
            fhir_resource_type=resource,
            description=A.text(
                "Healthcare organizations including practices, claims billing organizations, and pharmacies."
            ),
            keyword=FhirList(
                [
                    Coding(
                        system=FileTypeCategoryCode.codeset,
                        code=FileTypeCategoryCodeValues.ProviderRoster,
                    ),
                    Coding(
                        system=FileTypeCategoryCode.codeset,
                        code=FileTypeCategoryCodeValues.RxClaimsFile,
                    ),
                    Coding(
                        system=FileTypeCategoryCode.codeset,
                        code=FileTypeCategoryCodeValues.MedicalClaimsFile,
                    ),
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
            # IDENTIFIERS
            .concat(DataElementIdentifier.get_identifier_any(resource=resource))
            .concat(DataElementIdentifier.get_npi(resource=resource))
            .concat(DataElementIdentifier.get_tin(resource=resource))
            .concat(
                FhirList(
                    [
                        # ACTIVE
                        ElementDefinition(
                            id_=A.concat(resource, ".active"),
                            path=A.concat(resource, ".active"),
                            min=1,
                            type_=FhirList([ElementDefinitionType(code="boolean")]),
                            mustSupport=A.boolean(True),
                        ),
                    ]
                )
            )
            .concat(
                # TYPE
                DataElementOrganizationType.get_organization_type_any(resource=resource)
            )
            .concat(DataElementOrganizationType.get_healthcare_type(resource=resource))
            .concat(
                FhirList(
                    [
                        ElementDefinition(
                            id_=A.concat(resource, ".name"),
                            path=A.concat(resource, ".name"),
                            label="organization-name",
                            code=FhirList(
                                [
                                    Coding(
                                        system=ProductFeatureCode.codeset,
                                        code=ProductFeatureCodeValues.ProviderSearch,
                                    )
                                ]
                            ),
                            short="Name of the organization",
                            min=1,
                            mustSupport=A.boolean(True),
                        ),
                    ],
                )
            )
            .concat(
                # TELECOM
                DataElementContactPoint.get_contact_point_any(resource=resource)
            )
            .concat(DataElementContactPoint.get_business_phone(resource=resource))
            .concat(
                DataElementContactPoint.get_business_fax(resource=resource),
            )
            .concat(DataElementAddress.get_address_any(resource=resource))
            .concat(DataElementAddress.get_business_address(resource=resource))
            .concat(
                FhirList(
                    [
                        ElementDefinition(
                            id_=A.concat(resource, ".partOf"),
                            path=A.concat(resource, ".partOf"),
                            label="parent-organization",
                            short="The parent organization",
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
                        ),
                    ]
                )
            ),
        )
    )

    return [mapper]

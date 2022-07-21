from typing import Dict, Any, List

from spark_auto_mapper.automappers.automapper import AutoMapper
from spark_auto_mapper.data_types.text_like_base import AutoMapperTextLikeBase
from spark_auto_mapper.helpers.automapper_helpers import AutoMapperHelpers as A
from spark_auto_mapper_fhir.backbone_elements.element_definition import (
    ElementDefinition,
)
from spark_auto_mapper_fhir.backbone_elements.element_definition_example import (
    ElementDefinitionExample,
)
from spark_auto_mapper_fhir.complex_types.coding import Coding
from spark_auto_mapper_fhir.fhir_types.id import FhirId
from spark_auto_mapper_fhir.fhir_types.list import FhirList

from library.fhir_profiles.data_elements.v1.meta_element import (
    DataElementMeta,
)
from library.fhir_profiles.schema.v1.file_type_category_codes import (
    FileTypeCategoryCode,
    FileTypeCategoryCodeValues,
)
from library.fhir_profiles.schema.v1.profile_definition_schema import (
    ProfileDefinition,
)


class ProfilePartnerOrganization:
    @staticmethod
    def get_profile_id() -> AutoMapperTextLikeBase:
        return A.text("pr-partner-organization")

    @staticmethod
    def get_profile_url() -> AutoMapperTextLikeBase:
        return A.concat(
            ProfileDefinition.get_url_base(),
            ProfilePartnerOrganization.get_profile_id(),
        )


def mapping(parameters: Dict[str, Any]) -> List[AutoMapper]:
    resource = A.text("Organization")

    mapper = AutoMapper(
        view=parameters["view_partner_organization"],
        source_view=parameters["view_profile_config"],
        use_schema=False,
    ).complex(
        ProfileDefinition(
            profile_id=FhirId(ProfilePartnerOrganization.get_profile_id()),
            profile_name=A.text("Partner Organization"),
            computer_friendly_profile_name=A.text("PartnerOrganization"),
            fhir_resource_type=resource,
            description=A.text("A client organization"),
            keyword=FhirList(
                [
                    Coding(
                        system=FileTypeCategoryCode.codeset,
                        code=FileTypeCategoryCodeValues.EmployeeFile,
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
                        ElementDefinition(
                            id_=A.concat(resource, ".name"),
                            path=A.concat(resource, ".name"),
                            label="organization-name",
                            short=A.text("The name of the organization"),
                            example=FhirList(
                                [
                                    ElementDefinitionExample(
                                        label="A client organization",
                                        valueString="bWell Connected Health",
                                    )
                                ]
                            ),
                            mustSupport=A.boolean(True),
                        ),
                    ],
                    True,
                ),
            ),
        )
    )

    return [mapper]

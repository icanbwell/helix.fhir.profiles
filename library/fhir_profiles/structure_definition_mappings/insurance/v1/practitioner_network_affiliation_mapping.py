from typing import Dict, Any, List

from library.fhir_profiles.schema.v1.file_type_category_codes import (
    FileTypeCategoryCode,
    FileTypeCategoryCodeValues,
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
from library.fhir_profiles.data_elements.v1.extension_element import (
    DataElementExtension,
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
        return A.text("pr-practitioner-network-affiliation")

    @staticmethod
    def get_profile_url() -> AutoMapperTextLikeBase:
        return A.concat(
            ProfileDefinition.get_url_base(), ProfilePractitionerRole.get_profile_id()
        )


def mapping(parameters: Dict[str, Any]) -> List[AutoMapper]:
    resource = A.text("PractitionerRole")

    mapper = AutoMapper(
        view=parameters["view_practitioner_network_affiliation"],
        source_view=parameters["view_profile_config"],
        use_schema=False,
    ).complex(
        ProfileDefinition(
            profile_id=FhirId(ProfilePractitionerRole.get_profile_id()),
            profile_name=A.text("Practitioner Network Affiliation"),
            computer_friendly_profile_name=A.text("PractitionerRole"),
            fhir_resource_type=resource,
            description="PractitionerRole to represent a practitioner's association to a healthcare network",
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
                DataElementExtension.get_reference_network(resource=resource)
            )
            # IDENTIFIERS
            .concat(DataElementIdentifier.get_identifier_any(resource=resource)).concat(
                DataElementIdentifier.get_npi(resource=resource)
            )
            # PRACTITIONER
            .concat(
                FhirList(
                    [
                        ElementDefinition(
                            id_=A.concat(resource, ".practitioner"),
                            path=A.concat(resource, ".practitioner"),
                            short="Practitioner associated to the network",
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
                        )
                    ]
                )
            ),
        )
    )

    return [mapper]

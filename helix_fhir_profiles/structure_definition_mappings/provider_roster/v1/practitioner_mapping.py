from typing import Dict, Any, List

from helix_fhir_profiles.data_elements.v1.attachment_element import (
    DataElementAttachment,
)
from helix_fhir_profiles.backbone_elements.v1.backbone_element_practitioner_qualification import (
    DataBackboneElementPractitionerQualification,
)
from helix_fhir_profiles.data_elements.v1.extension_element import (
    DataElementExtension,
)
from helix_fhir_profiles.data_elements.v1.practitioner_communication_element import (
    DataElementCommunication,
)

from helix_fhir_profiles.schema.v1.file_type_category_codes import (
    FileTypeCategoryCode,
    FileTypeCategoryCodeValues,
)
from helix_fhir_profiles.schema.v1.product_feature_codes import (
    ProductFeatureCodeValues,
    ProductFeatureCode,
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

from helix_fhir_profiles.data_elements.v1.human_name_element import (
    DataElementHumanName,
)
from helix_fhir_profiles.data_elements.v1.identifier_element import (
    DataElementIdentifier,
)
from helix_fhir_profiles.data_elements.v1.meta_element import (
    DataElementMeta,
)
from helix_fhir_profiles.schema.v1.profile_definition_schema import (
    ProfileDefinition,
)


class ProfilePractitioner:
    @staticmethod
    def get_profile_id() -> AutoMapperTextLikeBase:
        return A.text("pr-practitioner")

    @staticmethod
    def get_profile_url() -> AutoMapperTextLikeBase:
        return A.concat(
            ProfileDefinition.get_url_base(), ProfilePractitioner.get_profile_id()
        )


def mapping(parameters: Dict[str, Any]) -> List[AutoMapper]:
    resource = A.text("Practitioner")

    mapper = AutoMapper(
        view=parameters["view_practitioner"],
        source_view=parameters["view_profile_config"],
        use_schema=False,
    ).complex(
        ProfileDefinition(
            profile_id=FhirId(ProfilePractitioner.get_profile_id()),
            profile_name="Practitioner",
            computer_friendly_profile_name="Practitioner",
            fhir_resource_type="Practitioner",
            description="Client-agnostic record for a Practitioner",
            keyword=FhirList(
                [
                    Coding(
                        system=FileTypeCategoryCode.codeset,
                        code=FileTypeCategoryCodeValues.ProviderRoster,
                    ),
                    Coding(
                        system=FileTypeCategoryCode.codeset,
                        code=FileTypeCategoryCodeValues.MedicalClaimsFile,
                    ),
                    Coding(
                        system=FileTypeCategoryCode.codeset,
                        code=FileTypeCategoryCodeValues.RxClaimsFile,
                    ),
                    Coding(
                        system=FileTypeCategoryCode.codeset,
                        code=FileTypeCategoryCodeValues.ElibilityFile,
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
            # EXTENSIONS
            .concat(DataElementExtension.get_extension_any(resource=resource))
            # IDENTIFIERS
            .concat(DataElementIdentifier.get_identifier_any(resource=resource))
            .concat(DataElementIdentifier.get_npi(resource=resource))
            .concat(DataElementIdentifier.get_provider_id(resource=resource))
            .concat(DataElementIdentifier.get_dea_number(resource=resource))
            .concat(
                FhirList(
                    [
                        # ACTIVE
                        ElementDefinition(
                            id_=A.concat(resource, ".active"),
                            path=A.concat(resource, ".active"),
                            code=FhirList(
                                [
                                    Coding(
                                        system=ProductFeatureCode.codeset,
                                        code=ProductFeatureCodeValues.ProviderSearch,
                                    )
                                ]
                            ),
                            type_=FhirList([ElementDefinitionType(code="boolean")]),
                            mustSupport=A.boolean(True),
                        ),
                    ]
                )
            )
            .concat(
                # NAME
                DataElementHumanName.get_human_name_any(resource=resource)
            )
            .concat(
                FhirList(
                    [
                        # TELECOM - none
                        ElementDefinition(
                            id_=A.concat(resource, ".telecom"),
                            path=A.concat(resource, ".telecom"),
                            comment="telecom of the practitioner should be associated to a Healthcare Location",
                            max="0",
                        ),
                        # ADDRESS - none
                        ElementDefinition(
                            id_=A.concat(resource, ".address"),
                            path=A.concat(resource, ".address"),
                            comment="address of the practitioner should be assocated to a Healthcare Location",
                            max="0",
                        ),
                        # GENDER
                        ElementDefinition(
                            id_=A.concat(resource, ".gender"),
                            path=A.concat(resource, ".gender"),
                            label="gender",
                            code=FhirList(
                                [
                                    Coding(
                                        system=ProductFeatureCode.codeset,
                                        code=ProductFeatureCodeValues.ProviderSearch,
                                    )
                                ]
                            ),
                            short="male | female | other | unknown",
                            type_=FhirList([ElementDefinitionType(code="code")]),
                            mustSupport=A.boolean(True),
                        ),
                        # DATE OF BIRTH
                        ElementDefinition(
                            id_=A.concat(resource, ".birthDate"),
                            path=A.concat(resource, ".birthDate"),
                            label="birth-date",
                            short="DOB of the provider",
                            min=0,
                            max="1",
                            type_=FhirList([ElementDefinitionType(code="date")]),
                        ),
                    ]
                )
            )
            # PHOTO
            .concat(DataElementAttachment.get_practitioner_photo(resource=resource))
            # QUALIFICATION
            .concat(
                DataBackboneElementPractitionerQualification.get_practitioner_qualification(
                    resource=resource
                )
            )
            # COMMUNICATION
            .concat(DataElementCommunication.get_language(resource=resource)),
        )
    )

    return [mapper]

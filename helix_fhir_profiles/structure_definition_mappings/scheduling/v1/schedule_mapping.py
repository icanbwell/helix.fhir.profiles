from typing import Dict, Any, List

from helix_fhir_profiles.data_elements.v1.extension_element import (
    DataElementExtension,
)

from helix_fhir_profiles.schema.v1.file_type_category_codes import (
    FileTypeCategoryCode,
    FileTypeCategoryCodeValues,
)
from helix_fhir_profiles.schema.v1.product_feature_codes import (
    ProductFeatureCode,
    ProductFeatureCodeValues,
)
from spark_auto_mapper.automappers.automapper import AutoMapper
from spark_auto_mapper.data_types.text_like_base import AutoMapperTextLikeBase
from spark_auto_mapper.helpers.automapper_helpers import AutoMapperHelpers as A
from spark_auto_mapper_fhir.backbone_elements.element_definition import (
    ElementDefinition,
)
from spark_auto_mapper_fhir.backbone_elements.element_definition_slicing import (
    ElementDefinitionSlicing,
)
from spark_auto_mapper_fhir.backbone_elements.element_definition_type import (
    ElementDefinitionType,
)
from spark_auto_mapper_fhir.complex_types.coding import Coding
from spark_auto_mapper_fhir.fhir_types.id import FhirId
from spark_auto_mapper_fhir.fhir_types.list import FhirList
from spark_auto_mapper_fhir.value_sets.slicing_rules import SlicingRulesCodeValues

from helix_fhir_profiles.data_elements.v1.identifier_element import (
    DataElementIdentifier,
)
from helix_fhir_profiles.data_elements.v1.meta_element import (
    DataElementMeta,
)
from helix_fhir_profiles.structure_definition_mappings.scheduling.v1.healthcare_service_mapping import (
    ProfileHealthcareService,
)
from helix_fhir_profiles.structure_definition_mappings.provider_roster.v1.practitioner_role_mapping import (
    ProfilePractitionerRole,
)
from helix_fhir_profiles.schema.v1.profile_definition_schema import (
    ProfileDefinition,
)


class ProfileSchedule:
    @staticmethod
    def get_profile_id() -> AutoMapperTextLikeBase:
        return A.text("pr-schedule")

    @staticmethod
    def get_profile_url() -> AutoMapperTextLikeBase:
        return A.concat(
            ProfileDefinition.get_url_base(), ProfileSchedule.get_profile_id()
        )


def mapping(parameters: Dict[str, Any]) -> List[AutoMapper]:
    resource = A.text("Schedule")

    mapper = AutoMapper(
        view=parameters["view_schedule"],
        source_view=parameters["view_profile_config"],
        use_schema=False,
    ).complex(
        ProfileDefinition(
            profile_id=FhirId(ProfileSchedule.get_profile_id()),
            profile_name=A.text("Schedule"),
            computer_friendly_profile_name=A.text("Schedule"),
            fhir_resource_type=resource,
            description=A.text(
                "Schedule resource for provider search & online booking"
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
                DataElementExtension.get_provider_search(resource=resource)
            )
            # IDENTIFIERS
            .concat(DataElementIdentifier.get_identifier_any(resource=resource))
            .concat(DataElementIdentifier.get_npi(resource=resource))
            .concat(DataElementIdentifier.get_facility_id(resource=resource))
            .concat(DataElementIdentifier.get_provider_id(resource=resource))
            .concat(
                FhirList(
                    [
                        ElementDefinition(
                            id_=A.concat(resource, ".active"),
                            path=A.concat(resource, ".active"),
                            code=FhirList(
                                [
                                    Coding(
                                        system=ProductFeatureCode.codeset,
                                        code=ProductFeatureCodeValues.ProviderSearch,
                                    ),
                                    Coding(
                                        system=ProductFeatureCode.codeset,
                                        code=ProductFeatureCodeValues.IntegratedScheduling,
                                    ),
                                ]
                            ),
                            short="active flag",
                            # definition="",
                            # comment="",
                            # requirements="Needs Review",
                            type_=FhirList([ElementDefinitionType(code="boolean")]),
                            mustSupport=A.boolean(True),
                        ),
                        ElementDefinition(
                            id_=A.concat(resource, ".serviceType"),
                            path=A.concat(resource, ".serviceType"),
                            label="visit-type",
                            code=FhirList(
                                [
                                    Coding(
                                        system=ProductFeatureCode.codeset,
                                        code=ProductFeatureCodeValues.ProviderSearch,
                                    ),
                                    Coding(
                                        system=ProductFeatureCode.codeset,
                                        code=ProductFeatureCodeValues.IntegratedScheduling,
                                    ),
                                ]
                            ),
                            short="the type of visit (appointment)",
                            definition="includes scheduling appointment types, triage groups and protocols",
                            # comment="",
                            requirements="Needs Review for integrated scheduling requirements",
                            type_=FhirList(
                                [ElementDefinitionType(code="CodeableConcept")]
                            ),
                            mustSupport=A.boolean(True),
                        ),
                        ElementDefinition(
                            id_=A.concat(resource, ".actor"),
                            path=A.concat(resource, ".actor"),
                            code=FhirList(
                                [
                                    Coding(
                                        system=ProductFeatureCode.codeset,
                                        code=ProductFeatureCodeValues.ProviderSearch,
                                    ),
                                    Coding(
                                        system=ProductFeatureCode.codeset,
                                        code=ProductFeatureCodeValues.IntegratedScheduling,
                                    ),
                                ]
                            ),
                            slicing=ElementDefinitionSlicing(
                                description="slice by type",
                                rules=SlicingRulesCodeValues.Open,
                            ),
                            min=1,
                            type_=FhirList(
                                [
                                    ElementDefinitionType(
                                        code="Reference",
                                        targetProfile=FhirList(
                                            [
                                                ProfileHealthcareService.get_profile_url(),
                                                ProfilePractitionerRole.get_profile_url(),
                                            ]
                                        ),
                                    )
                                ]
                            ),
                            mustSupport=A.boolean(True),
                        ),
                        ElementDefinition(
                            id_=A.concat(resource, ".actor-facility"),
                            path=A.concat(resource, ".actor"),
                            sliceName="actor-facility",
                            code=FhirList(
                                [
                                    Coding(
                                        system=ProductFeatureCode.codeset,
                                        code=ProductFeatureCodeValues.ProviderSearch,
                                    ),
                                    Coding(
                                        system=ProductFeatureCode.codeset,
                                        code=ProductFeatureCodeValues.IntegratedScheduling,
                                    ),
                                ]
                            ),
                            short="The healthcare facility the schedule pertains to",
                            definition="Use in instances where the schedule applies to the facility as a whole (and not any specific practitioner)",
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
                        ElementDefinition(
                            id_=A.concat(resource, ".actor-practitioner"),
                            path=A.concat(resource, ".actor"),
                            sliceName="actor-practitioner",
                            code=FhirList(
                                [
                                    Coding(
                                        system=ProductFeatureCode.codeset,
                                        code=ProductFeatureCodeValues.ProviderSearch,
                                    ),
                                    Coding(
                                        system=ProductFeatureCode.codeset,
                                        code=ProductFeatureCodeValues.IntegratedScheduling,
                                    ),
                                ]
                            ),
                            short="The practitioner the schedule pertains to",
                            definition="Use in instances where the schedule applies to a specific practitioner (at a specific healthcare location)",
                            min=0,
                            max="1",
                            type_=FhirList(
                                [
                                    ElementDefinitionType(
                                        code="Reference",
                                        targetProfile=FhirList(
                                            [ProfilePractitionerRole.get_profile_url()]
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

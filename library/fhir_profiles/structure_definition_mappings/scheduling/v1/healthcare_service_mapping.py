from typing import Dict, Any, List

from library.fhir_profiles.data_elements.v1.extension_element import (
    DataElementExtension,
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
from spark_auto_mapper_fhir.fhir_types.id import FhirId
from spark_auto_mapper_fhir.fhir_types.list import FhirList

from library.fhir_profiles.data_elements.v1.identifier_element import (
    DataElementIdentifier,
)
from library.fhir_profiles.data_elements.v1.meta_element import (
    DataElementMeta,
)
from library.fhir_profiles.structure_definition_mappings.provider_roster.v1.healthcare_location_mapping import (
    ProfileHealthcareLocation,
)
from library.fhir_profiles.structure_definition_mappings.provider_roster.v1.healthcare_organization_mapping import (
    ProfileHealthcareOrganization,
)
from library.fhir_profiles.schema.v1.profile_definition_schema import (
    ProfileDefinition,
)


class ProfileHealthcareService:
    @staticmethod
    def get_profile_id() -> AutoMapperTextLikeBase:
        return A.text("pr-healthcare-service")

    @staticmethod
    def get_profile_url() -> AutoMapperTextLikeBase:
        return A.concat(
            ProfileDefinition.get_url_base(), ProfileHealthcareService.get_profile_id()
        )


def mapping(parameters: Dict[str, Any]) -> List[AutoMapper]:
    resource = A.text("HealthcareService")

    mapper = AutoMapper(
        view=parameters["view_healthcare_service"],
        source_view=parameters["view_profile_config"],
        use_schema=False,
    ).complex(
        ProfileDefinition(
            profile_id=FhirId(ProfileHealthcareService.get_profile_id()),
            profile_name="Healthcare Service",
            computer_friendly_profile_name="HealthcareService",
            fhir_resource_type="HealthcareService",
            description="HealthcareService resource for bwell FHIR server. \n \n Includes indicators for ER, Urgent Care, and COVID services. \n \n Some elements need review.",
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
            .concat(
                FhirList(
                    [
                        ElementDefinition(
                            id_=A.concat(resource, ".active"),
                            path=A.concat(resource, ".active"),
                            short="Indicates if the resource is valid",
                            min=1,
                            mustSupport=A.boolean(True),
                        ),
                        ElementDefinition(
                            id_=A.concat(resource, ".providedBy"),
                            path=A.concat(resource, ".providedBy"),
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
                        # todo make element definition
                        ElementDefinition(
                            id_=A.concat(resource, ".type"),
                            path=A.concat(resource, ".type"),
                            mustSupport=A.boolean(True),
                        ),
                        # {
                        #                 "id": "HealthcareService.type:emergency-room-flag",
                        #                 "path": "HealthcareService.type",
                        #                 "sliceName": "emergency-room-flag",
                        #                 "min": 0,
                        #                 "max": "1",
                        #                 "type":  [
                        #                     {
                        #                         "code": "CodeableConcept"
                        #                     }
                        #                 ],
                        #                 "comment": "NEEDS REVIEW",
                        #                 "fixedCodeableConcept": {
                        #                     "coding":  [
                        #                         {
                        #                             "system": "http://terminology.hl7.org/CodeSystem/service-type",
                        #                             "code": "117"
                        #                         }
                        #                     ]
                        #                 }
                        #             },
                        #             {
                        #                 "id": "HealthcareService.type:urgent-care-flag",
                        #                 "path": "HealthcareService.type",
                        #                 "sliceName": "urgent-care-flag",
                        #                 "min": 0,
                        #                 "max": "1",
                        #                 "type":  [
                        #                     {
                        #                         "code": "CodeableConcept"
                        #                     }
                        #                 ],
                        #                 "comment": "NEEDS REVIEW",
                        #                 "fixedCodeableConcept": {
                        #                     "coding":  [
                        #                         {
                        #                             "system": "http://terminology.hl7.org/CodeSystem/service-type",
                        #                             "code": "556"
                        #                         }
                        #                     ]
                        #                 }
                        #             },
                        #             {
                        #                 "id": "HealthcareService.type:covid-testing-flag",
                        #                 "path": "HealthcareService.type",
                        #                 "sliceName": "covid-testing-flag",
                        #                 "min": 0,
                        #                 "max": "1",
                        #                 "type":  [
                        #                     {
                        #                         "code": "CodeableConcept"
                        #                     }
                        #                 ],
                        #                 "comment": "NEEDS REVIEW",
                        #                 "fixedCodeableConcept": {
                        #                     "coding":  [
                        #                         {
                        #                             "system": "http://loinc.org",
                        #                             "code": "94500-6"
                        #                         }
                        #                     ]
                        #                 }
                        #             },
                        #             {
                        #                 "id": "HealthcareService.type:covid-vaccine-flag",
                        #                 "path": "HealthcareService.type",
                        #                 "sliceName": "covid-vaccine-flag",
                        #                 "short": "flag to indicate COVID vaccines are provided at this location",
                        #                 "definition": "intended for locations",
                        #                 "min": 0,
                        #                 "max": "1",
                        #                 "type":  [
                        #                     {
                        #                         "code": "CodeableConcept"
                        #                     }
                        #                 ],
                        #                 "comment": "NEEDS REVIEW",
                        #                 "fixedCodeableConcept": {
                        #                     "coding":  [
                        #                         {
                        #                             "system": "https://www.snomed.org",
                        #                             "code": "840534001"
                        #                         }
                        #                     ]
                        #                 }
                        #             },
                        #             {
                        #                 "id": "HealthcareService.type:primary-care",
                        #                 "path": "HealthcareService.type",
                        #                 "sliceName": "primary-care",
                        #                 "min": 0,
                        #                 "max": "1",
                        #                 "type":  [
                        #                     {
                        #                         "code": "CodeableConcept"
                        #                     }
                        #                 ],
                        #                 "comment": "NEEDS REVIEW",
                        #                 "fixedCodeableConcept": {
                        #                     "coding":  [
                        #                         {
                        #                             "system": "http://terminology.hl7.org/CodeSystem/service-category",
                        #                             "code": "17"
                        #                         }
                        #                     ]
                        #                 }
                        #             },
                        ElementDefinition(
                            id_=A.concat(resource, ".specialty"),
                            path=A.concat(resource, ".specialty"),
                            mustSupport=A.boolean(True),
                        ),
                        #             {
                        #                 "id": "HealthcareService.specialty:taxonomy-code",
                        #                 "path": "HealthcareService.specialty",
                        #                 "sliceName": "specialty-taxonomy-code",
                        #                 "short": "NUCC taxonomy specialty code",
                        #                 "min": 0,
                        #                 "max": "*",
                        #                 "type":  [
                        #                     {
                        #                         "code": "CodeableConcept"
                        #                     }
                        #                 ],
                        #                 "binding": {
                        #                     "strength": "required",
                        #                     "valueSet": "http://nucc.org/provider-taxonomy"
                        #                 }
                        #             },
                        #             {
                        #                 "id": "HealthcareService.specialty:emergency-room",
                        #                 "path": "HealthcareService.specialty",
                        #                 "sliceName": "specialty-emergency-room",
                        #                 "min": 0,
                        #                 "max": "1",
                        #                 "type":  [
                        #                     {
                        #                         "code": "CodeableConcept"
                        #                     }
                        #                 ],
                        #                 "comment": "NEEDS REVIEW",
                        #                 "fixedCodeableConcept": {
                        #                     "coding":  [
                        #                         {
                        #                             "system": "http://snomed.info/sct",
                        #                             "code": "773568002"
                        #                         }
                        #                     ]
                        #                 }
                        #             },
                        #             {
                        #                 "id": "HealthcareService.specialty:covid-vaccine",
                        #                 "path": "HealthcareService.specialty",
                        #                 "sliceName": "specialty-covid-vaccine",
                        #                 "min": 0,
                        #                 "max": "1",
                        #                 "type":  [
                        #                     {
                        #                         "code": "CodeableConcept"
                        #                     }
                        #                 ],
                        #                 "comment": "NEEDS REVIEW",
                        #                 "fixedCodeableConcept": {
                        #                     "coding":  [
                        #                         {
                        #                             "system": "http://snomed.info/sct",
                        #                             "code": "46224007"
                        #                         }
                        #                     ]
                        #                 }
                        #             },
                        ElementDefinition(
                            id_=A.concat(resource, ".location"),
                            path=A.concat(resource, ".location"),
                            min=1,
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
                    ]
                )
            ),
        )
    )

    return [mapper]

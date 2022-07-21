from spark_auto_mapper_fhir.backbone_elements.element_definition_slicing import (
    ElementDefinitionSlicing,
)
from spark_auto_mapper_fhir.value_sets.slicing_rules import SlicingRulesCodeValues

from library.fhir_profiles.schema.v1.product_feature_codes import (
    ProductFeatureCode,
    ProductFeatureCodeValues,
)
from spark_auto_mapper_fhir.value_sets.generic_type import GenericTypeCode

from spark_auto_mapper.data_types.text_like_base import AutoMapperTextLikeBase
from spark_auto_mapper_fhir.backbone_elements.element_definition import (
    ElementDefinition,
)

from spark_auto_mapper.helpers.automapper_helpers import AutoMapperHelpers as A
from spark_auto_mapper_fhir.backbone_elements.element_definition_type import (
    ElementDefinitionType,
)
from spark_auto_mapper_fhir.fhir_types.list import FhirList
from spark_auto_mapper_fhir.complex_types.codeable_concept import CodeableConcept
from spark_auto_mapper_fhir.complex_types.coding import Coding

from library.fhir_profiles.structure_definition_mappings.provider_roster.v1.healthcare_location_mapping import (
    ProfileHealthcareLocation,
)
from library.fhir_profiles.structure_definition_mappings.scheduling.v1.healthcare_service_mapping import (
    ProfileHealthcareService,
)
from library.fhir_profiles.structure_definition_mappings.eligibility.v1.patient_mapping import (
    ProfilePatient,
)

from library.fhir_profiles.structure_definition_mappings.eligibility.v1.person_mapping import (
    ProfilePerson,
)

from library.fhir_profiles.structure_definition_mappings.provider_roster.v1.practitioner_mapping import (
    ProfilePractitioner,
)
from library.fhir_profiles.structure_definition_mappings.provider_roster.v1.practitioner_role_mapping import (
    ProfilePractitionerRole,
)


class DataBackboneElementParticipant:
    @staticmethod
    def get_participant_any(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "participant"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".participant"),
                    label=label,
                    code=FhirList(
                        [
                            Coding(
                                system=ProductFeatureCode.codeset,
                                code=ProductFeatureCodeValues.IntegratedScheduling,
                            )
                        ]
                    ),
                    slicing=ElementDefinitionSlicing(
                        description="slice by type", rules=SlicingRulesCodeValues.Open
                    ),
                    min=1,
                    type_=FhirList([ElementDefinitionType(code="BackboneElement")]),
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".id"),
                    path=A.concat(resource, ".participant.id"),
                    label=label,
                    short="set to type code",
                    min=1,
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".type"),
                    path=A.concat(resource, ".participant.type"),
                    label=label,
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".actor"),
                    path=A.concat(resource, ".participant.actor"),
                    label=label,
                    short="reference to participant's defining resource",
                    type_=FhirList(
                        [
                            ElementDefinitionType(
                                code="Reference",
                                targetProfile=FhirList(
                                    [
                                        ProfilePatient.get_profile_url(),
                                        ProfileHealthcareLocation.get_profile_url(),
                                        ProfileHealthcareService.get_profile_url(),
                                        ProfilePractitioner.get_profile_url(),
                                        ProfilePractitionerRole.get_profile_url(),
                                    ]
                                ),
                            )
                        ]
                    ),
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".status"),
                    path=A.concat(resource, ".participant.status"),
                    label=label,
                    short="accepted",
                    mustSupport=A.boolean(True),
                ),
            ],
            True,
        )

        return elements

    @staticmethod
    def get_patient(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "participating-patient"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".participant"),
                    sliceName=label,
                    label=label,
                    code=FhirList(
                        [
                            Coding(
                                system=ProductFeatureCode.codeset,
                                code=ProductFeatureCodeValues.IntegratedScheduling,
                            )
                        ]
                    ),
                    short="the patient / subject of the appointment",
                    type_=FhirList([ElementDefinitionType(code="BackboneElement")]),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".type"),
                    path=A.concat(resource, ".participant.type"),
                    label=label,
                    short="Fixed: patient|https//hl7.org/fhir/ValueSet/encounter-participant-type",
                    patternCodeableConcept=CodeableConcept(
                        coding=FhirList(
                            [
                                Coding(
                                    system="https://hl7.org/fhir/ValueSet/encounter-participant-type",  # todo move to reference
                                    code=GenericTypeCode("patient"),
                                )
                            ]
                        )
                    ),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".actor"),
                    path=A.concat(resource, ".participant.actor"),
                    label=label,
                    short="reference to the individual's Patient resource",
                    type_=FhirList(
                        [
                            ElementDefinitionType(
                                code="Reference",
                                targetProfile=FhirList(
                                    [ProfilePatient.get_profile_url()]
                                ),
                            )
                        ]
                    ),
                ),
            ],
            True,
        )

        return elements

    @staticmethod
    def get_booker(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "booker"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".participant"),
                    sliceName=label,
                    label=label,
                    code=FhirList(
                        [
                            Coding(
                                system=ProductFeatureCode.codeset,
                                code=ProductFeatureCodeValues.IntegratedScheduling,
                            )
                        ]
                    ),
                    short="the individual who scheduled the appointment on behalf of the patient",
                    type_=FhirList([ElementDefinitionType(code="BackboneElement")]),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".type"),
                    path=A.concat(resource, ".participant.type"),
                    label=label,
                    short="Fixed: booker|https//hl7.org/fhir/ValueSet/encounter-participant-type",
                    patternCodeableConcept=CodeableConcept(
                        coding=FhirList(
                            [
                                Coding(
                                    system="https://hl7.org/fhir/ValueSet/encounter-participant-type",  # todo move to reference
                                    code=GenericTypeCode("booker"),
                                )
                            ]
                        )
                    ),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".actor"),
                    path=A.concat(resource, ".participant.actor"),
                    label=label,
                    short="reference to the individual's Patient or Person resource",
                    type_=FhirList(
                        [
                            ElementDefinitionType(
                                code="Reference",
                                targetProfile=FhirList(
                                    [
                                        ProfilePatient.get_profile_url(),
                                        ProfilePerson.get_profile_url(),
                                    ]
                                ),
                            )
                        ]
                    ),
                ),
            ],
            True,
        )

        return elements

    @staticmethod
    def get_location(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "participating-location"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".participant"),
                    sliceName=label,
                    label=label,
                    code=FhirList(
                        [
                            Coding(
                                system=ProductFeatureCode.codeset,
                                code=ProductFeatureCodeValues.IntegratedScheduling,
                            )
                        ]
                    ),
                    short="reference the location of the appointment",
                    type_=FhirList([ElementDefinitionType(code="BackboneElement")]),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".type"),
                    path=A.concat(resource, ".participant.type"),
                    label=label,
                    short="Fixed: facility|https//hl7.org/fhir/ValueSet/encounter-participant-type",
                    patternCodeableConcept=CodeableConcept(
                        coding=FhirList(
                            [
                                Coding(
                                    system="https://hl7.org/fhir/ValueSet/encounter-participant-type",  # todo move to reference
                                    code=GenericTypeCode("facility"),
                                )
                            ]
                        )
                    ),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".actor"),
                    path=A.concat(resource, ".participant.actor"),
                    label=label,
                    short="reference to the provider's Location resource",
                    type_=FhirList(
                        [
                            ElementDefinitionType(
                                code="Reference",
                                targetProfile=FhirList(
                                    [ProfileHealthcareLocation.get_profile_url()]
                                ),
                            )
                        ]
                    ),
                ),
            ],
            True,
        )

        return elements

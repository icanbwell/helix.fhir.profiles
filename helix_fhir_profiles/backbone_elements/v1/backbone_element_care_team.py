from spark_auto_mapper.data_types.text_like_base import AutoMapperTextLikeBase
from spark_auto_mapper_fhir.backbone_elements.element_definition import (
    ElementDefinition,
)

from spark_auto_mapper.helpers.automapper_helpers import AutoMapperHelpers as A
from spark_auto_mapper_fhir.backbone_elements.element_definition_slicing import (
    ElementDefinitionSlicing,
)
from spark_auto_mapper_fhir.backbone_elements.element_definition_type import (
    ElementDefinitionType,
)
from spark_auto_mapper_fhir.complex_types.codeable_concept import CodeableConcept
from spark_auto_mapper_fhir.complex_types.coding import Coding
from spark_auto_mapper_fhir.fhir_types.list import FhirList
from spark_auto_mapper_fhir.value_sets.generic_type import GenericTypeCode
from spark_auto_mapper_fhir.value_sets.slicing_rules import SlicingRulesCodeValues

from helix_fhir_profiles.structure_definition_mappings.provider_roster.v1.healthcare_organization_mapping import (
    ProfileHealthcareOrganization,
)
from helix_fhir_profiles.structure_definition_mappings.provider_roster.v1.practitioner_mapping import (
    ProfilePractitioner,
)


class DataBackboneElementCareTeam:
    @staticmethod
    def get_care_team_any(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "care-team"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".careTeam"),
                    label=label,
                    short="Providers listed on the claim",
                    slicing=ElementDefinitionSlicing(
                        description="slice by type", rules=SlicingRulesCodeValues.Open
                    ),
                    # comment="",
                    type_=FhirList([ElementDefinitionType(code="BackboneElement")]),
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".id"),
                    path=A.concat(resource, ".careTeam.id"),
                    label=label,
                    short="set as role code",
                    min=1,
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".sequence"),
                    path=A.concat(resource, ".careTeam.sequence"),
                    label=label,
                    min=1,
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".provider"),
                    path=A.concat(resource, ".careTeam.provider"),
                    label=label,
                    min=1,
                    type_=FhirList(
                        [
                            ElementDefinitionType(
                                code="Reference",
                                targetProfile=FhirList(
                                    [
                                        ProfilePractitioner.get_profile_url(),
                                        ProfileHealthcareOrganization.get_profile_url(),
                                    ]
                                ),
                            )
                        ]
                    ),
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".responsible"),
                    path=A.concat(resource, ".careTeam.responsible"),
                    label=label,
                    min=1,
                    type_=FhirList([ElementDefinitionType(code="boolean")]),
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".role"),
                    path=A.concat(resource, ".careTeam.role"),
                    label=label,
                    min=1,
                    mustSupport=A.boolean(True),
                ),
            ],
            True,
        )

        return elements

    @staticmethod
    def get_care_team_prescriber(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "prescribing-practitioner"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".careTeam"),
                    sliceName=label,
                    label=label,
                    short="Practitioner who prescribed the product",
                    min=1,
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".sequence"),
                    path=A.concat(resource, ".careTeam.sequence"),
                    label=label,
                    short="Fixed: 1",
                    min=1,
                    fixedInteger=1,
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".responsible"),
                    path=A.concat(resource, ".careTeam.responsible"),
                    label=label,
                    min=1,
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".role"),
                    path=A.concat(resource, ".careTeam.role"),
                    label=label,
                    patternCodeableConcept=CodeableConcept(
                        coding=FhirList(
                            [
                                Coding(
                                    id_="role-code",
                                    system="http://terminology.hl7.org/CodeSystem/claimcareteamrole",
                                    code=GenericTypeCode("Prescribing"),
                                )
                            ]
                        )
                    ),
                    min=1,
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".provider"),
                    path=A.concat(resource, ".careTeam.provider"),
                    label=label,
                    min=1,
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
                ),
            ],
            True,
        )

        return elements

    @staticmethod
    def get_care_team_servicing(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "servicing-practitioner"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".careTeam"),
                    sliceName=label,
                    label=label,
                    short="Practitioner who prescribed the product",
                    min=1,
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".sequence"),
                    path=A.concat(resource, ".careTeam.sequence"),
                    label=label,
                    short="Fixed: 1",
                    min=1,
                    fixedInteger=1,
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".responsible"),
                    path=A.concat(resource, ".careTeam.responsible"),
                    label=label,
                    min=1,
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".role"),
                    path=A.concat(resource, ".careTeam.role"),
                    label=label,
                    patternCodeableConcept=CodeableConcept(
                        coding=FhirList(
                            [
                                Coding(
                                    id_="role-code",
                                    system="http://terminology.hl7.org/CodeSystem/claimcareteamrole",
                                    code=GenericTypeCode("Servicing"),
                                )
                            ]
                        )
                    ),
                    min=1,
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".provider"),
                    path=A.concat(resource, ".careTeam.provider"),
                    label=label,
                    min=1,
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
                ),
            ],
            True,
        )

        return elements

    @staticmethod
    def get_care_team_pharmacy(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "care-team-pharmacy"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".careTeam"),
                    sliceName=label,
                    label=label,
                    short="The pharmacy providing the prescription",
                    min=1,
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".sequence"),
                    path=A.concat(resource, ".careTeam.sequence"),
                    label=label,
                    short="Fixed: 2",
                    min=1,
                    fixedInteger=2,
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".responsible"),
                    path=A.concat(resource, ".careTeam.responsible"),
                    label=label,
                    min=1,
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".role"),
                    path=A.concat(resource, ".careTeam.role"),
                    label=label,
                    patternCodeableConcept=CodeableConcept(
                        coding=FhirList(
                            [
                                Coding(
                                    id_="role-code",
                                    system="http://terminology.hl7.org/CodeSystem/claimcareteamrole",
                                    code=GenericTypeCode("Servicing"),
                                )
                            ]
                        )
                    ),
                    min=1,
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".provider"),
                    path=A.concat(resource, ".careTeam.provider"),
                    label=label,
                    min=1,
                    type_=FhirList(
                        [
                            ElementDefinitionType(
                                code="Reference",
                                targetProfile=FhirList(
                                    [ProfileHealthcareOrganization.get_profile_url()]
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
    def get_care_team_attending(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "care-team-attending"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".careTeam"),
                    sliceName=label,
                    label=label,
                    min=1,
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".sequence"),
                    path=A.concat(resource, ".careTeam.sequence"),
                    label=label,
                    min=1,
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".responsible"),
                    path=A.concat(resource, ".careTeam.responsible"),
                    label=label,
                    min=1,
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".role"),
                    path=A.concat(resource, ".careTeam.role"),
                    label=label,
                    patternCodeableConcept=CodeableConcept(
                        coding=FhirList(
                            [
                                Coding(
                                    id_="role-code",
                                    system="http://terminology.hl7.org/CodeSystem/claimcareteamrole",
                                    code=GenericTypeCode("Attending"),
                                )
                            ]
                        )
                    ),
                    min=1,
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".provider"),
                    path=A.concat(resource, ".careTeam.provider"),
                    label=label,
                    min=1,
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
                ),
            ],
            True,
        )

        return elements

    @staticmethod
    def get_care_team_operating(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "care-team-operating"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".careTeam"),
                    sliceName=label,
                    label=label,
                    min=1,
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".sequence"),
                    path=A.concat(resource, ".careTeam.sequence"),
                    label=label,
                    min=1,
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".responsible"),
                    path=A.concat(resource, ".careTeam.responsible"),
                    label=label,
                    min=1,
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".role"),
                    path=A.concat(resource, ".careTeam.role"),
                    label=label,
                    patternCodeableConcept=CodeableConcept(
                        coding=FhirList(
                            [
                                Coding(
                                    id_="role-code",
                                    system="http://terminology.hl7.org/CodeSystem/claimcareteamrole",
                                    code=GenericTypeCode("Operating"),
                                )
                            ]
                        )
                    ),
                    min=1,
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".provider"),
                    path=A.concat(resource, ".careTeam.provider"),
                    label=label,
                    min=1,
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
                ),
            ],
            True,
        )

        return elements

    @staticmethod
    def get_care_team_rendering(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "care-team-rendering"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".careTeam"),
                    sliceName=label,
                    label=label,
                    min=1,
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".sequence"),
                    path=A.concat(resource, ".careTeam.sequence"),
                    label=label,
                    min=1,
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".responsible"),
                    path=A.concat(resource, ".careTeam.responsible"),
                    label=label,
                    min=1,
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".role"),
                    path=A.concat(resource, ".careTeam.role"),
                    label=label,
                    patternCodeableConcept=CodeableConcept(
                        coding=FhirList(
                            [
                                Coding(
                                    id_="role-code",
                                    system="http://terminology.hl7.org/CodeSystem/claimcareteamrole",
                                    code=GenericTypeCode("Rendering"),
                                )
                            ]
                        )
                    ),
                    min=1,
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".provider"),
                    path=A.concat(resource, ".careTeam.provider"),
                    label=label,
                    min=1,
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
                ),
            ],
            True,
        )

        return elements

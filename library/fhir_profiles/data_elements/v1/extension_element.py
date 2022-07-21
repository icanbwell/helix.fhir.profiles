from spark_auto_mapper_fhir.backbone_elements.element_definition_example import (
    ElementDefinitionExample,
)
from spark_auto_mapper_fhir.complex_types.codeable_concept import CodeableConcept
from spark_auto_mapper_fhir.complex_types.coding import Coding
from spark_auto_mapper_fhir.value_sets.custom.search_characteristic import (
    SearchCharacteristicCode,
    SearchCharacteristicCodeValues,
)
from spark_auto_mapper_fhir.value_sets.generic_type import GenericTypeCode

from library.fhir_profiles.structure_definition_mappings.insurance.v1.healthcare_network_mapping import (
    ProfileHealthcareNetwork,
)

from library.fhir_profiles.structure_definition_mappings.insurance.v1.insurance_plan_mapping import (
    ProfileInsurancePlan,
)

from library.fhir_profiles.structure_definition_mappings.eligibility.v1.partner_organization_mapping import (
    ProfilePartnerOrganization,
)

from library.fhir_profiles.structure_definition_mappings.eligibility.v1.patient_mapping import (
    ProfilePatient,
)
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
from spark_auto_mapper_fhir.fhir_types.list import FhirList
from spark_auto_mapper_fhir.value_sets.slicing_rules import SlicingRulesCodeValues


class DataElementExtension:
    @staticmethod
    def get_extension_any(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "extension-any"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".extension"),
                    label=label,
                    slicing=ElementDefinitionSlicing(
                        description="slice by types", rules=SlicingRulesCodeValues.Open
                    ),
                    type_=FhirList([ElementDefinitionType(code="Extension")]),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".id"),
                    path=A.concat(resource, ".extension.id"),
                    label=label,
                    short="defined case-by-case, but is frequently the extension url",
                    min=1,
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".extension"),
                    path=A.concat(resource, ".extension.extension"),
                    label=label,
                    min=0,
                    max="*",
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".url"),
                    path=A.concat(resource, ".extension.url"),
                    label=label,
                    min=1,
                    max="1",
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".value[x]"),
                    path=A.concat(resource, ".extension.value[x]"),
                    label=label,
                    min=0,
                    max="1",
                ),
            ],
            True,
        )

        return elements

    @staticmethod
    def get_reference_network(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "reference-network"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("extension-", label),
                    path=A.concat(resource, ".extension"),
                    sliceName=label,
                    label=label,
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="Extension")]),
                ),
                ElementDefinition(
                    id_=A.concat("extension-", label, ".id"),
                    path=A.concat(resource, ".extension.id"),
                    label=label,
                    short="referenced id",
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="string")]),
                ),
                ElementDefinition(
                    id_=A.concat("extension-", label, ".url"),
                    path=A.concat(resource, ".extension.url"),
                    label=label,
                    short="fixed value: ",
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="uri")])
                    # fixedUri="",
                ),
                ElementDefinition(
                    id_=A.concat("extension-", label, ".value[x]"),
                    path=A.concat(resource, ".extension.value[x]"),
                    label=label,
                    short="client code",
                    min=1,
                    max="1",
                    type_=FhirList(
                        [
                            ElementDefinitionType(
                                code="Reference",
                                targetProfile=FhirList(
                                    [ProfileHealthcareNetwork.get_profile_url()]
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
    def get_accepted_patients(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "accepted-patients"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("extension-", label),
                    path=A.concat(resource, ".extension"),
                    sliceName=label,
                    label=label,
                    short="Includes: New vs Existing Patient indicator & Patient Age Range(s)",
                    type_=FhirList([ElementDefinitionType(code="Extension")]),
                    # example=
                ),
                ElementDefinition(
                    id_=A.concat("extension-", label, ".id"),
                    path=A.concat(resource, ".extension.id"),
                    label=label,
                    short="accepted-patients",
                    min=1,
                    type_=FhirList([ElementDefinitionType(code="string")]),
                ),
                ElementDefinition(
                    id_=A.concat("extension-", label, ".extension"),
                    path=A.concat(resource, ".extension.extension"),
                    sliceName="new-patients",
                    label=A.concat(label, "-new-patients"),
                    short="an indicator for whether the provider accepts new and/or existing patients",
                    min=0,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="Extension")]),
                ),
                ElementDefinition(
                    id_=A.concat("extension-", label, ".extension.id"),
                    path=A.concat(resource, ".extension.extension.id"),
                    label=A.concat(label, "-new-patients"),
                    short="new-patients",
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="string")]),
                ),
                ElementDefinition(
                    id_=A.concat("extension-", label, ".extension.url"),
                    path=A.concat(resource, ".extension.extension.url"),
                    label=A.concat(label, "-new-patients"),
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="uri")]),
                    fixedUri="acceptingPatients",
                ),
                ElementDefinition(
                    id_=A.concat(
                        "extension-", label, ".extension.valueCodeableConcept"
                    ),
                    path=A.concat(resource, ".extension.extension.value[x]"),
                    label=A.concat(label, "-new-patients"),
                    short="coded value",
                    min=0,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="CodeableConcept")])
                    # binding = "https://build.fhir.org/ig/HL7/davinci-pdex-plan-net/CodeSystem-AcceptingPatientsCS.html"
                ),
                ElementDefinition(
                    id_=A.concat("extension-", label, ".extension"),
                    path=A.concat(resource, ".extension.extension"),
                    sliceName="age-range",
                    label=A.concat(label, "-age-range"),
                    short="age range(s) accepted",
                    min=0,
                    max="*",
                    type_=FhirList([ElementDefinitionType(code="Extension")]),
                ),
                ElementDefinition(
                    id_=A.concat("extension-", label, ".extension.id"),
                    path=A.concat(resource, ".extension.extension.id"),
                    label=A.concat(label, "-age-range"),
                    short="age-range or category code",
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="string")]),
                ),
                ElementDefinition(
                    id_=A.concat("extension-", label, ".extension.url"),
                    path=A.concat(resource, ".extension.extension.url"),
                    label=A.concat(label, "-age-range"),
                    short="fixed value: ageRange",
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="uri")]),
                    fixedUri="ageRange",
                ),
                ElementDefinition(
                    id_=A.concat("extension-", label, ".extension.valueRange"),
                    path=A.concat(resource, ".extension.extension.value[x]"),
                    label=A.concat(label, "-age-range"),
                    short="age range in unit = years",
                    min=0,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="Range")]),
                ),
                ElementDefinition(
                    id_=A.concat("extension-", label, ".url"),
                    path=A.concat(resource, ".extension.url"),
                    label=label,
                    short="fixed value: http://hl7.org/fhir/us/davinci-pdex-plan-net/StructureDefinition/newpatients",
                    definition="this spec is based upon Da-Vinci's extension for new patients",
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="uri")]),
                    fixedUri="http://hl7.org/fhir/us/davinci-pdex-plan-net/StructureDefinition/newpatients",
                ),
            ],
            True,
        )

        return elements

    @staticmethod
    def get_client_tag(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "client-tag"

        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("extension-", label),
                    path=A.concat(resource, ".extension"),
                    sliceName=label,
                    label=label,
                    type_=FhirList([ElementDefinitionType(code="Extension")]),
                ),
                ElementDefinition(
                    id_=A.concat("extension-", label, ".id"),
                    path=A.concat(resource, ".extension.id"),
                    label=label,
                    short="same as client code value",
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="string")]),
                ),
                ElementDefinition(
                    id_=A.concat("extension-", label, ".url"),
                    path=A.concat(resource, ".extension.url"),
                    label=label,
                    short="fixed value: https://www.icanbwell.com/client",
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="uri")]),
                    fixedUri="https://www.icanbwell.com/client",
                ),
                ElementDefinition(
                    id_=A.concat("extension-", label, ".value[x]"),
                    path=A.concat(resource, ".extension.value[x]"),
                    label=label,
                    short="client code",
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="code")]),
                ),
            ],
            True,
        )

        return elements

    @staticmethod
    def get_contact_related_patient(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "contact-related-patient"

        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("extension-", label),
                    path=A.concat(resource, ".extension"),
                    sliceName=label,
                    label=label,
                    short="Extension to reference another Patient resource",
                    type_=FhirList([ElementDefinitionType(code="Extension")]),
                ),
                ElementDefinition(
                    id_=A.concat("extension-", label, ".id"),
                    path=A.concat(resource, ".extension.id"),
                    label=label,
                    short="id to uniquely identify the individual / extension",
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="string")]),
                ),
                ElementDefinition(
                    id_=A.concat("extension-", label, ".url"),
                    path=A.concat(resource, ".extension.url"),
                    label=label,
                    short="fixed value: https://www.icanbwell.com/extension-contact-related-patient",
                    definition="identifies the meaning of the extension",
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="uri")]),
                    fixedUri="https://www.icanbwell.com/extension-contact-related-patient",
                ),
                ElementDefinition(
                    id_=A.concat("extension-", label, ".valueReference"),
                    path=A.concat(resource, ".extension.valueReference"),
                    label=label,
                    short="Reference to relevant Patient resource",
                    definition="Reference to relevant Patient resource",
                    min=0,
                    max="1",
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
    def get_employer_organization(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "employer-organization"

        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("extension-", label),
                    path=A.concat(resource, ".extension"),
                    sliceName=label,
                    label=label,
                    type_=FhirList([ElementDefinitionType(code="Extension")]),
                ),
                ElementDefinition(
                    id_=A.concat("extension-", label, ".id"),
                    path=A.concat(resource, ".extension.id"),
                    label=label,
                    short="employer",
                    min=1,
                    type_=FhirList([ElementDefinitionType(code="string")]),
                ),
                ElementDefinition(
                    id_=A.concat("extension-", label, ".url"),
                    path=A.concat(resource, ".extension.url"),
                    label=label,
                    short="fixed value: http://hl7.org/fhir/us/odh/StructureDefinition/odh-Employer-extension",
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="uri")]),
                    fixedUri="http://hl7.org/fhir/us/odh/StructureDefinition/odh-Employer-extension",
                ),
                ElementDefinition(
                    id_=A.concat("extension-", label, ".valueReference"),
                    path=A.concat(resource, ".extension.valueReference"),
                    label=label,
                    min=1,
                    max="1",
                    type_=FhirList(
                        [
                            ElementDefinitionType(
                                code="Reference",
                                targetProfile=FhirList(
                                    [ProfilePartnerOrganization.get_profile_url()]
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
    def get_insurance_plan(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "insurance-plan"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("extension-", label),
                    path=A.concat(resource, ".extension"),
                    sliceName=label,
                    label=label,
                    type_=FhirList([ElementDefinitionType(code="Extension")]),
                ),
                ElementDefinition(
                    id_=A.concat("extension-", label, ".id"),
                    path=A.concat(resource, ".extension.id"),
                    label=label,
                    short="tbd",  # todo
                    min=1,
                    type_=FhirList([ElementDefinitionType(code="string")]),
                ),
                ElementDefinition(
                    id_=A.concat("extension-", label, ".url"),
                    path=A.concat(resource, ".extension.url"),
                    label=label,
                    short="fixed value: https://raw.githubusercontent.com/imranq2/SparkAutoMapper.FHIR/main/StructureDefinition/insurance_plan",
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="uri")]),
                    fixedUri="https://raw.githubusercontent.com/imranq2/SparkAutoMapper.FHIR/main/StructureDefinition/insurance_plan",
                ),
                ElementDefinition(
                    id_=A.concat("extension-", label, ".valueReference"),
                    path=A.concat(resource, ".extension.valueReference"),
                    label=label,
                    min=1,
                    max="1",
                    type_=FhirList(
                        [
                            ElementDefinitionType(
                                code="Reference",
                                targetProfile=FhirList(
                                    [ProfileInsurancePlan.get_profile_url()]
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
    def get_location_image(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "location-image"

        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("extension-", label),
                    path=A.concat(resource, ".extension"),
                    sliceName=label,
                    label=label,
                    type_=FhirList([ElementDefinitionType(code="Extension")]),
                ),
                ElementDefinition(
                    id_=A.concat("extension-", label, ".id"),
                    path=A.concat(resource, ".extension.id"),
                    label=label,
                    short="photo",
                    min=1,
                    type_=FhirList([ElementDefinitionType(code="string")]),
                ),
                ElementDefinition(
                    id_=A.concat("extension-", label, ".url"),
                    path=A.concat(resource, ".extension.url"),
                    label=label,
                    comment="Needs Review, this value has been set as a client-specific value",
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="uri")]),
                ),
                ElementDefinition(
                    id_=A.concat("extension-", label, ".valueString"),
                    path=A.concat(resource, ".extension.valueString"),
                    label=label,
                    short="link to photo as a string value",
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="string")]),
                ),
            ],
            True,
        )

        return elements

    @staticmethod
    def get_location_parking(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "location-parking"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("extension-", label),
                    path=A.concat(resource, ".extension"),
                    sliceName=label,
                    label=label,
                    type_=FhirList([ElementDefinitionType(code="Extension")]),
                ),
                ElementDefinition(
                    id_=A.concat("extension-", label, ".id"),
                    path=A.concat(resource, ".extension.id"),
                    label=label,
                    short="parking",
                    min=1,
                    type_=FhirList([ElementDefinitionType(code="string")]),
                ),
                ElementDefinition(
                    id_=A.concat("extension-", label, ".url"),
                    path=A.concat(resource, ".extension.url"),
                    label=label,
                    comment="Needs Review, this value has been set as a client-specific value",
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="uri")]),
                ),
                ElementDefinition(
                    id_=A.concat("extension-", label, ".valueString"),
                    path=A.concat(resource, ".extension.valueString"),
                    label=label,
                    short="string value of the directions",
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="string")]),
                ),
            ],
            True,
        )

        return elements

    @staticmethod
    def get_provider_search(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "provider-search"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("extension-", label),
                    path=A.concat(resource, ".extension"),
                    sliceName=label,
                    label=label,
                    short="extension container for provider search characteristics per system",
                    type_=FhirList([ElementDefinitionType(code="Extension")]),
                ),
                ElementDefinition(
                    id_=A.concat("extension-", label, ".id"),
                    path=A.concat(resource, ".extension.id"),
                    label=label,
                    short="providersearch",
                    min=1,
                    type_=FhirList([ElementDefinitionType(code="string")]),
                ),
                # SEARCH SYSTEM SUB-EXTENSION
                ElementDefinition(
                    id_=A.concat("extension-", label, ".extension-search-system"),
                    path=A.concat(resource, ".extension.extension"),
                    sliceName="search-system",
                    label=A.concat(label, "-search-system"),
                    short="extension(s) to indicate the provider search system",
                    requirements="Indicate the provider search system URI, in case the provider instance belongs to feeds more than one search system",
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="Extension")]),
                ),
                ElementDefinition(
                    id_=A.concat("extension-", label, ".extension-search-system.id"),
                    path=A.concat(resource, ".extension.extension.id"),
                    label=A.concat(label, "-search-system"),
                    short="forsystem",
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="string")]),
                ),
                ElementDefinition(
                    id_=A.concat("extension-", label, ".extension-search-system.url"),
                    path=A.concat(resource, ".extension.extension.url"),
                    label=A.concat(label, "-search-system"),
                    short="fixed value: forSystem",
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="uri")]),
                    fixedUri="forSystem",
                ),
                ElementDefinition(
                    id_=A.concat(
                        "extension-", label, ".extension-search-system.valueUri"
                    ),
                    path=A.concat(resource, ".extension.extension.valueUri"),
                    label=A.concat(label, "-search-system"),
                    short="uri / url of the search system",
                    requirements="Although the context of this already implies it's for the Helix Provider Search Service, this field was included in the definition to specify which front end version of PSS. This would accommodate clients in the event they have more than one portal with us.",
                    min=0,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="uri")]),
                ),
                # SEARCHABLE SUB-EXTENSION
                ElementDefinition(
                    id_=A.concat("extension-", label, ".extension-searchable"),
                    path=A.concat(resource, ".extension.extension"),
                    sliceName="searchable",
                    label=A.concat(label, "-searchable"),
                    short="extension(s) for a coded characteristic",
                    definition="a list of characteristics to describe the behavior and/or visibility of the record. Examples: online bookable; provider searchable",
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="Extension")]),
                ),
                ElementDefinition(
                    id_=A.concat("extension-", label, ".extension-searchable.id"),
                    path=A.concat(resource, ".extension.extension.id"),
                    label=A.concat(label, "-searchable"),
                    short="searchable",
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="string")]),
                ),
                ElementDefinition(
                    id_=A.concat("extension-", label, ".extension-searchable.url"),
                    path=A.concat(resource, ".extension.extension.url"),
                    label=A.concat(label, "-searchable"),
                    short="fixed value: searchCharacteristic",
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="uri")]),
                    fixedUri="searchCharacteristic",
                ),
                ElementDefinition(
                    id_=A.concat(
                        "extension-",
                        label,
                        ".extension-searchable.valueCodeableConcept",
                    ),
                    path=A.concat(
                        resource, ".extension.extension.valueCodeableConcept"
                    ),
                    label=A.concat(label, "-searchable"),
                    short="searchable | hide-from-search",
                    min=0,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="CodeableConcept")]),
                ),
                # BOOKABLE SUB-EXTENSION
                ElementDefinition(
                    id_=A.concat("extension-", label, ".extension-bookable"),
                    path=A.concat(resource, ".extension.extension"),
                    sliceName="bookable",
                    label=A.concat(label, "-bookable"),
                    short="extension(s) for coded bookablity characteristics",
                    min=0,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="Extension")]),
                ),
                ElementDefinition(
                    id_=A.concat("extension-", label, ".extension-bookable.id"),
                    path=A.concat(resource, ".extension.extension.id"),
                    label=A.concat(label, "-bookable"),
                    short="bookable",
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="string")]),
                ),
                ElementDefinition(
                    id_=A.concat("extension-", label, ".extension-bookable.url"),
                    path=A.concat(resource, ".extension.extension.url"),
                    label=A.concat(label, "-bookable"),
                    short="fixed value: bookable",
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="uri")]),
                    fixedUri="bookable",
                ),
                ElementDefinition(
                    id_=A.concat(
                        "extension-", label, ".extension-bookable.valueCodeableConcept"
                    ),
                    path=A.concat(
                        resource, ".extension.extension.valueCodeableConcept"
                    ),
                    label=A.concat(label, "-bookable"),
                    short="bookable-phone | bookable-online",
                    requirements="through the Coding object, multiple codes can be assigned",
                    min=0,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="CodeableConcept")]),
                    example=FhirList(
                        [
                            ElementDefinitionExample(
                                label="provider is online bookable and has 'call to book' option",
                                valueCodeableConcept=CodeableConcept(
                                    coding=FhirList(
                                        [
                                            Coding(
                                                id_="bookable-phone",
                                                system=SearchCharacteristicCode.codeset,
                                                code=SearchCharacteristicCodeValues.BookablePhone,
                                            ),
                                            Coding(
                                                id_="bookable-online",
                                                system=SearchCharacteristicCode.codeset,
                                                code=SearchCharacteristicCodeValues.BookableOnline,
                                            ),
                                        ]
                                    )
                                ),
                            ),
                            ElementDefinitionExample(
                                label="epic open scheduling",
                                valueCodeableConcept=CodeableConcept(
                                    coding=FhirList(
                                        [
                                            Coding(
                                                id_="bookable-phone",
                                                system=SearchCharacteristicCode.codeset,
                                                code=SearchCharacteristicCodeValues.BookablePhone,
                                            ),
                                            Coding(
                                                id_="bookable-online",
                                                system=SearchCharacteristicCode.codeset,
                                                code=SearchCharacteristicCodeValues.BookableOnline,
                                            ),
                                            Coding(
                                                id_="epic-scheduling",
                                                system="https://healthcaresystem.org/epic/scheduling_type",
                                                code=GenericTypeCode("open"),
                                            ),
                                        ]
                                    )
                                ),
                            ),
                        ]
                    ),
                ),
                # parent extension url
                ElementDefinition(
                    id_=A.concat("extension-", label, ".url"),
                    path=A.concat(resource, ".extension.url"),
                    label=label,
                    short="fixed value: https://raw.githubusercontent.com/imranq2/SparkAutoMapper.FHIR/main/StructureDefinition/provider_search",
                    min=1,
                    max="1",
                    fixedUri="https://raw.githubusercontent.com/imranq2/SparkAutoMapper.FHIR/main/StructureDefinition/provider_search",
                ),
                # no value[x] because there were sub-extensions
                ElementDefinition(
                    id_=A.concat("extension-", label, ".value[x]"),
                    path=A.concat(resource, ".extension.value[x]"),
                    max="0",
                ),
            ],
            True,
        )

        return elements

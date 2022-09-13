from spark_auto_mapper.data_types.text_like_base import AutoMapperTextLikeBase
from spark_auto_mapper_fhir.backbone_elements.element_definition import (
    ElementDefinition,
)

from spark_auto_mapper.helpers.automapper_helpers import AutoMapperHelpers as A
from spark_auto_mapper_fhir.backbone_elements.element_definition_example import (
    ElementDefinitionExample,
)
from spark_auto_mapper_fhir.backbone_elements.element_definition_slicing import (
    ElementDefinitionSlicing,
)
from spark_auto_mapper_fhir.backbone_elements.element_definition_type import (
    ElementDefinitionType,
)
from spark_auto_mapper_fhir.complex_types.codeable_concept import CodeableConcept
from spark_auto_mapper_fhir.complex_types.coding import Coding
from spark_auto_mapper_fhir.complex_types.identifier import Identifier
from spark_auto_mapper_fhir.fhir_types.list import FhirList
from spark_auto_mapper_fhir.value_sets.identifier_type_codes import (
    IdentifierTypeCodesCodeValues,
    IdentifierTypeCodesCode,
)
from spark_auto_mapper_fhir.value_sets.identifier_use import IdentifierUseCodeValues
from spark_auto_mapper_fhir.value_sets.slicing_rules import SlicingRulesCodeValues

from helix_fhir_profiles.schema.v1.product_feature_codes import (
    ProductFeatureCode,
    ProductFeatureCodeValues,
)


class DataElementIdentifier:
    @staticmethod
    def get_identifier_any(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "identifier"
        element = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".identifier"),
                    label=label,
                    slicing=ElementDefinitionSlicing(
                        description="slice by types", rules=SlicingRulesCodeValues.Open
                    ),
                    short="a value to identify the resource by",
                    # definition="",
                    # comment="",
                    # requirements="",
                    type_=FhirList([ElementDefinitionType(code="Identifier")]),
                ),
                ElementDefinition(
                    id_=A.concat(label, ".id"),
                    path=A.concat(resource, ".identifier.id"),
                    label=label,
                    short="set case-by-case",
                    # definition="",
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="string")]),
                ),
                ElementDefinition(
                    id_=A.concat(label, ".use"),
                    path=A.concat(resource, ".identifier.use"),
                    label=label,
                    short="usual | official | temp | secondary | old (If known)",
                    definition="The purpose of this identifier.",
                    min=0,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="code")]),
                ),
                ElementDefinition(
                    id_=A.concat(label, ".type"),
                    path=A.concat(resource, ".identifier.type"),
                    label=label,
                    short="Description of identifier",
                    definition="A coded type for the identifier that can be used to determine which identifier to use for a specific purpose.",
                    requirements="Needs binding valueset",
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="CodeableConcept")]),
                    # binding
                ),
                ElementDefinition(
                    id_=A.concat(label, ".system"),
                    path=A.concat(resource, ".identifier.system"),
                    label=label,
                    short="The system which created the identifier",
                    definition="Values may be an oid, uri, url, or canonical",
                    comment="for mapped data, this is frequently a canonical url",
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="uri")]),
                    example=FhirList(
                        [
                            ElementDefinitionExample(
                                label="a client's unknown system",
                                valueUri="https://www.health.org/person-identifier",
                            )
                        ]
                    ),
                ),
                ElementDefinition(
                    id_=A.concat(label, ".value"),
                    path=A.concat(resource, ".identifier.value"),
                    label=label,
                    short="The unique value",
                    definition="The raw identifier value that represents a resource",
                    requirements="This should be the raw value, as it exists in the source data (ie without prefix)",
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="string")]),
                ),
            ],
            True,
        )
        return element

    # ENTITIES (people / orgs)
    @staticmethod
    def get_npi(resource: AutoMapperTextLikeBase) -> FhirList[ElementDefinition]:
        label = "npi"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".identifier"),
                    sliceName=label,
                    label=label,
                    code=FhirList(
                        [
                            Coding(
                                system=ProductFeatureCode.codeset,
                                code=ProductFeatureCodeValues.ProviderSearch,
                            ),
                        ]
                    ),
                    short="NPI of a practitioner or organization",
                    definition="national provider identifier as defined by nppes",
                    # comment="",
                    # requirements="",
                    type_=FhirList([ElementDefinitionType(code="Identifier")]),
                    patternIdentifier=Identifier(
                        id_="npi",
                        use=IdentifierUseCodeValues.Official,
                        type_=CodeableConcept(
                            coding=FhirList(
                                [
                                    Coding(
                                        id_="type-npi",
                                        system=IdentifierTypeCodesCode.codeset,
                                        code=IdentifierTypeCodesCodeValues.NationalProviderIdentifier,
                                    )
                                ]
                            )
                        ),
                        system="http://hl7.org/fhir/sid/us-npi",
                    ),
                )
            ]
        )

        return elements

    @staticmethod
    def get_facility_id(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "facility-id"
        elements = FhirList(
            [
                ElementDefinition(
                    id_="de-identifier-facility-id",
                    path=A.concat(resource, ".identifier"),
                    sliceName=label,
                    label=label,
                    code=FhirList(
                        [
                            Coding(
                                system=ProductFeatureCode.codeset,
                                code=ProductFeatureCodeValues.ProviderSearch,
                            )
                        ]
                    ),
                    short="external source id for the location",
                    definition="raw value used by the data source to identify the record",
                    # comment="",
                    min=1,
                    alias=FhirList(["location identifier", "practice identifier"]),
                    requirements="system = source URI",
                    type_=FhirList([ElementDefinitionType(code="Identifier")]),
                    patternIdentifier=Identifier(
                        id_="facility-id",
                        type_=CodeableConcept(
                            coding=FhirList(
                                [
                                    Coding(
                                        id_="facility-id",
                                        system=IdentifierTypeCodesCode.codeset,
                                        code=IdentifierTypeCodesCodeValues.FacilityID,
                                    )
                                ]
                            )
                        ),
                    ),
                )
            ]
        )

        return elements

    @staticmethod
    def get_tin(resource: AutoMapperTextLikeBase) -> FhirList[ElementDefinition]:
        label = "tax-id"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".identifier"),
                    sliceName=label,
                    label=label,
                    code=FhirList(
                        [
                            Coding(
                                system=ProductFeatureCode.codeset,
                                # code=ProductFeatureCodeValues.,
                            ),
                        ]
                    ),
                    short="Tax ID of a practitioner or organization",
                    definition="Tax ID as defined by nppes",
                    # comment="",
                    # requirements="",
                    min=0,
                    alias=FhirList(["tax identification number", "TIN"]),
                    type_=FhirList([ElementDefinitionType(code="Identifier")]),
                    patternIdentifier=Identifier(
                        id_="tin",
                        use=IdentifierUseCodeValues.Official,
                        type_=CodeableConcept(
                            coding=FhirList(
                                [
                                    Coding(
                                        id_="type-tin",
                                        system=IdentifierTypeCodesCode.codeset,
                                        code=IdentifierTypeCodesCodeValues.TaxIDNumber,
                                    )
                                ]
                            )
                        ),
                        system="http://hl7.org/fhir/sid/us-tin",
                    ),
                )
            ]
        )

        return elements

    @staticmethod
    def get_provider_id(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "provider-id"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".identifier"),
                    sliceName=label,
                    label=label,
                    code=FhirList(
                        [
                            Coding(
                                system=ProductFeatureCode.codeset,
                                code=ProductFeatureCodeValues.ProviderSearch,
                            )
                        ]
                    ),
                    short="external source id for the practitioner",
                    definition="raw value used by the data source to identify the practitioner",
                    # comment="",
                    min=0,
                    alias=FhirList(
                        ["practitioner identifier", "ehr identifier", "prn"]
                    ),
                    requirements="system = source URI",
                    type_=FhirList([ElementDefinitionType(code="Identifier")]),
                    patternIdentifier=Identifier(
                        id_="provider-id",
                        type_=CodeableConcept(
                            coding=FhirList(
                                [
                                    Coding(
                                        id_="provider-id",
                                        system=IdentifierTypeCodesCode.codeset,
                                        code=IdentifierTypeCodesCodeValues.ProviderNumber,
                                    )
                                ]
                            )
                        ),
                    ),
                )
            ]
        )

        return elements

    @staticmethod
    def get_dea_number(resource: AutoMapperTextLikeBase) -> FhirList[ElementDefinition]:
        label = "dea-number"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".identifier"),
                    sliceName=label,
                    label=label,
                    code=FhirList(
                        [
                            Coding(
                                system=ProductFeatureCode.codeset,
                                code=ProductFeatureCodeValues.ProviderSearch,
                            )
                        ]
                    ),
                    short="Provider's Drug Enforcement Administration license number",
                    # definition="",
                    # comment="",
                    min=0,
                    # alias=FhirList(
                    #     [
                    #     ]
                    # ),
                    # requirements="",
                    type_=FhirList([ElementDefinitionType(code="Identifier")]),
                    patternIdentifier=Identifier(
                        id_="dea-number",
                        type_=CodeableConcept(
                            coding=FhirList(
                                [
                                    Coding(
                                        id_="dea-number",
                                        system=IdentifierTypeCodesCode.codeset,
                                        code=IdentifierTypeCodesCodeValues.DrugEnforcementAdministrationRegistrationNumber,
                                    )
                                ]
                            )
                        ),
                    ),
                )
            ]
        )

        return elements

    @staticmethod
    def get_member_number(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "identifier-member-number"
        elements = FhirList(
            [
                ElementDefinition(
                    id_="de-member-number",
                    path=A.concat(resource, ".identifier"),
                    sliceName=label,
                    label=label,
                    code=FhirList(
                        [
                            Coding(
                                system=ProductFeatureCode.codeset,
                                # code=ProductFeatureCodeValues.,
                            ),
                        ]
                    ),
                    short="insurance coverage's unique identifier for the individual",
                    # definition="",
                    # comment="",
                    requirements="system = source URI",
                    type_=FhirList([ElementDefinitionType(code="Identifier")]),
                    patternIdentifier=Identifier(
                        id_="member-number",
                        type_=CodeableConcept(
                            coding=FhirList(
                                [
                                    Coding(
                                        id_="member-number-type",
                                        system=IdentifierTypeCodesCode.codeset,
                                        code=IdentifierTypeCodesCodeValues.MemberNumber,
                                    )
                                ]
                            )
                        ),
                    ),
                    # example=FhirList(
                    #     [
                    #         ElementDefinitionExample(
                    #             label="medicare beneficiary id",
                    #             valueIdentifier=Identifier(
                    #                 id_="mbi",
                    #                 type_=CodeableConcept(
                    #                     coding=FhirList(
                    #                         [
                    #                             Coding(
                    #                                 # id_="",
                    #                                 system="",
                    #                                 code=IdentifierTypeCodesCode("")
                    #                             )
                    #                         ]
                    #                     )
                    #                 ),
                    #                 system="",
                    #                 value="",
                    #             )
                    #         )
                    #     ]
                    # )
                )
            ]
        )

        return elements

    @staticmethod
    def get_employee_id(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "employee-id"
        elements = FhirList(
            [
                ElementDefinition(
                    id_="de-employee-id",
                    path=A.concat(resource, ".identifier"),
                    label=label,
                    sliceName="identifier-employee-id",
                    code=FhirList(
                        [
                            Coding(
                                system=ProductFeatureCode.codeset,
                                code=ProductFeatureCodeValues.Employment,
                            ),
                        ]
                    ),
                    short="employer's's unique identifier for the individual",
                    # definition="",
                    # comment="",
                    requirements="system = source URI",
                    type_=FhirList([ElementDefinitionType(code="Identifier")]),
                    patternIdentifier=Identifier(
                        id_="employee-id",
                        type_=CodeableConcept(
                            coding=FhirList(
                                [
                                    Coding(
                                        id_="employee-id-type",
                                        system=IdentifierTypeCodesCode.codeset,
                                        code=IdentifierTypeCodesCodeValues.EmployeeNumber,
                                    )
                                ]
                            )
                        ),
                    ),
                )
            ]
        )

        return elements

    @staticmethod
    def get_ssn(resource: AutoMapperTextLikeBase) -> FhirList[ElementDefinition]:
        label = "ssn"
        elements = FhirList(
            [
                ElementDefinition(
                    id_="de-ssn",
                    path=A.concat(resource, ".identifier"),
                    sliceName=label,
                    label=label,
                    code=FhirList(
                        [
                            Coding(
                                system=ProductFeatureCode.codeset,
                                code=ProductFeatureCodeValues.Person,
                            ),
                        ]
                    ),
                    short="social security number",
                    # definition="",
                    # comment="",
                    # requirements="",
                    type_=FhirList([ElementDefinitionType(code="Identifier")]),
                    patternIdentifier=Identifier(
                        id_="ssn",
                        type_=CodeableConcept(
                            coding=FhirList(
                                [
                                    Coding(
                                        id_="ssn-type",
                                        system=IdentifierTypeCodesCode.codeset,
                                        code=IdentifierTypeCodesCodeValues.SocialSecurityNumber,
                                    )
                                ]
                            )
                        ),
                        system="http://hl7.org/fhir/sid/us-ssn",
                        # value=""
                    ),
                )
            ]
        )

        return elements

    @staticmethod
    def get_medicare_beneficiary_id(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "medicare-beneficiary-id"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".identifier"),
                    sliceName=label,
                    label=label,
                    short="Medicare Beneficiary Identifier (US)",
                    # definition="",
                    # comment="",
                    # requirements="",
                    type_=FhirList([ElementDefinitionType(code="Identifier")]),
                    patternIdentifier=Identifier(
                        id_="mbi",
                        type_=CodeableConcept(
                            coding=FhirList(
                                [
                                    Coding(
                                        id_="mbi-type",
                                        system=IdentifierTypeCodesCode.codeset,
                                        code=IdentifierTypeCodesCodeValues.Patient_sMedicareNumber,
                                    )
                                ]
                            )
                        ),
                        system="http://hl7.org/fhir/sid/us-mbi",
                    ),
                )
            ]
        )

        return elements

    @staticmethod
    def get_provider_location_id(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "provider-location-id"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".identifier"),
                    sliceName=label,
                    label=label,
                    code=FhirList(
                        [
                            Coding(
                                system=ProductFeatureCode.codeset,
                                code=ProductFeatureCodeValues.ProviderSearch,
                            )
                        ]
                    ),
                    short="Identifier used by the data source to uniquely identify a provider's association to a healthcare location",
                    # definition="",
                    # comment="",
                    min=0,
                    # alias=FhirList(
                    #     [
                    #     ]
                    # ),
                    # requirements="",
                    type_=FhirList([ElementDefinitionType(code="Identifier")]),
                )
            ]
        )

        return elements

    # OTHER
    @staticmethod
    def get_claim_number(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "claim-number"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".identifier"),
                    sliceName=label,
                    label=label,
                    short="An identifier to the insurance claim / EOB",
                    # definition="",
                    # comment="",
                    # requirements="",
                    type_=FhirList([ElementDefinitionType(code="Identifier")]),
                    patternIdentifier=Identifier(
                        id_="claim-id",
                        type_=CodeableConcept(
                            coding=FhirList(
                                [
                                    Coding(
                                        id_="claim-id-type",
                                        # system=IdentifierTypeCodesCode.codeset,
                                        code=IdentifierTypeCodesCode("claimnumber"),
                                    )
                                ]
                            )
                        ),
                        system="http://hl7.org/fhir/sid/us-mbi",
                    ),
                )
            ]
        )

        return elements

    @staticmethod
    def get_visit_number(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "visit-number"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".identifier"),
                    sliceName=label,
                    label=label,
                    short="Appointment identifier value with type as VN|http://terminology.hl7.org/CodeSystem/v2-0203",
                    patternIdentifier=Identifier(
                        type_=CodeableConcept(
                            coding=FhirList(
                                [
                                    Coding(
                                        system=IdentifierTypeCodesCode.codeset,
                                        code=IdentifierTypeCodesCodeValues.VisitNumber,
                                    )
                                ]
                            )
                        )
                    ),
                )
            ]
        )

        return elements

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
from spark_auto_mapper_fhir.value_sets.organization_type import (
    OrganizationTypeCode,
    OrganizationTypeCodeValues,
)
from spark_auto_mapper_fhir.value_sets.slicing_rules import SlicingRulesCodeValues


class DataElementOrganizationType:
    @staticmethod
    def get_organization_type_any(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "organization-type"
        element = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".type"),
                    label=label,
                    slicing=ElementDefinitionSlicing(
                        description="slice by type", rules=SlicingRulesCodeValues.Open
                    ),
                    short="Type of organization",
                    # definition="",
                    # comment="",
                    # requirements="",
                    min=1,
                    max="*",
                    type_=FhirList([ElementDefinitionType(code="CodeableConcept")]),
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".type.id"),
                    path=A.concat(resource, ".type.id"),
                    label=label,
                    short="set to type code",
                    # definition="",
                    requirements="Needs Review",
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="string")]),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".type.coding"),
                    path=A.concat(resource, ".type.coding"),
                    label=label,
                    # short="",
                    # definition="",
                    min=1,
                    max="*",
                    type_=FhirList([ElementDefinitionType(code="Coding")]),
                ),
            ],
            True,
        )
        return element

    @staticmethod
    def get_healthcare_type(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "healthcare-type"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".type"),
                    sliceName=label,
                    label=label,
                    short="prov | pharm | other",
                    definition="A healthcare organization such as practices, pharmacies, etc.",
                    requirements="prov for healthcare practices \n \n pharm for pharmacies \n \n other + prov for parent organizations",
                    min=0,
                    max="*",
                    type_=FhirList([ElementDefinitionType(code="CodeableConcept")]),
                    patternCodeableConcept=CodeableConcept(
                        coding=FhirList(
                            [
                                Coding(
                                    system=OrganizationTypeCode.codeset,
                                )
                            ]
                        )
                    ),
                )
            ]
        )

        return elements

    @staticmethod
    def get_insurance_type(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "insurance-type"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".type"),
                    sliceName=label,
                    label=label,
                    short="fixed: ins",
                    definition="An insurance organization",
                    min=1,
                    type_=FhirList([ElementDefinitionType(code="CodeableConcept")]),
                    patternCodeableConcept=CodeableConcept(
                        coding=FhirList(
                            [
                                Coding(
                                    system=OrganizationTypeCode.codeset,
                                    code=OrganizationTypeCodeValues.InsuranceCompany,
                                )
                            ]
                        )
                    ),
                )
            ]
        )

        return elements

    @staticmethod
    def get_network_type(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "network-type"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".type"),
                    sliceName=label,
                    label=label,
                    # short="",
                    definition="defines the type of the resource, by default this should be network for the network resource",
                    min=1,
                    max="1",
                    patternCodeableConcept=CodeableConcept(
                        coding=FhirList(
                            [
                                Coding(
                                    system="http://hl7.org/fhir/us/davinci-pdex-plan-net/CodeSystem/OrgTypeCS",
                                    code=GenericTypeCode("ntwk"),
                                )
                            ]
                        )
                    ),
                    mustSupport=A.boolean(True),
                )
            ]
        )

        return elements

from typing import Dict, Any, List

from spark_auto_mapper_fhir.backbone_elements.element_definition_example import (
    ElementDefinitionExample,
)
from spark_auto_mapper_fhir.complex_types.codeable_concept import CodeableConcept
from spark_auto_mapper_fhir.complex_types.coding import Coding
from spark_auto_mapper_fhir.value_sets.coverage_class_codes import (
    CoverageClassCodesCode,
    CoverageClassCodesCodeValues,
)

from library.fhir_profiles.schema.v1.file_type_category_codes import (
    FileTypeCategoryCode,
    FileTypeCategoryCodeValues,
)
from library.fhir_profiles.structure_definition_mappings.insurance.v1.insurance_company_mapping import (
    ProfileInsuranceCompany,
)
from library.fhir_profiles.structure_definition_mappings.eligibility.v1.partner_organization_mapping import (
    ProfilePartnerOrganization,
)
from library.fhir_profiles.structure_definition_mappings.eligibility.v1.patient_mapping import (
    ProfilePatient,
)
from spark_auto_mapper.automappers.automapper import AutoMapper
from spark_auto_mapper.data_types.text_like_base import AutoMapperTextLikeBase
from spark_auto_mapper.helpers.automapper_helpers import AutoMapperHelpers as A
from spark_auto_mapper_fhir.backbone_elements.element_definition import (
    ElementDefinition,
)
from spark_auto_mapper_fhir.backbone_elements.element_definition_binding import (
    ElementDefinitionBinding,
)
from spark_auto_mapper_fhir.backbone_elements.element_definition_type import (
    ElementDefinitionType,
)
from spark_auto_mapper_fhir.fhir_types.id import FhirId
from spark_auto_mapper_fhir.fhir_types.list import FhirList
from spark_auto_mapper_fhir.value_sets.binding_strength import BindingStrengthCodeValues

from library.fhir_profiles.data_elements.v1.identifier_element import (
    DataElementIdentifier,
)
from library.fhir_profiles.data_elements.v1.meta_element import (
    DataElementMeta,
)
from library.fhir_profiles.schema.v1.profile_definition_schema import (
    ProfileDefinition,
)


class ProfileInsuranceCoverage:
    @staticmethod
    def get_profile_id() -> AutoMapperTextLikeBase:
        return A.text("pr-insurance-coverage")

    @staticmethod
    def get_profile_url() -> AutoMapperTextLikeBase:
        return A.concat(
            ProfileDefinition.get_url_base(), ProfileInsuranceCoverage.get_profile_id()
        )


def mapping(parameters: Dict[str, Any]) -> List[AutoMapper]:
    resource = A.text("Coverage")

    mapper = AutoMapper(
        view=parameters["view_insurance_coverage"],
        source_view=parameters["view_profile_config"],
        use_schema=False,
    ).complex(
        ProfileDefinition(
            profile_id=FhirId(ProfileInsuranceCoverage.get_profile_id()),
            profile_name="Insurance Coverage",
            computer_friendly_profile_name="InsuranceCoverage",
            fhir_resource_type="Coverage",
            description="Insurance coverage for a beneficiary",
            keyword=FhirList(
                [
                    Coding(
                        system=FileTypeCategoryCode.codeset,
                        code=FileTypeCategoryCodeValues.ElibilityFile,
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
            # IDENTIFIER
            .concat(DataElementIdentifier.get_identifier_any(resource=resource))
            .concat(DataElementIdentifier.get_member_number(resource=resource))
            .concat(
                DataElementIdentifier.get_medicare_beneficiary_id(resource=resource)
            )
            .concat(
                FhirList(
                    [
                        # STATUS
                        ElementDefinition(
                            id_=A.concat(resource, ".status"),
                            path=A.concat(resource, ".status"),
                            short="Indicates validity of the resource",
                            comment="record should remain active, even after coverage termination",
                            min=1,
                            max="1",
                            mustSupport=A.boolean(True),
                        ),
                        # TYPE
                        # todo make element definition
                        ElementDefinition(
                            id_=A.concat(resource, ".type"),
                            path=A.concat(resource, ".type"),
                            short="Type of coverage represented",
                            type_=FhirList(
                                [ElementDefinitionType(code="CodeableConcept")]
                            ),
                            binding=ElementDefinitionBinding(
                                strength=BindingStrengthCodeValues.Extensible,
                                valueSet="https://www.hl7.org/fhir/us/bwell/bwell-vs-coverage-type",  # todo update
                            ),
                            mustSupport=A.boolean(True),
                        ),
                        # SUBSCRIBER
                        ElementDefinition(
                            id_=A.concat(resource, ".subscriber"),
                            path=A.concat(resource, ".subscriber"),
                            short="Subscriber of the insurance plan policy",
                            comment="this may be the same individual as the beneficiary",
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
                            mustSupport=A.boolean(True),
                        ),
                        # SUBSCRIBER ID
                        ElementDefinition(
                            id_=A.concat(resource, ".subscriberId"),
                            path=A.concat(resource, ".subscriberId"),
                            short="The subscribing individual's unique member number",
                            min=0,
                            max="1",
                            type_=FhirList([ElementDefinitionType(code="string")]),
                            mustSupport=A.boolean(True),
                        ),
                        # BENEFICIARY
                        ElementDefinition(
                            id_=A.concat(resource, ".beneficiary"),
                            path=A.concat(resource, ".beneficiary"),
                            short="Beneficiary of the insurance plan coverage",
                            min=1,
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
                            mustSupport=A.boolean(True),
                        ),
                        # DEPENDENT
                        ElementDefinition(
                            id_=A.concat(resource, ".dependent"),
                            path=A.concat(resource, ".dependent"),
                            short="Sequence number for the dependent",
                            min=0,
                            requirements="Only needed if the individual is a dependent; If the individual is the subscriber, this should be omitted",
                            mustSupport=A.boolean(True),
                        ),
                        # RELATIONSHIP
                        ElementDefinition(
                            id_=A.concat(resource, ".relationship"),
                            path=A.concat(resource, ".relationship"),
                            type_=FhirList(
                                [ElementDefinitionType(code="CodeableConcept")]
                            ),
                            binding=ElementDefinitionBinding(
                                strength=BindingStrengthCodeValues.Extensible,
                                valueSet="https://www.hl7.org/fhir/us/bwell/bwell-vs-relationship",  # todo update
                            ),
                            mustSupport=A.boolean(True),
                        ),
                        # PERIOD
                        ElementDefinition(
                            id_=A.concat(resource, ".period"),
                            path=A.concat(resource, ".period"),
                            short="Effective date range",
                            min=1,
                            type_=FhirList([ElementDefinitionType(code="Period")]),
                            mustSupport=A.boolean(True),
                        ),
                        # PAYOR
                        ElementDefinition(
                            id_=A.concat(resource, ".payor"),
                            path=A.concat(resource, ".payor"),
                            short="Paying entity",
                            comment="Typically the Insurance Company",
                            type_=FhirList(
                                [
                                    ElementDefinitionType(
                                        code="Reference",
                                        targetProfile=FhirList(
                                            [
                                                ProfileInsuranceCompany.get_profile_url(),
                                                ProfilePartnerOrganization.get_profile_url(),
                                            ]
                                        ),
                                    )
                                ]
                            ),
                            mustSupport=A.boolean(True),
                        ),
                        # CLASS
                        ElementDefinition(
                            id_=A.concat(resource, ".class"),
                            path=A.concat(resource, ".class"),
                            label="group",
                            short="Group and subgroup",
                            definition="The codes provided on the health card which identify or confirm the specific policy for the insurer.",
                            alias=FhirList(["group id"]),
                            min=0,
                            max="*",
                            mustSupport=A.boolean(True),
                        ),
                        ElementDefinition(
                            id_=A.concat(resource, ".class.type"),
                            path=A.concat(resource, ".class.type"),
                            short="Coded value to describe the class",
                            definition="The policy classifications, eg. Group, Plan, Class, etc.",
                            min=1,
                            type_=FhirList(
                                [ElementDefinitionType(code="CodeableConcept")]
                            ),
                            binding=ElementDefinitionBinding(
                                strength=BindingStrengthCodeValues.Extensible,
                                valueSet="https://www.hl7.org/fhir/us/bwell/bwell-vs-coverage-class-type",  # todo update
                            ),
                            example=FhirList(
                                [
                                    ElementDefinitionExample(
                                        label="Group type",
                                        valueCodeableConcept=CodeableConcept(
                                            coding=FhirList(
                                                [
                                                    Coding(
                                                        system=CoverageClassCodesCode.codeset,
                                                        code=CoverageClassCodesCodeValues.Group,
                                                    )
                                                ]
                                            )
                                        ),
                                    )
                                ]
                            ),
                            mustSupport=A.boolean(True),
                        ),
                        ElementDefinition(
                            id_=A.concat(resource, ".class.value"),
                            path=A.concat(resource, ".class.value"),
                            type_=FhirList([ElementDefinitionType(code="string")]),
                            mustSupport=A.boolean(True),
                        ),
                        ElementDefinition(
                            id_=A.concat(resource, ".class.name"),
                            path=A.concat(resource, ".class.name"),
                            type_=FhirList([ElementDefinitionType(code="string")]),
                            mustSupport=A.boolean(True),
                        ),
                    ]
                )
            ),
        )
    )

    return [mapper]

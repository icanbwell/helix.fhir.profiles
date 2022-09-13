from typing import Dict, Any, List

from spark_auto_mapper_fhir.complex_types.coding import Coding

from helix_fhir_profiles.backbone_elements.v1.backbone_element_eob_total import (
    DataBackboneElementEOBTotal,
)
from helix_fhir_profiles.backbone_elements.v1.backbone_element_supporting_info import (
    DataBackboneElementSupportingInfo,
)
from helix_fhir_profiles.schema.v1.file_type_category_codes import (
    FileTypeCategoryCode,
    FileTypeCategoryCodeValues,
)
from helix_fhir_profiles.structure_definition_mappings.provider_roster.v1.healthcare_organization_mapping import (
    ProfileHealthcareOrganization,
)
from helix_fhir_profiles.structure_definition_mappings.insurance.v1.insurance_company_mapping import (
    ProfileInsuranceCompany,
)
from helix_fhir_profiles.structure_definition_mappings.eligibility.v1.patient_mapping import (
    ProfilePatient,
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
from spark_auto_mapper_fhir.value_sets.generic_type import GenericTypeCode

from helix_fhir_profiles.backbone_elements.v1.backbone_element_adjudication import (
    DataBackboneElementAdjudication,
)
from helix_fhir_profiles.backbone_elements.v1.backbone_element_care_team import (
    DataBackboneElementCareTeam,
)
from helix_fhir_profiles.backbone_elements.v1.backbone_element_diagnosis import (
    DataBackboneElementDiagnosis,
)
from helix_fhir_profiles.backbone_elements.v1.backbone_element_eob_item import (
    DataBackboneElementEOBItem,
)
from helix_fhir_profiles.backbone_elements.v1.backbone_element_insurance import (
    DataBackboneElementInsurance,
)
from helix_fhir_profiles.backbone_elements.v1.backbone_element_procedure import (
    DataBackboneElementProcedure,
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


class ProfileExplanatonOfBenefitMedical:
    @staticmethod
    def get_profile_id() -> AutoMapperTextLikeBase:
        return A.text("pr-explanation-of-benefit-medical")

    @staticmethod
    def get_profile_url() -> AutoMapperTextLikeBase:
        return A.concat(
            ProfileDefinition.get_url_base(),
            ProfileExplanatonOfBenefitMedical.get_profile_id(),
        )


def mapping(parameters: Dict[str, Any]) -> List[AutoMapper]:
    resource = A.text("ExplanationOfBenefit")

    mapper = AutoMapper(
        view=parameters["view_explanaton_of_benefit_medical"],
        source_view=parameters["view_profile_config"],
        use_schema=False,
    ).complex(
        ProfileDefinition(
            profile_id=FhirId(ProfileExplanatonOfBenefitMedical.get_profile_id()),
            profile_name="Explanaton Of Benefit - Medical",
            computer_friendly_profile_name="ExplanatonOfBenefitMedical",
            fhir_resource_type="ExplanationOfBenefit",
            description="Explanation of benefit resource for medical claims data",
            keyword=FhirList(
                [
                    Coding(
                        system=FileTypeCategoryCode.codeset,
                        code=FileTypeCategoryCodeValues.MedicalClaimsFile,
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
            # IDENTIFIERs
            .concat(DataElementIdentifier.get_identifier_any(resource=resource))
            .concat(DataElementIdentifier.get_claim_number(resource=resource))
            .concat(
                FhirList(
                    [
                        # STATUS
                        ElementDefinition(
                            id_=A.concat(resource, ".status"),
                            path=A.concat(resource, ".status"),
                            short="Claim status",
                            comment="default to active",
                            min=1,
                            mustSupport=A.boolean(True),
                        ),
                        # TYPE
                        ElementDefinition(
                            id_=A.concat(resource, ".type"),
                            path=A.concat(resource, ".type"),
                            short="Claim type",
                            min=1,
                            mustSupport=A.boolean(True),
                        ),
                        # USE
                        ElementDefinition(
                            id_=A.concat(resource, ".use"),
                            path=A.concat(resource, ".use"),
                            short="Fixed: 'claim'",
                            min=1,
                            max="1",
                            fixedCode=GenericTypeCode("claim"),
                            mustSupport=A.boolean(True),
                        ),
                        # PATIENT
                        ElementDefinition(
                            id_=A.concat(resource, ".patient"),
                            path=A.concat(resource, ".patient"),
                            short="Claim status",
                            comment="default to active",
                            min=1,
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
                        ElementDefinition(
                            id_=A.concat(resource, ".billablePeriod"),
                            path=A.concat(resource, ".billablePeriod"),
                            label="billable-period",
                            short="Billable period",
                            comment="Sometimes only provided as dates of service",
                            min=1,
                            type_=FhirList([ElementDefinitionType(code="Period")]),
                            mustSupport=A.boolean(True),
                        ),
                        # CREATED
                        ElementDefinition(
                            id_=A.concat(resource, ".created"),
                            path=A.concat(resource, ".created"),
                            short="when the claim record was created",
                            comment="set to the ending date of service if not otherwise specified",
                            min=1,
                            mustSupport=A.boolean(True),
                        ),
                        # INSURER
                        ElementDefinition(
                            id_=A.concat(resource, ".insurer"),
                            path=A.concat(resource, ".insurer"),
                            short="Insurance company covering benefits",
                            min=1,
                            type_=FhirList(
                                [
                                    ElementDefinitionType(
                                        code="Reference",
                                        targetProfile=FhirList(
                                            [ProfileInsuranceCompany.get_profile_url()]
                                        ),
                                    )
                                ]
                            ),
                            mustSupport=A.boolean(True),
                        ),
                        # PROVIDER
                        ElementDefinition(
                            id_=A.concat(resource, ".provider"),
                            path=A.concat(resource, ".provider"),
                            label="billing-provider",
                            short="Billing organization",
                            min=1,
                            max="1",
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
                        # OUTCOME
                        ElementDefinition(
                            id_=A.concat(resource, ".outcome"),
                            path=A.concat(resource, ".outcome"),
                            short="complete | partial",
                            comment="if not provided, presumed complete",
                            min=1,
                            max="1",
                            mustSupport=A.boolean(True),
                        ),
                    ]
                    # CARE TEAM
                )
                .concat(
                    DataBackboneElementCareTeam.get_care_team_any(resource=resource)
                )
                .concat(
                    DataBackboneElementCareTeam.get_care_team_attending(
                        resource=resource
                    )
                )
                .concat(
                    DataBackboneElementCareTeam.get_care_team_operating(
                        resource=resource
                    )
                )
                .concat(
                    DataBackboneElementCareTeam.get_care_team_rendering(
                        resource=resource
                    )
                )
                .concat(
                    # SUPPORTING INFO
                    DataBackboneElementSupportingInfo.get_supporting_info_any(
                        resource=resource
                    ),
                )
                .concat(
                    # type of bill
                    DataBackboneElementSupportingInfo.get_type_of_bill(
                        resource=resource
                    ),
                )
                .concat(
                    # discharge status
                    DataBackboneElementSupportingInfo.get_discharge_status(
                        resource=resource
                    ),
                )
                .concat(
                    # admission source
                    DataBackboneElementSupportingInfo.get_admission_source(
                        resource=resource
                    ),
                )
                .concat(
                    # admission type
                    DataBackboneElementSupportingInfo.get_admission_type(
                        resource=resource
                    ),
                )
                .concat(
                    # type of facility
                    DataBackboneElementSupportingInfo.get_type_of_facility(
                        resource=resource
                    ),
                )
                .concat(
                    # bill classification
                    DataBackboneElementSupportingInfo.get_bill_classification(
                        resource=resource
                    ),
                )
                .concat(
                    # frequency
                    DataBackboneElementSupportingInfo.get_frequency(resource=resource),
                )
                .concat(
                    # place of service
                    DataBackboneElementSupportingInfo.get_place_of_service(
                        resource=resource
                    ),
                )
                .concat(
                    # claim received date
                    DataBackboneElementSupportingInfo.get_received_date(
                        resource=resource
                    ),
                )
            )
            .concat(
                # DIAGNOSIS
                DataBackboneElementDiagnosis.get_diagnosis_any(resource=resource)
            )
            .concat(
                # PROCEDURE
                DataBackboneElementProcedure.get_procedure_any(resource=resource)
            )
            .concat(
                # INSURANCE
                DataBackboneElementInsurance.get_insurance_any(resource=resource)
                # ITEM
            )
            .concat(
                DataBackboneElementEOBItem.get_eob_item_any(resource=resource)
                # ADJUDICATION
            )
            .concat(
                DataBackboneElementAdjudication.get_adjudication_any(resource=resource)
            )
            .concat(
                DataBackboneElementAdjudication.get_submitted_amount(resource=resource)
            )
            .concat(
                DataBackboneElementAdjudication.get_allowed_amount(resource=resource)
            )
            .concat(DataBackboneElementAdjudication.get_copay_amount(resource=resource))
            .concat(
                # TOTAL
                DataBackboneElementEOBTotal.get_eob_total_any(resource=resource)
            )
            # PAYMENT
            .concat(
                DataBackboneElementAdjudication.get_payment_amount(resource=resource)
                # BENEFIT PERIOD
            ).concat(
                FhirList(
                    [
                        ElementDefinition(
                            id_=A.concat(resource, ".benefitPeriod"),
                            path=A.concat(resource, ".benefitPeriod"),
                            mustSupport=A.boolean(True),
                        )
                    ]
                )
            ),
        )
    )

    return [mapper]

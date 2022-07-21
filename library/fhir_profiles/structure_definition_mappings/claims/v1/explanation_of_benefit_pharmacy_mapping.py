from typing import Dict, Any, List

from spark_auto_mapper_fhir.complex_types.coding import Coding
from spark_auto_mapper_fhir.value_sets.generic_type import GenericTypeCode

from library.fhir_profiles.backbone_elements.v1.backbone_element_care_team import (
    DataBackboneElementCareTeam,
)
from library.fhir_profiles.backbone_elements.v1.backbone_element_eob_insurance import (
    DataBackboneElementEOBInsurance,
)
from library.fhir_profiles.backbone_elements.v1.backbone_element_eob_item import (
    DataBackboneElementEOBItem,
)
from library.fhir_profiles.backbone_elements.v1.backbone_element_eob_total import (
    DataBackboneElementEOBTotal,
)
from library.fhir_profiles.backbone_elements.v1.backbone_element_supporting_info import (
    DataBackboneElementSupportingInfo,
)
from library.fhir_profiles.schema.v1.file_type_category_codes import (
    FileTypeCategoryCode,
    FileTypeCategoryCodeValues,
)
from library.fhir_profiles.structure_definition_mappings.provider_roster.v1.healthcare_organization_mapping import (
    ProfileHealthcareOrganization,
)
from library.fhir_profiles.structure_definition_mappings.insurance.v1.insurance_company_mapping import (
    ProfileInsuranceCompany,
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
from library.fhir_profiles.schema.v1.profile_definition_schema import (
    ProfileDefinition,
)

profile_name = "Explanation Of Benefit - Pharmacy"


class ProfileExplanationOfBenefitPharmacy:
    @staticmethod
    def get_profile_id() -> AutoMapperTextLikeBase:
        return A.text("pr-explanation-of-benefit-pharmacy")

    @staticmethod
    def get_profile_url() -> AutoMapperTextLikeBase:
        return A.concat(
            ProfileDefinition.get_url_base(),
            ProfileExplanationOfBenefitPharmacy.get_profile_id(),
        )


def mapping(parameters: Dict[str, Any]) -> List[AutoMapper]:
    resource = A.text("ExplanationOfBenefit")

    mapper = AutoMapper(
        view=parameters["view_explanation_of_benefit_pharmacy"],
        source_view=parameters["view_profile_config"],
        use_schema=False,
    ).complex(
        ProfileDefinition(
            profile_id=FhirId(ProfileExplanationOfBenefitPharmacy.get_profile_id()),
            profile_name="Explanation Of Benefit - Pharmacy",
            computer_friendly_profile_name="ExplanationOfBenefitPharmacy",
            fhir_resource_type="ExplanationOfBenefit",
            description="EOB for Rx claims",
            keyword=FhirList(
                [
                    Coding(
                        system=FileTypeCategoryCode.codeset,
                        code=FileTypeCategoryCodeValues.RxClaimsFile,
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
                        # CREATED
                        ElementDefinition(
                            id_=A.concat(resource, ".created"),
                            path=A.concat(resource, ".created"),
                            short="Fill date",
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
                            label="pharmacy",
                            short="Dispensing pharmacy",
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
                            min=1,
                            max="1",
                            mustSupport=A.boolean(True),
                        ),
                    ]
                )
                # CARE TEAMs
                .concat(
                    DataBackboneElementCareTeam.get_care_team_any(resource=resource)
                )
                .concat(
                    DataBackboneElementCareTeam.get_care_team_prescriber(
                        resource=resource
                    )
                )
                .concat(
                    DataBackboneElementCareTeam.get_care_team_pharmacy(
                        resource=resource
                    )
                )
                # SUPPORTING INFO
                .concat(
                    DataBackboneElementSupportingInfo.get_supporting_info_any(
                        resource=resource
                    ),
                )
                .concat(
                    DataBackboneElementSupportingInfo.get_days_supply(
                        resource=resource
                    ),
                )
                .concat(
                    DataBackboneElementSupportingInfo.get_dispense_as_written(
                        resource=resource
                    ),
                )
                .concat(
                    DataBackboneElementSupportingInfo.get_generic_brand(
                        resource=resource
                    ),
                )
                .concat(
                    DataBackboneElementSupportingInfo.get_prescribed_date(
                        resource=resource
                    ),
                )
                .concat(
                    DataBackboneElementEOBInsurance.get_eob_insurance_any(
                        resource=resource
                    )
                )
                .concat(
                    # ITEM
                    DataBackboneElementEOBItem.get_eob_item_any(resource=resource)
                )
                .concat(DataBackboneElementEOBItem.get_eob_drug_ndc(resource=resource))
                .concat(
                    # TOTAL
                    DataBackboneElementEOBTotal.get_eob_total_any(resource=resource)
                )
            ),
        )
    )

    return [mapper]

from typing import Dict, Any, List

from spark_auto_mapper_fhir.backbone_elements.element_definition_example import (
    ElementDefinitionExample,
)
from spark_auto_mapper_fhir.complex_types.codeable_concept import CodeableConcept
from spark_auto_mapper_fhir.value_sets.insurance_plan_type import InsurancePlanTypeCode

from library.fhir_profiles.structure_definition_mappings.insurance.v1.healthcare_network_mapping import (
    ProfileHealthcareNetwork,
)

from library.fhir_profiles.structure_definition_mappings.insurance.v1.location_area_mapping import (
    ProfileLocationArea,
)
from library.fhir_profiles.structure_definition_mappings.provider_roster.v1.healthcare_organization_mapping import (
    ProfileHealthcareOrganization,
)
from spark_auto_mapper_fhir.backbone_elements.element_definition_type import (
    ElementDefinitionType,
)

from library.fhir_profiles.data_elements.v1.identifier_element import (
    DataElementIdentifier,
)
from spark_auto_mapper.automappers.automapper import AutoMapper
from spark_auto_mapper.data_types.text_like_base import AutoMapperTextLikeBase
from spark_auto_mapper.helpers.automapper_helpers import AutoMapperHelpers as A
from spark_auto_mapper_fhir.backbone_elements.element_definition import (
    ElementDefinition,
)
from spark_auto_mapper_fhir.complex_types.coding import Coding
from spark_auto_mapper_fhir.fhir_types.id import FhirId
from spark_auto_mapper_fhir.fhir_types.list import FhirList

from library.fhir_profiles.data_elements.v1.meta_element import (
    DataElementMeta,
)
from library.fhir_profiles.schema.v1.file_type_category_codes import (
    FileTypeCategoryCode,
    FileTypeCategoryCodeValues,
)
from library.fhir_profiles.schema.v1.profile_definition_schema import (
    ProfileDefinition,
)


class ProfileInsurancePlan:
    @staticmethod
    def get_profile_id() -> AutoMapperTextLikeBase:
        return A.text("pr-insurance-plan")

    @staticmethod
    def get_profile_url() -> AutoMapperTextLikeBase:
        return A.concat(
            ProfileDefinition.get_url_base(), ProfileInsurancePlan.get_profile_id()
        )


def mapping(parameters: Dict[str, Any]) -> List[AutoMapper]:
    resource = A.text("InsurancePlan")

    mapper = AutoMapper(
        view=parameters["view_insurance_plan"],
        source_view=parameters["view_profile_config"],
        use_schema=False,
    ).complex(
        ProfileDefinition(
            profile_id=FhirId(ProfileInsurancePlan.get_profile_id()),
            profile_name="Insurance Plan",
            computer_friendly_profile_name="InsurancePlan",
            fhir_resource_type="InsurancePlan",
            description="Insurance Plan resource",
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
                        id_=A.concat(resource, ".id"),
                        path=A.concat(resource, ".id"),
                    ),
                ],
                True,
            )
            # META
            .concat(DataElementMeta.get_meta(resource=resource))
            # IDENTIFIERS
            .concat(DataElementIdentifier.get_identifier_any(resource=resource))
            # insurance plan id
            # healthcare org
            # STATUS
            .concat(
                FhirList(
                    [
                        ElementDefinition(
                            id_=A.concat(resource, ".status"),
                            path=A.concat(resource, ".status"),
                            label="plan-status",
                            min=1,
                            max="1",
                            type_=FhirList([ElementDefinitionType(code="code")]),
                            mustSupport=A.boolean(True),
                        ),
                        # TYPE
                        ElementDefinition(
                            id_=A.concat(resource, ".type"),
                            path=A.concat(resource, ".type"),
                            label="plan-type",
                            short="insurance plan type",
                            min=1,
                            max="*",
                            type_=FhirList(
                                [ElementDefinitionType(code="CodeableConcept")]
                            ),
                            patternCodeableConcept=CodeableConcept(
                                coding=FhirList(
                                    [
                                        Coding(
                                            system=InsurancePlanTypeCode.codeset,
                                            # code=InsurancePlanTypeCodeValues.Medical
                                        )
                                    ]
                                )
                            ),
                            example=FhirList(
                                [
                                    ElementDefinitionExample(
                                        label="Medical plan type",
                                        valueCodeableConcept=CodeableConcept(
                                            coding=FhirList(
                                                [
                                                    Coding(
                                                        system=InsurancePlanTypeCode.codeset,
                                                        # code=InsurancePlanTypeCodeValues.Medical
                                                    )
                                                ]
                                            )
                                        ),
                                    )
                                ]
                            ),
                            mustSupport=A.boolean(True),
                        ),
                        # NAME
                        ElementDefinition(
                            id_=A.concat(resource, ".name"),
                            path=A.concat(resource, ".name"),
                            label="plan-name",
                            min=1,
                            max="1",
                            type_=FhirList([ElementDefinitionType(code="string")]),
                            example=FhirList(
                                [
                                    ElementDefinitionExample(
                                        label="insurance plan name",
                                        valueString="Unity Point Direct Contracting Plan",
                                    )
                                ]
                            ),
                            mustSupport=A.boolean(True),
                        ),
                        # OWNED BY
                        ElementDefinition(
                            id_=A.concat(resource, ".ownedBy"),
                            path=A.concat(resource, ".ownedBy"),
                            label="plan-owner",
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
                        ),
                        # ADMINISTERED BY
                        ElementDefinition(
                            id_=A.concat(resource, ".administeredBy"),
                            path=A.concat(resource, ".administeredBy"),
                            label="plan-administrater",
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
                        ),
                        # COVERAGE AREA
                        ElementDefinition(
                            id_=A.concat(resource, ".coverageArea"),
                            path=A.concat(resource, ".coverageArea"),
                            label="coverage-area",
                            alias=FhirList(["zip code", "state"]),
                            min=1,
                            max="*",
                            type_=FhirList(
                                [
                                    ElementDefinitionType(
                                        code="Reference",
                                        targetProfile=FhirList(
                                            [ProfileLocationArea.get_profile_url()]
                                        ),
                                    )
                                ]
                            ),
                        ),
                        # NETWORK
                        ElementDefinition(
                            id_=A.concat(resource, ".network"),
                            path=A.concat(resource, ".network"),
                            label="plan-network",
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
                    ]
                )
            ),
        )
    )

    return [mapper]

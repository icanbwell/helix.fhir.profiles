from typing import Dict, Any, List

from spark_auto_mapper.automappers.automapper import AutoMapper
from spark_auto_mapper.data_types.text_like_base import AutoMapperTextLikeBase
from spark_auto_mapper.helpers.automapper_helpers import AutoMapperHelpers as A
from spark_auto_mapper_fhir.backbone_elements.element_definition import (
    ElementDefinition,
)
from spark_auto_mapper_fhir.fhir_types.id import FhirId
from spark_auto_mapper_fhir.fhir_types.list import FhirList

from library.fhir_profiles.data_elements.v1.meta_element import (
    DataElementMeta,
)
from library.fhir_profiles.schema.v1.profile_definition_schema import (
    ProfileDefinition,
)

from library.fhir_profiles.structure_definition_mappings.eligibility.v1.patient_mapping import (
    ProfilePatient,
)
from spark_auto_mapper_fhir.backbone_elements.element_definition_type import (
    ElementDefinitionType,
)
from library.fhir_profiles.structure_definition_mappings.provider_roster.v1.healthcare_organization_mapping import (
    ProfileHealthcareOrganization,
)
from library.fhir_profiles.structure_definition_mappings.insurance.v1.insurance_company_mapping import (
    ProfileInsuranceCompany,
)
from library.fhir_profiles.structure_definition_mappings.eligibility.v1.partner_organization_mapping import (
    ProfilePartnerOrganization,
)


class ProfileContract:
    @staticmethod
    def get_profile_id() -> AutoMapperTextLikeBase:
        return A.text("pr-contract")

    @staticmethod
    def get_profile_url() -> AutoMapperTextLikeBase:
        return A.concat(
            ProfileDefinition.get_url_base(), ProfileContract.get_profile_id()
        )


def mapping(parameters: Dict[str, Any]) -> List[AutoMapper]:
    resource = A.text("Contract")

    mapper = AutoMapper(
        view=parameters["view_contract"],
        source_view=parameters["view_profile_config"],
        use_schema=False,
    ).complex(
        ProfileDefinition(
            profile_id=FhirId(ProfileContract.get_profile_id()),
            profile_name="Contract",
            computer_friendly_profile_name="Contract",
            fhir_resource_type="Contract",
            description="Contract resource",
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
            .concat(DataElementMeta.get_meta(resource=resource)).concat(
                FhirList(
                    [
                        # SUBJECT
                        ElementDefinition(
                            id_=A.concat(resource, ".subject"),
                            path=A.concat(resource, ".subject"),
                            label="subject",
                            short="The patient who signed the contract",
                            min=0,
                            max="*",
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
                        # AUTHORITY
                        ElementDefinition(
                            id_=A.concat(resource, ".authority"),
                            path=A.concat(resource, ".authority"),
                            label="authority",
                            short="Contract is signed through which organization",
                            min=0,
                            max="*",
                            type_=FhirList(
                                [
                                    ElementDefinitionType(
                                        code="Reference",
                                        targetProfile=FhirList(
                                            [
                                                ProfileInsuranceCompany.get_profile_url(),
                                                ProfilePartnerOrganization.get_profile_url(),
                                                ProfileHealthcareOrganization.get_profile_url(),
                                            ]
                                        ),
                                    )
                                ]
                            ),
                        ),
                        # AUTHOR
                        ElementDefinition(
                            id_=A.concat(resource, ".author"),
                            path=A.concat(resource, ".author"),
                            label="author",
                            short="who owns the contract program.",
                            min=0,
                            max="1",
                            type_=FhirList(
                                [
                                    ElementDefinitionType(
                                        code="Reference",
                                        targetProfile=FhirList(
                                            [
                                                ProfilePatient.get_profile_url(),
                                                ProfileHealthcareOrganization.get_profile_url(),
                                                ProfilePartnerOrganization.get_profile_url(),
                                                ProfileInsuranceCompany.get_profile_url(),
                                            ]
                                        ),
                                    )
                                ]
                            ),
                            mustSupport=A.boolean(True),
                        ),
                        # LEGAL
                        ElementDefinition(
                            id_=A.concat(resource, ".legal"),
                            path=A.concat(resource, ".legal"),
                            mustSupport=A.boolean(True),
                        ),
                        ElementDefinition(
                            id_=A.concat(resource, ".legal.id"),
                            path=A.concat(resource, ".legal.id"),
                            short="tbd",
                            min=1,
                            mustSupport=A.boolean(True),
                        ),
                        ElementDefinition(
                            id_=A.concat(resource, ".legal.content[x]"),
                            path=A.concat(resource, ".legal.content[x]"),
                            short="stores the generated pdf contract",
                            min=1,
                            max="1",
                            mustSupport=A.boolean(True),
                        ),
                    ],
                    True,
                ),
            ),
        )
    )

    return [mapper]

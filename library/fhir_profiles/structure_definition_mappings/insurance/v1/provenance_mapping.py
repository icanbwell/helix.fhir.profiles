from typing import Dict, Any, List

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

from library.fhir_profiles.backbone_elements.v1.backbone_element_agent import (
    DataBackboneElementAgent,
)
from library.fhir_profiles.data_elements.v1.meta_element import (
    DataElementMeta,
)
from library.fhir_profiles.data_elements.v1.signature_element import (
    DataElementSignature,
)
from library.fhir_profiles.structure_definition_mappings.insurance.v1.enrollment_request_mapping import (
    ProfileEnrollmentRequest,
)
from library.fhir_profiles.schema.v1.profile_definition_schema import (
    ProfileDefinition,
)


class ProfileProvenance:
    @staticmethod
    def get_profile_id() -> AutoMapperTextLikeBase:
        return A.text("pr-provenance")

    @staticmethod
    def get_profile_url() -> AutoMapperTextLikeBase:
        return A.concat(
            ProfileDefinition.get_url_base(), ProfileProvenance.get_profile_id()
        )


def mapping(parameters: Dict[str, Any]) -> List[AutoMapper]:
    resource = A.text("Provenance")

    mapper = AutoMapper(
        view=parameters["view_provenance"],
        source_view=parameters["view_profile_config"],
        use_schema=False,
    ).complex(
        ProfileDefinition(
            profile_id=FhirId(ProfileProvenance.get_profile_id()),
            profile_name="Provenance",
            computer_friendly_profile_name="Provenance",
            fhir_resource_type="Provenance",
            description="Provenance",
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
            .concat(
                FhirList(
                    [
                        # TARGET
                        ElementDefinition(
                            id_=A.concat(resource, ".target"),
                            path=A.concat(resource, ".target"),
                            short="Link to EnrollmentRequest",
                            min=1,
                            max="1",
                            type_=FhirList(
                                [
                                    ElementDefinitionType(
                                        code="Reference",
                                        targetProfile=FhirList(
                                            [ProfileEnrollmentRequest.get_profile_url()]
                                        ),
                                    )
                                ]
                            ),
                            mustSupport=A.boolean(True),
                        ),
                        # RECORDED
                        ElementDefinition(
                            id_=A.concat(resource, ".recorded"),
                            path=A.concat(resource, ".recorded"),
                            mustSupport=A.boolean(True),
                        ),
                    ],
                    True,
                )
            )
            .concat(
                # AGENT
                DataBackboneElementAgent.get_agent_any(resource=resource)
            )
            # SIGNATURE
            .concat(DataElementSignature.get_signature_any(resource=resource)),
        )
    )

    return [mapper]

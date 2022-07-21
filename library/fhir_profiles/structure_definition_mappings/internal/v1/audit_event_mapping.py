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

from library.fhir_profiles.data_elements.v1.meta_element import (
    DataElementMeta,
)
from library.fhir_profiles.schema.v1.profile_definition_schema import (
    ProfileDefinition,
)


class ProfileAuditEvent:
    @staticmethod
    def get_profile_id() -> AutoMapperTextLikeBase:
        return A.text("pr-audit-event")

    @staticmethod
    def get_profile_url() -> AutoMapperTextLikeBase:
        return A.concat(
            ProfileDefinition.get_url_base(), ProfileAuditEvent.get_profile_id()
        )


def mapping(parameters: Dict[str, Any]) -> List[AutoMapper]:
    resource = A.text("AuditEvent")

    mapper = AutoMapper(
        view=parameters["view_audit_event"],
        source_view=parameters["view_profile_config"],
        use_schema=False,
    ).complex(
        ProfileDefinition(
            profile_id=FhirId(ProfileAuditEvent.get_profile_id()),
            profile_name="Audit Event",
            computer_friendly_profile_name="AuditEvent",
            fhir_resource_type="AuditEvent",
            description="Audit Event",
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
            .concat(DataElementMeta.get_meta(resource=resource)).concat(
                FhirList(
                    [
                        ElementDefinition(
                            id_=A.concat(resource, ".type"),
                            path=A.concat(resource, ".type"),
                            min=1,
                            max="1",
                            type_=FhirList([ElementDefinitionType(code="Coding")]),
                            mustSupport=A.boolean(True),
                        ),
                        ElementDefinition(
                            id_=A.concat(resource, ".agent"),
                            path=A.concat(resource, ".agent"),
                            min=1,
                            max="*",
                            type_=FhirList(
                                [ElementDefinitionType(code="BackboneElement")]
                            ),
                            mustSupport=A.boolean(True),
                        ),
                        ElementDefinition(
                            id_=A.concat(resource, ".agent.type"),
                            path=A.concat(resource, ".agent.type"),
                            min=0,
                            max="1",
                            type_=FhirList(
                                [ElementDefinitionType(code="CodeableConcept")]
                            ),
                            mustSupport=A.boolean(True),
                        ),
                    ],
                    True,
                ),
            ),
        )
    )

    return [mapper]

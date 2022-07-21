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
from library.fhir_profiles.data_elements.v1.service_type_element import (
    DataElementServiceType,
)
from library.fhir_profiles.schema.v1.profile_definition_schema import (
    ProfileDefinition,
)
from library.fhir_profiles.structure_definition_mappings.scheduling.v1.schedule_mapping import (
    ProfileSchedule,
)


class ProfileSlot:
    @staticmethod
    def get_profile_id() -> AutoMapperTextLikeBase:
        return A.text("pr-slot")

    @staticmethod
    def get_profile_url() -> AutoMapperTextLikeBase:
        return A.concat(ProfileDefinition.get_url_base(), ProfileSlot.get_profile_id())


def mapping(parameters: Dict[str, Any]) -> List[AutoMapper]:
    resource = A.text("Slot")

    mapper = AutoMapper(
        view=parameters["view_slot"],
        source_view=parameters["view_profile_config"],
        use_schema=False,
    ).complex(
        ProfileDefinition(
            profile_id=FhirId(ProfileSlot.get_profile_id()),
            profile_name="Slot",
            computer_friendly_profile_name="Slot",
            fhir_resource_type="Slot",
            description="Appointment slot resource",
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
            # SERVICE TYPES
            .concat(
                DataElementServiceType.get_service_type_any(resource=resource),
            )
            .concat(DataElementServiceType.get_medical_services(resource=resource))
            .concat(DataElementServiceType.get_appointment_type(resource=resource))
            .concat(
                FhirList(
                    [
                        # SCHEDULE
                        ElementDefinition(
                            id_=A.concat(resource, ".schedule"),
                            path=A.concat(resource, ".schedule"),
                            short="corresponding Schedule resource",
                            definition="The schedule resource that this slot defines",
                            min=1,
                            max="1",
                            type_=FhirList(
                                [
                                    ElementDefinitionType(
                                        code="Reference",
                                        targetProfile=FhirList(
                                            [ProfileSchedule.get_profile_url()]
                                        ),
                                    )
                                ]
                            ),
                            mustSupport=A.boolean(True),
                        ),
                        # STATUS
                        ElementDefinition(
                            id_=A.concat(resource, ".status"),
                            path=A.concat(resource, ".status"),
                            short="status for the appointment slot",
                            definition="default to free",
                            min=1,
                            max="1",
                            type_=FhirList([ElementDefinitionType(code="code")]),
                            mustSupport=A.boolean(True),
                        ),
                        # START
                        ElementDefinition(
                            id_=A.concat(resource, ".start"),
                            path=A.concat(resource, ".start"),
                            short="appointment slot start time",
                            # definition="",
                            min=1,
                            max="1",
                            type_=FhirList([ElementDefinitionType(code="instant")]),
                            mustSupport=A.boolean(True),
                        ),
                        # END
                        ElementDefinition(
                            id_=A.concat(resource, ".end"),
                            path=A.concat(resource, ".end"),
                            short="appointment slot end time",
                            min=0,
                            max="1",
                            type_=FhirList([ElementDefinitionType(code="instant")]),
                            mustSupport=A.boolean(True),
                        ),
                    ]
                )
            ),
        )
    )

    return [mapper]

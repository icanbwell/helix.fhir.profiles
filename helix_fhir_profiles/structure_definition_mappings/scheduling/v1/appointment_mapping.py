from typing import Dict, Any, List

from helix_fhir_profiles.schema.v1.product_feature_codes import (
    ProductFeatureCode,
    ProductFeatureCodeValues,
)
from spark_auto_mapper.automappers.automapper import AutoMapper
from spark_auto_mapper.data_types.text_like_base import AutoMapperTextLikeBase
from spark_auto_mapper.helpers.automapper_helpers import AutoMapperHelpers as A
from spark_auto_mapper_fhir.backbone_elements.element_definition import (
    ElementDefinition,
)
from spark_auto_mapper_fhir.fhir_types.id import FhirId
from spark_auto_mapper_fhir.fhir_types.list import FhirList
from spark_auto_mapper_fhir.value_sets.generic_type import GenericTypeCode

from helix_fhir_profiles.backbone_elements.v1.backbone_element_participant import (
    DataBackboneElementParticipant,
)
from helix_fhir_profiles.data_elements.v1.meta_element import (
    DataElementMeta,
)
from helix_fhir_profiles.schema.v1.profile_definition_schema import (
    ProfileDefinition,
)
from spark_auto_mapper_fhir.backbone_elements.element_definition_example import (
    ElementDefinitionExample,
)
from spark_auto_mapper_fhir.complex_types.codeable_concept import CodeableConcept
from spark_auto_mapper_fhir.complex_types.coding import Coding
from spark_auto_mapper_fhir.value_sets.service_type import ServiceTypeCode

from helix_fhir_profiles.data_elements.v1.identifier_element import (
    DataElementIdentifier,
)
from spark_auto_mapper_fhir.backbone_elements.element_definition_type import (
    ElementDefinitionType,
)
from helix_fhir_profiles.structure_definition_mappings.scheduling.v1.slot_mapping import (
    ProfileSlot,
)


class ProfileAppointment:
    @staticmethod
    def get_profile_id() -> AutoMapperTextLikeBase:
        return A.text("pr-appointment")

    @staticmethod
    def get_profile_url() -> AutoMapperTextLikeBase:
        return A.concat(
            ProfileDefinition.get_url_base(), ProfileAppointment.get_profile_id()
        )


def mapping(parameters: Dict[str, Any]) -> List[AutoMapper]:
    resource = A.text("Appointment")

    mapper = AutoMapper(
        view=parameters["view_appointment"],
        source_view=parameters["view_profile_config"],
        use_schema=False,
    ).complex(
        ProfileDefinition(
            profile_id=FhirId(ProfileAppointment.get_profile_id()),
            profile_name="Appointment",
            computer_friendly_profile_name="Appointment",
            fhir_resource_type="Appointment",
            # description="",
            # keyword=FhirList(
            #     [
            #         Coding(
            #             system=FileTypeCategoryCode.codeset,
            #             code=FileTypeCategoryCodeValues.,
            #         )
            #     ]
            # ),
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
            # IDENTIFIERS
            .concat(DataElementIdentifier.get_identifier_any(resource=resource))
            .concat(DataElementIdentifier.get_visit_number(resource=resource))
            .concat(
                FhirList(
                    [
                        ElementDefinition(
                            id_=A.concat(resource, ".status"),
                            path=A.concat(resource, ".status"),
                            label="appointment-status",
                            code=FhirList(
                                [
                                    Coding(
                                        system=ProductFeatureCode.codeset,
                                        code=ProductFeatureCodeValues.IntegratedScheduling,
                                    )
                                ]
                            ),
                            short="Appointment status code",
                            min=1,
                            max="1",
                            type_=FhirList([ElementDefinitionType(code="code")]),
                            mustSupport=A.boolean(True),
                        ),
                        ElementDefinition(  # todo element def
                            id_=A.concat(resource, ".serviceType"),
                            path=A.concat(resource, ".serviceType"),
                            label="service-type",
                            code=FhirList(
                                [
                                    Coding(
                                        system=ProductFeatureCode.codeset,
                                        code=ProductFeatureCodeValues.IntegratedScheduling,
                                    )
                                ]
                            ),
                            short="Appointment service type",
                            comment="some resources in the fhir server (that don't have a source value) have a custom serviceType code w/ system incorrectly set to http://terminology.hl7.org/CodeSystem/service-type",
                            type_=FhirList(
                                [ElementDefinitionType(code="CodeableConcept")]
                            ),
                            example=FhirList(
                                [
                                    ElementDefinitionExample(
                                        label="service type with incorrect system",
                                        valueCodeableConcept=CodeableConcept(
                                            coding=FhirList(
                                                [
                                                    Coding(
                                                        system=ServiceTypeCode.codeset,
                                                        code=GenericTypeCode("p3ooKp"),
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
                            id_=A.concat(resource, ".start"),
                            path=A.concat(resource, ".start"),
                            label="start-time",
                            code=FhirList(
                                [
                                    Coding(
                                        system=ProductFeatureCode.codeset,
                                        code=ProductFeatureCodeValues.IntegratedScheduling,
                                    )
                                ]
                            ),
                            short="appointment start time; likely the same value as the corresponding Slot.start",
                            min=1,
                            max="1",
                            type_=FhirList([ElementDefinitionType(code="instant")]),
                            mustSupport=A.boolean(True),
                        ),
                        ElementDefinition(
                            id_=A.concat(resource, ".slot"),
                            path=A.concat(resource, ".slot"),
                            label="appointment-slot",
                            code=FhirList(
                                [
                                    Coding(
                                        system=ProductFeatureCode.codeset,
                                        code=ProductFeatureCodeValues.IntegratedScheduling,
                                    )
                                ]
                            ),
                            short="corresponding Slot resource for the appointment",
                            # min=,
                            # max="1",
                            type_=FhirList(
                                [
                                    ElementDefinitionType(
                                        code="Reference",
                                        targetProfile=FhirList(
                                            [ProfileSlot.get_profile_url()]
                                        ),
                                    )
                                ]
                            ),
                            mustSupport=A.boolean(True),
                        ),
                        ElementDefinition(
                            id_=A.concat(resource, ".created"),
                            path=A.concat(resource, ".created"),
                            label="appointment-created-date",
                            code=FhirList(
                                [
                                    Coding(
                                        system=ProductFeatureCode.codeset,
                                        code=ProductFeatureCodeValues.IntegratedScheduling,
                                    )
                                ]
                            ),
                            short="when the appointment resource was created",
                            type_=FhirList([ElementDefinitionType(code="dateTime")]),
                            mustSupport=A.boolean(True),
                        ),
                    ]
                )
                # PARTICIPANTs
                .concat(
                    DataBackboneElementParticipant.get_participant_any(
                        resource=resource
                    )
                )
                .concat(DataBackboneElementParticipant.get_patient(resource=resource))
                .concat(DataBackboneElementParticipant.get_booker(resource=resource))
                .concat(DataBackboneElementParticipant.get_location(resource=resource))
            ),
        )
    )

    return [mapper]

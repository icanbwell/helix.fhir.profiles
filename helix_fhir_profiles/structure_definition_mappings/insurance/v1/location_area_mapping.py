from typing import Dict, Any, List

from spark_auto_mapper.automappers.automapper import AutoMapper
from spark_auto_mapper.data_types.text_like_base import AutoMapperTextLikeBase
from spark_auto_mapper.helpers.automapper_helpers import AutoMapperHelpers as A
from spark_auto_mapper_fhir.backbone_elements.element_definition import (
    ElementDefinition,
)
from spark_auto_mapper_fhir.complex_types.codeable_concept import CodeableConcept
from spark_auto_mapper_fhir.complex_types.coding import Coding
from spark_auto_mapper_fhir.fhir_types.id import FhirId
from spark_auto_mapper_fhir.fhir_types.list import FhirList
from spark_auto_mapper_fhir.value_sets.location_type import (
    LocationTypeCode,
    LocationTypeCodeValues,
)


from helix_fhir_profiles.data_elements.v1.address_element import (
    DataElementAddress,
)
from helix_fhir_profiles.data_elements.v1.meta_element import (
    DataElementMeta,
)
from helix_fhir_profiles.schema.v1.profile_definition_schema import (
    ProfileDefinition,
)


class ProfileLocationArea:
    @staticmethod
    def get_profile_id() -> AutoMapperTextLikeBase:
        return A.text("pr-location-area")

    @staticmethod
    def get_profile_url() -> AutoMapperTextLikeBase:
        return A.concat(
            ProfileDefinition.get_url_base(), ProfileLocationArea.get_profile_id()
        )


def mapping(parameters: Dict[str, Any]) -> List[AutoMapper]:
    resource = A.text("Location")

    mapper = AutoMapper(
        view=parameters["view_pr_location_area"],
        source_view=parameters["view_profile_config"],
        use_schema=False,
    ).complex(
        ProfileDefinition(
            profile_id=FhirId(ProfileLocationArea.get_profile_id()),
            profile_name=A.text("Location Area"),
            computer_friendly_profile_name=A.text("LocationArea"),
            fhir_resource_type=resource,
            description=A.text("Location object representing a physical area"),
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
            # ADDRESS
            # .concat(DataElementAddress.get_address_any(resource=resource))
            .concat(DataElementAddress.get_coverage_area(resource=resource)).concat(
                FhirList(
                    [
                        ElementDefinition(
                            id_=A.concat(resource, ".physicalType"),
                            path=A.concat(resource, ".physicalType"),
                            short=A.concat(
                                "Fixed: ",
                                LocationTypeCodeValues.Area,
                                " | ",
                                LocationTypeCode.codeset,
                            ),
                            definition=A.text(
                                "Code indicating the Location resource describes an area"
                            ),
                            patternCodeableConcept=CodeableConcept(
                                id_="physical-type",
                                coding=FhirList(
                                    [
                                        Coding(
                                            id_="area",
                                            system=LocationTypeCode.codeset,
                                            code=LocationTypeCodeValues.Area,
                                        )
                                    ]
                                ),
                            ),
                        ),
                    ],
                )
            ),
        )
    )

    return [mapper]

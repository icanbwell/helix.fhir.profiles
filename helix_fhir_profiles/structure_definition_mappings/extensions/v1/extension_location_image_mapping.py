from typing import Dict, Any, List

from spark_auto_mapper_fhir.backbone_elements.structure_definition_context import (
    StructureDefinitionContext,
)
from spark_auto_mapper_fhir.value_sets.extension_context_type import (
    ExtensionContextTypeCodeValues,
)

from helix_fhir_profiles.data_elements.v1.meta_element import (
    DataElementMeta,
)
from spark_auto_mapper.automappers.automapper import AutoMapper
from spark_auto_mapper.data_types.text_like_base import AutoMapperTextLikeBase
from spark_auto_mapper.helpers.automapper_helpers import AutoMapperHelpers as A
from spark_auto_mapper_fhir.backbone_elements.element_definition import (
    ElementDefinition,
)
from spark_auto_mapper_fhir.fhir_types.id import FhirId
from spark_auto_mapper_fhir.fhir_types.list import FhirList

from helix_fhir_profiles.schema.v1.profile_definition_schema import (
    ProfileDefinition,
)

profile_name = "Extension - Location Image"


class ExtensionLocationImage:
    @staticmethod
    def get_profile_id() -> AutoMapperTextLikeBase:
        return A.text("ex-location-image")

    @staticmethod
    def get_profile_url() -> AutoMapperTextLikeBase:
        return A.concat(
            ProfileDefinition.get_url_base(), ExtensionLocationImage.get_profile_id()
        )


def mapping(parameters: Dict[str, Any]) -> List[AutoMapper]:
    resource = A.text("Extension")

    mapper = AutoMapper(
        view=parameters["view_extension_location_image"],
        source_view=parameters["view_profile_config"],
        use_schema=False,
    ).complex(
        ProfileDefinition(
            profile_id=FhirId(ExtensionLocationImage.get_profile_id()),
            profile_name="Extension - Location Image",
            computer_friendly_profile_name="ExtensionLocationImage",
            fhir_resource_type="Extension",
            description="extension for a location photo",
            context=FhirList(
                [
                    StructureDefinitionContext(
                        type_=ExtensionContextTypeCodeValues.ElementID,
                        expression="Location",
                    )
                ]
            ),
            differential_elements=FhirList(
                [
                    ElementDefinition(id_=A.concat(resource), path=A.concat(resource)),
                    ElementDefinition(
                        id_=A.concat(resource, ".id"), path=A.concat(resource, ".id")
                    ),
                ],
                True,
            ).concat(DataElementMeta.get_meta(resource=resource))
            #     todo
        )
    )

    return [mapper]

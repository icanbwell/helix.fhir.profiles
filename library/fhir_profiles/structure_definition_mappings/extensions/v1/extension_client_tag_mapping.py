from typing import Dict, Any, List

from spark_auto_mapper_fhir.backbone_elements.structure_definition_context import (
    StructureDefinitionContext,
)
from spark_auto_mapper_fhir.value_sets.extension_context_type import (
    ExtensionContextTypeCodeValues,
)

from library.fhir_profiles.data_elements.v1.meta_element import (
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

from library.fhir_profiles.schema.v1.profile_definition_schema import (
    ProfileDefinition,
)

profile_name = "Extension - Client Tag"
# NOTE this is to go on the complex-type / list elements within the Practitioner/Location/Organization resources, not as a resource.extension


class ExtensionClientTag:
    @staticmethod
    def get_profile_id() -> AutoMapperTextLikeBase:
        return A.text("ex-client-tag")

    @staticmethod
    def get_profile_url() -> AutoMapperTextLikeBase:
        return A.concat(
            ProfileDefinition.get_url_base(), ExtensionClientTag.get_profile_id()
        )


def mapping(parameters: Dict[str, Any]) -> List[AutoMapper]:
    resource = A.text("Extension")

    mapper = AutoMapper(
        view=parameters["view_extension_client_tag"],
        source_view=parameters["view_profile_config"],
        use_schema=False,
    ).complex(
        ProfileDefinition(
            profile_id=FhirId(ExtensionClientTag.get_profile_id()),
            profile_name="Extension - Client Tag",
            computer_friendly_profile_name="ExtensionClientTag",
            fhir_resource_type="Extension",
            description="An extension for PSS to be used on the 'generic' Practitioner resources (ie id = NPI with) to designate a client's preference for a particular element in an array. \n \n For example, HospitalOrg prefers NPPES's name data to appear in their provider search, while OtherHealthcare prefers their own data.",
            context=FhirList(
                [
                    StructureDefinitionContext(
                        type_=ExtensionContextTypeCodeValues.ElementID,
                        expression="Practitioner",
                    ),
                    StructureDefinitionContext(
                        type_=ExtensionContextTypeCodeValues.ElementID,
                        expression="Location",
                    ),
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

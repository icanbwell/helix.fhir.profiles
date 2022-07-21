from spark_auto_mapper.data_types.text_like_base import AutoMapperTextLikeBase
from spark_auto_mapper_fhir.backbone_elements.element_definition import (
    ElementDefinition,
)

from spark_auto_mapper.helpers.automapper_helpers import AutoMapperHelpers as A
from spark_auto_mapper_fhir.backbone_elements.element_definition_type import (
    ElementDefinitionType,
)
from spark_auto_mapper_fhir.complex_types.coding import Coding
from spark_auto_mapper_fhir.fhir_types.list import FhirList

from library.fhir_profiles.schema.v1.product_feature_codes import (
    ProductFeatureCode,
    ProductFeatureCodeValues,
)


class DataBackboneElementHoursOfOperation:
    @staticmethod
    def get_element_definition(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "hours-of-operation"
        elements = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".hoursOfOperation"),
                    sliceName=label,
                    label=label,
                    code=FhirList(
                        [
                            Coding(
                                system=ProductFeatureCode.codeset,
                                code=ProductFeatureCodeValues.ProviderSearch,
                            )
                        ]
                    ),
                    short="hours of operation",
                    definition="hours of operation",
                    # comment="",
                    requirements="preferred for provider search",
                    type_=FhirList([ElementDefinitionType(code="BackboneElement")]),
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".id"),
                    path=A.concat(resource, ".hoursOfOperation.id"),
                    label=label,
                    short="set to day of week code",
                    min=1,
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".daysOfWeek"),
                    path=A.concat(resource, ".hoursOfOperation.daysOfWeek"),
                    label=label,
                    short="mon | tue | wed | thu | fri | sat | sun",
                    # definition="",
                    min=0,
                    max="*",
                    # binding=ElementDefinitionBinding(
                    #     strength=BindingStrengthCodeValues.Required,
                    #     description="The days of the week.",
                    #     valueSet=DaysOfWeekCode.codeset,
                    # ),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".allDay"),
                    path=A.concat(resource, ".hoursOfOperation.allDay"),
                    label=label,
                    short="The Location is open all day (boolean)",
                    definition="The location is open all day.",
                    min=0,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="boolean")]),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".openingingTime"),
                    path=A.concat(resource, ".hoursOfOperation.openingTime"),
                    label=label,
                    short="Time that the location opens",
                    type_=FhirList([ElementDefinitionType(code="time")]),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".closingTime"),
                    path=A.concat(resource, ".hoursOfOperation.closingTime"),
                    label=label,
                    short="Time that the location closes",
                    type_=FhirList([ElementDefinitionType(code="time")]),
                ),
            ],
            True,
        )

        return elements

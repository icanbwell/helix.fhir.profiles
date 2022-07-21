from library.meta_security_labels.v1.security_label_codes import (
    BwellAllSecurityLabelsCode,
)
from spark_auto_mapper.data_types.text_like_base import AutoMapperTextLikeBase
from spark_auto_mapper_fhir.backbone_elements.element_definition import (
    ElementDefinition,
)

from spark_auto_mapper.helpers.automapper_helpers import AutoMapperHelpers as A
from spark_auto_mapper_fhir.backbone_elements.element_definition_example import (
    ElementDefinitionExample,
)
from spark_auto_mapper_fhir.backbone_elements.element_definition_type import (
    ElementDefinitionType,
)
from spark_auto_mapper_fhir.complex_types.coding import Coding
from spark_auto_mapper_fhir.fhir_types.list import FhirList


class DataElementMeta:
    @staticmethod
    def get_meta(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "meta"
        element = FhirList(
            [
                ElementDefinition(
                    id_=A.concat(resource, ".meta"),
                    path=A.concat(resource, ".meta"),
                    label=label,
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="Meta")]),
                ),
                ElementDefinition(
                    id_=A.concat(resource, ".meta.source"),
                    path=A.concat(resource, ".meta.source"),
                    sliceName="meta-source",
                    label=label,
                    short="uri of the data source",
                    definition="Typically the data owner's URL followed by a source/file description",
                    # comment="",
                    requirements="mandatory for all resources in bWell's FHIR Server",
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="uri")]),
                    example=FhirList(
                        [
                            ElementDefinitionExample(
                                label="example of meta.source",
                                valueUri="https://www.icanbwell.com/provider-directory",
                            )
                        ]
                    ),
                ),
                ElementDefinition(
                    id_=A.concat(resource, ".meta.security"),
                    path=A.concat(resource, ".meta.security"),
                    sliceName="meta-security",
                    label=label,
                    short="security tags representing the data's owner, vendor, and accessibility",
                    definition="data owner: \n \n data vendor: \n \n data access: ",
                    # comment="",
                    requirements="/owner & /access are mandatory for all resources in bWell's FHIR Server",
                    min=1,
                    max="*",
                    type_=FhirList([ElementDefinitionType(code="Coding")]),
                    example=FhirList(
                        [
                            ElementDefinitionExample(
                                label="example of data owner security tag",
                                valueCoding=Coding(
                                    system=BwellAllSecurityLabelsCode.owner_codeset,
                                    code=BwellAllSecurityLabelsCode.Bwell,
                                ),
                            ),
                            ElementDefinitionExample(
                                label="example of data access security tag",
                                valueCoding=Coding(
                                    system=BwellAllSecurityLabelsCode.access_codeset,
                                    code=BwellAllSecurityLabelsCode.Bwell,
                                ),
                            ),
                            ElementDefinitionExample(
                                label="example of data vendor security tag",
                                valueCoding=Coding(
                                    system=BwellAllSecurityLabelsCode.vendor_codeset,
                                    code=BwellAllSecurityLabelsCode.Bwell,
                                ),
                            ),
                        ]
                    ),
                    # binding=
                ),
            ]
        )

        return element

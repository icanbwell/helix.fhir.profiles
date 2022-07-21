from spark_auto_mapper_fhir.backbone_elements.element_definition_binding import (
    ElementDefinitionBinding,
)
from spark_auto_mapper_fhir.value_sets.binding_strength import BindingStrengthCodeValues

from library.fhir_profiles.structure_definition_mappings.eligibility.v1.patient_mapping import (
    ProfilePatient,
)
from spark_auto_mapper.data_types.text_like_base import AutoMapperTextLikeBase
from spark_auto_mapper_fhir.backbone_elements.element_definition import (
    ElementDefinition,
)

from spark_auto_mapper.helpers.automapper_helpers import AutoMapperHelpers as A
from spark_auto_mapper_fhir.backbone_elements.element_definition_slicing import (
    ElementDefinitionSlicing,
)
from spark_auto_mapper_fhir.backbone_elements.element_definition_type import (
    ElementDefinitionType,
)
from spark_auto_mapper_fhir.complex_types.coding import Coding
from spark_auto_mapper_fhir.fhir_types.list import FhirList
from spark_auto_mapper_fhir.value_sets.generic_type import GenericTypeCode
from spark_auto_mapper_fhir.value_sets.slicing_rules import SlicingRulesCodeValues


class DataElementSignature:
    @staticmethod
    def get_signature_any(
        resource: AutoMapperTextLikeBase,
    ) -> FhirList[ElementDefinition]:
        label = "signature"
        element = FhirList(
            [
                ElementDefinition(
                    id_=A.concat("de-", label),
                    path=A.concat(resource, ".signature"),
                    label=label,
                    slicing=ElementDefinitionSlicing(
                        description="slice by type", rules=SlicingRulesCodeValues.Open
                    ),
                    min=0,
                    max="*",
                    type_=FhirList([ElementDefinitionType(code="CodeableConcept")]),
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".id"),
                    path=A.concat(resource, ".signature.id"),
                    label=label,
                    short="signature",
                    min=1,
                    max="1",
                    type_=FhirList([ElementDefinitionType(code="string")]),
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".type"),
                    path=A.concat(resource, ".signature.type"),
                    label=label,
                    # short="",
                    min=1,
                    type_=FhirList([ElementDefinitionType(code="Coding")]),
                    binding=ElementDefinitionBinding(
                        strength=BindingStrengthCodeValues.Example,
                        valueSet="urn:iso-astm:E1762-95:2013",
                    ),
                    patternCoding=Coding(
                        system="urn:iso-astm:E1762-95:2013",
                        code=GenericTypeCode("1.2.840.10065.1.12.1.5"),
                        display="Verification Signature",
                    ),
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".when"),
                    path=A.concat(resource, ".signature.when"),
                    label=label,
                    short="When the signature was created",
                    min=1,
                    type_=FhirList([ElementDefinitionType(code="instant")]),
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".who"),
                    path=A.concat(resource, ".signature.who"),
                    label=label,
                    short="Who signed",
                    min=1,
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
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".targetFormat"),
                    path=A.concat(resource, ".signature.targetFormat"),
                    label=label,
                    short="The technical format of the signed resources",
                    type_=FhirList([ElementDefinitionType(code="code")]),
                    mustSupport=A.boolean(True),
                ),
                ElementDefinition(
                    id_=A.concat("de-", label, ".data"),
                    path=A.concat(resource, ".signature.data"),
                    label=label,
                    short="The actual signature content (xml, picture, etc)",
                    min=1,
                    type_=FhirList([ElementDefinitionType(code="base64Binary")]),
                    mustSupport=A.boolean(True),
                ),
            ],
            True,
        )

        return element

from typing import Optional, Union, List

from spark_auto_mapper_fhir.backbone_elements.element_definition import (
    ElementDefinition,
)
from spark_auto_mapper_fhir.backbone_elements.structure_definition_context import (
    StructureDefinitionContext,
)
from spark_auto_mapper_fhir.complex_types.codeable_concept import CodeableConcept
from spark_auto_mapper_fhir.complex_types.identifier import Identifier
from spark_auto_mapper_fhir.fhir_types.markdown import FhirMarkdown
from spark_auto_mapper_fhir.value_sets.definition_use_codes import (
    DefinitionUseCodesCode,
)
from spark_auto_mapper_fhir.value_sets.fhir_version import FHIRVersionCodeValues
from spark_auto_mapper_fhir.value_sets.jurisdiction_value_set import (
    JurisdictionValueSetCode,
)
from spark_auto_mapper_fhir.value_sets.publication_status import (
    PublicationStatusCodeValues,
)
from spark_auto_mapper_fhir.value_sets.structure_definition_kind import (
    StructureDefinitionKindCodeValues,
)

from library.bwell.meta_security_labels.v1.security_label_codes import (
    BwellAllSecurityLabelsCode,
)
from spark_auto_mapper.helpers.automapper_helpers import AutoMapperHelpers as A

# noinspection PyPackageRequirements
from pyspark.sql.types import StructType, DataType
from spark_auto_mapper_fhir.complex_types.coding import Coding
from spark_auto_mapper_fhir.complex_types.meta import Meta
from spark_auto_mapper_fhir.fhir_types.list import FhirList
from spark_auto_mapper_fhir.fhir_types.string import FhirString
from spark_auto_mapper_fhir.fhir_types.id import FhirId
from spark_auto_mapper_fhir.fhir_types.uri import FhirUri

from spark_auto_mapper_fhir.resources.structure_definition import StructureDefinition
from spark_auto_mapper_fhir.value_sets.type_derivation_rule import (
    TypeDerivationRuleCodeValues,
)
from spark_fhir_schemas.r4.resources.structuredefinition import (
    StructureDefinitionSchema,
)
from spark_auto_mapper_fhir.backbone_elements.structure_definition_differential import (
    StructureDefinitionDifferential,
)


# noinspection PyPep8Naming
class ProfileDefinition(StructureDefinition):
    @staticmethod
    def get_url_base() -> str:
        return "https://fhir.icanbwell.com/4_0_0/StructureDefinition/"

    # noinspection PyPep8Naming
    def __init__(
        self,
        profile_id: FhirId,
        profile_name: FhirString,
        computer_friendly_profile_name: FhirString,
        fhir_resource_type: FhirUri,
        identifier: Optional[FhirList[Identifier]] = None,
        version: Optional[FhirString] = A.text("1.02"),
        description: Optional[FhirMarkdown] = None,
        purpose: Optional[FhirMarkdown] = None,
        keyword: Optional[FhirList[Coding[DefinitionUseCodesCode]]] = None,
        context: Optional[FhirList[StructureDefinitionContext]] = None,
        differential_elements: FhirList[ElementDefinition] = FhirList([]),
    ) -> None:
        """
        :profile_id: pr-{lower-cased profile_name}
            example - "pr-healthcare-location"
        :profile_name: concise description, preferably proper-cased
            example - "Healthcare Location"
        """
        super().__init__(
            # resourceType="StructureDefinition",
            id_=profile_id,
            meta=Meta(
                source=A.text("https://www.icanbwell.com/fhir_profile_definitions"),
                security=FhirList(
                    [
                        Coding(
                            system=BwellAllSecurityLabelsCode.owner_codeset,
                            code=BwellAllSecurityLabelsCode.Bwell,
                        ),
                        Coding(
                            system=BwellAllSecurityLabelsCode.access_codeset,
                            code=BwellAllSecurityLabelsCode.Bwell,
                        ),
                    ]
                ),
            ),
            # implicitRules=implicitRules,
            # language=language,
            # text=text,
            # contained=contained,
            # extension=extension,
            # modifierExtension=modifierExtension,
            url=A.concat(ProfileDefinition.get_url_base(), profile_id),
            identifier=identifier,
            version=version,
            name=computer_friendly_profile_name,
            title=A.concat("Profile: ", profile_name),
            status=PublicationStatusCodeValues.Active,
            experimental=A.boolean(False),
            date=A.date(
                "2022-06-02"
            ),  # when set to date.today() unit tests will fail if a day goes by
            publisher=A.text("bWell Connected Health"),
            # contact=contact,
            description=description,
            # useContext=useContext,
            jurisdiction=FhirList(
                [
                    CodeableConcept(
                        coding=FhirList(
                            [
                                Coding(
                                    system=JurisdictionValueSetCode.codeset_urn_iso_std_iso_3166,
                                    code=JurisdictionValueSetCode(A.text("US")),
                                    display="United States of America",
                                )
                            ]
                        ),
                        text=A.text("United States of America"),
                    )
                ]
            ),
            purpose=purpose,
            # copyright=copyright,
            keyword=keyword,
            fhirVersion=FHIRVersionCodeValues._4_0_0,
            # mapping=mapping,
            kind=StructureDefinitionKindCodeValues.Resource,
            abstract=A.boolean(False),
            context=context,
            # contextInvariant=contextInvariant,
            type_=fhir_resource_type,
            baseDefinition=A.concat(
                "http://hl7.org/fhir/StructureDefinition/", fhir_resource_type
            ),
            derivation=TypeDerivationRuleCodeValues.Constraint,
            differential=StructureDefinitionDifferential(element=differential_elements),
        )

    def get_schema(
        self, include_extension: bool, extension_fields: Optional[List[str]] = None
    ) -> Optional[Union[StructType, DataType]]:
        return StructureDefinitionSchema.get_schema(
            include_extension=include_extension, extension_fields=extension_fields
        )

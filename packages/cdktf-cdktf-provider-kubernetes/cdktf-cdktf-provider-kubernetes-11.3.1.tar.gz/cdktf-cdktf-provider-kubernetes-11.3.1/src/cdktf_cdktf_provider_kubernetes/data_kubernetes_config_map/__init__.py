'''
# `data_kubernetes_config_map`

Refer to the Terraform Registry for docs: [`data_kubernetes_config_map`](https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/data-sources/config_map).
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class DataKubernetesConfigMap(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-kubernetes.dataKubernetesConfigMap.DataKubernetesConfigMap",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/data-sources/config_map kubernetes_config_map}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        metadata: typing.Union["DataKubernetesConfigMapMetadata", typing.Dict[builtins.str, typing.Any]],
        id: typing.Optional[builtins.str] = None,
        immutable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/data-sources/config_map kubernetes_config_map} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param metadata: metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/data-sources/config_map#metadata DataKubernetesConfigMap#metadata}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/data-sources/config_map#id DataKubernetesConfigMap#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param immutable: Immutable, if set to true, ensures that data stored in the ConfigMap cannot be updated (only object metadata can be modified). If not set to true, the field can be modified at any time. Defaulted to nil. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/data-sources/config_map#immutable DataKubernetesConfigMap#immutable}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59ef89cf9dd8234ba60c0b3515f4b25329db78581613b804a2178773f23ac398)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataKubernetesConfigMapConfig(
            metadata=metadata,
            id=id,
            immutable=immutable,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a DataKubernetesConfigMap resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataKubernetesConfigMap to import.
        :param import_from_id: The id of the existing DataKubernetesConfigMap that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/data-sources/config_map#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataKubernetesConfigMap to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ef524e4ff0bbc9a54abb0f1ce303877f872b2948860c2b4cf6c63d43143ecd6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putMetadata")
    def put_metadata(
        self,
        *,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param annotations: An unstructured key value map stored with the config_map that may be used to store arbitrary metadata. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/data-sources/config_map#annotations DataKubernetesConfigMap#annotations}
        :param labels: Map of string keys and values that can be used to organize and categorize (scope and select) the config_map. May match selectors of replication controllers and services. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/data-sources/config_map#labels DataKubernetesConfigMap#labels}
        :param name: Name of the config_map, must be unique. Cannot be updated. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/data-sources/config_map#name DataKubernetesConfigMap#name}
        :param namespace: Namespace defines the space within which name of the config_map must be unique. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/data-sources/config_map#namespace DataKubernetesConfigMap#namespace}
        '''
        value = DataKubernetesConfigMapMetadata(
            annotations=annotations, labels=labels, name=name, namespace=namespace
        )

        return typing.cast(None, jsii.invoke(self, "putMetadata", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetImmutable")
    def reset_immutable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImmutable", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="synthesizeHclAttributes")
    def _synthesize_hcl_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeHclAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="binaryData")
    def binary_data(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "binaryData"))

    @builtins.property
    @jsii.member(jsii_name="data")
    def data(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "data"))

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> "DataKubernetesConfigMapMetadataOutputReference":
        return typing.cast("DataKubernetesConfigMapMetadataOutputReference", jsii.get(self, "metadata"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="immutableInput")
    def immutable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "immutableInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataInput")
    def metadata_input(self) -> typing.Optional["DataKubernetesConfigMapMetadata"]:
        return typing.cast(typing.Optional["DataKubernetesConfigMapMetadata"], jsii.get(self, "metadataInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53a77a0fbaffd44fa13923e2eb9d411551c9d084af492c9f90a1a340025634ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="immutable")
    def immutable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "immutable"))

    @immutable.setter
    def immutable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85db4318fdb10a12382b97cb217c529c7281e6f9418fe7665bf3d1af5ba9f0fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "immutable", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-kubernetes.dataKubernetesConfigMap.DataKubernetesConfigMapConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "metadata": "metadata",
        "id": "id",
        "immutable": "immutable",
    },
)
class DataKubernetesConfigMapConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        metadata: typing.Union["DataKubernetesConfigMapMetadata", typing.Dict[builtins.str, typing.Any]],
        id: typing.Optional[builtins.str] = None,
        immutable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param metadata: metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/data-sources/config_map#metadata DataKubernetesConfigMap#metadata}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/data-sources/config_map#id DataKubernetesConfigMap#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param immutable: Immutable, if set to true, ensures that data stored in the ConfigMap cannot be updated (only object metadata can be modified). If not set to true, the field can be modified at any time. Defaulted to nil. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/data-sources/config_map#immutable DataKubernetesConfigMap#immutable}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(metadata, dict):
            metadata = DataKubernetesConfigMapMetadata(**metadata)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fad11651a93e26756e2e182e1e1c298f3ccdc97c5094899c57036fd78e0e6b34)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument immutable", value=immutable, expected_type=type_hints["immutable"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "metadata": metadata,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if id is not None:
            self._values["id"] = id
        if immutable is not None:
            self._values["immutable"] = immutable

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def metadata(self) -> "DataKubernetesConfigMapMetadata":
        '''metadata block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/data-sources/config_map#metadata DataKubernetesConfigMap#metadata}
        '''
        result = self._values.get("metadata")
        assert result is not None, "Required property 'metadata' is missing"
        return typing.cast("DataKubernetesConfigMapMetadata", result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/data-sources/config_map#id DataKubernetesConfigMap#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def immutable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Immutable, if set to true, ensures that data stored in the ConfigMap cannot be updated (only object metadata can be modified).

        If not set to true, the field can be modified at any time. Defaulted to nil.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/data-sources/config_map#immutable DataKubernetesConfigMap#immutable}
        '''
        result = self._values.get("immutable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataKubernetesConfigMapConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-kubernetes.dataKubernetesConfigMap.DataKubernetesConfigMapMetadata",
    jsii_struct_bases=[],
    name_mapping={
        "annotations": "annotations",
        "labels": "labels",
        "name": "name",
        "namespace": "namespace",
    },
)
class DataKubernetesConfigMapMetadata:
    def __init__(
        self,
        *,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param annotations: An unstructured key value map stored with the config_map that may be used to store arbitrary metadata. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/data-sources/config_map#annotations DataKubernetesConfigMap#annotations}
        :param labels: Map of string keys and values that can be used to organize and categorize (scope and select) the config_map. May match selectors of replication controllers and services. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/data-sources/config_map#labels DataKubernetesConfigMap#labels}
        :param name: Name of the config_map, must be unique. Cannot be updated. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/data-sources/config_map#name DataKubernetesConfigMap#name}
        :param namespace: Namespace defines the space within which name of the config_map must be unique. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/data-sources/config_map#namespace DataKubernetesConfigMap#namespace}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fa762726fbd9bc27aac8c5a58568a09c036e4270a2cb01854c35fbeeb5f4885)
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if annotations is not None:
            self._values["annotations"] = annotations
        if labels is not None:
            self._values["labels"] = labels
        if name is not None:
            self._values["name"] = name
        if namespace is not None:
            self._values["namespace"] = namespace

    @builtins.property
    def annotations(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''An unstructured key value map stored with the config_map that may be used to store arbitrary metadata.

        More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/data-sources/config_map#annotations DataKubernetesConfigMap#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Map of string keys and values that can be used to organize and categorize (scope and select) the config_map.

        May match selectors of replication controllers and services. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/data-sources/config_map#labels DataKubernetesConfigMap#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the config_map, must be unique. Cannot be updated. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/data-sources/config_map#name DataKubernetesConfigMap#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''Namespace defines the space within which name of the config_map must be unique.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/data-sources/config_map#namespace DataKubernetesConfigMap#namespace}
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataKubernetesConfigMapMetadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataKubernetesConfigMapMetadataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-kubernetes.dataKubernetesConfigMap.DataKubernetesConfigMapMetadataOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4eeeba8e1ea75e716f1e2967a437483f0a6477cd2cb7ed8b8ca2360403e9f72)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAnnotations")
    def reset_annotations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotations", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetNamespace")
    def reset_namespace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamespace", []))

    @builtins.property
    @jsii.member(jsii_name="generation")
    def generation(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "generation"))

    @builtins.property
    @jsii.member(jsii_name="resourceVersion")
    def resource_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceVersion"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="annotationsInput")
    def annotations_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "annotationsInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="namespaceInput")
    def namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71306e7c01c0d19c51785f65f314f1ad809a2a8ff05ba44ac92c727a7096c704)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value)

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13d0e455de6a122f327c5fde9ae736b277b7e39a7a3573b37cd12235aa5fd31a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a4509b5cab1512b9cdbd857e56f54fd36e107ed84d68486cb9ea22ef84bbabc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f0417160e10575d879e9035a0fa2de0140bd7b5ddcb89977a3579ced2705c7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataKubernetesConfigMapMetadata]:
        return typing.cast(typing.Optional[DataKubernetesConfigMapMetadata], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataKubernetesConfigMapMetadata],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19738a3f953dc7ab259699eca8d4959eaf88c270106f38521c06fde58650a62f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "DataKubernetesConfigMap",
    "DataKubernetesConfigMapConfig",
    "DataKubernetesConfigMapMetadata",
    "DataKubernetesConfigMapMetadataOutputReference",
]

publication.publish()

def _typecheckingstub__59ef89cf9dd8234ba60c0b3515f4b25329db78581613b804a2178773f23ac398(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    metadata: typing.Union[DataKubernetesConfigMapMetadata, typing.Dict[builtins.str, typing.Any]],
    id: typing.Optional[builtins.str] = None,
    immutable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ef524e4ff0bbc9a54abb0f1ce303877f872b2948860c2b4cf6c63d43143ecd6(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53a77a0fbaffd44fa13923e2eb9d411551c9d084af492c9f90a1a340025634ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85db4318fdb10a12382b97cb217c529c7281e6f9418fe7665bf3d1af5ba9f0fb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fad11651a93e26756e2e182e1e1c298f3ccdc97c5094899c57036fd78e0e6b34(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    metadata: typing.Union[DataKubernetesConfigMapMetadata, typing.Dict[builtins.str, typing.Any]],
    id: typing.Optional[builtins.str] = None,
    immutable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fa762726fbd9bc27aac8c5a58568a09c036e4270a2cb01854c35fbeeb5f4885(
    *,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4eeeba8e1ea75e716f1e2967a437483f0a6477cd2cb7ed8b8ca2360403e9f72(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71306e7c01c0d19c51785f65f314f1ad809a2a8ff05ba44ac92c727a7096c704(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13d0e455de6a122f327c5fde9ae736b277b7e39a7a3573b37cd12235aa5fd31a(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a4509b5cab1512b9cdbd857e56f54fd36e107ed84d68486cb9ea22ef84bbabc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f0417160e10575d879e9035a0fa2de0140bd7b5ddcb89977a3579ced2705c7f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19738a3f953dc7ab259699eca8d4959eaf88c270106f38521c06fde58650a62f(
    value: typing.Optional[DataKubernetesConfigMapMetadata],
) -> None:
    """Type checking stubs"""
    pass

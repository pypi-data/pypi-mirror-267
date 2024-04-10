'''
# `kubernetes_mutating_webhook_configuration_v1`

Refer to the Terraform Registry for docs: [`kubernetes_mutating_webhook_configuration_v1`](https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1).
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


class MutatingWebhookConfigurationV1(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-kubernetes.mutatingWebhookConfigurationV1.MutatingWebhookConfigurationV1",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1 kubernetes_mutating_webhook_configuration_v1}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        metadata: typing.Union["MutatingWebhookConfigurationV1Metadata", typing.Dict[builtins.str, typing.Any]],
        webhook: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MutatingWebhookConfigurationV1Webhook", typing.Dict[builtins.str, typing.Any]]]],
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1 kubernetes_mutating_webhook_configuration_v1} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param metadata: metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#metadata MutatingWebhookConfigurationV1#metadata}
        :param webhook: webhook block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#webhook MutatingWebhookConfigurationV1#webhook}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#id MutatingWebhookConfigurationV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8aefc9e02ad1b07bfdd07e7475c174c888f288313db6538cfe72533c1434a386)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MutatingWebhookConfigurationV1Config(
            metadata=metadata,
            webhook=webhook,
            id=id,
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
        '''Generates CDKTF code for importing a MutatingWebhookConfigurationV1 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the MutatingWebhookConfigurationV1 to import.
        :param import_from_id: The id of the existing MutatingWebhookConfigurationV1 that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the MutatingWebhookConfigurationV1 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__630496ce038b7cbfda9ef5d1d9c845c207b47510c8e7775e0f543aec3c2417cf)
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
        generate_name: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param annotations: An unstructured key value map stored with the mutating webhook configuration that may be used to store arbitrary metadata. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#annotations MutatingWebhookConfigurationV1#annotations}
        :param generate_name: Prefix, used by the server, to generate a unique name ONLY IF the ``name`` field has not been provided. This value will also be combined with a unique suffix. More info: https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md#idempotency Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#generate_name MutatingWebhookConfigurationV1#generate_name}
        :param labels: Map of string keys and values that can be used to organize and categorize (scope and select) the mutating webhook configuration. May match selectors of replication controllers and services. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#labels MutatingWebhookConfigurationV1#labels}
        :param name: Name of the mutating webhook configuration, must be unique. Cannot be updated. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#name MutatingWebhookConfigurationV1#name}
        '''
        value = MutatingWebhookConfigurationV1Metadata(
            annotations=annotations,
            generate_name=generate_name,
            labels=labels,
            name=name,
        )

        return typing.cast(None, jsii.invoke(self, "putMetadata", [value]))

    @jsii.member(jsii_name="putWebhook")
    def put_webhook(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MutatingWebhookConfigurationV1Webhook", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01f9ead77d2c011f66ecbf59fc95fc2940ec4878c105df5b8fa6b22d294892f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putWebhook", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> "MutatingWebhookConfigurationV1MetadataOutputReference":
        return typing.cast("MutatingWebhookConfigurationV1MetadataOutputReference", jsii.get(self, "metadata"))

    @builtins.property
    @jsii.member(jsii_name="webhook")
    def webhook(self) -> "MutatingWebhookConfigurationV1WebhookList":
        return typing.cast("MutatingWebhookConfigurationV1WebhookList", jsii.get(self, "webhook"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataInput")
    def metadata_input(
        self,
    ) -> typing.Optional["MutatingWebhookConfigurationV1Metadata"]:
        return typing.cast(typing.Optional["MutatingWebhookConfigurationV1Metadata"], jsii.get(self, "metadataInput"))

    @builtins.property
    @jsii.member(jsii_name="webhookInput")
    def webhook_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MutatingWebhookConfigurationV1Webhook"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MutatingWebhookConfigurationV1Webhook"]]], jsii.get(self, "webhookInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bda02b4997f14f3f4ff88fb723c4deb6a22c13a7e7f744f7665eeefbfb91f606)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-kubernetes.mutatingWebhookConfigurationV1.MutatingWebhookConfigurationV1Config",
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
        "webhook": "webhook",
        "id": "id",
    },
)
class MutatingWebhookConfigurationV1Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        metadata: typing.Union["MutatingWebhookConfigurationV1Metadata", typing.Dict[builtins.str, typing.Any]],
        webhook: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MutatingWebhookConfigurationV1Webhook", typing.Dict[builtins.str, typing.Any]]]],
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param metadata: metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#metadata MutatingWebhookConfigurationV1#metadata}
        :param webhook: webhook block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#webhook MutatingWebhookConfigurationV1#webhook}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#id MutatingWebhookConfigurationV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(metadata, dict):
            metadata = MutatingWebhookConfigurationV1Metadata(**metadata)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36189b2242e62f7bea18c1c088cfcd196b22663cf5301ed59466c62ebb18ccfe)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument webhook", value=webhook, expected_type=type_hints["webhook"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "metadata": metadata,
            "webhook": webhook,
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
    def metadata(self) -> "MutatingWebhookConfigurationV1Metadata":
        '''metadata block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#metadata MutatingWebhookConfigurationV1#metadata}
        '''
        result = self._values.get("metadata")
        assert result is not None, "Required property 'metadata' is missing"
        return typing.cast("MutatingWebhookConfigurationV1Metadata", result)

    @builtins.property
    def webhook(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MutatingWebhookConfigurationV1Webhook"]]:
        '''webhook block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#webhook MutatingWebhookConfigurationV1#webhook}
        '''
        result = self._values.get("webhook")
        assert result is not None, "Required property 'webhook' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MutatingWebhookConfigurationV1Webhook"]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#id MutatingWebhookConfigurationV1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MutatingWebhookConfigurationV1Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-kubernetes.mutatingWebhookConfigurationV1.MutatingWebhookConfigurationV1Metadata",
    jsii_struct_bases=[],
    name_mapping={
        "annotations": "annotations",
        "generate_name": "generateName",
        "labels": "labels",
        "name": "name",
    },
)
class MutatingWebhookConfigurationV1Metadata:
    def __init__(
        self,
        *,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        generate_name: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param annotations: An unstructured key value map stored with the mutating webhook configuration that may be used to store arbitrary metadata. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#annotations MutatingWebhookConfigurationV1#annotations}
        :param generate_name: Prefix, used by the server, to generate a unique name ONLY IF the ``name`` field has not been provided. This value will also be combined with a unique suffix. More info: https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md#idempotency Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#generate_name MutatingWebhookConfigurationV1#generate_name}
        :param labels: Map of string keys and values that can be used to organize and categorize (scope and select) the mutating webhook configuration. May match selectors of replication controllers and services. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#labels MutatingWebhookConfigurationV1#labels}
        :param name: Name of the mutating webhook configuration, must be unique. Cannot be updated. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#name MutatingWebhookConfigurationV1#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa1d4be776e728f2403df06945c3507c5ad93d29c57abbd8390b74b545c7e758)
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
            check_type(argname="argument generate_name", value=generate_name, expected_type=type_hints["generate_name"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if annotations is not None:
            self._values["annotations"] = annotations
        if generate_name is not None:
            self._values["generate_name"] = generate_name
        if labels is not None:
            self._values["labels"] = labels
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def annotations(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''An unstructured key value map stored with the mutating webhook configuration that may be used to store arbitrary metadata.

        More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#annotations MutatingWebhookConfigurationV1#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def generate_name(self) -> typing.Optional[builtins.str]:
        '''Prefix, used by the server, to generate a unique name ONLY IF the ``name`` field has not been provided.

        This value will also be combined with a unique suffix. More info: https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md#idempotency

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#generate_name MutatingWebhookConfigurationV1#generate_name}
        '''
        result = self._values.get("generate_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Map of string keys and values that can be used to organize and categorize (scope and select) the mutating webhook configuration.

        May match selectors of replication controllers and services. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#labels MutatingWebhookConfigurationV1#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the mutating webhook configuration, must be unique. Cannot be updated. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#name MutatingWebhookConfigurationV1#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MutatingWebhookConfigurationV1Metadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MutatingWebhookConfigurationV1MetadataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-kubernetes.mutatingWebhookConfigurationV1.MutatingWebhookConfigurationV1MetadataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a10c5bcb502fdb672db9e2c1ce91ade42ea615de4c967e8662a6cd4c28b8a2ba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAnnotations")
    def reset_annotations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotations", []))

    @jsii.member(jsii_name="resetGenerateName")
    def reset_generate_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGenerateName", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

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
    @jsii.member(jsii_name="generateNameInput")
    def generate_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "generateNameInput"))

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
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81e011669a711f712b50450827742b0e1b74a064cb36824b568803c47d4c7e9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value)

    @builtins.property
    @jsii.member(jsii_name="generateName")
    def generate_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "generateName"))

    @generate_name.setter
    def generate_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af82a471cdb21e595de789b96bd1e81c3c40512dba384be9bc30ab1e59d005e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generateName", value)

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e81c2aa8fa5f7e892f58b7ca9f799dc7bfb3be2394f01e578426a90f526bb29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30087be18246e7158aa34ca2e7d40e486e3cc21b5f31e65c34dcb0766a28dc3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MutatingWebhookConfigurationV1Metadata]:
        return typing.cast(typing.Optional[MutatingWebhookConfigurationV1Metadata], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MutatingWebhookConfigurationV1Metadata],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49bfcc67c37416bdae47d69b4d73f9a1b7b288c94acab176942cfadcc94c1555)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-kubernetes.mutatingWebhookConfigurationV1.MutatingWebhookConfigurationV1Webhook",
    jsii_struct_bases=[],
    name_mapping={
        "client_config": "clientConfig",
        "name": "name",
        "admission_review_versions": "admissionReviewVersions",
        "failure_policy": "failurePolicy",
        "match_policy": "matchPolicy",
        "namespace_selector": "namespaceSelector",
        "object_selector": "objectSelector",
        "reinvocation_policy": "reinvocationPolicy",
        "rule": "rule",
        "side_effects": "sideEffects",
        "timeout_seconds": "timeoutSeconds",
    },
)
class MutatingWebhookConfigurationV1Webhook:
    def __init__(
        self,
        *,
        client_config: typing.Union["MutatingWebhookConfigurationV1WebhookClientConfig", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        admission_review_versions: typing.Optional[typing.Sequence[builtins.str]] = None,
        failure_policy: typing.Optional[builtins.str] = None,
        match_policy: typing.Optional[builtins.str] = None,
        namespace_selector: typing.Optional[typing.Union["MutatingWebhookConfigurationV1WebhookNamespaceSelector", typing.Dict[builtins.str, typing.Any]]] = None,
        object_selector: typing.Optional[typing.Union["MutatingWebhookConfigurationV1WebhookObjectSelector", typing.Dict[builtins.str, typing.Any]]] = None,
        reinvocation_policy: typing.Optional[builtins.str] = None,
        rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MutatingWebhookConfigurationV1WebhookRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        side_effects: typing.Optional[builtins.str] = None,
        timeout_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param client_config: client_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#client_config MutatingWebhookConfigurationV1#client_config}
        :param name: The name of the admission webhook. Name should be fully qualified, e.g., imagepolicy.kubernetes.io, where "imagepolicy" is the name of the webhook, and kubernetes.io is the name of the organization. Required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#name MutatingWebhookConfigurationV1#name}
        :param admission_review_versions: AdmissionReviewVersions is an ordered list of preferred ``AdmissionReview`` versions the Webhook expects. API server will try to use first version in the list which it supports. If none of the versions specified in this list supported by API server, validation will fail for this object. If a persisted webhook configuration specifies allowed versions and does not include any versions known to the API Server, calls to the webhook will fail and be subject to the failure policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#admission_review_versions MutatingWebhookConfigurationV1#admission_review_versions}
        :param failure_policy: FailurePolicy defines how unrecognized errors from the admission endpoint are handled - allowed values are Ignore or Fail. Defaults to Fail. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#failure_policy MutatingWebhookConfigurationV1#failure_policy}
        :param match_policy: matchPolicy defines how the "rules" list is used to match incoming requests. Allowed values are "Exact" or "Equivalent". - Exact: match a request only if it exactly matches a specified rule. For example, if deployments can be modified via apps/v1, apps/v1beta1, and extensions/v1beta1, but "rules" only included ``apiGroups:["apps"], apiVersions:["v1"], resources: ["deployments"]``, a request to apps/v1beta1 or extensions/v1beta1 would not be sent to the webhook. - Equivalent: match a request if modifies a resource listed in rules, even via another API group or version. For example, if deployments can be modified via apps/v1, apps/v1beta1, and extensions/v1beta1, and "rules" only included ``apiGroups:["apps"], apiVersions:["v1"], resources: ["deployments"]``, a request to apps/v1beta1 or extensions/v1beta1 would be converted to apps/v1 and sent to the webhook. Defaults to "Equivalent" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#match_policy MutatingWebhookConfigurationV1#match_policy}
        :param namespace_selector: namespace_selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#namespace_selector MutatingWebhookConfigurationV1#namespace_selector}
        :param object_selector: object_selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#object_selector MutatingWebhookConfigurationV1#object_selector}
        :param reinvocation_policy: reinvocationPolicy indicates whether this webhook should be called multiple times as part of a single admission evaluation. Allowed values are "Never" and "IfNeeded". Never: the webhook will not be called more than once in a single admission evaluation. IfNeeded: the webhook will be called at least one additional time as part of the admission evaluation if the object being admitted is modified by other admission plugins after the initial webhook call. Webhooks that specify this option *must* be idempotent, able to process objects they previously admitted. Note: * the number of additional invocations is not guaranteed to be exactly one. * if additional invocations result in further modifications to the object, webhooks are not guaranteed to be invoked again. * webhooks that use this option may be reordered to minimize the number of additional invocations. * to validate an object after all mutations are guaranteed complete, use a validating admission webhook instead. Defaults to "Never". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#reinvocation_policy MutatingWebhookConfigurationV1#reinvocation_policy}
        :param rule: rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#rule MutatingWebhookConfigurationV1#rule}
        :param side_effects: SideEffects states whether this webhook has side effects. Acceptable values are: None, NoneOnDryRun (webhooks created via v1beta1 may also specify Some or Unknown). Webhooks with side effects MUST implement a reconciliation system, since a request may be rejected by a future step in the admission chain and the side effects therefore need to be undone. Requests with the dryRun attribute will be auto-rejected if they match a webhook with sideEffects == Unknown or Some. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#side_effects MutatingWebhookConfigurationV1#side_effects}
        :param timeout_seconds: TimeoutSeconds specifies the timeout for this webhook. After the timeout passes, the webhook call will be ignored or the API call will fail based on the failure policy. The timeout value must be between 1 and 30 seconds. Default to 10 seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#timeout_seconds MutatingWebhookConfigurationV1#timeout_seconds}
        '''
        if isinstance(client_config, dict):
            client_config = MutatingWebhookConfigurationV1WebhookClientConfig(**client_config)
        if isinstance(namespace_selector, dict):
            namespace_selector = MutatingWebhookConfigurationV1WebhookNamespaceSelector(**namespace_selector)
        if isinstance(object_selector, dict):
            object_selector = MutatingWebhookConfigurationV1WebhookObjectSelector(**object_selector)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f542d99e73ccf049496dd70e9b1b1b425c36ba2451073c99df3ab242dabbfbc)
            check_type(argname="argument client_config", value=client_config, expected_type=type_hints["client_config"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument admission_review_versions", value=admission_review_versions, expected_type=type_hints["admission_review_versions"])
            check_type(argname="argument failure_policy", value=failure_policy, expected_type=type_hints["failure_policy"])
            check_type(argname="argument match_policy", value=match_policy, expected_type=type_hints["match_policy"])
            check_type(argname="argument namespace_selector", value=namespace_selector, expected_type=type_hints["namespace_selector"])
            check_type(argname="argument object_selector", value=object_selector, expected_type=type_hints["object_selector"])
            check_type(argname="argument reinvocation_policy", value=reinvocation_policy, expected_type=type_hints["reinvocation_policy"])
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
            check_type(argname="argument side_effects", value=side_effects, expected_type=type_hints["side_effects"])
            check_type(argname="argument timeout_seconds", value=timeout_seconds, expected_type=type_hints["timeout_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_config": client_config,
            "name": name,
        }
        if admission_review_versions is not None:
            self._values["admission_review_versions"] = admission_review_versions
        if failure_policy is not None:
            self._values["failure_policy"] = failure_policy
        if match_policy is not None:
            self._values["match_policy"] = match_policy
        if namespace_selector is not None:
            self._values["namespace_selector"] = namespace_selector
        if object_selector is not None:
            self._values["object_selector"] = object_selector
        if reinvocation_policy is not None:
            self._values["reinvocation_policy"] = reinvocation_policy
        if rule is not None:
            self._values["rule"] = rule
        if side_effects is not None:
            self._values["side_effects"] = side_effects
        if timeout_seconds is not None:
            self._values["timeout_seconds"] = timeout_seconds

    @builtins.property
    def client_config(self) -> "MutatingWebhookConfigurationV1WebhookClientConfig":
        '''client_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#client_config MutatingWebhookConfigurationV1#client_config}
        '''
        result = self._values.get("client_config")
        assert result is not None, "Required property 'client_config' is missing"
        return typing.cast("MutatingWebhookConfigurationV1WebhookClientConfig", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the admission webhook.

        Name should be fully qualified, e.g., imagepolicy.kubernetes.io, where "imagepolicy" is the name of the webhook, and kubernetes.io is the name of the organization. Required.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#name MutatingWebhookConfigurationV1#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def admission_review_versions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''AdmissionReviewVersions is an ordered list of preferred ``AdmissionReview`` versions the Webhook expects.

        API server will try to use first version in the list which it supports. If none of the versions specified in this list supported by API server, validation will fail for this object. If a persisted webhook configuration specifies allowed versions and does not include any versions known to the API Server, calls to the webhook will fail and be subject to the failure policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#admission_review_versions MutatingWebhookConfigurationV1#admission_review_versions}
        '''
        result = self._values.get("admission_review_versions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def failure_policy(self) -> typing.Optional[builtins.str]:
        '''FailurePolicy defines how unrecognized errors from the admission endpoint are handled - allowed values are Ignore or Fail.

        Defaults to Fail.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#failure_policy MutatingWebhookConfigurationV1#failure_policy}
        '''
        result = self._values.get("failure_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def match_policy(self) -> typing.Optional[builtins.str]:
        '''matchPolicy defines how the "rules" list is used to match incoming requests. Allowed values are "Exact" or "Equivalent".

        - Exact: match a request only if it exactly matches a specified rule. For example, if deployments can be modified via apps/v1, apps/v1beta1, and extensions/v1beta1, but "rules" only included ``apiGroups:["apps"], apiVersions:["v1"], resources: ["deployments"]``, a request to apps/v1beta1 or extensions/v1beta1 would not be sent to the webhook.
        - Equivalent: match a request if modifies a resource listed in rules, even via another API group or version. For example, if deployments can be modified via apps/v1, apps/v1beta1, and extensions/v1beta1, and "rules" only included ``apiGroups:["apps"], apiVersions:["v1"], resources: ["deployments"]``, a request to apps/v1beta1 or extensions/v1beta1 would be converted to apps/v1 and sent to the webhook.

        Defaults to "Equivalent"

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#match_policy MutatingWebhookConfigurationV1#match_policy}
        '''
        result = self._values.get("match_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace_selector(
        self,
    ) -> typing.Optional["MutatingWebhookConfigurationV1WebhookNamespaceSelector"]:
        '''namespace_selector block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#namespace_selector MutatingWebhookConfigurationV1#namespace_selector}
        '''
        result = self._values.get("namespace_selector")
        return typing.cast(typing.Optional["MutatingWebhookConfigurationV1WebhookNamespaceSelector"], result)

    @builtins.property
    def object_selector(
        self,
    ) -> typing.Optional["MutatingWebhookConfigurationV1WebhookObjectSelector"]:
        '''object_selector block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#object_selector MutatingWebhookConfigurationV1#object_selector}
        '''
        result = self._values.get("object_selector")
        return typing.cast(typing.Optional["MutatingWebhookConfigurationV1WebhookObjectSelector"], result)

    @builtins.property
    def reinvocation_policy(self) -> typing.Optional[builtins.str]:
        '''reinvocationPolicy indicates whether this webhook should be called multiple times as part of a single admission evaluation.

        Allowed values are "Never" and "IfNeeded".

        Never: the webhook will not be called more than once in a single admission evaluation.

        IfNeeded: the webhook will be called at least one additional time as part of the admission evaluation if the object being admitted is modified by other admission plugins after the initial webhook call. Webhooks that specify this option *must* be idempotent, able to process objects they previously admitted. Note: * the number of additional invocations is not guaranteed to be exactly one. * if additional invocations result in further modifications to the object, webhooks are not guaranteed to be invoked again. * webhooks that use this option may be reordered to minimize the number of additional invocations. * to validate an object after all mutations are guaranteed complete, use a validating admission webhook instead.

        Defaults to "Never".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#reinvocation_policy MutatingWebhookConfigurationV1#reinvocation_policy}
        '''
        result = self._values.get("reinvocation_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MutatingWebhookConfigurationV1WebhookRule"]]]:
        '''rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#rule MutatingWebhookConfigurationV1#rule}
        '''
        result = self._values.get("rule")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MutatingWebhookConfigurationV1WebhookRule"]]], result)

    @builtins.property
    def side_effects(self) -> typing.Optional[builtins.str]:
        '''SideEffects states whether this webhook has side effects.

        Acceptable values are: None, NoneOnDryRun (webhooks created via v1beta1 may also specify Some or Unknown). Webhooks with side effects MUST implement a reconciliation system, since a request may be rejected by a future step in the admission chain and the side effects therefore need to be undone. Requests with the dryRun attribute will be auto-rejected if they match a webhook with sideEffects == Unknown or Some.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#side_effects MutatingWebhookConfigurationV1#side_effects}
        '''
        result = self._values.get("side_effects")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout_seconds(self) -> typing.Optional[jsii.Number]:
        '''TimeoutSeconds specifies the timeout for this webhook.

        After the timeout passes, the webhook call will be ignored or the API call will fail based on the failure policy. The timeout value must be between 1 and 30 seconds. Default to 10 seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#timeout_seconds MutatingWebhookConfigurationV1#timeout_seconds}
        '''
        result = self._values.get("timeout_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MutatingWebhookConfigurationV1Webhook(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-kubernetes.mutatingWebhookConfigurationV1.MutatingWebhookConfigurationV1WebhookClientConfig",
    jsii_struct_bases=[],
    name_mapping={"ca_bundle": "caBundle", "service": "service", "url": "url"},
)
class MutatingWebhookConfigurationV1WebhookClientConfig:
    def __init__(
        self,
        *,
        ca_bundle: typing.Optional[builtins.str] = None,
        service: typing.Optional[typing.Union["MutatingWebhookConfigurationV1WebhookClientConfigService", typing.Dict[builtins.str, typing.Any]]] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ca_bundle: ``caBundle`` is a PEM encoded CA bundle which will be used to validate the webhook's server certificate. If unspecified, system trust roots on the apiserver are used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#ca_bundle MutatingWebhookConfigurationV1#ca_bundle}
        :param service: service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#service MutatingWebhookConfigurationV1#service}
        :param url: ``url`` gives the location of the webhook, in standard URL form (``scheme://host:port/path``). Exactly one of ``url`` or ``service`` must be specified. The ``host`` should not refer to a service running in the cluster; use the ``service`` field instead. The host might be resolved via external DNS in some apiservers (e.g., ``kube-apiserver`` cannot resolve in-cluster DNS as that would be a layering violation). ``host`` may also be an IP address. Please note that using ``localhost`` or ``127.0.0.1`` as a ``host`` is risky unless you take great care to run this webhook on all hosts which run an apiserver which might need to make calls to this webhook. Such installs are likely to be non-portable, i.e., not easy to turn up in a new cluster. The scheme must be "https"; the URL must begin with "https://". A path is optional, and if present may be any string permissible in a URL. You may use the path to pass an arbitrary string to the webhook, for example, a cluster identifier. Attempting to use a user or basic auth e.g. "user:password@" is not allowed. Fragments ("#...") and query parameters ("?...") are not allowed, either. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#url MutatingWebhookConfigurationV1#url}
        '''
        if isinstance(service, dict):
            service = MutatingWebhookConfigurationV1WebhookClientConfigService(**service)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63c3e1987f1afa96b738a66f7defee0d4f27f099ae14ece7a12140383a040663)
            check_type(argname="argument ca_bundle", value=ca_bundle, expected_type=type_hints["ca_bundle"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ca_bundle is not None:
            self._values["ca_bundle"] = ca_bundle
        if service is not None:
            self._values["service"] = service
        if url is not None:
            self._values["url"] = url

    @builtins.property
    def ca_bundle(self) -> typing.Optional[builtins.str]:
        '''``caBundle`` is a PEM encoded CA bundle which will be used to validate the webhook's server certificate.

        If unspecified, system trust roots on the apiserver are used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#ca_bundle MutatingWebhookConfigurationV1#ca_bundle}
        '''
        result = self._values.get("ca_bundle")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service(
        self,
    ) -> typing.Optional["MutatingWebhookConfigurationV1WebhookClientConfigService"]:
        '''service block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#service MutatingWebhookConfigurationV1#service}
        '''
        result = self._values.get("service")
        return typing.cast(typing.Optional["MutatingWebhookConfigurationV1WebhookClientConfigService"], result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''``url`` gives the location of the webhook, in standard URL form (``scheme://host:port/path``).

        Exactly one of ``url`` or ``service`` must be specified.

        The ``host`` should not refer to a service running in the cluster; use the ``service`` field instead. The host might be resolved via external DNS in some apiservers (e.g., ``kube-apiserver`` cannot resolve in-cluster DNS as that would be a layering violation). ``host`` may also be an IP address.

        Please note that using ``localhost`` or ``127.0.0.1`` as a ``host`` is risky unless you take great care to run this webhook on all hosts which run an apiserver which might need to make calls to this webhook. Such installs are likely to be non-portable, i.e., not easy to turn up in a new cluster.

        The scheme must be "https"; the URL must begin with "https://".

        A path is optional, and if present may be any string permissible in a URL. You may use the path to pass an arbitrary string to the webhook, for example, a cluster identifier.

        Attempting to use a user or basic auth e.g. "user:password@" is not allowed. Fragments ("#...") and query parameters ("?...") are not allowed, either.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#url MutatingWebhookConfigurationV1#url}
        '''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MutatingWebhookConfigurationV1WebhookClientConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MutatingWebhookConfigurationV1WebhookClientConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-kubernetes.mutatingWebhookConfigurationV1.MutatingWebhookConfigurationV1WebhookClientConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c69f25621008c45a0b17a04de54b4903f2a6cf2f4f95ba67e7254e72612348d8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putService")
    def put_service(
        self,
        *,
        name: builtins.str,
        namespace: builtins.str,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param name: ``name`` is the name of the service. Required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#name MutatingWebhookConfigurationV1#name}
        :param namespace: ``namespace`` is the namespace of the service. Required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#namespace MutatingWebhookConfigurationV1#namespace}
        :param path: ``path`` is an optional URL path which will be sent in any request to this service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#path MutatingWebhookConfigurationV1#path}
        :param port: If specified, the port on the service that hosting webhook. Default to 443 for backward compatibility. ``port`` should be a valid port number (1-65535, inclusive). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#port MutatingWebhookConfigurationV1#port}
        '''
        value = MutatingWebhookConfigurationV1WebhookClientConfigService(
            name=name, namespace=namespace, path=path, port=port
        )

        return typing.cast(None, jsii.invoke(self, "putService", [value]))

    @jsii.member(jsii_name="resetCaBundle")
    def reset_ca_bundle(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCaBundle", []))

    @jsii.member(jsii_name="resetService")
    def reset_service(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetService", []))

    @jsii.member(jsii_name="resetUrl")
    def reset_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrl", []))

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(
        self,
    ) -> "MutatingWebhookConfigurationV1WebhookClientConfigServiceOutputReference":
        return typing.cast("MutatingWebhookConfigurationV1WebhookClientConfigServiceOutputReference", jsii.get(self, "service"))

    @builtins.property
    @jsii.member(jsii_name="caBundleInput")
    def ca_bundle_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "caBundleInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceInput")
    def service_input(
        self,
    ) -> typing.Optional["MutatingWebhookConfigurationV1WebhookClientConfigService"]:
        return typing.cast(typing.Optional["MutatingWebhookConfigurationV1WebhookClientConfigService"], jsii.get(self, "serviceInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="caBundle")
    def ca_bundle(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "caBundle"))

    @ca_bundle.setter
    def ca_bundle(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c093f887b35fca3db7730687d0aaaca92ff862af7264a77479cc01785abee34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "caBundle", value)

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d44ba3c8c9d54dee2f01b52b7a02b8d4073f47967d302527f4080a1cd5b2a240)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MutatingWebhookConfigurationV1WebhookClientConfig]:
        return typing.cast(typing.Optional[MutatingWebhookConfigurationV1WebhookClientConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MutatingWebhookConfigurationV1WebhookClientConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e4cc9342435d00d6c343a6c4214fb0e16d4b94d50df1d41fa9d0adb568c60ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-kubernetes.mutatingWebhookConfigurationV1.MutatingWebhookConfigurationV1WebhookClientConfigService",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "namespace": "namespace",
        "path": "path",
        "port": "port",
    },
)
class MutatingWebhookConfigurationV1WebhookClientConfigService:
    def __init__(
        self,
        *,
        name: builtins.str,
        namespace: builtins.str,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param name: ``name`` is the name of the service. Required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#name MutatingWebhookConfigurationV1#name}
        :param namespace: ``namespace`` is the namespace of the service. Required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#namespace MutatingWebhookConfigurationV1#namespace}
        :param path: ``path`` is an optional URL path which will be sent in any request to this service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#path MutatingWebhookConfigurationV1#path}
        :param port: If specified, the port on the service that hosting webhook. Default to 443 for backward compatibility. ``port`` should be a valid port number (1-65535, inclusive). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#port MutatingWebhookConfigurationV1#port}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc8e9f428acbcbdaeb98697d0fb6d58b14e156f25224cf20a1f95933e68b6a20)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "namespace": namespace,
        }
        if path is not None:
            self._values["path"] = path
        if port is not None:
            self._values["port"] = port

    @builtins.property
    def name(self) -> builtins.str:
        '''``name`` is the name of the service. Required.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#name MutatingWebhookConfigurationV1#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def namespace(self) -> builtins.str:
        '''``namespace`` is the namespace of the service. Required.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#namespace MutatingWebhookConfigurationV1#namespace}
        '''
        result = self._values.get("namespace")
        assert result is not None, "Required property 'namespace' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''``path`` is an optional URL path which will be sent in any request to this service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#path MutatingWebhookConfigurationV1#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''If specified, the port on the service that hosting webhook.

        Default to 443 for backward compatibility. ``port`` should be a valid port number (1-65535, inclusive).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#port MutatingWebhookConfigurationV1#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MutatingWebhookConfigurationV1WebhookClientConfigService(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MutatingWebhookConfigurationV1WebhookClientConfigServiceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-kubernetes.mutatingWebhookConfigurationV1.MutatingWebhookConfigurationV1WebhookClientConfigServiceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e26b3526037de348814fed6570199df36caa2855ff577a6c03a0abd18ae3d02)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="namespaceInput")
    def namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58246cb3335366d1078de9b6175abe60678a5f5a3b73ac061ea376bee8143906)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fd06761d7b182fdb8396d9c21f6c47d04b3843e927522787f88f8bad9328fce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value)

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfa8ed3df80e6ee4ed0b6500807bec749712b58062e32fb6b3e3618de102bf3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value)

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e22f1a5213f0a17e3d26c30921df1990bde506c19560d792e1fc164cac96298b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MutatingWebhookConfigurationV1WebhookClientConfigService]:
        return typing.cast(typing.Optional[MutatingWebhookConfigurationV1WebhookClientConfigService], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MutatingWebhookConfigurationV1WebhookClientConfigService],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f55191f88e25d7dc25e381025219b844a00b9858e232a2dbc4a5f9496a9d441)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class MutatingWebhookConfigurationV1WebhookList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-kubernetes.mutatingWebhookConfigurationV1.MutatingWebhookConfigurationV1WebhookList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e9e9050e9e99acabd5677dc6c21c84dfb5f5b437b32295e03d19a946267c8fa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MutatingWebhookConfigurationV1WebhookOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39591ee798b3ff26a5b8246a9de88210b187402edefad6f8726b41004a239b6f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MutatingWebhookConfigurationV1WebhookOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4edd509533dec474b170ed23066f0df58694f8148d52ab4573738b821ac54f08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8d3934764480b06632a9935233a239310cf42e87a34cc648d070c1e6091c837)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23e78305aa93723c16c5c8b6b2d418703b572259351d7f2e69cd379da60aa6d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MutatingWebhookConfigurationV1Webhook]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MutatingWebhookConfigurationV1Webhook]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MutatingWebhookConfigurationV1Webhook]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dc87791cb3e51ff21034f21716d9941161cf7e92b200bb49fc4f5679651eeea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-kubernetes.mutatingWebhookConfigurationV1.MutatingWebhookConfigurationV1WebhookNamespaceSelector",
    jsii_struct_bases=[],
    name_mapping={
        "match_expressions": "matchExpressions",
        "match_labels": "matchLabels",
    },
)
class MutatingWebhookConfigurationV1WebhookNamespaceSelector:
    def __init__(
        self,
        *,
        match_expressions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MutatingWebhookConfigurationV1WebhookNamespaceSelectorMatchExpressions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        match_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param match_expressions: match_expressions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#match_expressions MutatingWebhookConfigurationV1#match_expressions}
        :param match_labels: A map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of ``match_expressions``, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#match_labels MutatingWebhookConfigurationV1#match_labels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f91c373c376dd86cc01b4a1694b1acbe7aae8c3a8c8b656a9a2521f26fea252)
            check_type(argname="argument match_expressions", value=match_expressions, expected_type=type_hints["match_expressions"])
            check_type(argname="argument match_labels", value=match_labels, expected_type=type_hints["match_labels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if match_expressions is not None:
            self._values["match_expressions"] = match_expressions
        if match_labels is not None:
            self._values["match_labels"] = match_labels

    @builtins.property
    def match_expressions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MutatingWebhookConfigurationV1WebhookNamespaceSelectorMatchExpressions"]]]:
        '''match_expressions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#match_expressions MutatingWebhookConfigurationV1#match_expressions}
        '''
        result = self._values.get("match_expressions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MutatingWebhookConfigurationV1WebhookNamespaceSelectorMatchExpressions"]]], result)

    @builtins.property
    def match_labels(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of {key,value} pairs.

        A single {key,value} in the matchLabels map is equivalent to an element of ``match_expressions``, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#match_labels MutatingWebhookConfigurationV1#match_labels}
        '''
        result = self._values.get("match_labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MutatingWebhookConfigurationV1WebhookNamespaceSelector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-kubernetes.mutatingWebhookConfigurationV1.MutatingWebhookConfigurationV1WebhookNamespaceSelectorMatchExpressions",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "operator": "operator", "values": "values"},
)
class MutatingWebhookConfigurationV1WebhookNamespaceSelectorMatchExpressions:
    def __init__(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        operator: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param key: The label key that the selector applies to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#key MutatingWebhookConfigurationV1#key}
        :param operator: A key's relationship to a set of values. Valid operators ard ``In``, ``NotIn``, ``Exists`` and ``DoesNotExist``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#operator MutatingWebhookConfigurationV1#operator}
        :param values: An array of string values. If the operator is ``In`` or ``NotIn``, the values array must be non-empty. If the operator is ``Exists`` or ``DoesNotExist``, the values array must be empty. This array is replaced during a strategic merge patch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#values MutatingWebhookConfigurationV1#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__854cd027f562b89949a87091beef3e11c1062162020ac15df827ceb585170d6f)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if key is not None:
            self._values["key"] = key
        if operator is not None:
            self._values["operator"] = operator
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''The label key that the selector applies to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#key MutatingWebhookConfigurationV1#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def operator(self) -> typing.Optional[builtins.str]:
        '''A key's relationship to a set of values. Valid operators ard ``In``, ``NotIn``, ``Exists`` and ``DoesNotExist``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#operator MutatingWebhookConfigurationV1#operator}
        '''
        result = self._values.get("operator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of string values.

        If the operator is ``In`` or ``NotIn``, the values array must be non-empty. If the operator is ``Exists`` or ``DoesNotExist``, the values array must be empty. This array is replaced during a strategic merge patch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#values MutatingWebhookConfigurationV1#values}
        '''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MutatingWebhookConfigurationV1WebhookNamespaceSelectorMatchExpressions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MutatingWebhookConfigurationV1WebhookNamespaceSelectorMatchExpressionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-kubernetes.mutatingWebhookConfigurationV1.MutatingWebhookConfigurationV1WebhookNamespaceSelectorMatchExpressionsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7e658fda041e10cb9267cb083b1e9e0dbe8580b4f63cccf9c25e756a50a693c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MutatingWebhookConfigurationV1WebhookNamespaceSelectorMatchExpressionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35228c2f3aaf1217028ac33518024e2bc177ae09274973fd04163201a9674b21)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MutatingWebhookConfigurationV1WebhookNamespaceSelectorMatchExpressionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8743124684d8b119c8f4c7243312fad44a5439351f2e8d1b56afd60991d0f39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b0e0f581fe9b8fe73856b338d4cc9731d59b01cd7f57c9b6f35cff3c602db20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8229c169a48654a0cacc41938be4808014bef16bf801f4e268e55cd4f727d1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MutatingWebhookConfigurationV1WebhookNamespaceSelectorMatchExpressions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MutatingWebhookConfigurationV1WebhookNamespaceSelectorMatchExpressions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MutatingWebhookConfigurationV1WebhookNamespaceSelectorMatchExpressions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__141d73388bd581e538cffd6233ffd2458e77d5c84b7b3fd10e2ed27db0562b24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class MutatingWebhookConfigurationV1WebhookNamespaceSelectorMatchExpressionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-kubernetes.mutatingWebhookConfigurationV1.MutatingWebhookConfigurationV1WebhookNamespaceSelectorMatchExpressionsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53dc2546e2b9cfb939788fa6cd9ad6b06dbe4dd1c3860364a6321ad19d06bcc1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetOperator")
    def reset_operator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperator", []))

    @jsii.member(jsii_name="resetValues")
    def reset_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValues", []))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__161ac260e1682021bdcd32c5565ce12e4e58e892fdeba4182f9d80691093129e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e2ae97b761150bc23b2ab93f1fc01cde8aa9f806f8cc41130eda09d990c8d14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value)

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c21b984aedb2509a3ff7cafa0101a322a7d8a8c9a25e8fa0a2c2a3090c94dcf4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MutatingWebhookConfigurationV1WebhookNamespaceSelectorMatchExpressions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MutatingWebhookConfigurationV1WebhookNamespaceSelectorMatchExpressions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MutatingWebhookConfigurationV1WebhookNamespaceSelectorMatchExpressions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__800d75673a9ec5f0f32afbc5ebdf0b08b04146b875833662afead7c22804a417)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class MutatingWebhookConfigurationV1WebhookNamespaceSelectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-kubernetes.mutatingWebhookConfigurationV1.MutatingWebhookConfigurationV1WebhookNamespaceSelectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9458038c15e383ef8a5f78a50d7269d81020befdbcb2bbbfa6c16e0037fb19c3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMatchExpressions")
    def put_match_expressions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MutatingWebhookConfigurationV1WebhookNamespaceSelectorMatchExpressions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acce4a4f598559a5f5022e4217103bd7ab441aefdb7e873802c16ad815ff9c95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMatchExpressions", [value]))

    @jsii.member(jsii_name="resetMatchExpressions")
    def reset_match_expressions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchExpressions", []))

    @jsii.member(jsii_name="resetMatchLabels")
    def reset_match_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchLabels", []))

    @builtins.property
    @jsii.member(jsii_name="matchExpressions")
    def match_expressions(
        self,
    ) -> MutatingWebhookConfigurationV1WebhookNamespaceSelectorMatchExpressionsList:
        return typing.cast(MutatingWebhookConfigurationV1WebhookNamespaceSelectorMatchExpressionsList, jsii.get(self, "matchExpressions"))

    @builtins.property
    @jsii.member(jsii_name="matchExpressionsInput")
    def match_expressions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MutatingWebhookConfigurationV1WebhookNamespaceSelectorMatchExpressions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MutatingWebhookConfigurationV1WebhookNamespaceSelectorMatchExpressions]]], jsii.get(self, "matchExpressionsInput"))

    @builtins.property
    @jsii.member(jsii_name="matchLabelsInput")
    def match_labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "matchLabelsInput"))

    @builtins.property
    @jsii.member(jsii_name="matchLabels")
    def match_labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "matchLabels"))

    @match_labels.setter
    def match_labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eab483c2bdbaa83f71caebdeb1357d2333ce0771a400280f95ccff05fcd2a0e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchLabels", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MutatingWebhookConfigurationV1WebhookNamespaceSelector]:
        return typing.cast(typing.Optional[MutatingWebhookConfigurationV1WebhookNamespaceSelector], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MutatingWebhookConfigurationV1WebhookNamespaceSelector],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36261d59a2f86f58374e612473990e9a4b799190cc2a2335ffe3b4fe9cb300e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-kubernetes.mutatingWebhookConfigurationV1.MutatingWebhookConfigurationV1WebhookObjectSelector",
    jsii_struct_bases=[],
    name_mapping={
        "match_expressions": "matchExpressions",
        "match_labels": "matchLabels",
    },
)
class MutatingWebhookConfigurationV1WebhookObjectSelector:
    def __init__(
        self,
        *,
        match_expressions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MutatingWebhookConfigurationV1WebhookObjectSelectorMatchExpressions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        match_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param match_expressions: match_expressions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#match_expressions MutatingWebhookConfigurationV1#match_expressions}
        :param match_labels: A map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of ``match_expressions``, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#match_labels MutatingWebhookConfigurationV1#match_labels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f7989f8e10e99f81f7c25a4054136c07d9d1f5717c6056cf4881bf2f5e2cc60)
            check_type(argname="argument match_expressions", value=match_expressions, expected_type=type_hints["match_expressions"])
            check_type(argname="argument match_labels", value=match_labels, expected_type=type_hints["match_labels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if match_expressions is not None:
            self._values["match_expressions"] = match_expressions
        if match_labels is not None:
            self._values["match_labels"] = match_labels

    @builtins.property
    def match_expressions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MutatingWebhookConfigurationV1WebhookObjectSelectorMatchExpressions"]]]:
        '''match_expressions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#match_expressions MutatingWebhookConfigurationV1#match_expressions}
        '''
        result = self._values.get("match_expressions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MutatingWebhookConfigurationV1WebhookObjectSelectorMatchExpressions"]]], result)

    @builtins.property
    def match_labels(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of {key,value} pairs.

        A single {key,value} in the matchLabels map is equivalent to an element of ``match_expressions``, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#match_labels MutatingWebhookConfigurationV1#match_labels}
        '''
        result = self._values.get("match_labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MutatingWebhookConfigurationV1WebhookObjectSelector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-kubernetes.mutatingWebhookConfigurationV1.MutatingWebhookConfigurationV1WebhookObjectSelectorMatchExpressions",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "operator": "operator", "values": "values"},
)
class MutatingWebhookConfigurationV1WebhookObjectSelectorMatchExpressions:
    def __init__(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        operator: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param key: The label key that the selector applies to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#key MutatingWebhookConfigurationV1#key}
        :param operator: A key's relationship to a set of values. Valid operators ard ``In``, ``NotIn``, ``Exists`` and ``DoesNotExist``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#operator MutatingWebhookConfigurationV1#operator}
        :param values: An array of string values. If the operator is ``In`` or ``NotIn``, the values array must be non-empty. If the operator is ``Exists`` or ``DoesNotExist``, the values array must be empty. This array is replaced during a strategic merge patch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#values MutatingWebhookConfigurationV1#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4a7be3ece4ebf0738acaf8a544a8f5b836c76884335d4b25440ee3db48a031d)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if key is not None:
            self._values["key"] = key
        if operator is not None:
            self._values["operator"] = operator
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''The label key that the selector applies to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#key MutatingWebhookConfigurationV1#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def operator(self) -> typing.Optional[builtins.str]:
        '''A key's relationship to a set of values. Valid operators ard ``In``, ``NotIn``, ``Exists`` and ``DoesNotExist``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#operator MutatingWebhookConfigurationV1#operator}
        '''
        result = self._values.get("operator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of string values.

        If the operator is ``In`` or ``NotIn``, the values array must be non-empty. If the operator is ``Exists`` or ``DoesNotExist``, the values array must be empty. This array is replaced during a strategic merge patch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#values MutatingWebhookConfigurationV1#values}
        '''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MutatingWebhookConfigurationV1WebhookObjectSelectorMatchExpressions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MutatingWebhookConfigurationV1WebhookObjectSelectorMatchExpressionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-kubernetes.mutatingWebhookConfigurationV1.MutatingWebhookConfigurationV1WebhookObjectSelectorMatchExpressionsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b5082828249c0586629a093789ba541c88939dd598007f035829fb78ef1dea8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MutatingWebhookConfigurationV1WebhookObjectSelectorMatchExpressionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5c911e6194b88f974c7f7217fe10ae3fda4572f499e7e2a832c3613f87bef0c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MutatingWebhookConfigurationV1WebhookObjectSelectorMatchExpressionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__437b9a23e3c016f2a30f58fae6b9e6e7232daeea70ceb7c83b5600a3e50f60a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e08ec9aa4db9169b125e419f40043e8ee465c79a4f2dd21370ca3fe1cba7fab3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ad95b57a413a0d0719ae124d831a7215b7c0b3c5df53e17208254d3b2ee0063)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MutatingWebhookConfigurationV1WebhookObjectSelectorMatchExpressions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MutatingWebhookConfigurationV1WebhookObjectSelectorMatchExpressions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MutatingWebhookConfigurationV1WebhookObjectSelectorMatchExpressions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed8989ecfb3e0f8d33e428a4cbb082726248741407117ea90c2878eedcf456bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class MutatingWebhookConfigurationV1WebhookObjectSelectorMatchExpressionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-kubernetes.mutatingWebhookConfigurationV1.MutatingWebhookConfigurationV1WebhookObjectSelectorMatchExpressionsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d70c78bddf9b66dd27b758a9f065404b9ede1a7d7b6098af0b41663de2d6cea)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetOperator")
    def reset_operator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperator", []))

    @jsii.member(jsii_name="resetValues")
    def reset_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValues", []))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd95fcfdab97dfaae39222493839191fdeb7dc8ecbe1919cb61b1d1b48a49e7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9d894a848a30d366de623f7f2d405e38a57a73872cdf19f3e6ee26b86002f2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value)

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b98397315ae5e455002d63af3900717692b79108cbb2bd2ea16ac4ff79ac807)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MutatingWebhookConfigurationV1WebhookObjectSelectorMatchExpressions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MutatingWebhookConfigurationV1WebhookObjectSelectorMatchExpressions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MutatingWebhookConfigurationV1WebhookObjectSelectorMatchExpressions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b21e60a528d9cce8e2ef1341aba6ce67acb4c2933e3cfd8b6ef2956d658c452f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class MutatingWebhookConfigurationV1WebhookObjectSelectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-kubernetes.mutatingWebhookConfigurationV1.MutatingWebhookConfigurationV1WebhookObjectSelectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aaf775b4a2d9e19fce0e016d3f4f97df773bd577ab849ae05f3088f2a443039a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMatchExpressions")
    def put_match_expressions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MutatingWebhookConfigurationV1WebhookObjectSelectorMatchExpressions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ceed8dbd249bfe9fc82c430ac09eac9ad676f4292fe7a2ba9d0ae60efa7523e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMatchExpressions", [value]))

    @jsii.member(jsii_name="resetMatchExpressions")
    def reset_match_expressions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchExpressions", []))

    @jsii.member(jsii_name="resetMatchLabels")
    def reset_match_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchLabels", []))

    @builtins.property
    @jsii.member(jsii_name="matchExpressions")
    def match_expressions(
        self,
    ) -> MutatingWebhookConfigurationV1WebhookObjectSelectorMatchExpressionsList:
        return typing.cast(MutatingWebhookConfigurationV1WebhookObjectSelectorMatchExpressionsList, jsii.get(self, "matchExpressions"))

    @builtins.property
    @jsii.member(jsii_name="matchExpressionsInput")
    def match_expressions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MutatingWebhookConfigurationV1WebhookObjectSelectorMatchExpressions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MutatingWebhookConfigurationV1WebhookObjectSelectorMatchExpressions]]], jsii.get(self, "matchExpressionsInput"))

    @builtins.property
    @jsii.member(jsii_name="matchLabelsInput")
    def match_labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "matchLabelsInput"))

    @builtins.property
    @jsii.member(jsii_name="matchLabels")
    def match_labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "matchLabels"))

    @match_labels.setter
    def match_labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__509d5caeb1e674dffa7a99c8b91e989672d147b280d9f60036fbc44308363fea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchLabels", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MutatingWebhookConfigurationV1WebhookObjectSelector]:
        return typing.cast(typing.Optional[MutatingWebhookConfigurationV1WebhookObjectSelector], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MutatingWebhookConfigurationV1WebhookObjectSelector],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31e10c989d7c26f4475dcbbd773bbbd9d97e222af517f3f79d81c022d4085628)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class MutatingWebhookConfigurationV1WebhookOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-kubernetes.mutatingWebhookConfigurationV1.MutatingWebhookConfigurationV1WebhookOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3673b37ad9ee1e3c48baa0036a06ededc27e94299c50430f8455209231825b5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putClientConfig")
    def put_client_config(
        self,
        *,
        ca_bundle: typing.Optional[builtins.str] = None,
        service: typing.Optional[typing.Union[MutatingWebhookConfigurationV1WebhookClientConfigService, typing.Dict[builtins.str, typing.Any]]] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ca_bundle: ``caBundle`` is a PEM encoded CA bundle which will be used to validate the webhook's server certificate. If unspecified, system trust roots on the apiserver are used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#ca_bundle MutatingWebhookConfigurationV1#ca_bundle}
        :param service: service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#service MutatingWebhookConfigurationV1#service}
        :param url: ``url`` gives the location of the webhook, in standard URL form (``scheme://host:port/path``). Exactly one of ``url`` or ``service`` must be specified. The ``host`` should not refer to a service running in the cluster; use the ``service`` field instead. The host might be resolved via external DNS in some apiservers (e.g., ``kube-apiserver`` cannot resolve in-cluster DNS as that would be a layering violation). ``host`` may also be an IP address. Please note that using ``localhost`` or ``127.0.0.1`` as a ``host`` is risky unless you take great care to run this webhook on all hosts which run an apiserver which might need to make calls to this webhook. Such installs are likely to be non-portable, i.e., not easy to turn up in a new cluster. The scheme must be "https"; the URL must begin with "https://". A path is optional, and if present may be any string permissible in a URL. You may use the path to pass an arbitrary string to the webhook, for example, a cluster identifier. Attempting to use a user or basic auth e.g. "user:password@" is not allowed. Fragments ("#...") and query parameters ("?...") are not allowed, either. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#url MutatingWebhookConfigurationV1#url}
        '''
        value = MutatingWebhookConfigurationV1WebhookClientConfig(
            ca_bundle=ca_bundle, service=service, url=url
        )

        return typing.cast(None, jsii.invoke(self, "putClientConfig", [value]))

    @jsii.member(jsii_name="putNamespaceSelector")
    def put_namespace_selector(
        self,
        *,
        match_expressions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MutatingWebhookConfigurationV1WebhookNamespaceSelectorMatchExpressions, typing.Dict[builtins.str, typing.Any]]]]] = None,
        match_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param match_expressions: match_expressions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#match_expressions MutatingWebhookConfigurationV1#match_expressions}
        :param match_labels: A map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of ``match_expressions``, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#match_labels MutatingWebhookConfigurationV1#match_labels}
        '''
        value = MutatingWebhookConfigurationV1WebhookNamespaceSelector(
            match_expressions=match_expressions, match_labels=match_labels
        )

        return typing.cast(None, jsii.invoke(self, "putNamespaceSelector", [value]))

    @jsii.member(jsii_name="putObjectSelector")
    def put_object_selector(
        self,
        *,
        match_expressions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MutatingWebhookConfigurationV1WebhookObjectSelectorMatchExpressions, typing.Dict[builtins.str, typing.Any]]]]] = None,
        match_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param match_expressions: match_expressions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#match_expressions MutatingWebhookConfigurationV1#match_expressions}
        :param match_labels: A map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of ``match_expressions``, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#match_labels MutatingWebhookConfigurationV1#match_labels}
        '''
        value = MutatingWebhookConfigurationV1WebhookObjectSelector(
            match_expressions=match_expressions, match_labels=match_labels
        )

        return typing.cast(None, jsii.invoke(self, "putObjectSelector", [value]))

    @jsii.member(jsii_name="putRule")
    def put_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MutatingWebhookConfigurationV1WebhookRule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efdf65bdd5011de3397cd95d7c75a553f85b7646a7ec4041eae914305b0fed95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRule", [value]))

    @jsii.member(jsii_name="resetAdmissionReviewVersions")
    def reset_admission_review_versions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdmissionReviewVersions", []))

    @jsii.member(jsii_name="resetFailurePolicy")
    def reset_failure_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailurePolicy", []))

    @jsii.member(jsii_name="resetMatchPolicy")
    def reset_match_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchPolicy", []))

    @jsii.member(jsii_name="resetNamespaceSelector")
    def reset_namespace_selector(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamespaceSelector", []))

    @jsii.member(jsii_name="resetObjectSelector")
    def reset_object_selector(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetObjectSelector", []))

    @jsii.member(jsii_name="resetReinvocationPolicy")
    def reset_reinvocation_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReinvocationPolicy", []))

    @jsii.member(jsii_name="resetRule")
    def reset_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRule", []))

    @jsii.member(jsii_name="resetSideEffects")
    def reset_side_effects(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSideEffects", []))

    @jsii.member(jsii_name="resetTimeoutSeconds")
    def reset_timeout_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeoutSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="clientConfig")
    def client_config(
        self,
    ) -> MutatingWebhookConfigurationV1WebhookClientConfigOutputReference:
        return typing.cast(MutatingWebhookConfigurationV1WebhookClientConfigOutputReference, jsii.get(self, "clientConfig"))

    @builtins.property
    @jsii.member(jsii_name="namespaceSelector")
    def namespace_selector(
        self,
    ) -> MutatingWebhookConfigurationV1WebhookNamespaceSelectorOutputReference:
        return typing.cast(MutatingWebhookConfigurationV1WebhookNamespaceSelectorOutputReference, jsii.get(self, "namespaceSelector"))

    @builtins.property
    @jsii.member(jsii_name="objectSelector")
    def object_selector(
        self,
    ) -> MutatingWebhookConfigurationV1WebhookObjectSelectorOutputReference:
        return typing.cast(MutatingWebhookConfigurationV1WebhookObjectSelectorOutputReference, jsii.get(self, "objectSelector"))

    @builtins.property
    @jsii.member(jsii_name="rule")
    def rule(self) -> "MutatingWebhookConfigurationV1WebhookRuleList":
        return typing.cast("MutatingWebhookConfigurationV1WebhookRuleList", jsii.get(self, "rule"))

    @builtins.property
    @jsii.member(jsii_name="admissionReviewVersionsInput")
    def admission_review_versions_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "admissionReviewVersionsInput"))

    @builtins.property
    @jsii.member(jsii_name="clientConfigInput")
    def client_config_input(
        self,
    ) -> typing.Optional[MutatingWebhookConfigurationV1WebhookClientConfig]:
        return typing.cast(typing.Optional[MutatingWebhookConfigurationV1WebhookClientConfig], jsii.get(self, "clientConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="failurePolicyInput")
    def failure_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "failurePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="matchPolicyInput")
    def match_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "matchPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="namespaceSelectorInput")
    def namespace_selector_input(
        self,
    ) -> typing.Optional[MutatingWebhookConfigurationV1WebhookNamespaceSelector]:
        return typing.cast(typing.Optional[MutatingWebhookConfigurationV1WebhookNamespaceSelector], jsii.get(self, "namespaceSelectorInput"))

    @builtins.property
    @jsii.member(jsii_name="objectSelectorInput")
    def object_selector_input(
        self,
    ) -> typing.Optional[MutatingWebhookConfigurationV1WebhookObjectSelector]:
        return typing.cast(typing.Optional[MutatingWebhookConfigurationV1WebhookObjectSelector], jsii.get(self, "objectSelectorInput"))

    @builtins.property
    @jsii.member(jsii_name="reinvocationPolicyInput")
    def reinvocation_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "reinvocationPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleInput")
    def rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MutatingWebhookConfigurationV1WebhookRule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MutatingWebhookConfigurationV1WebhookRule"]]], jsii.get(self, "ruleInput"))

    @builtins.property
    @jsii.member(jsii_name="sideEffectsInput")
    def side_effects_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sideEffectsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutSecondsInput")
    def timeout_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="admissionReviewVersions")
    def admission_review_versions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "admissionReviewVersions"))

    @admission_review_versions.setter
    def admission_review_versions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0238b8e583cb225882a3e132f67be1dcf670ef063f5b841a2f960d2034b509f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "admissionReviewVersions", value)

    @builtins.property
    @jsii.member(jsii_name="failurePolicy")
    def failure_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "failurePolicy"))

    @failure_policy.setter
    def failure_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46c579cdeeb27080f377db03c4dd39de73128013bc46bd652afa16cb2d8df3e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failurePolicy", value)

    @builtins.property
    @jsii.member(jsii_name="matchPolicy")
    def match_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "matchPolicy"))

    @match_policy.setter
    def match_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fde5dbeb06c942225cac2e1b7be18603f21018648951c740c8f96d457da73ee4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aeedf2835c87c74ff464097e35f30caadacf423fc8f2227d74f62002353e8585)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="reinvocationPolicy")
    def reinvocation_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reinvocationPolicy"))

    @reinvocation_policy.setter
    def reinvocation_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__356149677b9b9ad2adad66eb8c32ffceac35cb156603ba644cb599c0f5957126)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reinvocationPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="sideEffects")
    def side_effects(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sideEffects"))

    @side_effects.setter
    def side_effects(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba1b429ec96360d259b125e8409525df48afe0a8a49f6f2cec7b88c0c0596a22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sideEffects", value)

    @builtins.property
    @jsii.member(jsii_name="timeoutSeconds")
    def timeout_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutSeconds"))

    @timeout_seconds.setter
    def timeout_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__287f6e5fa3fdab10ebcedd55e2eb62c51bf882f26dc9c3c7134740331f11de4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MutatingWebhookConfigurationV1Webhook]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MutatingWebhookConfigurationV1Webhook]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MutatingWebhookConfigurationV1Webhook]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__205391cc2a5a4029cc0ea3c1514f07432c9c086fdb76815e22f6cc0c2ce0399a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-kubernetes.mutatingWebhookConfigurationV1.MutatingWebhookConfigurationV1WebhookRule",
    jsii_struct_bases=[],
    name_mapping={
        "api_groups": "apiGroups",
        "api_versions": "apiVersions",
        "operations": "operations",
        "resources": "resources",
        "scope": "scope",
    },
)
class MutatingWebhookConfigurationV1WebhookRule:
    def __init__(
        self,
        *,
        api_groups: typing.Sequence[builtins.str],
        api_versions: typing.Sequence[builtins.str],
        operations: typing.Sequence[builtins.str],
        resources: typing.Sequence[builtins.str],
        scope: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param api_groups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#api_groups MutatingWebhookConfigurationV1#api_groups}.
        :param api_versions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#api_versions MutatingWebhookConfigurationV1#api_versions}.
        :param operations: Operations is the operations the admission hook cares about - CREATE, UPDATE, DELETE, CONNECT or * for all of those operations and any future admission operations that are added. If '*' is present, the length of the slice must be one. Required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#operations MutatingWebhookConfigurationV1#operations}
        :param resources: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#resources MutatingWebhookConfigurationV1#resources}.
        :param scope: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#scope MutatingWebhookConfigurationV1#scope}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ca8eb292ea73444b4e5629de55601b22d6d73e95be3b7db570388df769e50f6)
            check_type(argname="argument api_groups", value=api_groups, expected_type=type_hints["api_groups"])
            check_type(argname="argument api_versions", value=api_versions, expected_type=type_hints["api_versions"])
            check_type(argname="argument operations", value=operations, expected_type=type_hints["operations"])
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_groups": api_groups,
            "api_versions": api_versions,
            "operations": operations,
            "resources": resources,
        }
        if scope is not None:
            self._values["scope"] = scope

    @builtins.property
    def api_groups(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#api_groups MutatingWebhookConfigurationV1#api_groups}.'''
        result = self._values.get("api_groups")
        assert result is not None, "Required property 'api_groups' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def api_versions(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#api_versions MutatingWebhookConfigurationV1#api_versions}.'''
        result = self._values.get("api_versions")
        assert result is not None, "Required property 'api_versions' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def operations(self) -> typing.List[builtins.str]:
        '''Operations is the operations the admission hook cares about - CREATE, UPDATE, DELETE, CONNECT or * for all of those operations and any future admission operations that are added.

        If '*' is present, the length of the slice must be one. Required.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#operations MutatingWebhookConfigurationV1#operations}
        '''
        result = self._values.get("operations")
        assert result is not None, "Required property 'operations' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def resources(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#resources MutatingWebhookConfigurationV1#resources}.'''
        result = self._values.get("resources")
        assert result is not None, "Required property 'resources' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def scope(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/kubernetes/2.28.1/docs/resources/mutating_webhook_configuration_v1#scope MutatingWebhookConfigurationV1#scope}.'''
        result = self._values.get("scope")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MutatingWebhookConfigurationV1WebhookRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MutatingWebhookConfigurationV1WebhookRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-kubernetes.mutatingWebhookConfigurationV1.MutatingWebhookConfigurationV1WebhookRuleList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18f992920885b9498979008f62de9b1ca8aaf75c39217b3f78906de370ad2d8d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MutatingWebhookConfigurationV1WebhookRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc904b894e9491981f6c3fbd4376732f8bfe8626c0ee2c6210bd23e7e401e05a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MutatingWebhookConfigurationV1WebhookRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__738cf369bb3118af157e1c903cbdb3f022ce03dcbec158babf5b3e5f4acf9f47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e225a486cb52d77ab6887b00d6a71ccb04f362e97f8cb33919834185ffe094b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fcee2f2a7c44e6d4dc91c28d9ab0da3c700f6dfbc1eb8d225627f5c334ae826)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MutatingWebhookConfigurationV1WebhookRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MutatingWebhookConfigurationV1WebhookRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MutatingWebhookConfigurationV1WebhookRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22f969307d3609656c7cb97959052707e93cc2c843bd97cfa075512f20e4c08a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class MutatingWebhookConfigurationV1WebhookRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-kubernetes.mutatingWebhookConfigurationV1.MutatingWebhookConfigurationV1WebhookRuleOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d45248734bffc2bc7f4922b9885885bc542afc036fb8f450b8f678a062067a29)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetScope")
    def reset_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScope", []))

    @builtins.property
    @jsii.member(jsii_name="apiGroupsInput")
    def api_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "apiGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="apiVersionsInput")
    def api_versions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "apiVersionsInput"))

    @builtins.property
    @jsii.member(jsii_name="operationsInput")
    def operations_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "operationsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourcesInput")
    def resources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="scopeInput")
    def scope_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeInput"))

    @builtins.property
    @jsii.member(jsii_name="apiGroups")
    def api_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "apiGroups"))

    @api_groups.setter
    def api_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3838633e20fa5e1829987578895725ee9c22066a773c765e5d49e4f3b587dbe9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiGroups", value)

    @builtins.property
    @jsii.member(jsii_name="apiVersions")
    def api_versions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "apiVersions"))

    @api_versions.setter
    def api_versions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa1f3ccd05121a468dbea41294c566c53376304c2ee047a3a4304e1c02bb8fec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiVersions", value)

    @builtins.property
    @jsii.member(jsii_name="operations")
    def operations(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "operations"))

    @operations.setter
    def operations(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bf746c54cd1618b590207bf084ad8420d40987a9f10dadc2b2471f7728a2d15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operations", value)

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resources"))

    @resources.setter
    def resources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__566ba82f6eab8d14bd730247620b6d32bc8c2a3dab83fe03a133096b6601db3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resources", value)

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scope"))

    @scope.setter
    def scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9b77eaf34e5aaef1ff176d73242992c4464c7b14f5022837271fa5626a7b9f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MutatingWebhookConfigurationV1WebhookRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MutatingWebhookConfigurationV1WebhookRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MutatingWebhookConfigurationV1WebhookRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2f7d9a5c7c2e1762611623be7d8a7877e32682384da81743edae6c2244d4ea4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "MutatingWebhookConfigurationV1",
    "MutatingWebhookConfigurationV1Config",
    "MutatingWebhookConfigurationV1Metadata",
    "MutatingWebhookConfigurationV1MetadataOutputReference",
    "MutatingWebhookConfigurationV1Webhook",
    "MutatingWebhookConfigurationV1WebhookClientConfig",
    "MutatingWebhookConfigurationV1WebhookClientConfigOutputReference",
    "MutatingWebhookConfigurationV1WebhookClientConfigService",
    "MutatingWebhookConfigurationV1WebhookClientConfigServiceOutputReference",
    "MutatingWebhookConfigurationV1WebhookList",
    "MutatingWebhookConfigurationV1WebhookNamespaceSelector",
    "MutatingWebhookConfigurationV1WebhookNamespaceSelectorMatchExpressions",
    "MutatingWebhookConfigurationV1WebhookNamespaceSelectorMatchExpressionsList",
    "MutatingWebhookConfigurationV1WebhookNamespaceSelectorMatchExpressionsOutputReference",
    "MutatingWebhookConfigurationV1WebhookNamespaceSelectorOutputReference",
    "MutatingWebhookConfigurationV1WebhookObjectSelector",
    "MutatingWebhookConfigurationV1WebhookObjectSelectorMatchExpressions",
    "MutatingWebhookConfigurationV1WebhookObjectSelectorMatchExpressionsList",
    "MutatingWebhookConfigurationV1WebhookObjectSelectorMatchExpressionsOutputReference",
    "MutatingWebhookConfigurationV1WebhookObjectSelectorOutputReference",
    "MutatingWebhookConfigurationV1WebhookOutputReference",
    "MutatingWebhookConfigurationV1WebhookRule",
    "MutatingWebhookConfigurationV1WebhookRuleList",
    "MutatingWebhookConfigurationV1WebhookRuleOutputReference",
]

publication.publish()

def _typecheckingstub__8aefc9e02ad1b07bfdd07e7475c174c888f288313db6538cfe72533c1434a386(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    metadata: typing.Union[MutatingWebhookConfigurationV1Metadata, typing.Dict[builtins.str, typing.Any]],
    webhook: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MutatingWebhookConfigurationV1Webhook, typing.Dict[builtins.str, typing.Any]]]],
    id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__630496ce038b7cbfda9ef5d1d9c845c207b47510c8e7775e0f543aec3c2417cf(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01f9ead77d2c011f66ecbf59fc95fc2940ec4878c105df5b8fa6b22d294892f5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MutatingWebhookConfigurationV1Webhook, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bda02b4997f14f3f4ff88fb723c4deb6a22c13a7e7f744f7665eeefbfb91f606(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36189b2242e62f7bea18c1c088cfcd196b22663cf5301ed59466c62ebb18ccfe(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    metadata: typing.Union[MutatingWebhookConfigurationV1Metadata, typing.Dict[builtins.str, typing.Any]],
    webhook: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MutatingWebhookConfigurationV1Webhook, typing.Dict[builtins.str, typing.Any]]]],
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa1d4be776e728f2403df06945c3507c5ad93d29c57abbd8390b74b545c7e758(
    *,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    generate_name: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a10c5bcb502fdb672db9e2c1ce91ade42ea615de4c967e8662a6cd4c28b8a2ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81e011669a711f712b50450827742b0e1b74a064cb36824b568803c47d4c7e9a(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af82a471cdb21e595de789b96bd1e81c3c40512dba384be9bc30ab1e59d005e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e81c2aa8fa5f7e892f58b7ca9f799dc7bfb3be2394f01e578426a90f526bb29(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30087be18246e7158aa34ca2e7d40e486e3cc21b5f31e65c34dcb0766a28dc3e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49bfcc67c37416bdae47d69b4d73f9a1b7b288c94acab176942cfadcc94c1555(
    value: typing.Optional[MutatingWebhookConfigurationV1Metadata],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f542d99e73ccf049496dd70e9b1b1b425c36ba2451073c99df3ab242dabbfbc(
    *,
    client_config: typing.Union[MutatingWebhookConfigurationV1WebhookClientConfig, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    admission_review_versions: typing.Optional[typing.Sequence[builtins.str]] = None,
    failure_policy: typing.Optional[builtins.str] = None,
    match_policy: typing.Optional[builtins.str] = None,
    namespace_selector: typing.Optional[typing.Union[MutatingWebhookConfigurationV1WebhookNamespaceSelector, typing.Dict[builtins.str, typing.Any]]] = None,
    object_selector: typing.Optional[typing.Union[MutatingWebhookConfigurationV1WebhookObjectSelector, typing.Dict[builtins.str, typing.Any]]] = None,
    reinvocation_policy: typing.Optional[builtins.str] = None,
    rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MutatingWebhookConfigurationV1WebhookRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
    side_effects: typing.Optional[builtins.str] = None,
    timeout_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63c3e1987f1afa96b738a66f7defee0d4f27f099ae14ece7a12140383a040663(
    *,
    ca_bundle: typing.Optional[builtins.str] = None,
    service: typing.Optional[typing.Union[MutatingWebhookConfigurationV1WebhookClientConfigService, typing.Dict[builtins.str, typing.Any]]] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c69f25621008c45a0b17a04de54b4903f2a6cf2f4f95ba67e7254e72612348d8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c093f887b35fca3db7730687d0aaaca92ff862af7264a77479cc01785abee34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d44ba3c8c9d54dee2f01b52b7a02b8d4073f47967d302527f4080a1cd5b2a240(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e4cc9342435d00d6c343a6c4214fb0e16d4b94d50df1d41fa9d0adb568c60ef(
    value: typing.Optional[MutatingWebhookConfigurationV1WebhookClientConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc8e9f428acbcbdaeb98697d0fb6d58b14e156f25224cf20a1f95933e68b6a20(
    *,
    name: builtins.str,
    namespace: builtins.str,
    path: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e26b3526037de348814fed6570199df36caa2855ff577a6c03a0abd18ae3d02(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58246cb3335366d1078de9b6175abe60678a5f5a3b73ac061ea376bee8143906(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fd06761d7b182fdb8396d9c21f6c47d04b3843e927522787f88f8bad9328fce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfa8ed3df80e6ee4ed0b6500807bec749712b58062e32fb6b3e3618de102bf3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e22f1a5213f0a17e3d26c30921df1990bde506c19560d792e1fc164cac96298b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f55191f88e25d7dc25e381025219b844a00b9858e232a2dbc4a5f9496a9d441(
    value: typing.Optional[MutatingWebhookConfigurationV1WebhookClientConfigService],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e9e9050e9e99acabd5677dc6c21c84dfb5f5b437b32295e03d19a946267c8fa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39591ee798b3ff26a5b8246a9de88210b187402edefad6f8726b41004a239b6f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4edd509533dec474b170ed23066f0df58694f8148d52ab4573738b821ac54f08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8d3934764480b06632a9935233a239310cf42e87a34cc648d070c1e6091c837(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23e78305aa93723c16c5c8b6b2d418703b572259351d7f2e69cd379da60aa6d7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dc87791cb3e51ff21034f21716d9941161cf7e92b200bb49fc4f5679651eeea(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MutatingWebhookConfigurationV1Webhook]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f91c373c376dd86cc01b4a1694b1acbe7aae8c3a8c8b656a9a2521f26fea252(
    *,
    match_expressions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MutatingWebhookConfigurationV1WebhookNamespaceSelectorMatchExpressions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    match_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__854cd027f562b89949a87091beef3e11c1062162020ac15df827ceb585170d6f(
    *,
    key: typing.Optional[builtins.str] = None,
    operator: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7e658fda041e10cb9267cb083b1e9e0dbe8580b4f63cccf9c25e756a50a693c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35228c2f3aaf1217028ac33518024e2bc177ae09274973fd04163201a9674b21(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8743124684d8b119c8f4c7243312fad44a5439351f2e8d1b56afd60991d0f39(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b0e0f581fe9b8fe73856b338d4cc9731d59b01cd7f57c9b6f35cff3c602db20(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8229c169a48654a0cacc41938be4808014bef16bf801f4e268e55cd4f727d1e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__141d73388bd581e538cffd6233ffd2458e77d5c84b7b3fd10e2ed27db0562b24(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MutatingWebhookConfigurationV1WebhookNamespaceSelectorMatchExpressions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53dc2546e2b9cfb939788fa6cd9ad6b06dbe4dd1c3860364a6321ad19d06bcc1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__161ac260e1682021bdcd32c5565ce12e4e58e892fdeba4182f9d80691093129e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e2ae97b761150bc23b2ab93f1fc01cde8aa9f806f8cc41130eda09d990c8d14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c21b984aedb2509a3ff7cafa0101a322a7d8a8c9a25e8fa0a2c2a3090c94dcf4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__800d75673a9ec5f0f32afbc5ebdf0b08b04146b875833662afead7c22804a417(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MutatingWebhookConfigurationV1WebhookNamespaceSelectorMatchExpressions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9458038c15e383ef8a5f78a50d7269d81020befdbcb2bbbfa6c16e0037fb19c3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acce4a4f598559a5f5022e4217103bd7ab441aefdb7e873802c16ad815ff9c95(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MutatingWebhookConfigurationV1WebhookNamespaceSelectorMatchExpressions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eab483c2bdbaa83f71caebdeb1357d2333ce0771a400280f95ccff05fcd2a0e0(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36261d59a2f86f58374e612473990e9a4b799190cc2a2335ffe3b4fe9cb300e4(
    value: typing.Optional[MutatingWebhookConfigurationV1WebhookNamespaceSelector],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f7989f8e10e99f81f7c25a4054136c07d9d1f5717c6056cf4881bf2f5e2cc60(
    *,
    match_expressions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MutatingWebhookConfigurationV1WebhookObjectSelectorMatchExpressions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    match_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4a7be3ece4ebf0738acaf8a544a8f5b836c76884335d4b25440ee3db48a031d(
    *,
    key: typing.Optional[builtins.str] = None,
    operator: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b5082828249c0586629a093789ba541c88939dd598007f035829fb78ef1dea8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5c911e6194b88f974c7f7217fe10ae3fda4572f499e7e2a832c3613f87bef0c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__437b9a23e3c016f2a30f58fae6b9e6e7232daeea70ceb7c83b5600a3e50f60a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e08ec9aa4db9169b125e419f40043e8ee465c79a4f2dd21370ca3fe1cba7fab3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ad95b57a413a0d0719ae124d831a7215b7c0b3c5df53e17208254d3b2ee0063(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed8989ecfb3e0f8d33e428a4cbb082726248741407117ea90c2878eedcf456bf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MutatingWebhookConfigurationV1WebhookObjectSelectorMatchExpressions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d70c78bddf9b66dd27b758a9f065404b9ede1a7d7b6098af0b41663de2d6cea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd95fcfdab97dfaae39222493839191fdeb7dc8ecbe1919cb61b1d1b48a49e7f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9d894a848a30d366de623f7f2d405e38a57a73872cdf19f3e6ee26b86002f2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b98397315ae5e455002d63af3900717692b79108cbb2bd2ea16ac4ff79ac807(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b21e60a528d9cce8e2ef1341aba6ce67acb4c2933e3cfd8b6ef2956d658c452f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MutatingWebhookConfigurationV1WebhookObjectSelectorMatchExpressions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaf775b4a2d9e19fce0e016d3f4f97df773bd577ab849ae05f3088f2a443039a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ceed8dbd249bfe9fc82c430ac09eac9ad676f4292fe7a2ba9d0ae60efa7523e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MutatingWebhookConfigurationV1WebhookObjectSelectorMatchExpressions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__509d5caeb1e674dffa7a99c8b91e989672d147b280d9f60036fbc44308363fea(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31e10c989d7c26f4475dcbbd773bbbd9d97e222af517f3f79d81c022d4085628(
    value: typing.Optional[MutatingWebhookConfigurationV1WebhookObjectSelector],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3673b37ad9ee1e3c48baa0036a06ededc27e94299c50430f8455209231825b5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efdf65bdd5011de3397cd95d7c75a553f85b7646a7ec4041eae914305b0fed95(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MutatingWebhookConfigurationV1WebhookRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0238b8e583cb225882a3e132f67be1dcf670ef063f5b841a2f960d2034b509f8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46c579cdeeb27080f377db03c4dd39de73128013bc46bd652afa16cb2d8df3e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fde5dbeb06c942225cac2e1b7be18603f21018648951c740c8f96d457da73ee4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeedf2835c87c74ff464097e35f30caadacf423fc8f2227d74f62002353e8585(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__356149677b9b9ad2adad66eb8c32ffceac35cb156603ba644cb599c0f5957126(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba1b429ec96360d259b125e8409525df48afe0a8a49f6f2cec7b88c0c0596a22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__287f6e5fa3fdab10ebcedd55e2eb62c51bf882f26dc9c3c7134740331f11de4a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__205391cc2a5a4029cc0ea3c1514f07432c9c086fdb76815e22f6cc0c2ce0399a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MutatingWebhookConfigurationV1Webhook]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ca8eb292ea73444b4e5629de55601b22d6d73e95be3b7db570388df769e50f6(
    *,
    api_groups: typing.Sequence[builtins.str],
    api_versions: typing.Sequence[builtins.str],
    operations: typing.Sequence[builtins.str],
    resources: typing.Sequence[builtins.str],
    scope: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18f992920885b9498979008f62de9b1ca8aaf75c39217b3f78906de370ad2d8d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc904b894e9491981f6c3fbd4376732f8bfe8626c0ee2c6210bd23e7e401e05a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__738cf369bb3118af157e1c903cbdb3f022ce03dcbec158babf5b3e5f4acf9f47(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e225a486cb52d77ab6887b00d6a71ccb04f362e97f8cb33919834185ffe094b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fcee2f2a7c44e6d4dc91c28d9ab0da3c700f6dfbc1eb8d225627f5c334ae826(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22f969307d3609656c7cb97959052707e93cc2c843bd97cfa075512f20e4c08a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MutatingWebhookConfigurationV1WebhookRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d45248734bffc2bc7f4922b9885885bc542afc036fb8f450b8f678a062067a29(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3838633e20fa5e1829987578895725ee9c22066a773c765e5d49e4f3b587dbe9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa1f3ccd05121a468dbea41294c566c53376304c2ee047a3a4304e1c02bb8fec(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bf746c54cd1618b590207bf084ad8420d40987a9f10dadc2b2471f7728a2d15(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__566ba82f6eab8d14bd730247620b6d32bc8c2a3dab83fe03a133096b6601db3d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9b77eaf34e5aaef1ff176d73242992c4464c7b14f5022837271fa5626a7b9f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2f7d9a5c7c2e1762611623be7d8a7877e32682384da81743edae6c2244d4ea4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MutatingWebhookConfigurationV1WebhookRule]],
) -> None:
    """Type checking stubs"""
    pass

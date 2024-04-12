'''
# `aws_imagebuilder_image`

Refer to the Terraform Registry for docs: [`aws_imagebuilder_image`](https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image).
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


class ImagebuilderImage(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.imagebuilderImage.ImagebuilderImage",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image aws_imagebuilder_image}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        infrastructure_configuration_arn: builtins.str,
        container_recipe_arn: typing.Optional[builtins.str] = None,
        distribution_configuration_arn: typing.Optional[builtins.str] = None,
        enhanced_image_metadata_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        image_recipe_arn: typing.Optional[builtins.str] = None,
        image_scanning_configuration: typing.Optional[typing.Union["ImagebuilderImageImageScanningConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        image_tests_configuration: typing.Optional[typing.Union["ImagebuilderImageImageTestsConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ImagebuilderImageTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image aws_imagebuilder_image} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param infrastructure_configuration_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#infrastructure_configuration_arn ImagebuilderImage#infrastructure_configuration_arn}.
        :param container_recipe_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#container_recipe_arn ImagebuilderImage#container_recipe_arn}.
        :param distribution_configuration_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#distribution_configuration_arn ImagebuilderImage#distribution_configuration_arn}.
        :param enhanced_image_metadata_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#enhanced_image_metadata_enabled ImagebuilderImage#enhanced_image_metadata_enabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#id ImagebuilderImage#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param image_recipe_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#image_recipe_arn ImagebuilderImage#image_recipe_arn}.
        :param image_scanning_configuration: image_scanning_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#image_scanning_configuration ImagebuilderImage#image_scanning_configuration}
        :param image_tests_configuration: image_tests_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#image_tests_configuration ImagebuilderImage#image_tests_configuration}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#tags ImagebuilderImage#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#tags_all ImagebuilderImage#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#timeouts ImagebuilderImage#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93762517c1fb413c4a7607c4cd45f2c30dd5852093ccc3d61c060beb0a8961b1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ImagebuilderImageConfig(
            infrastructure_configuration_arn=infrastructure_configuration_arn,
            container_recipe_arn=container_recipe_arn,
            distribution_configuration_arn=distribution_configuration_arn,
            enhanced_image_metadata_enabled=enhanced_image_metadata_enabled,
            id=id,
            image_recipe_arn=image_recipe_arn,
            image_scanning_configuration=image_scanning_configuration,
            image_tests_configuration=image_tests_configuration,
            tags=tags,
            tags_all=tags_all,
            timeouts=timeouts,
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
        '''Generates CDKTF code for importing a ImagebuilderImage resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ImagebuilderImage to import.
        :param import_from_id: The id of the existing ImagebuilderImage that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ImagebuilderImage to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e977b3a49d78bb999095b64fc430eee274866588f93727abf63084b110a23c5c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putImageScanningConfiguration")
    def put_image_scanning_configuration(
        self,
        *,
        ecr_configuration: typing.Optional[typing.Union["ImagebuilderImageImageScanningConfigurationEcrConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        image_scanning_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param ecr_configuration: ecr_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#ecr_configuration ImagebuilderImage#ecr_configuration}
        :param image_scanning_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#image_scanning_enabled ImagebuilderImage#image_scanning_enabled}.
        '''
        value = ImagebuilderImageImageScanningConfiguration(
            ecr_configuration=ecr_configuration,
            image_scanning_enabled=image_scanning_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putImageScanningConfiguration", [value]))

    @jsii.member(jsii_name="putImageTestsConfiguration")
    def put_image_tests_configuration(
        self,
        *,
        image_tests_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeout_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param image_tests_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#image_tests_enabled ImagebuilderImage#image_tests_enabled}.
        :param timeout_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#timeout_minutes ImagebuilderImage#timeout_minutes}.
        '''
        value = ImagebuilderImageImageTestsConfiguration(
            image_tests_enabled=image_tests_enabled, timeout_minutes=timeout_minutes
        )

        return typing.cast(None, jsii.invoke(self, "putImageTestsConfiguration", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(self, *, create: typing.Optional[builtins.str] = None) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#create ImagebuilderImage#create}.
        '''
        value = ImagebuilderImageTimeouts(create=create)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetContainerRecipeArn")
    def reset_container_recipe_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerRecipeArn", []))

    @jsii.member(jsii_name="resetDistributionConfigurationArn")
    def reset_distribution_configuration_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDistributionConfigurationArn", []))

    @jsii.member(jsii_name="resetEnhancedImageMetadataEnabled")
    def reset_enhanced_image_metadata_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnhancedImageMetadataEnabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetImageRecipeArn")
    def reset_image_recipe_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageRecipeArn", []))

    @jsii.member(jsii_name="resetImageScanningConfiguration")
    def reset_image_scanning_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageScanningConfiguration", []))

    @jsii.member(jsii_name="resetImageTestsConfiguration")
    def reset_image_tests_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageTestsConfiguration", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

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
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="dateCreated")
    def date_created(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dateCreated"))

    @builtins.property
    @jsii.member(jsii_name="imageScanningConfiguration")
    def image_scanning_configuration(
        self,
    ) -> "ImagebuilderImageImageScanningConfigurationOutputReference":
        return typing.cast("ImagebuilderImageImageScanningConfigurationOutputReference", jsii.get(self, "imageScanningConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="imageTestsConfiguration")
    def image_tests_configuration(
        self,
    ) -> "ImagebuilderImageImageTestsConfigurationOutputReference":
        return typing.cast("ImagebuilderImageImageTestsConfigurationOutputReference", jsii.get(self, "imageTestsConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="osVersion")
    def os_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osVersion"))

    @builtins.property
    @jsii.member(jsii_name="outputResources")
    def output_resources(self) -> "ImagebuilderImageOutputResourcesList":
        return typing.cast("ImagebuilderImageOutputResourcesList", jsii.get(self, "outputResources"))

    @builtins.property
    @jsii.member(jsii_name="platform")
    def platform(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "platform"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ImagebuilderImageTimeoutsOutputReference":
        return typing.cast("ImagebuilderImageTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @builtins.property
    @jsii.member(jsii_name="containerRecipeArnInput")
    def container_recipe_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerRecipeArnInput"))

    @builtins.property
    @jsii.member(jsii_name="distributionConfigurationArnInput")
    def distribution_configuration_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "distributionConfigurationArnInput"))

    @builtins.property
    @jsii.member(jsii_name="enhancedImageMetadataEnabledInput")
    def enhanced_image_metadata_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enhancedImageMetadataEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="imageRecipeArnInput")
    def image_recipe_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageRecipeArnInput"))

    @builtins.property
    @jsii.member(jsii_name="imageScanningConfigurationInput")
    def image_scanning_configuration_input(
        self,
    ) -> typing.Optional["ImagebuilderImageImageScanningConfiguration"]:
        return typing.cast(typing.Optional["ImagebuilderImageImageScanningConfiguration"], jsii.get(self, "imageScanningConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="imageTestsConfigurationInput")
    def image_tests_configuration_input(
        self,
    ) -> typing.Optional["ImagebuilderImageImageTestsConfiguration"]:
        return typing.cast(typing.Optional["ImagebuilderImageImageTestsConfiguration"], jsii.get(self, "imageTestsConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="infrastructureConfigurationArnInput")
    def infrastructure_configuration_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "infrastructureConfigurationArnInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsAllInput")
    def tags_all_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsAllInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ImagebuilderImageTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ImagebuilderImageTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="containerRecipeArn")
    def container_recipe_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "containerRecipeArn"))

    @container_recipe_arn.setter
    def container_recipe_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daffca500b571cfdd8563df3271f248d43797f2be4a515fba4d71f95283e732f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerRecipeArn", value)

    @builtins.property
    @jsii.member(jsii_name="distributionConfigurationArn")
    def distribution_configuration_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "distributionConfigurationArn"))

    @distribution_configuration_arn.setter
    def distribution_configuration_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95d93a61c8f767ad31a08c0e33c867a4f0e1e5882db6a16783f769e9e5779419)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "distributionConfigurationArn", value)

    @builtins.property
    @jsii.member(jsii_name="enhancedImageMetadataEnabled")
    def enhanced_image_metadata_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enhancedImageMetadataEnabled"))

    @enhanced_image_metadata_enabled.setter
    def enhanced_image_metadata_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be2fab9e81b2e9419d1bdfdb033e1db8a3b71af3338df0949c67fdaa2df650a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enhancedImageMetadataEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a582fee1a5c2b2138ab32fca7b29e54aae9623e5c647e7c78dbb7c6c25fcb7ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="imageRecipeArn")
    def image_recipe_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageRecipeArn"))

    @image_recipe_arn.setter
    def image_recipe_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__deb5e6fea42acec5833c488f338e7fa99dfb42e9431b855b7ba49b9416f3fa58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageRecipeArn", value)

    @builtins.property
    @jsii.member(jsii_name="infrastructureConfigurationArn")
    def infrastructure_configuration_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "infrastructureConfigurationArn"))

    @infrastructure_configuration_arn.setter
    def infrastructure_configuration_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7363a2adb7a4bdfc4a74ba21a3fbe942434716cc6fa6accba43ad98d00419e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "infrastructureConfigurationArn", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f0e4dcf87d4a58943a36cec82e221269e71b07ba56bec56c7443dfc52b902c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__645ff1ca333dafc93e756a1442b19559e7f163322bc9d669f260e9143ba22624)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.imagebuilderImage.ImagebuilderImageConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "infrastructure_configuration_arn": "infrastructureConfigurationArn",
        "container_recipe_arn": "containerRecipeArn",
        "distribution_configuration_arn": "distributionConfigurationArn",
        "enhanced_image_metadata_enabled": "enhancedImageMetadataEnabled",
        "id": "id",
        "image_recipe_arn": "imageRecipeArn",
        "image_scanning_configuration": "imageScanningConfiguration",
        "image_tests_configuration": "imageTestsConfiguration",
        "tags": "tags",
        "tags_all": "tagsAll",
        "timeouts": "timeouts",
    },
)
class ImagebuilderImageConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        infrastructure_configuration_arn: builtins.str,
        container_recipe_arn: typing.Optional[builtins.str] = None,
        distribution_configuration_arn: typing.Optional[builtins.str] = None,
        enhanced_image_metadata_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        image_recipe_arn: typing.Optional[builtins.str] = None,
        image_scanning_configuration: typing.Optional[typing.Union["ImagebuilderImageImageScanningConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        image_tests_configuration: typing.Optional[typing.Union["ImagebuilderImageImageTestsConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ImagebuilderImageTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param infrastructure_configuration_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#infrastructure_configuration_arn ImagebuilderImage#infrastructure_configuration_arn}.
        :param container_recipe_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#container_recipe_arn ImagebuilderImage#container_recipe_arn}.
        :param distribution_configuration_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#distribution_configuration_arn ImagebuilderImage#distribution_configuration_arn}.
        :param enhanced_image_metadata_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#enhanced_image_metadata_enabled ImagebuilderImage#enhanced_image_metadata_enabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#id ImagebuilderImage#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param image_recipe_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#image_recipe_arn ImagebuilderImage#image_recipe_arn}.
        :param image_scanning_configuration: image_scanning_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#image_scanning_configuration ImagebuilderImage#image_scanning_configuration}
        :param image_tests_configuration: image_tests_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#image_tests_configuration ImagebuilderImage#image_tests_configuration}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#tags ImagebuilderImage#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#tags_all ImagebuilderImage#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#timeouts ImagebuilderImage#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(image_scanning_configuration, dict):
            image_scanning_configuration = ImagebuilderImageImageScanningConfiguration(**image_scanning_configuration)
        if isinstance(image_tests_configuration, dict):
            image_tests_configuration = ImagebuilderImageImageTestsConfiguration(**image_tests_configuration)
        if isinstance(timeouts, dict):
            timeouts = ImagebuilderImageTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a7a0e0b0a331b30a97ef326568a146ae388955633dc60e20c18f448fd194e25)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument infrastructure_configuration_arn", value=infrastructure_configuration_arn, expected_type=type_hints["infrastructure_configuration_arn"])
            check_type(argname="argument container_recipe_arn", value=container_recipe_arn, expected_type=type_hints["container_recipe_arn"])
            check_type(argname="argument distribution_configuration_arn", value=distribution_configuration_arn, expected_type=type_hints["distribution_configuration_arn"])
            check_type(argname="argument enhanced_image_metadata_enabled", value=enhanced_image_metadata_enabled, expected_type=type_hints["enhanced_image_metadata_enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument image_recipe_arn", value=image_recipe_arn, expected_type=type_hints["image_recipe_arn"])
            check_type(argname="argument image_scanning_configuration", value=image_scanning_configuration, expected_type=type_hints["image_scanning_configuration"])
            check_type(argname="argument image_tests_configuration", value=image_tests_configuration, expected_type=type_hints["image_tests_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "infrastructure_configuration_arn": infrastructure_configuration_arn,
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
        if container_recipe_arn is not None:
            self._values["container_recipe_arn"] = container_recipe_arn
        if distribution_configuration_arn is not None:
            self._values["distribution_configuration_arn"] = distribution_configuration_arn
        if enhanced_image_metadata_enabled is not None:
            self._values["enhanced_image_metadata_enabled"] = enhanced_image_metadata_enabled
        if id is not None:
            self._values["id"] = id
        if image_recipe_arn is not None:
            self._values["image_recipe_arn"] = image_recipe_arn
        if image_scanning_configuration is not None:
            self._values["image_scanning_configuration"] = image_scanning_configuration
        if image_tests_configuration is not None:
            self._values["image_tests_configuration"] = image_tests_configuration
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if timeouts is not None:
            self._values["timeouts"] = timeouts

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
    def infrastructure_configuration_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#infrastructure_configuration_arn ImagebuilderImage#infrastructure_configuration_arn}.'''
        result = self._values.get("infrastructure_configuration_arn")
        assert result is not None, "Required property 'infrastructure_configuration_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def container_recipe_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#container_recipe_arn ImagebuilderImage#container_recipe_arn}.'''
        result = self._values.get("container_recipe_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def distribution_configuration_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#distribution_configuration_arn ImagebuilderImage#distribution_configuration_arn}.'''
        result = self._values.get("distribution_configuration_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enhanced_image_metadata_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#enhanced_image_metadata_enabled ImagebuilderImage#enhanced_image_metadata_enabled}.'''
        result = self._values.get("enhanced_image_metadata_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#id ImagebuilderImage#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_recipe_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#image_recipe_arn ImagebuilderImage#image_recipe_arn}.'''
        result = self._values.get("image_recipe_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_scanning_configuration(
        self,
    ) -> typing.Optional["ImagebuilderImageImageScanningConfiguration"]:
        '''image_scanning_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#image_scanning_configuration ImagebuilderImage#image_scanning_configuration}
        '''
        result = self._values.get("image_scanning_configuration")
        return typing.cast(typing.Optional["ImagebuilderImageImageScanningConfiguration"], result)

    @builtins.property
    def image_tests_configuration(
        self,
    ) -> typing.Optional["ImagebuilderImageImageTestsConfiguration"]:
        '''image_tests_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#image_tests_configuration ImagebuilderImage#image_tests_configuration}
        '''
        result = self._values.get("image_tests_configuration")
        return typing.cast(typing.Optional["ImagebuilderImageImageTestsConfiguration"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#tags ImagebuilderImage#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#tags_all ImagebuilderImage#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ImagebuilderImageTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#timeouts ImagebuilderImage#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ImagebuilderImageTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ImagebuilderImageConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.imagebuilderImage.ImagebuilderImageImageScanningConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "ecr_configuration": "ecrConfiguration",
        "image_scanning_enabled": "imageScanningEnabled",
    },
)
class ImagebuilderImageImageScanningConfiguration:
    def __init__(
        self,
        *,
        ecr_configuration: typing.Optional[typing.Union["ImagebuilderImageImageScanningConfigurationEcrConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        image_scanning_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param ecr_configuration: ecr_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#ecr_configuration ImagebuilderImage#ecr_configuration}
        :param image_scanning_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#image_scanning_enabled ImagebuilderImage#image_scanning_enabled}.
        '''
        if isinstance(ecr_configuration, dict):
            ecr_configuration = ImagebuilderImageImageScanningConfigurationEcrConfiguration(**ecr_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b08a6f5d1dbfa73dca82932c4be683af0030ddf727ef59e761d77eb4f5ef4d4)
            check_type(argname="argument ecr_configuration", value=ecr_configuration, expected_type=type_hints["ecr_configuration"])
            check_type(argname="argument image_scanning_enabled", value=image_scanning_enabled, expected_type=type_hints["image_scanning_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ecr_configuration is not None:
            self._values["ecr_configuration"] = ecr_configuration
        if image_scanning_enabled is not None:
            self._values["image_scanning_enabled"] = image_scanning_enabled

    @builtins.property
    def ecr_configuration(
        self,
    ) -> typing.Optional["ImagebuilderImageImageScanningConfigurationEcrConfiguration"]:
        '''ecr_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#ecr_configuration ImagebuilderImage#ecr_configuration}
        '''
        result = self._values.get("ecr_configuration")
        return typing.cast(typing.Optional["ImagebuilderImageImageScanningConfigurationEcrConfiguration"], result)

    @builtins.property
    def image_scanning_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#image_scanning_enabled ImagebuilderImage#image_scanning_enabled}.'''
        result = self._values.get("image_scanning_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ImagebuilderImageImageScanningConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.imagebuilderImage.ImagebuilderImageImageScanningConfigurationEcrConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "container_tags": "containerTags",
        "repository_name": "repositoryName",
    },
)
class ImagebuilderImageImageScanningConfigurationEcrConfiguration:
    def __init__(
        self,
        *,
        container_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        repository_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param container_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#container_tags ImagebuilderImage#container_tags}.
        :param repository_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#repository_name ImagebuilderImage#repository_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17826c89e68b783f373330979e9f293279e8eb09ff5a6d17f7c051f97b3ec8ed)
            check_type(argname="argument container_tags", value=container_tags, expected_type=type_hints["container_tags"])
            check_type(argname="argument repository_name", value=repository_name, expected_type=type_hints["repository_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if container_tags is not None:
            self._values["container_tags"] = container_tags
        if repository_name is not None:
            self._values["repository_name"] = repository_name

    @builtins.property
    def container_tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#container_tags ImagebuilderImage#container_tags}.'''
        result = self._values.get("container_tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def repository_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#repository_name ImagebuilderImage#repository_name}.'''
        result = self._values.get("repository_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ImagebuilderImageImageScanningConfigurationEcrConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ImagebuilderImageImageScanningConfigurationEcrConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.imagebuilderImage.ImagebuilderImageImageScanningConfigurationEcrConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__753ee7198a1946e23fc28cb0cb05c6ebbafc33c98c4494d432e010e7bf650ef8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetContainerTags")
    def reset_container_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerTags", []))

    @jsii.member(jsii_name="resetRepositoryName")
    def reset_repository_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRepositoryName", []))

    @builtins.property
    @jsii.member(jsii_name="containerTagsInput")
    def container_tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "containerTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryNameInput")
    def repository_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryNameInput"))

    @builtins.property
    @jsii.member(jsii_name="containerTags")
    def container_tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "containerTags"))

    @container_tags.setter
    def container_tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af7c5acf564d14f71853aaf6115864e637562a258fea38715c3ce7e572a6d69f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerTags", value)

    @builtins.property
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repositoryName"))

    @repository_name.setter
    def repository_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3a65f7883449ddcbc8aa94915c5be6cd5a2968b0000fe1ec1f02140ebd988ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryName", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ImagebuilderImageImageScanningConfigurationEcrConfiguration]:
        return typing.cast(typing.Optional[ImagebuilderImageImageScanningConfigurationEcrConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ImagebuilderImageImageScanningConfigurationEcrConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8ba8601c61db0e5784ec5f89960aed07b6a271c19ad2938187653891ff956f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class ImagebuilderImageImageScanningConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.imagebuilderImage.ImagebuilderImageImageScanningConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb328cf1efe4b95d7a2eb0dcd60a32c860a64a8f4fa79635d8a0815b160ea2e5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putEcrConfiguration")
    def put_ecr_configuration(
        self,
        *,
        container_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        repository_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param container_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#container_tags ImagebuilderImage#container_tags}.
        :param repository_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#repository_name ImagebuilderImage#repository_name}.
        '''
        value = ImagebuilderImageImageScanningConfigurationEcrConfiguration(
            container_tags=container_tags, repository_name=repository_name
        )

        return typing.cast(None, jsii.invoke(self, "putEcrConfiguration", [value]))

    @jsii.member(jsii_name="resetEcrConfiguration")
    def reset_ecr_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEcrConfiguration", []))

    @jsii.member(jsii_name="resetImageScanningEnabled")
    def reset_image_scanning_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageScanningEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="ecrConfiguration")
    def ecr_configuration(
        self,
    ) -> ImagebuilderImageImageScanningConfigurationEcrConfigurationOutputReference:
        return typing.cast(ImagebuilderImageImageScanningConfigurationEcrConfigurationOutputReference, jsii.get(self, "ecrConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="ecrConfigurationInput")
    def ecr_configuration_input(
        self,
    ) -> typing.Optional[ImagebuilderImageImageScanningConfigurationEcrConfiguration]:
        return typing.cast(typing.Optional[ImagebuilderImageImageScanningConfigurationEcrConfiguration], jsii.get(self, "ecrConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="imageScanningEnabledInput")
    def image_scanning_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "imageScanningEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="imageScanningEnabled")
    def image_scanning_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "imageScanningEnabled"))

    @image_scanning_enabled.setter
    def image_scanning_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d607e49714612694dca8df85d5bcf7c36f249e6a5b7a58b3b0a5a9db46e72ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageScanningEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ImagebuilderImageImageScanningConfiguration]:
        return typing.cast(typing.Optional[ImagebuilderImageImageScanningConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ImagebuilderImageImageScanningConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b7a0aae32d192f6216599af3ff49dc365ec64e07c8f8ff37c5212cb873ecae4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.imagebuilderImage.ImagebuilderImageImageTestsConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "image_tests_enabled": "imageTestsEnabled",
        "timeout_minutes": "timeoutMinutes",
    },
)
class ImagebuilderImageImageTestsConfiguration:
    def __init__(
        self,
        *,
        image_tests_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeout_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param image_tests_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#image_tests_enabled ImagebuilderImage#image_tests_enabled}.
        :param timeout_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#timeout_minutes ImagebuilderImage#timeout_minutes}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53b8833367f971c5a37ad16a1102a61ccdd8d658b79d89dd32ab7c5c9192fcd4)
            check_type(argname="argument image_tests_enabled", value=image_tests_enabled, expected_type=type_hints["image_tests_enabled"])
            check_type(argname="argument timeout_minutes", value=timeout_minutes, expected_type=type_hints["timeout_minutes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if image_tests_enabled is not None:
            self._values["image_tests_enabled"] = image_tests_enabled
        if timeout_minutes is not None:
            self._values["timeout_minutes"] = timeout_minutes

    @builtins.property
    def image_tests_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#image_tests_enabled ImagebuilderImage#image_tests_enabled}.'''
        result = self._values.get("image_tests_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timeout_minutes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#timeout_minutes ImagebuilderImage#timeout_minutes}.'''
        result = self._values.get("timeout_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ImagebuilderImageImageTestsConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ImagebuilderImageImageTestsConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.imagebuilderImage.ImagebuilderImageImageTestsConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c77fc6aa774fd6d824e0708213902cad549dfbb3bcd8fe109ca9d128653c0ef)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetImageTestsEnabled")
    def reset_image_tests_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageTestsEnabled", []))

    @jsii.member(jsii_name="resetTimeoutMinutes")
    def reset_timeout_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeoutMinutes", []))

    @builtins.property
    @jsii.member(jsii_name="imageTestsEnabledInput")
    def image_tests_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "imageTestsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutMinutesInput")
    def timeout_minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutMinutesInput"))

    @builtins.property
    @jsii.member(jsii_name="imageTestsEnabled")
    def image_tests_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "imageTestsEnabled"))

    @image_tests_enabled.setter
    def image_tests_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb2f85f8f79d303117a6dfaa32152f9f4ca783420cf970a1f893150f575aa02d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageTestsEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="timeoutMinutes")
    def timeout_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutMinutes"))

    @timeout_minutes.setter
    def timeout_minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9b72035527c7f7f0b8f675a69e6f5b5cd6a54b6860f804ff366386fb0c527cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutMinutes", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ImagebuilderImageImageTestsConfiguration]:
        return typing.cast(typing.Optional[ImagebuilderImageImageTestsConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ImagebuilderImageImageTestsConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90419cdcd70bb8dfef6fd827fde0c40e3e1d6db9a3939eec0f625f6b72ce9cd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.imagebuilderImage.ImagebuilderImageOutputResources",
    jsii_struct_bases=[],
    name_mapping={},
)
class ImagebuilderImageOutputResources:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ImagebuilderImageOutputResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.imagebuilderImage.ImagebuilderImageOutputResourcesAmis",
    jsii_struct_bases=[],
    name_mapping={},
)
class ImagebuilderImageOutputResourcesAmis:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ImagebuilderImageOutputResourcesAmis(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ImagebuilderImageOutputResourcesAmisList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.imagebuilderImage.ImagebuilderImageOutputResourcesAmisList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b76c01743f72b783766d45baf97ad8fcd243d621f85b3127339a580b4ee04c5b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ImagebuilderImageOutputResourcesAmisOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8519ac5e78d2953b0d83f5f3b1e7c3311107b71aa494d952164603fc20d3ff6c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ImagebuilderImageOutputResourcesAmisOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cc6871a91ebf5aa70ad0892d703caaaa4f250309fb5563cd4a50b469ce1b4d9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__591fdf68ad800b9cd7f698660e554faa98b8330f4571a81e5e198a2dabbe4c45)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d91fadd1e607dabf53ec50564b7e8111cd928adf40ae0d899bd73b3aa19d5c46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class ImagebuilderImageOutputResourcesAmisOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.imagebuilderImage.ImagebuilderImageOutputResourcesAmisOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab81ace786c0f56c718f3322cb43cf4776e940fee9bbefbbb5559cf15bdacc17)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "image"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ImagebuilderImageOutputResourcesAmis]:
        return typing.cast(typing.Optional[ImagebuilderImageOutputResourcesAmis], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ImagebuilderImageOutputResourcesAmis],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e513ac53c13f9e6dcbc6878b6bb9735a53c26d393988446ecbea103830d6f7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.imagebuilderImage.ImagebuilderImageOutputResourcesContainers",
    jsii_struct_bases=[],
    name_mapping={},
)
class ImagebuilderImageOutputResourcesContainers:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ImagebuilderImageOutputResourcesContainers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ImagebuilderImageOutputResourcesContainersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.imagebuilderImage.ImagebuilderImageOutputResourcesContainersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__83f415c3c8c85a62bfc3213d067110ec1871dc1d1adf7431307321cd0a4bb396)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ImagebuilderImageOutputResourcesContainersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe73e79c1f10328c9411fbd5ae5bf41293dd8593639f6e56aafcb4723346a9f6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ImagebuilderImageOutputResourcesContainersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d211033b5f425eb6f11cf0c8953c3301ca67fe10c706d3e07c937f6422fe4866)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd01692abebf0741dbcef0690f46a5337808aaa53f6a6838682125f2e4172d42)
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
            type_hints = typing.get_type_hints(_typecheckingstub__960160241dc00b1b1a0064bcc5a115c0547d318e0d50ce92668651b8cff5820e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class ImagebuilderImageOutputResourcesContainersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.imagebuilderImage.ImagebuilderImageOutputResourcesContainersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__74fa3a4e6acc8232b61d49841f8c1a6ce03561651710aa8f6568cc139972d352)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="imageUris")
    def image_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "imageUris"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ImagebuilderImageOutputResourcesContainers]:
        return typing.cast(typing.Optional[ImagebuilderImageOutputResourcesContainers], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ImagebuilderImageOutputResourcesContainers],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48c0f4f28c363a1708cc9fd11b6ba670cf6421e46d6b1d398b8d2eaa1f38b9a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class ImagebuilderImageOutputResourcesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.imagebuilderImage.ImagebuilderImageOutputResourcesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee00428a91ef1b0e878e2165567ac9a1928a7d0840b169a5e2c2e9aeff395647)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ImagebuilderImageOutputResourcesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c35ef7a9ce220ccad276c160dce28b6cb8fd3b8ff774447d6deaeb0907a46ed)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ImagebuilderImageOutputResourcesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c078d203e80b7a3228671908f231447bd4e35e599813ccef1dba64f1e07ae64)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a94cc9082a863d26d3270af4e4828c9b6bf7cb8f8174c864e6c725492a58250f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1136f1d97abacd87d32f1583a636f161bc686565511c261466d0e024558f4f62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class ImagebuilderImageOutputResourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.imagebuilderImage.ImagebuilderImageOutputResourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__77c304bfd55054fe88f18db67d747592ca906e00735fe56d0a2f13e3d8fb8d3b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="amis")
    def amis(self) -> ImagebuilderImageOutputResourcesAmisList:
        return typing.cast(ImagebuilderImageOutputResourcesAmisList, jsii.get(self, "amis"))

    @builtins.property
    @jsii.member(jsii_name="containers")
    def containers(self) -> ImagebuilderImageOutputResourcesContainersList:
        return typing.cast(ImagebuilderImageOutputResourcesContainersList, jsii.get(self, "containers"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ImagebuilderImageOutputResources]:
        return typing.cast(typing.Optional[ImagebuilderImageOutputResources], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ImagebuilderImageOutputResources],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7be7ce226000a287e3bc6f48ffb08cdf53458f97fba2408df20cdf9c8e9fd76d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.imagebuilderImage.ImagebuilderImageTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create"},
)
class ImagebuilderImageTimeouts:
    def __init__(self, *, create: typing.Optional[builtins.str] = None) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#create ImagebuilderImage#create}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__405f388ba6cc1b41efdc55af7bfa02d68f015f4f8ed558f94676525a37079c40)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.45.0/docs/resources/imagebuilder_image#create ImagebuilderImage#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ImagebuilderImageTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ImagebuilderImageTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.imagebuilderImage.ImagebuilderImageTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d388a9dbe5da675e9d2df476e306466ed742444651b51b88a18943576aad101)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__131b644229c43aff7c24038bb8c8044b0602fc334de551a532281209a66f0dd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ImagebuilderImageTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ImagebuilderImageTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ImagebuilderImageTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2099b987a4a68f0df46e22ad8dc4fa5677074940a85a88f07b678a154dbbbb0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "ImagebuilderImage",
    "ImagebuilderImageConfig",
    "ImagebuilderImageImageScanningConfiguration",
    "ImagebuilderImageImageScanningConfigurationEcrConfiguration",
    "ImagebuilderImageImageScanningConfigurationEcrConfigurationOutputReference",
    "ImagebuilderImageImageScanningConfigurationOutputReference",
    "ImagebuilderImageImageTestsConfiguration",
    "ImagebuilderImageImageTestsConfigurationOutputReference",
    "ImagebuilderImageOutputResources",
    "ImagebuilderImageOutputResourcesAmis",
    "ImagebuilderImageOutputResourcesAmisList",
    "ImagebuilderImageOutputResourcesAmisOutputReference",
    "ImagebuilderImageOutputResourcesContainers",
    "ImagebuilderImageOutputResourcesContainersList",
    "ImagebuilderImageOutputResourcesContainersOutputReference",
    "ImagebuilderImageOutputResourcesList",
    "ImagebuilderImageOutputResourcesOutputReference",
    "ImagebuilderImageTimeouts",
    "ImagebuilderImageTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__93762517c1fb413c4a7607c4cd45f2c30dd5852093ccc3d61c060beb0a8961b1(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    infrastructure_configuration_arn: builtins.str,
    container_recipe_arn: typing.Optional[builtins.str] = None,
    distribution_configuration_arn: typing.Optional[builtins.str] = None,
    enhanced_image_metadata_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    image_recipe_arn: typing.Optional[builtins.str] = None,
    image_scanning_configuration: typing.Optional[typing.Union[ImagebuilderImageImageScanningConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    image_tests_configuration: typing.Optional[typing.Union[ImagebuilderImageImageTestsConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ImagebuilderImageTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__e977b3a49d78bb999095b64fc430eee274866588f93727abf63084b110a23c5c(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daffca500b571cfdd8563df3271f248d43797f2be4a515fba4d71f95283e732f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95d93a61c8f767ad31a08c0e33c867a4f0e1e5882db6a16783f769e9e5779419(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be2fab9e81b2e9419d1bdfdb033e1db8a3b71af3338df0949c67fdaa2df650a5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a582fee1a5c2b2138ab32fca7b29e54aae9623e5c647e7c78dbb7c6c25fcb7ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deb5e6fea42acec5833c488f338e7fa99dfb42e9431b855b7ba49b9416f3fa58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7363a2adb7a4bdfc4a74ba21a3fbe942434716cc6fa6accba43ad98d00419e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f0e4dcf87d4a58943a36cec82e221269e71b07ba56bec56c7443dfc52b902c4(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__645ff1ca333dafc93e756a1442b19559e7f163322bc9d669f260e9143ba22624(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a7a0e0b0a331b30a97ef326568a146ae388955633dc60e20c18f448fd194e25(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    infrastructure_configuration_arn: builtins.str,
    container_recipe_arn: typing.Optional[builtins.str] = None,
    distribution_configuration_arn: typing.Optional[builtins.str] = None,
    enhanced_image_metadata_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    image_recipe_arn: typing.Optional[builtins.str] = None,
    image_scanning_configuration: typing.Optional[typing.Union[ImagebuilderImageImageScanningConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    image_tests_configuration: typing.Optional[typing.Union[ImagebuilderImageImageTestsConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ImagebuilderImageTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b08a6f5d1dbfa73dca82932c4be683af0030ddf727ef59e761d77eb4f5ef4d4(
    *,
    ecr_configuration: typing.Optional[typing.Union[ImagebuilderImageImageScanningConfigurationEcrConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    image_scanning_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17826c89e68b783f373330979e9f293279e8eb09ff5a6d17f7c051f97b3ec8ed(
    *,
    container_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    repository_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__753ee7198a1946e23fc28cb0cb05c6ebbafc33c98c4494d432e010e7bf650ef8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af7c5acf564d14f71853aaf6115864e637562a258fea38715c3ce7e572a6d69f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3a65f7883449ddcbc8aa94915c5be6cd5a2968b0000fe1ec1f02140ebd988ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8ba8601c61db0e5784ec5f89960aed07b6a271c19ad2938187653891ff956f7(
    value: typing.Optional[ImagebuilderImageImageScanningConfigurationEcrConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb328cf1efe4b95d7a2eb0dcd60a32c860a64a8f4fa79635d8a0815b160ea2e5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d607e49714612694dca8df85d5bcf7c36f249e6a5b7a58b3b0a5a9db46e72ed(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b7a0aae32d192f6216599af3ff49dc365ec64e07c8f8ff37c5212cb873ecae4(
    value: typing.Optional[ImagebuilderImageImageScanningConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53b8833367f971c5a37ad16a1102a61ccdd8d658b79d89dd32ab7c5c9192fcd4(
    *,
    image_tests_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeout_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c77fc6aa774fd6d824e0708213902cad549dfbb3bcd8fe109ca9d128653c0ef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb2f85f8f79d303117a6dfaa32152f9f4ca783420cf970a1f893150f575aa02d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9b72035527c7f7f0b8f675a69e6f5b5cd6a54b6860f804ff366386fb0c527cf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90419cdcd70bb8dfef6fd827fde0c40e3e1d6db9a3939eec0f625f6b72ce9cd1(
    value: typing.Optional[ImagebuilderImageImageTestsConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b76c01743f72b783766d45baf97ad8fcd243d621f85b3127339a580b4ee04c5b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8519ac5e78d2953b0d83f5f3b1e7c3311107b71aa494d952164603fc20d3ff6c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cc6871a91ebf5aa70ad0892d703caaaa4f250309fb5563cd4a50b469ce1b4d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__591fdf68ad800b9cd7f698660e554faa98b8330f4571a81e5e198a2dabbe4c45(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d91fadd1e607dabf53ec50564b7e8111cd928adf40ae0d899bd73b3aa19d5c46(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab81ace786c0f56c718f3322cb43cf4776e940fee9bbefbbb5559cf15bdacc17(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e513ac53c13f9e6dcbc6878b6bb9735a53c26d393988446ecbea103830d6f7b(
    value: typing.Optional[ImagebuilderImageOutputResourcesAmis],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83f415c3c8c85a62bfc3213d067110ec1871dc1d1adf7431307321cd0a4bb396(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe73e79c1f10328c9411fbd5ae5bf41293dd8593639f6e56aafcb4723346a9f6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d211033b5f425eb6f11cf0c8953c3301ca67fe10c706d3e07c937f6422fe4866(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd01692abebf0741dbcef0690f46a5337808aaa53f6a6838682125f2e4172d42(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__960160241dc00b1b1a0064bcc5a115c0547d318e0d50ce92668651b8cff5820e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74fa3a4e6acc8232b61d49841f8c1a6ce03561651710aa8f6568cc139972d352(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48c0f4f28c363a1708cc9fd11b6ba670cf6421e46d6b1d398b8d2eaa1f38b9a9(
    value: typing.Optional[ImagebuilderImageOutputResourcesContainers],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee00428a91ef1b0e878e2165567ac9a1928a7d0840b169a5e2c2e9aeff395647(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c35ef7a9ce220ccad276c160dce28b6cb8fd3b8ff774447d6deaeb0907a46ed(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c078d203e80b7a3228671908f231447bd4e35e599813ccef1dba64f1e07ae64(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a94cc9082a863d26d3270af4e4828c9b6bf7cb8f8174c864e6c725492a58250f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1136f1d97abacd87d32f1583a636f161bc686565511c261466d0e024558f4f62(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77c304bfd55054fe88f18db67d747592ca906e00735fe56d0a2f13e3d8fb8d3b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7be7ce226000a287e3bc6f48ffb08cdf53458f97fba2408df20cdf9c8e9fd76d(
    value: typing.Optional[ImagebuilderImageOutputResources],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__405f388ba6cc1b41efdc55af7bfa02d68f015f4f8ed558f94676525a37079c40(
    *,
    create: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d388a9dbe5da675e9d2df476e306466ed742444651b51b88a18943576aad101(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__131b644229c43aff7c24038bb8c8044b0602fc334de551a532281209a66f0dd9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2099b987a4a68f0df46e22ad8dc4fa5677074940a85a88f07b678a154dbbbb0a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ImagebuilderImageTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

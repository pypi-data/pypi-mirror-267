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

import ros_cdk_core as _ros_cdk_core_7adfd82f


class Aliases(
    _ros_cdk_core_7adfd82f.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@alicloud/ros-cdk-fc.datasource.Aliases",
):
    '''This class encapsulates and extends the ROS resource type ``DATASOURCE::FC::Aliases``, which is used to query the aliases of a Function Compute service.

    :Note:

    This class may have some new functions to facilitate development, so it is recommended to use this class instead of ``RosAliases``for a more convenient development experience.
    See https://www.alibabacloud.com/help/ros/developer-reference/datasource-fc-aliases
    '''

    def __init__(
        self,
        scope: _ros_cdk_core_7adfd82f.Construct,
        id: builtins.str,
        props: typing.Union["AliasesProps", typing.Dict[builtins.str, typing.Any]],
        enable_resource_property_constraint: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Param scope - scope in which this resource is defined Param id    - scoped id of the resource Param props - resource properties.

        :param scope: -
        :param id: -
        :param props: -
        :param enable_resource_property_constraint: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__406fba9975ae133f6a89b76c08618f3ca89aac2c7b47a51887e7e3479c656bb7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
            check_type(argname="argument enable_resource_property_constraint", value=enable_resource_property_constraint, expected_type=type_hints["enable_resource_property_constraint"])
        jsii.create(self.__class__, self, [scope, id, props, enable_resource_property_constraint])

    @builtins.property
    @jsii.member(jsii_name="attrAliases")
    def attr_aliases(self) -> _ros_cdk_core_7adfd82f.IResolvable:
        '''Attribute Aliases: The list of aliases.'''
        return typing.cast(_ros_cdk_core_7adfd82f.IResolvable, jsii.get(self, "attrAliases"))

    @builtins.property
    @jsii.member(jsii_name="attrAliasNames")
    def attr_alias_names(self) -> _ros_cdk_core_7adfd82f.IResolvable:
        '''Attribute AliasNames: The list of alias names.'''
        return typing.cast(_ros_cdk_core_7adfd82f.IResolvable, jsii.get(self, "attrAliasNames"))

    @builtins.property
    @jsii.member(jsii_name="enableResourcePropertyConstraint")
    def _enable_resource_property_constraint(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "enableResourcePropertyConstraint"))

    @_enable_resource_property_constraint.setter
    def _enable_resource_property_constraint(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__149c1188224a96f687044b73122acf933aec8842ec077423116ff7764e21d1ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableResourcePropertyConstraint", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def _id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @_id.setter
    def _id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8f1f8f7bd925d9d607fc44bb702e63db3ab38a28f1f467d633095eb192365c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> "AliasesProps":
        return typing.cast("AliasesProps", jsii.get(self, "props"))

    @_props.setter
    def _props(self, value: "AliasesProps") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdab1691db15a10bdc1a357dbd17816530c1fdf0ef77ca7935440e9629782c0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "props", value)

    @builtins.property
    @jsii.member(jsii_name="scope")
    def _scope(self) -> _ros_cdk_core_7adfd82f.Construct:
        return typing.cast(_ros_cdk_core_7adfd82f.Construct, jsii.get(self, "scope"))

    @_scope.setter
    def _scope(self, value: _ros_cdk_core_7adfd82f.Construct) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da66925fee8c67f7f226464a7d611303476ade2b5479186ddbdc6d88fc0bd5e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value)


@jsii.data_type(
    jsii_type="@alicloud/ros-cdk-fc.datasource.AliasesProps",
    jsii_struct_bases=[],
    name_mapping={"service_name": "serviceName", "prefix": "prefix"},
)
class AliasesProps:
    def __init__(
        self,
        *,
        service_name: typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable],
        prefix: typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]] = None,
    ) -> None:
        '''Properties for defining a ``Aliases``.

        See https://www.alibabacloud.com/help/ros/developer-reference/datasource-fc-aliases

        :param service_name: Property serviceName: Service name.
        :param prefix: Property prefix: Qualified returned alias names must be prefixed with Prefix. For example, if the Prefix is "a", the returned alias names should be started with "a".
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58cc243b6cc0f45e7eecfa347337ef658b839368e9d006ccc3799fb43d2c591b)
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service_name": service_name,
        }
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def service_name(
        self,
    ) -> typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]:
        '''Property serviceName: Service name.'''
        result = self._values.get("service_name")
        assert result is not None, "Required property 'service_name' is missing"
        return typing.cast(typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable], result)

    @builtins.property
    def prefix(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]]:
        '''Property prefix: Qualified returned alias names must be prefixed with Prefix.

        For example, if the Prefix is "a", the returned alias names should be started with "a".
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AliasesProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CustomDomains(
    _ros_cdk_core_7adfd82f.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@alicloud/ros-cdk-fc.datasource.CustomDomains",
):
    '''This class encapsulates and extends the ROS resource type ``DATASOURCE::FC::CustomDomains``, which is used to query custom domain names in Function Compute.

    :Note:

    This class may have some new functions to facilitate development, so it is recommended to use this class instead of ``RosCustomDomains``for a more convenient development experience.
    See https://www.alibabacloud.com/help/ros/developer-reference/datasource-fc-customdomains
    '''

    def __init__(
        self,
        scope: _ros_cdk_core_7adfd82f.Construct,
        id: builtins.str,
        props: typing.Optional[typing.Union["CustomDomainsProps", typing.Dict[builtins.str, typing.Any]]] = None,
        enable_resource_property_constraint: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Param scope - scope in which this resource is defined Param id    - scoped id of the resource Param props - resource properties.

        :param scope: -
        :param id: -
        :param props: -
        :param enable_resource_property_constraint: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b9c958602c3e7b3efd6dee1f904cb3cf0e36b4f378b4f06b01a36c0dc808426)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
            check_type(argname="argument enable_resource_property_constraint", value=enable_resource_property_constraint, expected_type=type_hints["enable_resource_property_constraint"])
        jsii.create(self.__class__, self, [scope, id, props, enable_resource_property_constraint])

    @builtins.property
    @jsii.member(jsii_name="attrCustomDomains")
    def attr_custom_domains(self) -> _ros_cdk_core_7adfd82f.IResolvable:
        '''Attribute CustomDomains: The list of custom_domain.'''
        return typing.cast(_ros_cdk_core_7adfd82f.IResolvable, jsii.get(self, "attrCustomDomains"))

    @builtins.property
    @jsii.member(jsii_name="attrDomainNames")
    def attr_domain_names(self) -> _ros_cdk_core_7adfd82f.IResolvable:
        '''Attribute DomainNames: The list of custom_domain names.'''
        return typing.cast(_ros_cdk_core_7adfd82f.IResolvable, jsii.get(self, "attrDomainNames"))

    @builtins.property
    @jsii.member(jsii_name="enableResourcePropertyConstraint")
    def _enable_resource_property_constraint(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "enableResourcePropertyConstraint"))

    @_enable_resource_property_constraint.setter
    def _enable_resource_property_constraint(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a32faf6ee223de3d19551201d71fe36e9f6b3385f0fc1da61859ee21ee77da2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableResourcePropertyConstraint", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def _id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @_id.setter
    def _id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b477d5e78b74a3a1cbe5953ee0b1204ee3cfe218c15be058441e945736691e28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> "CustomDomainsProps":
        return typing.cast("CustomDomainsProps", jsii.get(self, "props"))

    @_props.setter
    def _props(self, value: "CustomDomainsProps") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a274d9b89064618442b8ad3ed121b10108baa6d55fad690293370e6cc9aac97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "props", value)

    @builtins.property
    @jsii.member(jsii_name="scope")
    def _scope(self) -> _ros_cdk_core_7adfd82f.Construct:
        return typing.cast(_ros_cdk_core_7adfd82f.Construct, jsii.get(self, "scope"))

    @_scope.setter
    def _scope(self, value: _ros_cdk_core_7adfd82f.Construct) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0aef34d6c7aa7f1fb4dc52750f7730aec02a277b3c15ee8b2c06eeb053f9aa05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value)


@jsii.data_type(
    jsii_type="@alicloud/ros-cdk-fc.datasource.CustomDomainsProps",
    jsii_struct_bases=[],
    name_mapping={"prefix": "prefix"},
)
class CustomDomainsProps:
    def __init__(
        self,
        *,
        prefix: typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]] = None,
    ) -> None:
        '''Properties for defining a ``CustomDomains``.

        See https://www.alibabacloud.com/help/ros/developer-reference/datasource-fc-customdomains

        :param prefix: Property prefix: Qualified returned custom domain names must be prefixed with Prefix. For example, if the Prefix is "a", the returned custom domain names should be started with "a".
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__605f228db674c8dff66be96784830ba286fbbd9eecc11a1ca13cb16881ec8457)
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def prefix(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]]:
        '''Property prefix: Qualified returned custom domain names must be prefixed with Prefix.

        For example, if the Prefix is "a", the returned custom domain names should be started with "a".
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomDomainsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Functions(
    _ros_cdk_core_7adfd82f.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@alicloud/ros-cdk-fc.datasource.Functions",
):
    '''This class encapsulates and extends the ROS resource type ``DATASOURCE::FC::Functions``, which is used to query functions.

    :Note:

    This class may have some new functions to facilitate development, so it is recommended to use this class instead of ``RosFunctions``for a more convenient development experience.
    See https://www.alibabacloud.com/help/ros/developer-reference/datasource-fc-functions
    '''

    def __init__(
        self,
        scope: _ros_cdk_core_7adfd82f.Construct,
        id: builtins.str,
        props: typing.Union["FunctionsProps", typing.Dict[builtins.str, typing.Any]],
        enable_resource_property_constraint: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Param scope - scope in which this resource is defined Param id    - scoped id of the resource Param props - resource properties.

        :param scope: -
        :param id: -
        :param props: -
        :param enable_resource_property_constraint: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1772103ac05d24ad595f5cfce123332b52efa00448817131f7d7f05abbf3f37)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
            check_type(argname="argument enable_resource_property_constraint", value=enable_resource_property_constraint, expected_type=type_hints["enable_resource_property_constraint"])
        jsii.create(self.__class__, self, [scope, id, props, enable_resource_property_constraint])

    @builtins.property
    @jsii.member(jsii_name="attrFunctionNames")
    def attr_function_names(self) -> _ros_cdk_core_7adfd82f.IResolvable:
        '''Attribute FunctionNames: The list of function names.'''
        return typing.cast(_ros_cdk_core_7adfd82f.IResolvable, jsii.get(self, "attrFunctionNames"))

    @builtins.property
    @jsii.member(jsii_name="attrFunctions")
    def attr_functions(self) -> _ros_cdk_core_7adfd82f.IResolvable:
        '''Attribute Functions: The list of functions.'''
        return typing.cast(_ros_cdk_core_7adfd82f.IResolvable, jsii.get(self, "attrFunctions"))

    @builtins.property
    @jsii.member(jsii_name="enableResourcePropertyConstraint")
    def _enable_resource_property_constraint(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "enableResourcePropertyConstraint"))

    @_enable_resource_property_constraint.setter
    def _enable_resource_property_constraint(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__239819977ecf4a0b98212c3c31cdb38ba3d3bb6bf1ff5b06db8ecd56f2fe298b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableResourcePropertyConstraint", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def _id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @_id.setter
    def _id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38129283cdf5a25e8c079ac2d41fc229cbc00a208f47c3a049baf515bb6025b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> "FunctionsProps":
        return typing.cast("FunctionsProps", jsii.get(self, "props"))

    @_props.setter
    def _props(self, value: "FunctionsProps") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fb0b23486f0a126d1a014bd92e6a3427efc8e76eb7973167229feab35a2cdb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "props", value)

    @builtins.property
    @jsii.member(jsii_name="scope")
    def _scope(self) -> _ros_cdk_core_7adfd82f.Construct:
        return typing.cast(_ros_cdk_core_7adfd82f.Construct, jsii.get(self, "scope"))

    @_scope.setter
    def _scope(self, value: _ros_cdk_core_7adfd82f.Construct) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c43949a6b8c445ccdc23c143c023fa1217c39a5530267fd8d5a4bcb126c6afc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value)


@jsii.data_type(
    jsii_type="@alicloud/ros-cdk-fc.datasource.FunctionsProps",
    jsii_struct_bases=[],
    name_mapping={
        "service_name": "serviceName",
        "prefix": "prefix",
        "qualifier": "qualifier",
    },
)
class FunctionsProps:
    def __init__(
        self,
        *,
        service_name: typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable],
        prefix: typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]] = None,
        qualifier: typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]] = None,
    ) -> None:
        '''Properties for defining a ``Functions``.

        See https://www.alibabacloud.com/help/ros/developer-reference/datasource-fc-functions

        :param service_name: Property serviceName: Service name.
        :param prefix: Property prefix: Qualified returned function names must be prefixed with Prefix. For example, if the Prefix is "a", the returned function names should be started with "a".
        :param qualifier: Property qualifier: The service version, which can be version ID or alias name.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d62ac56d32b68b62d7391c5a4b2baf78e50ee5c39305fec2e43a76843393f67e)
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            check_type(argname="argument qualifier", value=qualifier, expected_type=type_hints["qualifier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service_name": service_name,
        }
        if prefix is not None:
            self._values["prefix"] = prefix
        if qualifier is not None:
            self._values["qualifier"] = qualifier

    @builtins.property
    def service_name(
        self,
    ) -> typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]:
        '''Property serviceName: Service name.'''
        result = self._values.get("service_name")
        assert result is not None, "Required property 'service_name' is missing"
        return typing.cast(typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable], result)

    @builtins.property
    def prefix(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]]:
        '''Property prefix: Qualified returned function names must be prefixed with Prefix.

        For example, if the Prefix is "a", the returned function names should be started with "a".
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]], result)

    @builtins.property
    def qualifier(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]]:
        '''Property qualifier: The service version, which can be version ID or alias name.'''
        result = self._values.get("qualifier")
        return typing.cast(typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RosAliases(
    _ros_cdk_core_7adfd82f.RosResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@alicloud/ros-cdk-fc.datasource.RosAliases",
):
    '''This class is a base encapsulation around the ROS resource type ``DATASOURCE::FC::Aliases``, which is used to query the aliases of a Function Compute service.

    :Note:

    This class does not contain additional functions, so it is recommended to use the ``Aliases`` class instead of this class for a more convenient development experience.
    See https://www.alibabacloud.com/help/ros/developer-reference/datasource-fc-aliases
    '''

    def __init__(
        self,
        scope: _ros_cdk_core_7adfd82f.Construct,
        id: builtins.str,
        props: typing.Union["RosAliasesProps", typing.Dict[builtins.str, typing.Any]],
        enable_resource_property_constraint: builtins.bool,
    ) -> None:
        '''
        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param enable_resource_property_constraint: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7687867826cef27c259d4a4c712fe79cff6038089a3b237c259826fec77748d3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
            check_type(argname="argument enable_resource_property_constraint", value=enable_resource_property_constraint, expected_type=type_hints["enable_resource_property_constraint"])
        jsii.create(self.__class__, self, [scope, id, props, enable_resource_property_constraint])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95aa46e902ce81ea23fd2d8b586d925fb2a9b17ee05fac8796daab9213b74d83)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ROS_RESOURCE_TYPE_NAME")
    def ROS_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "ROS_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAliases")
    def attr_aliases(self) -> _ros_cdk_core_7adfd82f.IResolvable:
        '''
        :Attribute: Aliases: The list of aliases.
        '''
        return typing.cast(_ros_cdk_core_7adfd82f.IResolvable, jsii.get(self, "attrAliases"))

    @builtins.property
    @jsii.member(jsii_name="attrAliasNames")
    def attr_alias_names(self) -> _ros_cdk_core_7adfd82f.IResolvable:
        '''
        :Attribute: AliasNames: The list of alias names.
        '''
        return typing.cast(_ros_cdk_core_7adfd82f.IResolvable, jsii.get(self, "attrAliasNames"))

    @builtins.property
    @jsii.member(jsii_name="rosProperties")
    def _ros_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "rosProperties"))

    @builtins.property
    @jsii.member(jsii_name="enableResourcePropertyConstraint")
    def enable_resource_property_constraint(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "enableResourcePropertyConstraint"))

    @enable_resource_property_constraint.setter
    def enable_resource_property_constraint(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a70af20d5e11d7fb868682f1d40cc35eaa786f2ef7b829c5f91dbcc027f0c8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableResourcePropertyConstraint", value)

    @builtins.property
    @jsii.member(jsii_name="serviceName")
    def service_name(
        self,
    ) -> typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]:
        '''
        :Property: serviceName: Service name.
        '''
        return typing.cast(typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable], jsii.get(self, "serviceName"))

    @service_name.setter
    def service_name(
        self,
        value: typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b15ed8df84dc4cf9ef29a173c03e89cff65a48e3d82dc006e86db9682441a0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceName", value)

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]]:
        '''
        :Property: prefix: Qualified returned alias names must be prefixed with Prefix. For example, if the Prefix is "a", the returned alias names should be started with "a".
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]], jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(
        self,
        value: typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f1557e798a07cec0fb23ad741f93c91157ca0c3c4dfdcf528f2469cbe1909cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value)


@jsii.data_type(
    jsii_type="@alicloud/ros-cdk-fc.datasource.RosAliasesProps",
    jsii_struct_bases=[],
    name_mapping={"service_name": "serviceName", "prefix": "prefix"},
)
class RosAliasesProps:
    def __init__(
        self,
        *,
        service_name: typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable],
        prefix: typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]] = None,
    ) -> None:
        '''Properties for defining a ``RosAliases``.

        See https://www.alibabacloud.com/help/ros/developer-reference/datasource-fc-aliases

        :param service_name: 
        :param prefix: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__949fece33f4295db3eb34b6ae9c509ca5b23da8780c56a18100149cd673f8b09)
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service_name": service_name,
        }
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def service_name(
        self,
    ) -> typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]:
        '''
        :Property: serviceName: Service name.
        '''
        result = self._values.get("service_name")
        assert result is not None, "Required property 'service_name' is missing"
        return typing.cast(typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable], result)

    @builtins.property
    def prefix(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]]:
        '''
        :Property: prefix: Qualified returned alias names must be prefixed with Prefix. For example, if the Prefix is "a", the returned alias names should be started with "a".
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RosAliasesProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RosCustomDomains(
    _ros_cdk_core_7adfd82f.RosResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@alicloud/ros-cdk-fc.datasource.RosCustomDomains",
):
    '''This class is a base encapsulation around the ROS resource type ``DATASOURCE::FC::CustomDomains``, which is used to query custom domain names in Function Compute.

    :Note:

    This class does not contain additional functions, so it is recommended to use the ``CustomDomains`` class instead of this class for a more convenient development experience.
    See https://www.alibabacloud.com/help/ros/developer-reference/datasource-fc-customdomains
    '''

    def __init__(
        self,
        scope: _ros_cdk_core_7adfd82f.Construct,
        id: builtins.str,
        props: typing.Union["RosCustomDomainsProps", typing.Dict[builtins.str, typing.Any]],
        enable_resource_property_constraint: builtins.bool,
    ) -> None:
        '''
        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param enable_resource_property_constraint: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd504668a86cd4d9a50f23212fc1a0445194b59c824938f5c94f5e2a25af9ae4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
            check_type(argname="argument enable_resource_property_constraint", value=enable_resource_property_constraint, expected_type=type_hints["enable_resource_property_constraint"])
        jsii.create(self.__class__, self, [scope, id, props, enable_resource_property_constraint])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a053f0ac6f26cfa1ea46b5e4048bc0a33ccbce2490c6b93aefe6e2b33bfbf636)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ROS_RESOURCE_TYPE_NAME")
    def ROS_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "ROS_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrCustomDomains")
    def attr_custom_domains(self) -> _ros_cdk_core_7adfd82f.IResolvable:
        '''
        :Attribute: CustomDomains: The list of custom_domain.
        '''
        return typing.cast(_ros_cdk_core_7adfd82f.IResolvable, jsii.get(self, "attrCustomDomains"))

    @builtins.property
    @jsii.member(jsii_name="attrDomainNames")
    def attr_domain_names(self) -> _ros_cdk_core_7adfd82f.IResolvable:
        '''
        :Attribute: DomainNames: The list of custom_domain names.
        '''
        return typing.cast(_ros_cdk_core_7adfd82f.IResolvable, jsii.get(self, "attrDomainNames"))

    @builtins.property
    @jsii.member(jsii_name="rosProperties")
    def _ros_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "rosProperties"))

    @builtins.property
    @jsii.member(jsii_name="enableResourcePropertyConstraint")
    def enable_resource_property_constraint(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "enableResourcePropertyConstraint"))

    @enable_resource_property_constraint.setter
    def enable_resource_property_constraint(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0735fa75116312263fe92e43ada97104c2c2c4a90d7f09969fe8e63e3fce9a84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableResourcePropertyConstraint", value)

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]]:
        '''
        :Property: prefix: Qualified returned custom domain names must be prefixed with Prefix. For example, if the Prefix is "a", the returned custom domain names should be started with "a".
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]], jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(
        self,
        value: typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2ebe5001f6b4480657526fd5dc7b2407e13f014640494be3ded49c13c22c42e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value)


@jsii.data_type(
    jsii_type="@alicloud/ros-cdk-fc.datasource.RosCustomDomainsProps",
    jsii_struct_bases=[],
    name_mapping={"prefix": "prefix"},
)
class RosCustomDomainsProps:
    def __init__(
        self,
        *,
        prefix: typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]] = None,
    ) -> None:
        '''Properties for defining a ``RosCustomDomains``.

        See https://www.alibabacloud.com/help/ros/developer-reference/datasource-fc-customdomains

        :param prefix: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a125dd0495533ad729b28b21907c5058003d84012e5f9e2d4d1a90d75ca56b7e)
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def prefix(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]]:
        '''
        :Property: prefix: Qualified returned custom domain names must be prefixed with Prefix. For example, if the Prefix is "a", the returned custom domain names should be started with "a".
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RosCustomDomainsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RosFunctions(
    _ros_cdk_core_7adfd82f.RosResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@alicloud/ros-cdk-fc.datasource.RosFunctions",
):
    '''This class is a base encapsulation around the ROS resource type ``DATASOURCE::FC::Functions``, which is used to query functions.

    :Note:

    This class does not contain additional functions, so it is recommended to use the ``Functions`` class instead of this class for a more convenient development experience.
    See https://www.alibabacloud.com/help/ros/developer-reference/datasource-fc-functions
    '''

    def __init__(
        self,
        scope: _ros_cdk_core_7adfd82f.Construct,
        id: builtins.str,
        props: typing.Union["RosFunctionsProps", typing.Dict[builtins.str, typing.Any]],
        enable_resource_property_constraint: builtins.bool,
    ) -> None:
        '''
        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param enable_resource_property_constraint: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3227d2de5f356ef213b102b1786d7ae719d21fd8eaea96e3c375587544b03615)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
            check_type(argname="argument enable_resource_property_constraint", value=enable_resource_property_constraint, expected_type=type_hints["enable_resource_property_constraint"])
        jsii.create(self.__class__, self, [scope, id, props, enable_resource_property_constraint])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ce109d8b23e44de7e82e69cd86fd2730bcd8b6322b4c526bb501989f079afec)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ROS_RESOURCE_TYPE_NAME")
    def ROS_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "ROS_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrFunctionNames")
    def attr_function_names(self) -> _ros_cdk_core_7adfd82f.IResolvable:
        '''
        :Attribute: FunctionNames: The list of function names.
        '''
        return typing.cast(_ros_cdk_core_7adfd82f.IResolvable, jsii.get(self, "attrFunctionNames"))

    @builtins.property
    @jsii.member(jsii_name="attrFunctions")
    def attr_functions(self) -> _ros_cdk_core_7adfd82f.IResolvable:
        '''
        :Attribute: Functions: The list of functions.
        '''
        return typing.cast(_ros_cdk_core_7adfd82f.IResolvable, jsii.get(self, "attrFunctions"))

    @builtins.property
    @jsii.member(jsii_name="rosProperties")
    def _ros_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "rosProperties"))

    @builtins.property
    @jsii.member(jsii_name="enableResourcePropertyConstraint")
    def enable_resource_property_constraint(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "enableResourcePropertyConstraint"))

    @enable_resource_property_constraint.setter
    def enable_resource_property_constraint(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9906711945b99edf7784b9228df7e754d5324504ca36710600ce147727e40eab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableResourcePropertyConstraint", value)

    @builtins.property
    @jsii.member(jsii_name="serviceName")
    def service_name(
        self,
    ) -> typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]:
        '''
        :Property: serviceName: Service name.
        '''
        return typing.cast(typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable], jsii.get(self, "serviceName"))

    @service_name.setter
    def service_name(
        self,
        value: typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d67d16006e9a7bc1c9f839c8657a5eecae6644477df6ff0f8f69afe7ae1017b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceName", value)

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]]:
        '''
        :Property: prefix: Qualified returned function names must be prefixed with Prefix. For example, if the Prefix is "a", the returned function names should be started with "a".
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]], jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(
        self,
        value: typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da5d2ef85d6e516f9ee643b01dce4e3c34de5e65a8aa495ba79a6ba8fcf1de42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value)

    @builtins.property
    @jsii.member(jsii_name="qualifier")
    def qualifier(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]]:
        '''
        :Property: qualifier: The service version, which can be version ID or alias name.
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]], jsii.get(self, "qualifier"))

    @qualifier.setter
    def qualifier(
        self,
        value: typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7eeef71719218f9bde851879f5a90b1ebcb8306fb4cc5fa368227220862cf17d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "qualifier", value)


@jsii.data_type(
    jsii_type="@alicloud/ros-cdk-fc.datasource.RosFunctionsProps",
    jsii_struct_bases=[],
    name_mapping={
        "service_name": "serviceName",
        "prefix": "prefix",
        "qualifier": "qualifier",
    },
)
class RosFunctionsProps:
    def __init__(
        self,
        *,
        service_name: typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable],
        prefix: typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]] = None,
        qualifier: typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]] = None,
    ) -> None:
        '''Properties for defining a ``RosFunctions``.

        See https://www.alibabacloud.com/help/ros/developer-reference/datasource-fc-functions

        :param service_name: 
        :param prefix: 
        :param qualifier: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__716bb89a2ee68019026b5c4e6dbc468ce0f7484b804c6511213da6e7e72e11bd)
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            check_type(argname="argument qualifier", value=qualifier, expected_type=type_hints["qualifier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service_name": service_name,
        }
        if prefix is not None:
            self._values["prefix"] = prefix
        if qualifier is not None:
            self._values["qualifier"] = qualifier

    @builtins.property
    def service_name(
        self,
    ) -> typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]:
        '''
        :Property: serviceName: Service name.
        '''
        result = self._values.get("service_name")
        assert result is not None, "Required property 'service_name' is missing"
        return typing.cast(typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable], result)

    @builtins.property
    def prefix(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]]:
        '''
        :Property: prefix: Qualified returned function names must be prefixed with Prefix. For example, if the Prefix is "a", the returned function names should be started with "a".
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]], result)

    @builtins.property
    def qualifier(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]]:
        '''
        :Property: qualifier: The service version, which can be version ID or alias name.
        '''
        result = self._values.get("qualifier")
        return typing.cast(typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RosFunctionsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RosServices(
    _ros_cdk_core_7adfd82f.RosResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@alicloud/ros-cdk-fc.datasource.RosServices",
):
    '''This class is a base encapsulation around the ROS resource type ``DATASOURCE::FC::Services``, which is used to query services.

    :Note:

    This class does not contain additional functions, so it is recommended to use the ``Services`` class instead of this class for a more convenient development experience.
    See https://www.alibabacloud.com/help/ros/developer-reference/datasource-fc-services
    '''

    def __init__(
        self,
        scope: _ros_cdk_core_7adfd82f.Construct,
        id: builtins.str,
        props: typing.Union["RosServicesProps", typing.Dict[builtins.str, typing.Any]],
        enable_resource_property_constraint: builtins.bool,
    ) -> None:
        '''
        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param enable_resource_property_constraint: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2423ac51e1d23e9f14b734a6447f58ddb48e837e7da2869a825c79c2308ce48)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
            check_type(argname="argument enable_resource_property_constraint", value=enable_resource_property_constraint, expected_type=type_hints["enable_resource_property_constraint"])
        jsii.create(self.__class__, self, [scope, id, props, enable_resource_property_constraint])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6831febbcf131cacb4529c95ab4d15f4ce5b72d765750fe6dcfb80d39fdb813c)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ROS_RESOURCE_TYPE_NAME")
    def ROS_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "ROS_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrServiceNames")
    def attr_service_names(self) -> _ros_cdk_core_7adfd82f.IResolvable:
        '''
        :Attribute: ServiceNames: The list of service names.
        '''
        return typing.cast(_ros_cdk_core_7adfd82f.IResolvable, jsii.get(self, "attrServiceNames"))

    @builtins.property
    @jsii.member(jsii_name="attrServices")
    def attr_services(self) -> _ros_cdk_core_7adfd82f.IResolvable:
        '''
        :Attribute: Services: The list of services.
        '''
        return typing.cast(_ros_cdk_core_7adfd82f.IResolvable, jsii.get(self, "attrServices"))

    @builtins.property
    @jsii.member(jsii_name="rosProperties")
    def _ros_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "rosProperties"))

    @builtins.property
    @jsii.member(jsii_name="enableResourcePropertyConstraint")
    def enable_resource_property_constraint(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "enableResourcePropertyConstraint"))

    @enable_resource_property_constraint.setter
    def enable_resource_property_constraint(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c08cde0cdf8cb70d877544f6c2f0cc7e25ce412283238e83bc3fc4e63eaf657a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableResourcePropertyConstraint", value)

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]]:
        '''
        :Property: prefix: Qualified returned service names must be prefixed with Prefix. For example, if the Prefix is "a", the returned service names should be started with "a".
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]], jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(
        self,
        value: typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a74bbfc2cbc07085e22df1c2d0dd19e7be985b8d735dba3bf030912d8531b3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value)


@jsii.data_type(
    jsii_type="@alicloud/ros-cdk-fc.datasource.RosServicesProps",
    jsii_struct_bases=[],
    name_mapping={"prefix": "prefix"},
)
class RosServicesProps:
    def __init__(
        self,
        *,
        prefix: typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]] = None,
    ) -> None:
        '''Properties for defining a ``RosServices``.

        See https://www.alibabacloud.com/help/ros/developer-reference/datasource-fc-services

        :param prefix: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c70ec5f6200a00435652b36395a43a5bf4cac76db896127a90233c0f2aaa4bbf)
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def prefix(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]]:
        '''
        :Property: prefix: Qualified returned service names must be prefixed with Prefix. For example, if the Prefix is "a", the returned service names should be started with "a".
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RosServicesProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RosTriggers(
    _ros_cdk_core_7adfd82f.RosResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@alicloud/ros-cdk-fc.datasource.RosTriggers",
):
    '''This class is a base encapsulation around the ROS resource type ``DATASOURCE::FC::Triggers``, which is used to query triggers.

    :Note:

    This class does not contain additional functions, so it is recommended to use the ``Triggers`` class instead of this class for a more convenient development experience.
    See https://www.alibabacloud.com/help/ros/developer-reference/datasource-fc-triggers
    '''

    def __init__(
        self,
        scope: _ros_cdk_core_7adfd82f.Construct,
        id: builtins.str,
        props: typing.Union["RosTriggersProps", typing.Dict[builtins.str, typing.Any]],
        enable_resource_property_constraint: builtins.bool,
    ) -> None:
        '''
        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param enable_resource_property_constraint: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__294763ce4c3594cef5560c9e023a0a156867258ef5c04fb916f2fc8dc425e6cd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
            check_type(argname="argument enable_resource_property_constraint", value=enable_resource_property_constraint, expected_type=type_hints["enable_resource_property_constraint"])
        jsii.create(self.__class__, self, [scope, id, props, enable_resource_property_constraint])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f3bf1a44ad7b26267eabdc88c8cadba637583ee6c5bf0ed1b4fb43a544ed64b)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ROS_RESOURCE_TYPE_NAME")
    def ROS_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "ROS_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrTriggerNames")
    def attr_trigger_names(self) -> _ros_cdk_core_7adfd82f.IResolvable:
        '''
        :Attribute: TriggerNames: The list of trigger names.
        '''
        return typing.cast(_ros_cdk_core_7adfd82f.IResolvable, jsii.get(self, "attrTriggerNames"))

    @builtins.property
    @jsii.member(jsii_name="attrTriggers")
    def attr_triggers(self) -> _ros_cdk_core_7adfd82f.IResolvable:
        '''
        :Attribute: Triggers: The list of triggers.
        '''
        return typing.cast(_ros_cdk_core_7adfd82f.IResolvable, jsii.get(self, "attrTriggers"))

    @builtins.property
    @jsii.member(jsii_name="rosProperties")
    def _ros_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "rosProperties"))

    @builtins.property
    @jsii.member(jsii_name="enableResourcePropertyConstraint")
    def enable_resource_property_constraint(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "enableResourcePropertyConstraint"))

    @enable_resource_property_constraint.setter
    def enable_resource_property_constraint(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__897e0eea90a47242b81865548cbd9c12e78e266513decbaa4bf80d522cc7440f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableResourcePropertyConstraint", value)

    @builtins.property
    @jsii.member(jsii_name="functionName")
    def function_name(
        self,
    ) -> typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]:
        '''
        :Property: functionName: Function name.
        '''
        return typing.cast(typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable], jsii.get(self, "functionName"))

    @function_name.setter
    def function_name(
        self,
        value: typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__532f7ae9617b484aac3dd135ece45adfc4054a5f7114ac3c608adc2f41c79923)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functionName", value)

    @builtins.property
    @jsii.member(jsii_name="serviceName")
    def service_name(
        self,
    ) -> typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]:
        '''
        :Property: serviceName: Service name.
        '''
        return typing.cast(typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable], jsii.get(self, "serviceName"))

    @service_name.setter
    def service_name(
        self,
        value: typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de7f95df6778116f217676a497fa2c9aaa9d3dccfd387a362b4f31e757cd80eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceName", value)

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]]:
        '''
        :Property: prefix: Qualified returned trigger names must be prefixed with Prefix. For example, if the Prefix is "a", the returned trigger names should be started with "a".
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]], jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(
        self,
        value: typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__728534bbf295eae7eb51615a91602046988e198a1837f3620dd39ed51f52e866)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value)


@jsii.data_type(
    jsii_type="@alicloud/ros-cdk-fc.datasource.RosTriggersProps",
    jsii_struct_bases=[],
    name_mapping={
        "function_name": "functionName",
        "service_name": "serviceName",
        "prefix": "prefix",
    },
)
class RosTriggersProps:
    def __init__(
        self,
        *,
        function_name: typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable],
        service_name: typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable],
        prefix: typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]] = None,
    ) -> None:
        '''Properties for defining a ``RosTriggers``.

        See https://www.alibabacloud.com/help/ros/developer-reference/datasource-fc-triggers

        :param function_name: 
        :param service_name: 
        :param prefix: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59180312e3315d67661586ddd2b3631bb5772644dc40e389ed4b9444b5faf99f)
            check_type(argname="argument function_name", value=function_name, expected_type=type_hints["function_name"])
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "function_name": function_name,
            "service_name": service_name,
        }
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def function_name(
        self,
    ) -> typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]:
        '''
        :Property: functionName: Function name.
        '''
        result = self._values.get("function_name")
        assert result is not None, "Required property 'function_name' is missing"
        return typing.cast(typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable], result)

    @builtins.property
    def service_name(
        self,
    ) -> typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]:
        '''
        :Property: serviceName: Service name.
        '''
        result = self._values.get("service_name")
        assert result is not None, "Required property 'service_name' is missing"
        return typing.cast(typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable], result)

    @builtins.property
    def prefix(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]]:
        '''
        :Property: prefix: Qualified returned trigger names must be prefixed with Prefix. For example, if the Prefix is "a", the returned trigger names should be started with "a".
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RosTriggersProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Services(
    _ros_cdk_core_7adfd82f.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@alicloud/ros-cdk-fc.datasource.Services",
):
    '''This class encapsulates and extends the ROS resource type ``DATASOURCE::FC::Services``, which is used to query services.

    :Note:

    This class may have some new functions to facilitate development, so it is recommended to use this class instead of ``RosServices``for a more convenient development experience.
    See https://www.alibabacloud.com/help/ros/developer-reference/datasource-fc-services
    '''

    def __init__(
        self,
        scope: _ros_cdk_core_7adfd82f.Construct,
        id: builtins.str,
        props: typing.Optional[typing.Union["ServicesProps", typing.Dict[builtins.str, typing.Any]]] = None,
        enable_resource_property_constraint: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Param scope - scope in which this resource is defined Param id    - scoped id of the resource Param props - resource properties.

        :param scope: -
        :param id: -
        :param props: -
        :param enable_resource_property_constraint: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa9b5e0637dd81ac886db77377afb9cbeadf8631649e51ebcc95cf17a7e66ce4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
            check_type(argname="argument enable_resource_property_constraint", value=enable_resource_property_constraint, expected_type=type_hints["enable_resource_property_constraint"])
        jsii.create(self.__class__, self, [scope, id, props, enable_resource_property_constraint])

    @builtins.property
    @jsii.member(jsii_name="attrServiceNames")
    def attr_service_names(self) -> _ros_cdk_core_7adfd82f.IResolvable:
        '''Attribute ServiceNames: The list of service names.'''
        return typing.cast(_ros_cdk_core_7adfd82f.IResolvable, jsii.get(self, "attrServiceNames"))

    @builtins.property
    @jsii.member(jsii_name="attrServices")
    def attr_services(self) -> _ros_cdk_core_7adfd82f.IResolvable:
        '''Attribute Services: The list of services.'''
        return typing.cast(_ros_cdk_core_7adfd82f.IResolvable, jsii.get(self, "attrServices"))

    @builtins.property
    @jsii.member(jsii_name="enableResourcePropertyConstraint")
    def _enable_resource_property_constraint(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "enableResourcePropertyConstraint"))

    @_enable_resource_property_constraint.setter
    def _enable_resource_property_constraint(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03370fa1603a2462178dfc9c05a5601347d1bc6c93325edc650a83d4c70dd2ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableResourcePropertyConstraint", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def _id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @_id.setter
    def _id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8339683061b365802572d234aca072aba6262f8ed8418030d0d42e395704e7e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> "ServicesProps":
        return typing.cast("ServicesProps", jsii.get(self, "props"))

    @_props.setter
    def _props(self, value: "ServicesProps") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f23a1f47fbee42acbe87185c85f3d53cad87057a88eaa2dad03aa027e15c39ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "props", value)

    @builtins.property
    @jsii.member(jsii_name="scope")
    def _scope(self) -> _ros_cdk_core_7adfd82f.Construct:
        return typing.cast(_ros_cdk_core_7adfd82f.Construct, jsii.get(self, "scope"))

    @_scope.setter
    def _scope(self, value: _ros_cdk_core_7adfd82f.Construct) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0166d752ad89e853ff3d134b3635fab88968e173a5f2e7ad07a5c8849ea27cfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value)


@jsii.data_type(
    jsii_type="@alicloud/ros-cdk-fc.datasource.ServicesProps",
    jsii_struct_bases=[],
    name_mapping={"prefix": "prefix"},
)
class ServicesProps:
    def __init__(
        self,
        *,
        prefix: typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]] = None,
    ) -> None:
        '''Properties for defining a ``Services``.

        See https://www.alibabacloud.com/help/ros/developer-reference/datasource-fc-services

        :param prefix: Property prefix: Qualified returned service names must be prefixed with Prefix. For example, if the Prefix is "a", the returned service names should be started with "a".
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e47bd2faa8202e38e5db91015c9b7451e2949829524463b61058d70fb22b97ed)
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def prefix(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]]:
        '''Property prefix: Qualified returned service names must be prefixed with Prefix.

        For example, if the Prefix is "a", the returned service names should be started with "a".
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServicesProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Triggers(
    _ros_cdk_core_7adfd82f.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@alicloud/ros-cdk-fc.datasource.Triggers",
):
    '''This class encapsulates and extends the ROS resource type ``DATASOURCE::FC::Triggers``, which is used to query triggers.

    :Note:

    This class may have some new functions to facilitate development, so it is recommended to use this class instead of ``RosTriggers``for a more convenient development experience.
    See https://www.alibabacloud.com/help/ros/developer-reference/datasource-fc-triggers
    '''

    def __init__(
        self,
        scope: _ros_cdk_core_7adfd82f.Construct,
        id: builtins.str,
        props: typing.Union["TriggersProps", typing.Dict[builtins.str, typing.Any]],
        enable_resource_property_constraint: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Param scope - scope in which this resource is defined Param id    - scoped id of the resource Param props - resource properties.

        :param scope: -
        :param id: -
        :param props: -
        :param enable_resource_property_constraint: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d30a6d0f959bac1b13033ba0b4eab4c46c396f29037115944abbec64ee548bee)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
            check_type(argname="argument enable_resource_property_constraint", value=enable_resource_property_constraint, expected_type=type_hints["enable_resource_property_constraint"])
        jsii.create(self.__class__, self, [scope, id, props, enable_resource_property_constraint])

    @builtins.property
    @jsii.member(jsii_name="attrTriggerNames")
    def attr_trigger_names(self) -> _ros_cdk_core_7adfd82f.IResolvable:
        '''Attribute TriggerNames: The list of trigger names.'''
        return typing.cast(_ros_cdk_core_7adfd82f.IResolvable, jsii.get(self, "attrTriggerNames"))

    @builtins.property
    @jsii.member(jsii_name="attrTriggers")
    def attr_triggers(self) -> _ros_cdk_core_7adfd82f.IResolvable:
        '''Attribute Triggers: The list of triggers.'''
        return typing.cast(_ros_cdk_core_7adfd82f.IResolvable, jsii.get(self, "attrTriggers"))

    @builtins.property
    @jsii.member(jsii_name="enableResourcePropertyConstraint")
    def _enable_resource_property_constraint(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "enableResourcePropertyConstraint"))

    @_enable_resource_property_constraint.setter
    def _enable_resource_property_constraint(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e925a498f53dcf038ebefc32361c891490775f731187c95bf61597ecf0307432)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableResourcePropertyConstraint", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def _id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @_id.setter
    def _id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__978f8aa4c8865491c0769a99b6de38387cbbb034d769cec0ebc67b7f470ae807)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> "TriggersProps":
        return typing.cast("TriggersProps", jsii.get(self, "props"))

    @_props.setter
    def _props(self, value: "TriggersProps") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c83d0a552b19979e695689e4c72368c0baae90bb067af3206548ae922ea11f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "props", value)

    @builtins.property
    @jsii.member(jsii_name="scope")
    def _scope(self) -> _ros_cdk_core_7adfd82f.Construct:
        return typing.cast(_ros_cdk_core_7adfd82f.Construct, jsii.get(self, "scope"))

    @_scope.setter
    def _scope(self, value: _ros_cdk_core_7adfd82f.Construct) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f14edd5efc18a2b66dc3d9688861850a544c2f9b89de1a31dd103f5f26a4a86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value)


@jsii.data_type(
    jsii_type="@alicloud/ros-cdk-fc.datasource.TriggersProps",
    jsii_struct_bases=[],
    name_mapping={
        "function_name": "functionName",
        "service_name": "serviceName",
        "prefix": "prefix",
    },
)
class TriggersProps:
    def __init__(
        self,
        *,
        function_name: typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable],
        service_name: typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable],
        prefix: typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]] = None,
    ) -> None:
        '''Properties for defining a ``Triggers``.

        See https://www.alibabacloud.com/help/ros/developer-reference/datasource-fc-triggers

        :param function_name: Property functionName: Function name.
        :param service_name: Property serviceName: Service name.
        :param prefix: Property prefix: Qualified returned trigger names must be prefixed with Prefix. For example, if the Prefix is "a", the returned trigger names should be started with "a".
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be9587bd858a19d8c74e0f6a91e935bdaca8c283d4ed2324fb359afca9b0ae0f)
            check_type(argname="argument function_name", value=function_name, expected_type=type_hints["function_name"])
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "function_name": function_name,
            "service_name": service_name,
        }
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def function_name(
        self,
    ) -> typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]:
        '''Property functionName: Function name.'''
        result = self._values.get("function_name")
        assert result is not None, "Required property 'function_name' is missing"
        return typing.cast(typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable], result)

    @builtins.property
    def service_name(
        self,
    ) -> typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]:
        '''Property serviceName: Service name.'''
        result = self._values.get("service_name")
        assert result is not None, "Required property 'service_name' is missing"
        return typing.cast(typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable], result)

    @builtins.property
    def prefix(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]]:
        '''Property prefix: Qualified returned trigger names must be prefixed with Prefix.

        For example, if the Prefix is "a", the returned trigger names should be started with "a".
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TriggersProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Aliases",
    "AliasesProps",
    "CustomDomains",
    "CustomDomainsProps",
    "Functions",
    "FunctionsProps",
    "RosAliases",
    "RosAliasesProps",
    "RosCustomDomains",
    "RosCustomDomainsProps",
    "RosFunctions",
    "RosFunctionsProps",
    "RosServices",
    "RosServicesProps",
    "RosTriggers",
    "RosTriggersProps",
    "Services",
    "ServicesProps",
    "Triggers",
    "TriggersProps",
]

publication.publish()

def _typecheckingstub__406fba9975ae133f6a89b76c08618f3ca89aac2c7b47a51887e7e3479c656bb7(
    scope: _ros_cdk_core_7adfd82f.Construct,
    id: builtins.str,
    props: typing.Union[AliasesProps, typing.Dict[builtins.str, typing.Any]],
    enable_resource_property_constraint: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__149c1188224a96f687044b73122acf933aec8842ec077423116ff7764e21d1ce(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8f1f8f7bd925d9d607fc44bb702e63db3ab38a28f1f467d633095eb192365c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdab1691db15a10bdc1a357dbd17816530c1fdf0ef77ca7935440e9629782c0c(
    value: AliasesProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da66925fee8c67f7f226464a7d611303476ade2b5479186ddbdc6d88fc0bd5e0(
    value: _ros_cdk_core_7adfd82f.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58cc243b6cc0f45e7eecfa347337ef658b839368e9d006ccc3799fb43d2c591b(
    *,
    service_name: typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable],
    prefix: typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b9c958602c3e7b3efd6dee1f904cb3cf0e36b4f378b4f06b01a36c0dc808426(
    scope: _ros_cdk_core_7adfd82f.Construct,
    id: builtins.str,
    props: typing.Optional[typing.Union[CustomDomainsProps, typing.Dict[builtins.str, typing.Any]]] = None,
    enable_resource_property_constraint: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a32faf6ee223de3d19551201d71fe36e9f6b3385f0fc1da61859ee21ee77da2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b477d5e78b74a3a1cbe5953ee0b1204ee3cfe218c15be058441e945736691e28(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a274d9b89064618442b8ad3ed121b10108baa6d55fad690293370e6cc9aac97(
    value: CustomDomainsProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aef34d6c7aa7f1fb4dc52750f7730aec02a277b3c15ee8b2c06eeb053f9aa05(
    value: _ros_cdk_core_7adfd82f.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__605f228db674c8dff66be96784830ba286fbbd9eecc11a1ca13cb16881ec8457(
    *,
    prefix: typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1772103ac05d24ad595f5cfce123332b52efa00448817131f7d7f05abbf3f37(
    scope: _ros_cdk_core_7adfd82f.Construct,
    id: builtins.str,
    props: typing.Union[FunctionsProps, typing.Dict[builtins.str, typing.Any]],
    enable_resource_property_constraint: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__239819977ecf4a0b98212c3c31cdb38ba3d3bb6bf1ff5b06db8ecd56f2fe298b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38129283cdf5a25e8c079ac2d41fc229cbc00a208f47c3a049baf515bb6025b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fb0b23486f0a126d1a014bd92e6a3427efc8e76eb7973167229feab35a2cdb0(
    value: FunctionsProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c43949a6b8c445ccdc23c143c023fa1217c39a5530267fd8d5a4bcb126c6afc(
    value: _ros_cdk_core_7adfd82f.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d62ac56d32b68b62d7391c5a4b2baf78e50ee5c39305fec2e43a76843393f67e(
    *,
    service_name: typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable],
    prefix: typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]] = None,
    qualifier: typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7687867826cef27c259d4a4c712fe79cff6038089a3b237c259826fec77748d3(
    scope: _ros_cdk_core_7adfd82f.Construct,
    id: builtins.str,
    props: typing.Union[RosAliasesProps, typing.Dict[builtins.str, typing.Any]],
    enable_resource_property_constraint: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95aa46e902ce81ea23fd2d8b586d925fb2a9b17ee05fac8796daab9213b74d83(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a70af20d5e11d7fb868682f1d40cc35eaa786f2ef7b829c5f91dbcc027f0c8c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b15ed8df84dc4cf9ef29a173c03e89cff65a48e3d82dc006e86db9682441a0f(
    value: typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f1557e798a07cec0fb23ad741f93c91157ca0c3c4dfdcf528f2469cbe1909cd(
    value: typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__949fece33f4295db3eb34b6ae9c509ca5b23da8780c56a18100149cd673f8b09(
    *,
    service_name: typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable],
    prefix: typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd504668a86cd4d9a50f23212fc1a0445194b59c824938f5c94f5e2a25af9ae4(
    scope: _ros_cdk_core_7adfd82f.Construct,
    id: builtins.str,
    props: typing.Union[RosCustomDomainsProps, typing.Dict[builtins.str, typing.Any]],
    enable_resource_property_constraint: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a053f0ac6f26cfa1ea46b5e4048bc0a33ccbce2490c6b93aefe6e2b33bfbf636(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0735fa75116312263fe92e43ada97104c2c2c4a90d7f09969fe8e63e3fce9a84(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2ebe5001f6b4480657526fd5dc7b2407e13f014640494be3ded49c13c22c42e(
    value: typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a125dd0495533ad729b28b21907c5058003d84012e5f9e2d4d1a90d75ca56b7e(
    *,
    prefix: typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3227d2de5f356ef213b102b1786d7ae719d21fd8eaea96e3c375587544b03615(
    scope: _ros_cdk_core_7adfd82f.Construct,
    id: builtins.str,
    props: typing.Union[RosFunctionsProps, typing.Dict[builtins.str, typing.Any]],
    enable_resource_property_constraint: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ce109d8b23e44de7e82e69cd86fd2730bcd8b6322b4c526bb501989f079afec(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9906711945b99edf7784b9228df7e754d5324504ca36710600ce147727e40eab(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d67d16006e9a7bc1c9f839c8657a5eecae6644477df6ff0f8f69afe7ae1017b0(
    value: typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da5d2ef85d6e516f9ee643b01dce4e3c34de5e65a8aa495ba79a6ba8fcf1de42(
    value: typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7eeef71719218f9bde851879f5a90b1ebcb8306fb4cc5fa368227220862cf17d(
    value: typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__716bb89a2ee68019026b5c4e6dbc468ce0f7484b804c6511213da6e7e72e11bd(
    *,
    service_name: typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable],
    prefix: typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]] = None,
    qualifier: typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2423ac51e1d23e9f14b734a6447f58ddb48e837e7da2869a825c79c2308ce48(
    scope: _ros_cdk_core_7adfd82f.Construct,
    id: builtins.str,
    props: typing.Union[RosServicesProps, typing.Dict[builtins.str, typing.Any]],
    enable_resource_property_constraint: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6831febbcf131cacb4529c95ab4d15f4ce5b72d765750fe6dcfb80d39fdb813c(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c08cde0cdf8cb70d877544f6c2f0cc7e25ce412283238e83bc3fc4e63eaf657a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a74bbfc2cbc07085e22df1c2d0dd19e7be985b8d735dba3bf030912d8531b3e(
    value: typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c70ec5f6200a00435652b36395a43a5bf4cac76db896127a90233c0f2aaa4bbf(
    *,
    prefix: typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__294763ce4c3594cef5560c9e023a0a156867258ef5c04fb916f2fc8dc425e6cd(
    scope: _ros_cdk_core_7adfd82f.Construct,
    id: builtins.str,
    props: typing.Union[RosTriggersProps, typing.Dict[builtins.str, typing.Any]],
    enable_resource_property_constraint: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f3bf1a44ad7b26267eabdc88c8cadba637583ee6c5bf0ed1b4fb43a544ed64b(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__897e0eea90a47242b81865548cbd9c12e78e266513decbaa4bf80d522cc7440f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__532f7ae9617b484aac3dd135ece45adfc4054a5f7114ac3c608adc2f41c79923(
    value: typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de7f95df6778116f217676a497fa2c9aaa9d3dccfd387a362b4f31e757cd80eb(
    value: typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__728534bbf295eae7eb51615a91602046988e198a1837f3620dd39ed51f52e866(
    value: typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59180312e3315d67661586ddd2b3631bb5772644dc40e389ed4b9444b5faf99f(
    *,
    function_name: typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable],
    service_name: typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable],
    prefix: typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa9b5e0637dd81ac886db77377afb9cbeadf8631649e51ebcc95cf17a7e66ce4(
    scope: _ros_cdk_core_7adfd82f.Construct,
    id: builtins.str,
    props: typing.Optional[typing.Union[ServicesProps, typing.Dict[builtins.str, typing.Any]]] = None,
    enable_resource_property_constraint: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03370fa1603a2462178dfc9c05a5601347d1bc6c93325edc650a83d4c70dd2ab(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8339683061b365802572d234aca072aba6262f8ed8418030d0d42e395704e7e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f23a1f47fbee42acbe87185c85f3d53cad87057a88eaa2dad03aa027e15c39ee(
    value: ServicesProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0166d752ad89e853ff3d134b3635fab88968e173a5f2e7ad07a5c8849ea27cfd(
    value: _ros_cdk_core_7adfd82f.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e47bd2faa8202e38e5db91015c9b7451e2949829524463b61058d70fb22b97ed(
    *,
    prefix: typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d30a6d0f959bac1b13033ba0b4eab4c46c396f29037115944abbec64ee548bee(
    scope: _ros_cdk_core_7adfd82f.Construct,
    id: builtins.str,
    props: typing.Union[TriggersProps, typing.Dict[builtins.str, typing.Any]],
    enable_resource_property_constraint: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e925a498f53dcf038ebefc32361c891490775f731187c95bf61597ecf0307432(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__978f8aa4c8865491c0769a99b6de38387cbbb034d769cec0ebc67b7f470ae807(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c83d0a552b19979e695689e4c72368c0baae90bb067af3206548ae922ea11f9(
    value: TriggersProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f14edd5efc18a2b66dc3d9688861850a544c2f9b89de1a31dd103f5f26a4a86(
    value: _ros_cdk_core_7adfd82f.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be9587bd858a19d8c74e0f6a91e935bdaca8c283d4ed2324fb359afca9b0ae0f(
    *,
    function_name: typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable],
    service_name: typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable],
    prefix: typing.Optional[typing.Union[builtins.str, _ros_cdk_core_7adfd82f.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

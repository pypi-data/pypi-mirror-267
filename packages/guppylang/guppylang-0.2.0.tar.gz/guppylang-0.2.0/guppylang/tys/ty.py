from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass, field
from functools import cached_property
from typing import TYPE_CHECKING, TypeAlias, cast

from guppylang.error import InternalGuppyError
from guppylang.hugr import tys
from guppylang.hugr.tys import TypeBound
from guppylang.tys.arg import Argument, ConstArg, TypeArg
from guppylang.tys.common import ToHugr, Transformable, Transformer, Visitor
from guppylang.tys.const import ExistentialConstVar
from guppylang.tys.param import Parameter
from guppylang.tys.var import BoundVar, ExistentialVar

if TYPE_CHECKING:
    from guppylang.tys.definition import OpaqueTypeDef
    from guppylang.tys.subst import Inst, Subst


@dataclass(frozen=True)
class TypeBase(ToHugr[tys.Type], Transformable["Type"], ABC):
    """Abstract base class for all Guppy types.

    Note that all subclasses are expected to be immutable.
    """

    @cached_property
    @abstractmethod
    def linear(self) -> bool:
        """Whether this type should be treated linearly."""

    @cached_property
    @abstractmethod
    def hugr_bound(self) -> tys.TypeBound:
        """The Hugr bound of this type, i.e. `Any`, `Copyable`, or `Equatable`.

        This needs to be specified explicitly, since opaque nonlinear types in a Hugr
        extension could be either declared as copyable or equatable. If we don't get the
        bound exactly right during serialisation, the Hugr validator will complain.
        """

    @cached_property
    def unsolved_vars(self) -> set[ExistentialVar]:
        """The existential type variables contained in this type."""
        return set()

    def substitute(self, subst: "Subst") -> "Type":
        """Substitutes existential variables in this type."""
        from guppylang.tys.subst import Substituter

        return self.transform(Substituter(subst))

    def __str__(self) -> str:
        """Returns a human-readable representation of the type."""
        from guppylang.tys.printing import TypePrinter

        # We use a custom printer that takes care of inserting parentheses and choosing
        # unique names
        return TypePrinter().visit(cast(Type, self))


@dataclass(frozen=True)
class ParametrizedTypeBase(TypeBase, ABC):
    """Abstract base class for types that depend on parameters.

    For example, `list`, `tuple`, etc. require arguments in order to be turned into a
    proper type.

    Note that all subclasses are expected to be immutable.
    """

    args: Sequence[Argument]

    def __post_init__(self) -> None:
        # Make sure that we don't have nested generic functions
        for arg in self.args:
            match arg:
                case TypeArg(ty=FunctionType(parametrized=True)):
                    raise InternalGuppyError(
                        "Tried to construct a higher-rank polymorphic type!"
                    )

    @property
    @abstractmethod
    def intrinsically_linear(self) -> bool:
        """Whether this type is linear, independent of the arguments.

        For example, a parametrized struct containing a qubit is linear, no matter what
        the arguments are.
        """

    @cached_property
    def linear(self) -> bool:
        """Whether this type should be treated linearly."""
        return self.intrinsically_linear or any(
            isinstance(arg, TypeArg) and arg.ty.linear for arg in self.args
        )

    @cached_property
    def unsolved_vars(self) -> set[ExistentialVar]:
        """The existential type variables contained in this type."""
        unsolved = set()
        for arg in self.args:
            match arg:
                case TypeArg(ty):
                    unsolved |= ty.unsolved_vars
                case ConstArg(c) if isinstance(c, ExistentialConstVar):
                    unsolved.add(c)
        return unsolved

    @cached_property
    def hugr_bound(self) -> tys.TypeBound:
        """The Hugr bound of this type, i.e. `Any`, `Copyable`, or `Equatable`."""
        if self.linear:
            return tys.TypeBound.Any
        return tys.TypeBound.join(
            *(arg.ty.hugr_bound for arg in self.args if isinstance(arg, TypeArg))
        )

    def visit(self, visitor: Visitor) -> None:
        """Accepts a visitor on this type."""
        if not visitor.visit(self):
            for arg in self.args:
                visitor.visit(arg)


@dataclass(frozen=True)
class BoundTypeVar(TypeBase, BoundVar):
    """Bound type variable, referencing a parameter of kind `Type`.

    For example, in the function type `forall T. list[T] -> T` we represent `T` as a
    `BoundTypeVar(idx=0)`.

    A bound type variables can be instantiated with a `TypeArg` argument.
    """

    linear: bool

    @cached_property
    def hugr_bound(self) -> tys.TypeBound:
        """The Hugr bound of this type, i.e. `Any`, `Copyable`, or `Equatable`."""
        if self.linear:
            return TypeBound.Any
        # We're conservative and don't require equatability for non-linear variables.
        # This is fine since Guppy doesn't use the equatable feature anyways.
        return TypeBound.Copyable

    def to_hugr(self) -> tys.Type:
        """Computes the Hugr representation of the type."""
        return tys.Variable(i=self.idx, b=self.hugr_bound)

    def visit(self, visitor: Visitor) -> None:
        """Accepts a visitor on this type."""
        visitor.visit(self)

    def transform(self, transformer: Transformer) -> "Type":
        """Accepts a transformer on this type."""
        return transformer.transform(self) or self

    def __str__(self) -> str:
        """Returns a human-readable representation of the type."""
        return self.display_name


@dataclass(frozen=True)
class ExistentialTypeVar(ExistentialVar, TypeBase):
    """Existential type variable.

    For example, the empty list literal `[]` is typed as `list[?T]` where `?T` stands
    for an existential type variable.

    During type checking we try to solve all existential type variables and substitute
    them with concrete types.
    """

    linear: bool

    @classmethod
    def fresh(cls, display_name: str, linear: bool) -> "ExistentialTypeVar":
        return ExistentialTypeVar(display_name, next(cls._fresh_id), linear)

    @cached_property
    def unsolved_vars(self) -> set[ExistentialVar]:
        """The existential type variables contained in this type."""
        return {self}

    @cached_property
    def hugr_bound(self) -> tys.TypeBound:
        """The Hugr bound of this type, i.e. `Any`, `Copyable`, or `Equatable`."""
        raise InternalGuppyError(
            "Tried to compute bound of unsolved existential type variable"
        )

    def to_hugr(self) -> tys.Type:
        """Computes the Hugr representation of the type."""
        raise InternalGuppyError(
            "Tried to convert unsolved existential type variable to Hugr"
        )

    def visit(self, visitor: Visitor) -> None:
        """Accepts a visitor on this type."""
        visitor.visit(self)

    def transform(self, transformer: Transformer) -> "Type":
        """Accepts a transformer on this type."""
        return transformer.transform(self) or self


@dataclass(frozen=True)
class NoneType(TypeBase):
    """Type of tuples."""

    linear: bool = field(default=False, init=False)
    hugr_bound: tys.TypeBound = field(default=tys.TypeBound.Eq, init=False)

    # Flag to avoid turning the type into a row when calling `type_to_row()`. This is
    # used to make sure that type vars instantiated to Nones are not broken up into
    # empty rows when generating a Hugr
    preserve: bool = field(default=False, compare=False)

    def to_hugr(self) -> tys.Type:
        """Computes the Hugr representation of the type."""
        return tys.TupleType(inner=[])

    def visit(self, visitor: Visitor) -> None:
        """Accepts a visitor on this type."""
        visitor.visit(self)

    def transform(self, transformer: Transformer) -> "Type":
        """Accepts a transformer on this type."""
        return transformer.transform(self) or self


@dataclass(frozen=True, init=False)
class FunctionType(ParametrizedTypeBase):
    """Type of (potentially generic) functions."""

    inputs: Sequence["Type"]
    output: "Type"
    params: Sequence[Parameter]
    input_names: Sequence[str] | None

    args: Sequence[Argument] = field(init=False)
    linear: bool = field(default=False, init=False)
    intrinsically_linear: bool = field(default=False, init=False)
    hugr_bound: tys.TypeBound = field(default=TypeBound.Copyable, init=False)

    def __init__(
        self,
        inputs: Sequence["Type"],
        output: "Type",
        input_names: Sequence[str] | None = None,
        params: Sequence[Parameter] | None = None,
    ) -> None:
        # We need a custom __init__ to set the args
        args = [TypeArg(ty) for ty in inputs]
        args.append(TypeArg(output))
        object.__setattr__(self, "args", args)
        object.__setattr__(self, "inputs", inputs)
        object.__setattr__(self, "output", output)
        object.__setattr__(self, "input_names", input_names or [])
        object.__setattr__(self, "params", params or [])

    @property
    def parametrized(self) -> bool:
        """Whether the function is parametrized."""
        return len(self.params) > 0

    def to_hugr(self) -> tys.Type:
        """Computes the Hugr representation of the type."""
        ins = [t.to_hugr() for t in self.inputs]
        outs = [t.to_hugr() for t in type_to_row(self.output)]
        func_ty = tys.FunctionType(input=ins, output=outs, extension_reqs=[])
        return tys.PolyFuncType(params=[p.to_hugr() for p in self.params], body=func_ty)

    def visit(self, visitor: Visitor) -> None:
        """Accepts a visitor on this type."""
        if not visitor.visit(self):
            for inp in self.inputs:
                visitor.visit(inp)
            visitor.visit(self.output)
            for param in self.params:
                visitor.visit(param)

    def transform(self, transformer: Transformer) -> "Type":
        """Accepts a transformer on this type."""
        return transformer.transform(self) or FunctionType(
            [inp.transform(transformer) for inp in self.inputs],
            self.output.transform(transformer),
            self.input_names,
            self.params,
        )

    def instantiate(self, args: "Inst") -> "FunctionType":
        """Instantiates all function parameters with concrete types."""
        from guppylang.tys.subst import Instantiator

        assert len(args) == len(self.params)

        # Set the `preserve` flag for instantiated tuples and None
        preserved_args: list[Argument] = []
        for arg in args:
            if isinstance(arg, TypeArg):
                if isinstance(arg.ty, TupleType):
                    arg = TypeArg(TupleType(arg.ty.element_types, preserve=True))
                elif isinstance(arg.ty, NoneType):
                    arg = TypeArg(NoneType(preserve=True))
            preserved_args.append(arg)

        inst = Instantiator(preserved_args)
        return FunctionType(
            [ty.transform(inst) for ty in self.inputs],
            self.output.transform(inst),
            self.input_names,
        )

    def unquantified(self) -> tuple["FunctionType", Sequence[ExistentialVar]]:
        """Instantiates all parameters with existential variables."""
        exs = [param.to_existential() for param in self.params]
        return self.instantiate([arg for arg, _ in exs]), [var for _, var in exs]


@dataclass(frozen=True, init=False)
class TupleType(ParametrizedTypeBase):
    """Type of tuples."""

    element_types: Sequence["Type"]

    # Flag to avoid turning the tuple into a row when calling `type_to_row()`. This is
    # used to make sure that type vars instantiated to tuples are not broken up into
    # rows when generating a Hugr
    preserve: bool = field(default=False, compare=False)

    def __init__(self, element_types: Sequence["Type"], preserve: bool = False) -> None:
        # We need a custom __init__ to set the args
        args = [TypeArg(ty) for ty in element_types]
        object.__setattr__(self, "args", args)
        object.__setattr__(self, "element_types", element_types)
        object.__setattr__(self, "preserve", preserve)

    @property
    def intrinsically_linear(self) -> bool:
        return False

    def to_hugr(self) -> tys.Type:
        """Computes the Hugr representation of the type."""
        return tys.TupleType(inner=[ty.to_hugr() for ty in self.element_types])

    def transform(self, transformer: Transformer) -> "Type":
        """Accepts a transformer on this type."""
        return transformer.transform(self) or TupleType(
            [ty.transform(transformer) for ty in self.element_types], self.preserve
        )


@dataclass(frozen=True, init=False)
class SumType(ParametrizedTypeBase):
    """Type of sums.

    Note that this type is only used internally when constructing the Hugr. Users cannot
    write down this type.
    """

    element_types: Sequence["Type"]

    def __init__(self, element_types: Sequence["Type"]) -> None:
        # We need a custom __init__ to set the args
        args = [TypeArg(ty) for ty in element_types]
        object.__setattr__(self, "args", args)
        object.__setattr__(self, "element_types", element_types)

    @property
    def intrinsically_linear(self) -> bool:
        return False

    def to_hugr(self) -> tys.Type:
        """Computes the Hugr representation of the type."""
        if all(
            isinstance(e, TupleType) and len(e.element_types) == 0
            for e in self.element_types
        ):
            return tys.UnitSum(size=len(self.element_types))
        return tys.GeneralSum(row=[t.to_hugr() for t in self.element_types])

    def transform(self, transformer: Transformer) -> "Type":
        """Accepts a transformer on this type."""
        return transformer.transform(self) or SumType(
            [ty.transform(transformer) for ty in self.element_types]
        )


@dataclass(frozen=True)
class OpaqueType(ParametrizedTypeBase):
    """Type that is directly backed by a Hugr opaque type.

    For example, many builtin types like `int`, `float`, `list` etc. are directly backed
    by a Hugr extension.
    """

    defn: "OpaqueTypeDef"

    @property
    def intrinsically_linear(self) -> bool:
        """Whether this type is linear, independent of the arguments."""
        return self.defn.always_linear

    @property
    def hugr_bound(self) -> tys.TypeBound:
        """The Hugr bound of this type, i.e. `Any`, `Copyable`, or `Equatable`."""
        if self.defn.bound is not None:
            return self.defn.bound
        return super().hugr_bound

    def to_hugr(self) -> tys.Type:
        """Computes the Hugr representation of the type."""
        return self.defn.to_hugr(self.args)

    def transform(self, transformer: Transformer) -> "Type":
        """Accepts a transformer on this type."""
        return transformer.transform(self) or OpaqueType(
            [arg.transform(transformer) for arg in self.args], self.defn
        )


# We define the `Type` type as a union of all `TypeBase` subclasses defined above. This
# models an algebraic data type and enables exhaustiveness checking in pattern matches
# etc.
# Note that this might become obsolete in case the `@sealed` decorator is added:
#  * https://peps.python.org/pep-0622/#sealed-classes-as-algebraic-data-types
#  * https://github.com/johnthagen/sealed-typing-pep
ParametrizedType: TypeAlias = FunctionType | TupleType | SumType | OpaqueType
Type: TypeAlias = BoundTypeVar | ExistentialTypeVar | NoneType | ParametrizedType

TypeRow: TypeAlias = Sequence[Type]


def row_to_type(row: TypeRow) -> Type:
    """Turns a row of types into a single type by packing into a tuple."""
    if len(row) == 0:
        return NoneType()
    elif len(row) == 1:
        return row[0]
    else:
        return TupleType(row)


def type_to_row(ty: Type) -> TypeRow:
    """Turns a type into a row of types by unpacking top-level tuples."""
    if isinstance(ty, NoneType) and not ty.preserve:
        return []
    if isinstance(ty, TupleType) and not ty.preserve:
        return ty.element_types
    return [ty]


def unify(s: Type, t: Type, subst: "Subst | None") -> "Subst | None":
    """Computes a most general unifier for two types.

    Return a substitutions `subst` such that `s[subst] == t[subst]` or `None` if this
    not possible.
    """
    if subst is None:
        return None
    match s, t:
        case ExistentialTypeVar(id=s_id), ExistentialTypeVar(id=t_id) if s_id == t_id:
            return subst
        case ExistentialTypeVar() as s, t:
            return _unify_var(s, t, subst)
        case s, ExistentialTypeVar() as t:
            return _unify_var(t, s, subst)
        case BoundTypeVar(idx=s_idx), BoundTypeVar(idx=t_idx) if s_idx == t_idx:
            return subst
        case NoneType(), NoneType():
            return subst
        case FunctionType() as s, FunctionType() as t if s.params == t.params:
            return _unify_args(s, t, subst)
        case TupleType() as s, TupleType() as t:
            return _unify_args(s, t, subst)
        case SumType() as s, SumType() as t:
            return _unify_args(s, t, subst)
        case OpaqueType() as s, OpaqueType() as t if s.defn == t.defn:
            return _unify_args(s, t, subst)
        case _:
            return None


def _unify_var(var: ExistentialTypeVar, t: Type, subst: "Subst") -> "Subst | None":
    """Helper function for unification of type variables."""
    if var in subst:
        return unify(subst[var], t, subst)
    if isinstance(t, ExistentialTypeVar) and t in subst:
        return unify(var, subst[t], subst)
    if var in t.unsolved_vars:
        return None
    return {var: t, **subst}


def _unify_args(
    s: ParametrizedType, t: ParametrizedType, subst: "Subst"
) -> "Subst | None":
    """Helper function for unification of type arguments of parametrised types."""
    if len(s.args) != len(t.args):
        return None
    for sa, ta in zip(s.args, t.args, strict=True):
        match sa, ta:
            case TypeArg(ty=sa_ty), TypeArg(ty=ta_ty):
                res = unify(sa_ty, ta_ty, subst)
                if res is None:
                    return None
                subst = res
            case ConstArg(), ConstArg():
                raise NotImplementedError
            case _:
                return None
    return subst

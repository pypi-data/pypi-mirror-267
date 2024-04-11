from typing import overload
import abc
import typing
import warnings

import System
import System.Collections.Generic
import System.Diagnostics.Contracts
import System.Runtime.CompilerServices
import System.Runtime.Serialization
import System.Threading
import System.Threading.Tasks

System_Runtime_CompilerServices_Unsafe_AsPointer_T = typing.TypeVar("System_Runtime_CompilerServices_Unsafe_AsPointer_T")
System_Runtime_CompilerServices_Unsafe_As_T = typing.TypeVar("System_Runtime_CompilerServices_Unsafe_As_T")
System_Runtime_CompilerServices_Unsafe_As_TFrom = typing.TypeVar("System_Runtime_CompilerServices_Unsafe_As_TFrom")
System_Runtime_CompilerServices_Unsafe_Add_T = typing.TypeVar("System_Runtime_CompilerServices_Unsafe_Add_T")
System_Runtime_CompilerServices_Unsafe_AddByteOffset_T = typing.TypeVar("System_Runtime_CompilerServices_Unsafe_AddByteOffset_T")
System_Runtime_CompilerServices_Unsafe_AreSame_T = typing.TypeVar("System_Runtime_CompilerServices_Unsafe_AreSame_T")
System_Runtime_CompilerServices_Unsafe_BitCast_TTo = typing.TypeVar("System_Runtime_CompilerServices_Unsafe_BitCast_TTo")
System_Runtime_CompilerServices_Unsafe_BitCast_TFrom = typing.TypeVar("System_Runtime_CompilerServices_Unsafe_BitCast_TFrom")
System_Runtime_CompilerServices_Unsafe_Copy_T = typing.TypeVar("System_Runtime_CompilerServices_Unsafe_Copy_T")
System_Runtime_CompilerServices_Unsafe_IsAddressGreaterThan_T = typing.TypeVar("System_Runtime_CompilerServices_Unsafe_IsAddressGreaterThan_T")
System_Runtime_CompilerServices_Unsafe_IsAddressLessThan_T = typing.TypeVar("System_Runtime_CompilerServices_Unsafe_IsAddressLessThan_T")
System_Runtime_CompilerServices_Unsafe_ReadUnaligned_T = typing.TypeVar("System_Runtime_CompilerServices_Unsafe_ReadUnaligned_T")
System_Runtime_CompilerServices_Unsafe_WriteUnaligned_T = typing.TypeVar("System_Runtime_CompilerServices_Unsafe_WriteUnaligned_T")
System_Runtime_CompilerServices_Unsafe_Read_T = typing.TypeVar("System_Runtime_CompilerServices_Unsafe_Read_T")
System_Runtime_CompilerServices_Unsafe_Write_T = typing.TypeVar("System_Runtime_CompilerServices_Unsafe_Write_T")
System_Runtime_CompilerServices_Unsafe_ByteOffset_T = typing.TypeVar("System_Runtime_CompilerServices_Unsafe_ByteOffset_T")
System_Runtime_CompilerServices_Unsafe_IsNullRef_T = typing.TypeVar("System_Runtime_CompilerServices_Unsafe_IsNullRef_T")
System_Runtime_CompilerServices_Unsafe_Subtract_T = typing.TypeVar("System_Runtime_CompilerServices_Unsafe_Subtract_T")
System_Runtime_CompilerServices_Unsafe_SubtractByteOffset_T = typing.TypeVar("System_Runtime_CompilerServices_Unsafe_SubtractByteOffset_T")
System_Runtime_CompilerServices_Unsafe_SkipInit_T = typing.TypeVar("System_Runtime_CompilerServices_Unsafe_SkipInit_T")
System_Runtime_CompilerServices_AsyncVoidMethodBuilder_Start_TStateMachine = typing.TypeVar("System_Runtime_CompilerServices_AsyncVoidMethodBuilder_Start_TStateMachine")
System_Runtime_CompilerServices_AsyncVoidMethodBuilder_AwaitOnCompleted_TAwaiter = typing.TypeVar("System_Runtime_CompilerServices_AsyncVoidMethodBuilder_AwaitOnCompleted_TAwaiter")
System_Runtime_CompilerServices_AsyncVoidMethodBuilder_AwaitOnCompleted_TStateMachine = typing.TypeVar("System_Runtime_CompilerServices_AsyncVoidMethodBuilder_AwaitOnCompleted_TStateMachine")
System_Runtime_CompilerServices_AsyncVoidMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter = typing.TypeVar("System_Runtime_CompilerServices_AsyncVoidMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter")
System_Runtime_CompilerServices_AsyncVoidMethodBuilder_AwaitUnsafeOnCompleted_TStateMachine = typing.TypeVar("System_Runtime_CompilerServices_AsyncVoidMethodBuilder_AwaitUnsafeOnCompleted_TStateMachine")
System_Runtime_CompilerServices_AsyncIteratorMethodBuilder_MoveNext_TStateMachine = typing.TypeVar("System_Runtime_CompilerServices_AsyncIteratorMethodBuilder_MoveNext_TStateMachine")
System_Runtime_CompilerServices_AsyncIteratorMethodBuilder_AwaitOnCompleted_TAwaiter = typing.TypeVar("System_Runtime_CompilerServices_AsyncIteratorMethodBuilder_AwaitOnCompleted_TAwaiter")
System_Runtime_CompilerServices_AsyncIteratorMethodBuilder_AwaitOnCompleted_TStateMachine = typing.TypeVar("System_Runtime_CompilerServices_AsyncIteratorMethodBuilder_AwaitOnCompleted_TStateMachine")
System_Runtime_CompilerServices_AsyncIteratorMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter = typing.TypeVar("System_Runtime_CompilerServices_AsyncIteratorMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter")
System_Runtime_CompilerServices_AsyncIteratorMethodBuilder_AwaitUnsafeOnCompleted_TStateMachine = typing.TypeVar("System_Runtime_CompilerServices_AsyncIteratorMethodBuilder_AwaitUnsafeOnCompleted_TStateMachine")
System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_Start_TStateMachine = typing.TypeVar("System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_Start_TStateMachine")
System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_TResult = typing.TypeVar("System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_TResult")
System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_AwaitOnCompleted_TAwaiter = typing.TypeVar("System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_AwaitOnCompleted_TAwaiter")
System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_AwaitOnCompleted_TStateMachine = typing.TypeVar("System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_AwaitOnCompleted_TStateMachine")
System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter = typing.TypeVar("System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter")
System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_AwaitUnsafeOnCompleted_TStateMachine = typing.TypeVar("System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_AwaitUnsafeOnCompleted_TStateMachine")
System_Runtime_CompilerServices_ConfiguredValueTaskAwaitable_TResult = typing.TypeVar("System_Runtime_CompilerServices_ConfiguredValueTaskAwaitable_TResult")
System_Runtime_CompilerServices_ConditionalWeakTable_TKey = typing.TypeVar("System_Runtime_CompilerServices_ConditionalWeakTable_TKey")
System_Runtime_CompilerServices_ConditionalWeakTable_TValue = typing.TypeVar("System_Runtime_CompilerServices_ConditionalWeakTable_TValue")
System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_Start_TStateMachine = typing.TypeVar("System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_Start_TStateMachine")
System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_AwaitOnCompleted_TAwaiter = typing.TypeVar("System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_AwaitOnCompleted_TAwaiter")
System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_AwaitOnCompleted_TStateMachine = typing.TypeVar("System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_AwaitOnCompleted_TStateMachine")
System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter = typing.TypeVar("System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter")
System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_AwaitUnsafeOnCompleted_TStateMachine = typing.TypeVar("System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_AwaitUnsafeOnCompleted_TStateMachine")
System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_TResult = typing.TypeVar("System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_TResult")
System_Runtime_CompilerServices_AsyncTaskMethodBuilder_Start_TStateMachine = typing.TypeVar("System_Runtime_CompilerServices_AsyncTaskMethodBuilder_Start_TStateMachine")
System_Runtime_CompilerServices_AsyncTaskMethodBuilder_AwaitOnCompleted_TAwaiter = typing.TypeVar("System_Runtime_CompilerServices_AsyncTaskMethodBuilder_AwaitOnCompleted_TAwaiter")
System_Runtime_CompilerServices_AsyncTaskMethodBuilder_AwaitOnCompleted_TStateMachine = typing.TypeVar("System_Runtime_CompilerServices_AsyncTaskMethodBuilder_AwaitOnCompleted_TStateMachine")
System_Runtime_CompilerServices_AsyncTaskMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter = typing.TypeVar("System_Runtime_CompilerServices_AsyncTaskMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter")
System_Runtime_CompilerServices_AsyncTaskMethodBuilder_AwaitUnsafeOnCompleted_TStateMachine = typing.TypeVar("System_Runtime_CompilerServices_AsyncTaskMethodBuilder_AwaitUnsafeOnCompleted_TStateMachine")
System_Runtime_CompilerServices_AsyncTaskMethodBuilder_TResult = typing.TypeVar("System_Runtime_CompilerServices_AsyncTaskMethodBuilder_TResult")
System_Runtime_CompilerServices_StrongBox_T = typing.TypeVar("System_Runtime_CompilerServices_StrongBox_T")
System_Runtime_CompilerServices_ValueTaskAwaiter_TResult = typing.TypeVar("System_Runtime_CompilerServices_ValueTaskAwaiter_TResult")
System_Runtime_CompilerServices_RuntimeHelpers_GetSubArray_T = typing.TypeVar("System_Runtime_CompilerServices_RuntimeHelpers_GetSubArray_T")
System_Runtime_CompilerServices_RuntimeHelpers_CreateSpan_T = typing.TypeVar("System_Runtime_CompilerServices_RuntimeHelpers_CreateSpan_T")
System_Runtime_CompilerServices_DefaultInterpolatedStringHandler_AppendFormatted_T = typing.TypeVar("System_Runtime_CompilerServices_DefaultInterpolatedStringHandler_AppendFormatted_T")
System_Runtime_CompilerServices_TaskAwaiter_TResult = typing.TypeVar("System_Runtime_CompilerServices_TaskAwaiter_TResult")
System_Runtime_CompilerServices_ConfiguredTaskAwaitable_TResult = typing.TypeVar("System_Runtime_CompilerServices_ConfiguredTaskAwaitable_TResult")
System_Runtime_CompilerServices_ConfiguredCancelableAsyncEnumerable_T = typing.TypeVar("System_Runtime_CompilerServices_ConfiguredCancelableAsyncEnumerable_T")
System_Runtime_CompilerServices__EventContainer_Callable = typing.TypeVar("System_Runtime_CompilerServices__EventContainer_Callable")
System_Runtime_CompilerServices__EventContainer_ReturnType = typing.TypeVar("System_Runtime_CompilerServices__EventContainer_ReturnType")


class CallerMemberNameAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class StateMachineAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def StateMachineType(self) -> typing.Type:
        ...

    def __init__(self, stateMachineType: typing.Type) -> None:
        ...


class AsyncStateMachineAttribute(System.Runtime.CompilerServices.StateMachineAttribute):
    """This class has no documentation."""

    def __init__(self, stateMachineType: typing.Type) -> None:
        ...


class CallerLineNumberAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class StringFreezingAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class UnsafeValueTypeAttribute(System.Attribute):
    """This class has no documentation."""


class RuntimeWrappedException(System.Exception):
    """Exception used to wrap all non-CLS compliant exceptions."""

    @property
    def WrappedException(self) -> System.Object:
        ...

    def __init__(self, thrownObject: typing.Any) -> None:
        ...

    def GetObjectData(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        """Obsoletions.LegacyFormatterImplMessage"""
        warnings.warn("Obsoletions.LegacyFormatterImplMessage", DeprecationWarning)


class Unsafe(System.Object):
    """Contains generic, low-level functionality for manipulating pointers."""

    @staticmethod
    @overload
    def Add(source: System_Runtime_CompilerServices_Unsafe_Add_T, elementOffset: int) -> typing.Any:
        """Adds an element offset to the given reference."""
        ...

    @staticmethod
    @overload
    def Add(source: System_Runtime_CompilerServices_Unsafe_Add_T, elementOffset: System.IntPtr) -> typing.Any:
        """Adds an element offset to the given reference."""
        ...

    @staticmethod
    @overload
    def Add(source: typing.Any, elementOffset: int) -> typing.Any:
        """Adds an element offset to the given pointer."""
        ...

    @staticmethod
    @overload
    def Add(source: System_Runtime_CompilerServices_Unsafe_Add_T, elementOffset: System.UIntPtr) -> typing.Any:
        """Adds an element offset to the given reference."""
        ...

    @staticmethod
    @overload
    def AddByteOffset(source: System_Runtime_CompilerServices_Unsafe_AddByteOffset_T, byteOffset: System.UIntPtr) -> typing.Any:
        """Adds an byte offset to the given reference."""
        ...

    @staticmethod
    @overload
    def AddByteOffset(source: System_Runtime_CompilerServices_Unsafe_AddByteOffset_T, byteOffset: System.IntPtr) -> typing.Any:
        """Adds an byte offset to the given reference."""
        ...

    @staticmethod
    def AreSame(left: System_Runtime_CompilerServices_Unsafe_AreSame_T, right: System_Runtime_CompilerServices_Unsafe_AreSame_T) -> bool:
        """Determines whether the specified references point to the same location."""
        ...

    @staticmethod
    @overload
    def As(o: typing.Any) -> System_Runtime_CompilerServices_Unsafe_As_T:
        """Casts the given object to the specified type, performs no dynamic type checking."""
        ...

    @staticmethod
    @overload
    def As(source: System_Runtime_CompilerServices_Unsafe_As_TFrom) -> typing.Any:
        """Reinterprets the given reference as a reference to a value of type TTo."""
        ...

    @staticmethod
    def AsPointer(value: System_Runtime_CompilerServices_Unsafe_AsPointer_T) -> typing.Any:
        """Returns a pointer to the given by-ref parameter."""
        ...

    @staticmethod
    def AsRef(source: typing.Any) -> typing.Any:
        """Reinterprets the given location as a reference to a value of type T."""
        ...

    @staticmethod
    def BitCast(source: System_Runtime_CompilerServices_Unsafe_BitCast_TFrom) -> System_Runtime_CompilerServices_Unsafe_BitCast_TTo:
        """Reinterprets the given value of type TFrom as a value of type TTo."""
        ...

    @staticmethod
    def ByteOffset(origin: System_Runtime_CompilerServices_Unsafe_ByteOffset_T, target: System_Runtime_CompilerServices_Unsafe_ByteOffset_T) -> System.IntPtr:
        """Determines the byte offset from origin to target from the given references."""
        ...

    @staticmethod
    @overload
    def Copy(destination: typing.Any, source: System_Runtime_CompilerServices_Unsafe_Copy_T) -> None:
        """Copies a value of type T to the given location."""
        ...

    @staticmethod
    @overload
    def Copy(destination: System_Runtime_CompilerServices_Unsafe_Copy_T, source: typing.Any) -> None:
        """Copies a value of type T to the given location."""
        ...

    @staticmethod
    @overload
    def CopyBlock(destination: typing.Any, source: typing.Any, byteCount: int) -> None:
        """Copies bytes from the source address to the destination address."""
        ...

    @staticmethod
    @overload
    def CopyBlock(destination: int, source: int, byteCount: int) -> None:
        """Copies bytes from the source address to the destination address."""
        ...

    @staticmethod
    @overload
    def CopyBlockUnaligned(destination: typing.Any, source: typing.Any, byteCount: int) -> None:
        """Copies bytes from the source address to the destination address without assuming architecture dependent alignment of the addresses."""
        ...

    @staticmethod
    @overload
    def CopyBlockUnaligned(destination: int, source: int, byteCount: int) -> None:
        """Copies bytes from the source address to the destination address without assuming architecture dependent alignment of the addresses."""
        ...

    @staticmethod
    @overload
    def InitBlock(startAddress: typing.Any, value: int, byteCount: int) -> None:
        """Initializes a block of memory at the given location with a given initial value."""
        ...

    @staticmethod
    @overload
    def InitBlock(startAddress: int, value: int, byteCount: int) -> None:
        """Initializes a block of memory at the given location with a given initial value."""
        ...

    @staticmethod
    @overload
    def InitBlockUnaligned(startAddress: typing.Any, value: int, byteCount: int) -> None:
        """
        Initializes a block of memory at the given location with a given initial value
        without assuming architecture dependent alignment of the address.
        """
        ...

    @staticmethod
    @overload
    def InitBlockUnaligned(startAddress: int, value: int, byteCount: int) -> None:
        """
        Initializes a block of memory at the given location with a given initial value
        without assuming architecture dependent alignment of the address.
        """
        ...

    @staticmethod
    def IsAddressGreaterThan(left: System_Runtime_CompilerServices_Unsafe_IsAddressGreaterThan_T, right: System_Runtime_CompilerServices_Unsafe_IsAddressGreaterThan_T) -> bool:
        """
        Determines whether the memory address referenced by  is greater than
        the memory address referenced by .
        """
        ...

    @staticmethod
    def IsAddressLessThan(left: System_Runtime_CompilerServices_Unsafe_IsAddressLessThan_T, right: System_Runtime_CompilerServices_Unsafe_IsAddressLessThan_T) -> bool:
        """
        Determines whether the memory address referenced by  is less than
        the memory address referenced by .
        """
        ...

    @staticmethod
    def IsNullRef(source: System_Runtime_CompilerServices_Unsafe_IsNullRef_T) -> bool:
        """Returns if a given by-ref to type T is a null reference."""
        ...

    @staticmethod
    def NullRef() -> typing.Any:
        """Returns a by-ref to type T that is a null reference."""
        ...

    @staticmethod
    def Read(source: typing.Any) -> System_Runtime_CompilerServices_Unsafe_Read_T:
        """Reads a value of type T from the given location."""
        ...

    @staticmethod
    @overload
    def ReadUnaligned(source: typing.Any) -> System_Runtime_CompilerServices_Unsafe_ReadUnaligned_T:
        """Reads a value of type T from the given location."""
        ...

    @staticmethod
    @overload
    def ReadUnaligned(source: int) -> System_Runtime_CompilerServices_Unsafe_ReadUnaligned_T:
        """Reads a value of type T from the given location."""
        ...

    @staticmethod
    def SizeOf() -> int:
        """Returns the size of an object of the given type parameter."""
        ...

    @staticmethod
    def SkipInit(value: typing.Optional[System_Runtime_CompilerServices_Unsafe_SkipInit_T]) -> typing.Union[None, System_Runtime_CompilerServices_Unsafe_SkipInit_T]:
        """Bypasses definite assignment rules by taking advantage of out semantics."""
        ...

    @staticmethod
    @overload
    def Subtract(source: System_Runtime_CompilerServices_Unsafe_Subtract_T, elementOffset: int) -> typing.Any:
        """Subtracts an element offset from the given reference."""
        ...

    @staticmethod
    @overload
    def Subtract(source: typing.Any, elementOffset: int) -> typing.Any:
        """Subtracts an element offset from the given void pointer."""
        ...

    @staticmethod
    @overload
    def Subtract(source: System_Runtime_CompilerServices_Unsafe_Subtract_T, elementOffset: System.IntPtr) -> typing.Any:
        """Subtracts an element offset from the given reference."""
        ...

    @staticmethod
    @overload
    def Subtract(source: System_Runtime_CompilerServices_Unsafe_Subtract_T, elementOffset: System.UIntPtr) -> typing.Any:
        """Subtracts an element offset from the given reference."""
        ...

    @staticmethod
    @overload
    def SubtractByteOffset(source: System_Runtime_CompilerServices_Unsafe_SubtractByteOffset_T, byteOffset: System.IntPtr) -> typing.Any:
        """Subtracts a byte offset from the given reference."""
        ...

    @staticmethod
    @overload
    def SubtractByteOffset(source: System_Runtime_CompilerServices_Unsafe_SubtractByteOffset_T, byteOffset: System.UIntPtr) -> typing.Any:
        """Subtracts a byte offset from the given reference."""
        ...

    @staticmethod
    def Unbox(box: typing.Any) -> typing.Any:
        """Returns a mutable ref to a boxed value"""
        ...

    @staticmethod
    def Write(destination: typing.Any, value: System_Runtime_CompilerServices_Unsafe_Write_T) -> None:
        """Writes a value of type T to the given location."""
        ...

    @staticmethod
    @overload
    def WriteUnaligned(destination: typing.Any, value: System_Runtime_CompilerServices_Unsafe_WriteUnaligned_T) -> None:
        """Writes a value of type T to the given location."""
        ...

    @staticmethod
    @overload
    def WriteUnaligned(destination: int, value: System_Runtime_CompilerServices_Unsafe_WriteUnaligned_T) -> None:
        """Writes a value of type T to the given location."""
        ...


class CompilerGeneratedAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class IAsyncStateMachine(metaclass=abc.ABCMeta):
    """
    Represents state machines generated for asynchronous methods.
    This type is intended for compiler use only.
    """


class AsyncVoidMethodBuilder:
    """
    Provides a builder for asynchronous methods that return void.
    This type is intended for compiler use only.
    """

    def AwaitOnCompleted(self, awaiter: System_Runtime_CompilerServices_AsyncVoidMethodBuilder_AwaitOnCompleted_TAwaiter, stateMachine: System_Runtime_CompilerServices_AsyncVoidMethodBuilder_AwaitOnCompleted_TStateMachine) -> None:
        """
        Schedules the specified state machine to be pushed forward when the specified awaiter completes.
        
        :param awaiter: The awaiter.
        :param stateMachine: The state machine.
        """
        ...

    def AwaitUnsafeOnCompleted(self, awaiter: System_Runtime_CompilerServices_AsyncVoidMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter, stateMachine: System_Runtime_CompilerServices_AsyncVoidMethodBuilder_AwaitUnsafeOnCompleted_TStateMachine) -> None:
        """
        Schedules the specified state machine to be pushed forward when the specified awaiter completes.
        
        :param awaiter: The awaiter.
        :param stateMachine: The state machine.
        """
        ...

    @staticmethod
    def Create() -> System.Runtime.CompilerServices.AsyncVoidMethodBuilder:
        """
        Initializes a new AsyncVoidMethodBuilder.
        
        :returns: The initialized AsyncVoidMethodBuilder.
        """
        ...

    def SetException(self, exception: System.Exception) -> None:
        """
        Faults the method builder with an exception.
        
        :param exception: The exception that is the cause of this fault.
        """
        ...

    def SetResult(self) -> None:
        """Completes the method builder successfully."""
        ...

    def SetStateMachine(self, stateMachine: System.Runtime.CompilerServices.IAsyncStateMachine) -> None:
        """
        Associates the builder with the state machine it represents.
        
        :param stateMachine: The heap-allocated state machine object.
        """
        ...

    def Start(self, stateMachine: System_Runtime_CompilerServices_AsyncVoidMethodBuilder_Start_TStateMachine) -> None:
        """
        Initiates the builder's execution with the associated state machine.
        
        :param stateMachine: The state machine instance, passed by reference.
        """
        ...


class ScopedRefAttribute(System.Attribute):
    """
    Reserved for use by a compiler for tracking metadata.
    This attribute should not be used by developers in source code.
    """

    def __init__(self) -> None:
        """Initializes the attribute."""
        ...


class AsyncIteratorMethodBuilder:
    """Represents a builder for asynchronous iterators."""

    def AwaitOnCompleted(self, awaiter: System_Runtime_CompilerServices_AsyncIteratorMethodBuilder_AwaitOnCompleted_TAwaiter, stateMachine: System_Runtime_CompilerServices_AsyncIteratorMethodBuilder_AwaitOnCompleted_TStateMachine) -> None:
        """
        Schedules the state machine to proceed to the next action when the specified awaiter completes.
        
        :param awaiter: The awaiter.
        :param stateMachine: The state machine.
        """
        ...

    def AwaitUnsafeOnCompleted(self, awaiter: System_Runtime_CompilerServices_AsyncIteratorMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter, stateMachine: System_Runtime_CompilerServices_AsyncIteratorMethodBuilder_AwaitUnsafeOnCompleted_TStateMachine) -> None:
        """
        Schedules the state machine to proceed to the next action when the specified awaiter completes.
        
        :param awaiter: The awaiter.
        :param stateMachine: The state machine.
        """
        ...

    def Complete(self) -> None:
        """Marks iteration as being completed, whether successfully or otherwise."""
        ...

    @staticmethod
    def Create() -> System.Runtime.CompilerServices.AsyncIteratorMethodBuilder:
        """
        Creates an instance of the AsyncIteratorMethodBuilder struct.
        
        :returns: The initialized instance.
        """
        ...

    def MoveNext(self, stateMachine: System_Runtime_CompilerServices_AsyncIteratorMethodBuilder_MoveNext_TStateMachine) -> None:
        """
        Invokes IAsyncStateMachine.MoveNext on the state machine while guarding the ExecutionContext.
        
        :param stateMachine: The state machine instance, passed by reference.
        """
        ...


class IsReadOnlyAttribute(System.Attribute):
    """
    Reserved for use by a compiler for tracking metadata.
    This attribute should not be used by developers in source code.
    """

    def __init__(self) -> None:
        """Initializes the attribute."""
        ...


class CallConvCdecl(System.Object):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class CallConvFastcall(System.Object):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class CallConvStdcall(System.Object):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class CallConvSwift(System.Object):
    """Indicates that a method should using the https://github.com/apple/swift/blob/main/docs/ABIStabilityManifesto.md#calling-conventioncalling convention."""

    def __init__(self) -> None:
        """Initializes a new instance of the CallConvSwift class."""
        ...


class CallConvSuppressGCTransition(System.Object):
    """Indicates that a method should suppress the GC transition as part of the calling convention."""

    def __init__(self) -> None:
        """Initializes a new instance of the CallConvSuppressGCTransition class."""
        ...


class CallConvThiscall(System.Object):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class CallConvMemberFunction(System.Object):
    """Indicates that the calling convention used is the member function variant."""

    def __init__(self) -> None:
        """Initializes a new instance of the CallConvMemberFunction class."""
        ...


class LoadHint(System.Enum):
    """This class has no documentation."""

    Default = ...

    Always = ...

    Sometimes = ...


class AsyncValueTaskMethodBuilder(typing.Generic[System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_TResult]):
    """Represents a builder for asynchronous methods that returns a ValueTask{TResult}."""

    @property
    def Task(self) -> System.Threading.Tasks.ValueTask[System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_TResult]:
        """Gets the value task for this builder."""
        ...

    @overload
    def AwaitOnCompleted(self, awaiter: System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_AwaitOnCompleted_TAwaiter, stateMachine: System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_AwaitOnCompleted_TStateMachine) -> None:
        """
        Schedules the state machine to proceed to the next action when the specified awaiter completes.
        
        :param awaiter: the awaiter
        :param stateMachine: The state machine.
        """
        ...

    @overload
    def AwaitOnCompleted(self, awaiter: System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_AwaitOnCompleted_TAwaiter, stateMachine: System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_AwaitOnCompleted_TStateMachine) -> None:
        """
        Schedules the state machine to proceed to the next action when the specified awaiter completes.
        
        :param awaiter: The awaiter.
        :param stateMachine: The state machine.
        """
        ...

    @overload
    def AwaitUnsafeOnCompleted(self, awaiter: System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter, stateMachine: System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_AwaitUnsafeOnCompleted_TStateMachine) -> None:
        """
        Schedules the state machine to proceed to the next action when the specified awaiter completes.
        
        :param awaiter: the awaiter
        :param stateMachine: The state machine.
        """
        ...

    @overload
    def AwaitUnsafeOnCompleted(self, awaiter: System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter, stateMachine: System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_AwaitUnsafeOnCompleted_TStateMachine) -> None:
        """
        Schedules the state machine to proceed to the next action when the specified awaiter completes.
        
        :param awaiter: The awaiter.
        :param stateMachine: The state machine.
        """
        ...

    @staticmethod
    @overload
    def Create() -> System.Runtime.CompilerServices.AsyncValueTaskMethodBuilder[System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_TResult]:
        """
        Creates an instance of the AsyncValueTaskMethodBuilder{TResult} struct.
        
        :returns: The initialized instance.
        """
        ...

    @staticmethod
    @overload
    def Create() -> System.Runtime.CompilerServices.AsyncValueTaskMethodBuilder:
        """
        Creates an instance of the AsyncValueTaskMethodBuilder struct.
        
        :returns: The initialized instance.
        """
        ...

    @overload
    def SetException(self, exception: System.Exception) -> None:
        """
        Marks the value task as failed and binds the specified exception to the value task.
        
        :param exception: The exception to bind to the value task.
        """
        ...

    @overload
    def SetException(self, exception: System.Exception) -> None:
        """
        Marks the task as failed and binds the specified exception to the task.
        
        :param exception: The exception to bind to the task.
        """
        ...

    @overload
    def SetResult(self, result: System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_TResult) -> None:
        """
        Marks the value task as successfully completed.
        
        :param result: The result to use to complete the value task.
        """
        ...

    @overload
    def SetResult(self) -> None:
        """Marks the task as successfully completed."""
        ...

    @overload
    def SetStateMachine(self, stateMachine: System.Runtime.CompilerServices.IAsyncStateMachine) -> None:
        """
        Associates the builder with the specified state machine.
        
        :param stateMachine: The state machine instance to associate with the builder.
        """
        ...

    @overload
    def SetStateMachine(self, stateMachine: System.Runtime.CompilerServices.IAsyncStateMachine) -> None:
        """
        Associates the builder with the specified state machine.
        
        :param stateMachine: The state machine instance to associate with the builder.
        """
        ...

    @overload
    def Start(self, stateMachine: System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_Start_TStateMachine) -> None:
        """
        Begins running the builder with the associated state machine.
        
        :param stateMachine: The state machine instance, passed by reference.
        """
        ...

    @overload
    def Start(self, stateMachine: System_Runtime_CompilerServices_AsyncValueTaskMethodBuilder_Start_TStateMachine) -> None:
        """
        Begins running the builder with the associated state machine.
        
        :param stateMachine: The state machine instance, passed by reference.
        """
        ...


class ConfiguredValueTaskAwaitable(typing.Generic[System_Runtime_CompilerServices_ConfiguredValueTaskAwaitable_TResult]):
    """Provides an awaitable type that enables configured awaits on a ValueTask{TResult}."""

    @overload
    def GetAwaiter(self) -> System.Runtime.CompilerServices.ConfiguredValueTaskAwaitable.ConfiguredValueTaskAwaiter:
        """Returns an awaiter for this ConfiguredValueTaskAwaitable instance."""
        ...

    @overload
    def GetAwaiter(self) -> System.Runtime.CompilerServices.ConfiguredValueTaskAwaitable.ConfiguredValueTaskAwaiter:
        """Returns an awaiter for this ConfiguredValueTaskAwaitable{TResult} instance."""
        ...


class TupleElementNamesAttribute(System.Attribute):
    """Indicates that the use of ValueTuple on a member is meant to be treated as a tuple with element names."""

    @property
    def TransformNames(self) -> System.Collections.Generic.IList[str]:
        """
        Specifies, in a pre-order depth-first traversal of a type's
        construction, which ValueTuple elements are
        meant to carry element names.
        """
        ...

    def __init__(self, transformNames: typing.List[str]) -> None:
        """
        Initializes a new instance of the TupleElementNamesAttribute class.
        
        :param transformNames: Specifies, in a pre-order depth-first traversal of a type's construction, which ValueType occurrences are meant to carry element names.
        """
        ...


class EnumeratorCancellationAttribute(System.Attribute):
    """Allows users of async-enumerable methods to mark the parameter that should receive the cancellation token value from System.Collections.Generic.IAsyncEnumerable`1.GetAsyncEnumerator(System.Threading.CancellationToken)."""

    def __init__(self) -> None:
        """Initializes a new instance of the System.Runtime.CompilerServices.EnumeratorCancellationAttribute class."""
        ...


class PreserveBaseOverridesAttribute(System.Attribute):
    """This class has no documentation."""


class DecimalConstantAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def Value(self) -> float:
        ...

    @overload
    def __init__(self, scale: int, sign: int, hi: int, mid: int, low: int) -> None:
        ...

    @overload
    def __init__(self, scale: int, sign: int, hi: int, mid: int, low: int) -> None:
        ...


class RuntimeFeature(System.Object):
    """This class has no documentation."""

    IsDynamicCodeSupported: bool

    IsDynamicCodeCompiled: bool

    PortablePdb: str = ...
    """Name of the Portable PDB feature."""

    DefaultImplementationsOfInterfaces: str = ...
    """Indicates that this version of runtime supports default interface method implementations."""

    UnmanagedSignatureCallingConvention: str = ...
    """Indicates that this version of runtime supports the Unmanaged calling convention value."""

    CovariantReturnsOfClasses: str = ...
    """Indicates that this version of runtime supports covariant returns in overrides of methods declared in classes."""

    ByRefFields: str = ...
    """Represents a runtime feature where types can define ref fields."""

    ByRefLikeGenerics: str = ...
    """Represents a runtime feature where byref-like types can be used in Generic parameters."""

    VirtualStaticsInInterfaces: str = ...
    """Indicates that this version of runtime supports virtual static members of interfaces."""

    NumericIntPtr: str = ...
    """Indicates that this version of runtime supports System.IntPtr and System.UIntPtr as numeric types."""

    @staticmethod
    def IsSupported(feature: str) -> bool:
        """Checks whether a certain feature is supported by the Runtime."""
        ...


class ParamCollectionAttribute(System.Attribute):
    """Indicates that a method will allow a variable number of arguments in its invocation."""


class ConditionalWeakTable(typing.Generic[System_Runtime_CompilerServices_ConditionalWeakTable_TKey, System_Runtime_CompilerServices_ConditionalWeakTable_TValue], System.Object, typing.Iterable[System.Collections.Generic.KeyValuePair[System_Runtime_CompilerServices_ConditionalWeakTable_TKey, System_Runtime_CompilerServices_ConditionalWeakTable_TValue]]):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...

    def Add(self, key: System_Runtime_CompilerServices_ConditionalWeakTable_TKey, value: System_Runtime_CompilerServices_ConditionalWeakTable_TValue) -> None:
        """
        Adds a key to the table.
        
        :param key: key to add. May not be null.
        :param value: value to associate with key.
        """
        ...

    def AddOrUpdate(self, key: System_Runtime_CompilerServices_ConditionalWeakTable_TKey, value: System_Runtime_CompilerServices_ConditionalWeakTable_TValue) -> None:
        """
        Adds the key and value if the key doesn't exist, or updates the existing key's value if it does exist.
        
        :param key: key to add or update. May not be null.
        :param value: value to associate with key.
        """
        ...

    def Clear(self) -> None:
        """Clear all the key/value pairs"""
        ...

    def CreateValueCallback(self, key: System_Runtime_CompilerServices_ConditionalWeakTable_TKey) -> System_Runtime_CompilerServices_ConditionalWeakTable_TValue:
        ...

    def GetOrCreateValue(self, key: System_Runtime_CompilerServices_ConditionalWeakTable_TKey) -> System_Runtime_CompilerServices_ConditionalWeakTable_TValue:
        """
        Helper method to call GetValue without passing a creation delegate.  Uses Activator.CreateInstance
        to create new instances as needed.  If TValue does not have a default constructor, this will throw.
        
        :param key: key of the value to find. Cannot be null.
        """
        ...

    def GetValue(self, key: System_Runtime_CompilerServices_ConditionalWeakTable_TKey, createValueCallback: typing.Callable[[System_Runtime_CompilerServices_ConditionalWeakTable_TKey], System_Runtime_CompilerServices_ConditionalWeakTable_TValue]) -> System_Runtime_CompilerServices_ConditionalWeakTable_TValue:
        """
        Atomically searches for a specified key in the table and returns the corresponding value.
        If the key does not exist in the table, the method invokes a callback method to create a
        value that is bound to the specified key.
        
        :param key: key of the value to find. Cannot be null.
        :param createValueCallback: callback that creates value for key. Cannot be null.
        """
        ...

    def Remove(self, key: System_Runtime_CompilerServices_ConditionalWeakTable_TKey) -> bool:
        """
        Removes a key and its value from the table.
        
        :param key: key to remove. May not be null.
        :returns: true if the key is found and removed. Returns false if the key was not in the dictionary.
        """
        ...

    def TryAdd(self, key: System_Runtime_CompilerServices_ConditionalWeakTable_TKey, value: System_Runtime_CompilerServices_ConditionalWeakTable_TValue) -> bool:
        """
        Adds a key to the table if it doesn't already exist.
        
        :param key: The key to add.
        :param value: The key's property value.
        :returns: true if the key/value pair was added; false if the table already contained the key.
        """
        ...

    def TryGetValue(self, key: System_Runtime_CompilerServices_ConditionalWeakTable_TKey, value: typing.Optional[System_Runtime_CompilerServices_ConditionalWeakTable_TValue]) -> typing.Union[bool, System_Runtime_CompilerServices_ConditionalWeakTable_TValue]:
        """
        Gets the value of the specified key.
        
        :param key: key of the value to find. Cannot be null.
        :param value: If the key is found, contains the value associated with the key upon method return. If the key is not found, contains default(TValue).
        :returns: Returns "true" if key was found, "false" otherwise.
        """
        ...


class CallerFilePathAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class MethodImplOptions(System.Enum):
    """This class has no documentation."""

    Unmanaged = ...

    NoInlining = ...

    ForwardRef = ...

    Synchronized = ...

    NoOptimization = ...

    PreserveSig = ...

    AggressiveInlining = ...

    AggressiveOptimization = ...

    InternalCall = ...


class PoolingAsyncValueTaskMethodBuilder(typing.Generic[System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_TResult]):
    """Represents a builder for asynchronous methods that returns a ValueTask{TResult}."""

    @property
    def Task(self) -> System.Threading.Tasks.ValueTask:
        """Gets the task for this builder."""
        ...

    @overload
    def AwaitOnCompleted(self, awaiter: System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_AwaitOnCompleted_TAwaiter, stateMachine: System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_AwaitOnCompleted_TStateMachine) -> None:
        """
        Schedules the state machine to proceed to the next action when the specified awaiter completes.
        
        :param awaiter: The awaiter.
        :param stateMachine: The state machine.
        """
        ...

    @overload
    def AwaitOnCompleted(self, awaiter: System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_AwaitOnCompleted_TAwaiter, stateMachine: System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_AwaitOnCompleted_TStateMachine) -> None:
        """
        Schedules the state machine to proceed to the next action when the specified awaiter completes.
        
        :param awaiter: the awaiter
        :param stateMachine: The state machine.
        """
        ...

    @overload
    def AwaitUnsafeOnCompleted(self, awaiter: System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter, stateMachine: System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_AwaitUnsafeOnCompleted_TStateMachine) -> None:
        """
        Schedules the state machine to proceed to the next action when the specified awaiter completes.
        
        :param awaiter: The awaiter.
        :param stateMachine: The state machine.
        """
        ...

    @overload
    def AwaitUnsafeOnCompleted(self, awaiter: System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter, stateMachine: System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_AwaitUnsafeOnCompleted_TStateMachine) -> None:
        """
        Schedules the state machine to proceed to the next action when the specified awaiter completes.
        
        :param awaiter: the awaiter
        :param stateMachine: The state machine.
        """
        ...

    @staticmethod
    @overload
    def Create() -> System.Runtime.CompilerServices.PoolingAsyncValueTaskMethodBuilder:
        """
        Creates an instance of the PoolingAsyncValueTaskMethodBuilder struct.
        
        :returns: The initialized instance.
        """
        ...

    @staticmethod
    @overload
    def Create() -> System.Runtime.CompilerServices.PoolingAsyncValueTaskMethodBuilder[System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_TResult]:
        """
        Creates an instance of the PoolingAsyncValueTaskMethodBuilder{TResult} struct.
        
        :returns: The initialized instance.
        """
        ...

    @overload
    def SetException(self, exception: System.Exception) -> None:
        """
        Marks the task as failed and binds the specified exception to the task.
        
        :param exception: The exception to bind to the task.
        """
        ...

    @overload
    def SetException(self, exception: System.Exception) -> None:
        """
        Marks the value task as failed and binds the specified exception to the value task.
        
        :param exception: The exception to bind to the value task.
        """
        ...

    @overload
    def SetResult(self) -> None:
        """Marks the task as successfully completed."""
        ...

    @overload
    def SetResult(self, result: System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_TResult) -> None:
        """
        Marks the value task as successfully completed.
        
        :param result: The result to use to complete the value task.
        """
        ...

    @overload
    def SetStateMachine(self, stateMachine: System.Runtime.CompilerServices.IAsyncStateMachine) -> None:
        """
        Associates the builder with the specified state machine.
        
        :param stateMachine: The state machine instance to associate with the builder.
        """
        ...

    @overload
    def SetStateMachine(self, stateMachine: System.Runtime.CompilerServices.IAsyncStateMachine) -> None:
        """
        Associates the builder with the specified state machine.
        
        :param stateMachine: The state machine instance to associate with the builder.
        """
        ...

    @overload
    def Start(self, stateMachine: System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_Start_TStateMachine) -> None:
        """
        Begins running the builder with the associated state machine.
        
        :param stateMachine: The state machine instance, passed by reference.
        """
        ...

    @overload
    def Start(self, stateMachine: System_Runtime_CompilerServices_PoolingAsyncValueTaskMethodBuilder_Start_TStateMachine) -> None:
        """
        Begins running the builder with the associated state machine.
        
        :param stateMachine: The state machine instance, passed by reference.
        """
        ...


class DisableRuntimeMarshallingAttribute(System.Attribute):
    """
    Disables the built-in runtime managed/unmanaged marshalling subsystem for
    P/Invokes, Delegate types, and unmanaged function pointer invocations.
    """


class AsyncTaskMethodBuilder(typing.Generic[System_Runtime_CompilerServices_AsyncTaskMethodBuilder_TResult]):
    """
    Provides a builder for asynchronous methods that return Task{TResult}.
    This type is intended for compiler use only.
    """

    @property
    def Task(self) -> System.Threading.Tasks.Task:
        """Gets the Threading.Tasks.Task for this builder."""
        ...

    @overload
    def AwaitOnCompleted(self, awaiter: System_Runtime_CompilerServices_AsyncTaskMethodBuilder_AwaitOnCompleted_TAwaiter, stateMachine: System_Runtime_CompilerServices_AsyncTaskMethodBuilder_AwaitOnCompleted_TStateMachine) -> None:
        """
        Schedules the specified state machine to be pushed forward when the specified awaiter completes.
        
        :param awaiter: The awaiter.
        :param stateMachine: The state machine.
        """
        ...

    @overload
    def AwaitOnCompleted(self, awaiter: System_Runtime_CompilerServices_AsyncTaskMethodBuilder_AwaitOnCompleted_TAwaiter, stateMachine: System_Runtime_CompilerServices_AsyncTaskMethodBuilder_AwaitOnCompleted_TStateMachine) -> None:
        """
        Schedules the specified state machine to be pushed forward when the specified awaiter completes.
        
        :param awaiter: The awaiter.
        :param stateMachine: The state machine.
        """
        ...

    @overload
    def AwaitUnsafeOnCompleted(self, awaiter: System_Runtime_CompilerServices_AsyncTaskMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter, stateMachine: System_Runtime_CompilerServices_AsyncTaskMethodBuilder_AwaitUnsafeOnCompleted_TStateMachine) -> None:
        """
        Schedules the specified state machine to be pushed forward when the specified awaiter completes.
        
        :param awaiter: The awaiter.
        :param stateMachine: The state machine.
        """
        ...

    @overload
    def AwaitUnsafeOnCompleted(self, awaiter: System_Runtime_CompilerServices_AsyncTaskMethodBuilder_AwaitUnsafeOnCompleted_TAwaiter, stateMachine: System_Runtime_CompilerServices_AsyncTaskMethodBuilder_AwaitUnsafeOnCompleted_TStateMachine) -> None:
        """
        Schedules the specified state machine to be pushed forward when the specified awaiter completes.
        
        :param awaiter: The awaiter.
        :param stateMachine: The state machine.
        """
        ...

    @staticmethod
    @overload
    def Create() -> System.Runtime.CompilerServices.AsyncTaskMethodBuilder:
        """
        Initializes a new AsyncTaskMethodBuilder.
        
        :returns: The initialized AsyncTaskMethodBuilder.
        """
        ...

    @staticmethod
    @overload
    def Create() -> System.Runtime.CompilerServices.AsyncTaskMethodBuilder[System_Runtime_CompilerServices_AsyncTaskMethodBuilder_TResult]:
        """
        Initializes a new AsyncTaskMethodBuilder.
        
        :returns: The initialized AsyncTaskMethodBuilder.
        """
        ...

    @overload
    def SetException(self, exception: System.Exception) -> None:
        """
        Completes the Threading.Tasks.Task in the
        TaskStatus state with the specified exception.
        
        :param exception: The Exception to use to fault the task.
        """
        ...

    @overload
    def SetException(self, exception: System.Exception) -> None:
        """
        Completes the Task{TResult} in the
        TaskStatus state with the specified exception.
        
        :param exception: The Exception to use to fault the task.
        """
        ...

    @overload
    def SetResult(self) -> None:
        """
        Completes the Threading.Tasks.Task in the
        TaskStatus state.
        """
        ...

    @overload
    def SetResult(self, result: System_Runtime_CompilerServices_AsyncTaskMethodBuilder_TResult) -> None:
        """
        Completes the Task{TResult} in the
        TaskStatus state with the specified result.
        
        :param result: The result to use to complete the task.
        """
        ...

    @overload
    def SetStateMachine(self, stateMachine: System.Runtime.CompilerServices.IAsyncStateMachine) -> None:
        """
        Associates the builder with the state machine it represents.
        
        :param stateMachine: The heap-allocated state machine object.
        """
        ...

    @overload
    def SetStateMachine(self, stateMachine: System.Runtime.CompilerServices.IAsyncStateMachine) -> None:
        """
        Associates the builder with the state machine it represents.
        
        :param stateMachine: The heap-allocated state machine object.
        """
        ...

    @overload
    def Start(self, stateMachine: System_Runtime_CompilerServices_AsyncTaskMethodBuilder_Start_TStateMachine) -> None:
        """
        Initiates the builder's execution with the associated state machine.
        
        :param stateMachine: The state machine instance, passed by reference.
        """
        ...

    @overload
    def Start(self, stateMachine: System_Runtime_CompilerServices_AsyncTaskMethodBuilder_Start_TStateMachine) -> None:
        """
        Initiates the builder's execution with the associated state machine.
        
        :param stateMachine: The state machine instance, passed by reference.
        """
        ...


class CompilationRelaxations(System.Enum):
    """This class has no documentation."""

    NoStringInterning = ...


class FormattableStringFactory(System.Object):
    """Provides a static method to create a FormattableString object from a composite format string and its arguments."""

    @staticmethod
    def Create(format: str, *arguments: typing.Any) -> System.FormattableString:
        """
        Create a FormattableString from a composite format string and object
        array containing zero or more objects to format.
        """
        ...


class ModuleInitializerAttribute(System.Attribute):
    """
    Used to indicate to the compiler that a method should be called
    in its containing module's initializer.
    """

    def __init__(self) -> None:
        ...


class CreateNewOnMetadataUpdateAttribute(System.Attribute):
    """Indicates a type should be replaced rather than updated when applying metadata updates."""


class IndexerNameAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self, indexerName: str) -> None:
        ...


class IsVolatile(System.Object):
    """This class has no documentation."""


class IteratorStateMachineAttribute(System.Runtime.CompilerServices.StateMachineAttribute):
    """This class has no documentation."""

    def __init__(self, stateMachineType: typing.Type) -> None:
        ...


class IsUnmanagedAttribute(System.Attribute):
    """
    Reserved for use by a compiler for tracking metadata.
    This attribute should not be used by developers in source code.
    """

    def __init__(self) -> None:
        """Initializes the attribute."""
        ...


class UnsafeAccessorKind(System.Enum):
    """Specifies the kind of target to which an UnsafeAccessorAttribute is providing access."""

    Constructor = 0
    """Provide access to a constructor."""

    Method = 1
    """Provide access to a method."""

    StaticMethod = 2
    """Provide access to a static method."""

    Field = 3
    """Provide access to a field."""

    StaticField = 4
    """Provide access to a static field."""


class UnsafeAccessorAttribute(System.Attribute):
    """Provides access to an inaccessible member of a specific type."""

    @property
    def Kind(self) -> int:
        """
        Gets the kind of member to which access is provided.
        
        This property contains the int value of a member of the System.Runtime.CompilerServices.UnsafeAccessorKind enum.
        """
        ...

    @property
    def Name(self) -> str:
        """Gets or sets the name of the member to which access is provided."""
        ...

    def __init__(self, kind: System.Runtime.CompilerServices.UnsafeAccessorKind) -> None:
        ...


class CustomConstantAttribute(System.Attribute, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    @abc.abstractmethod
    def Value(self) -> System.Object:
        ...


class DateTimeConstantAttribute(System.Runtime.CompilerServices.CustomConstantAttribute):
    """This class has no documentation."""

    @property
    def Value(self) -> System.Object:
        ...

    def __init__(self, ticks: int) -> None:
        ...


class RefSafetyRulesAttribute(System.Attribute):
    """Indicates the language version of the ref safety rules used when the module was compiled."""

    @property
    def Version(self) -> int:
        """Gets the language version of the ref safety rules used when the module was compiled."""
        ...

    def __init__(self, version: int) -> None:
        """
        Initializes a new instance of the RefSafetyRulesAttribute class.
        
        :param version: The language version of the ref safety rules used when the module was compiled.
        """
        ...


class IsConst(System.Object):
    """This class has no documentation."""


class InterpolatedStringHandlerAttribute(System.Attribute):
    """Indicates the attributed type is to be used as an interpolated string handler."""

    def __init__(self) -> None:
        """Initializes the InterpolatedStringHandlerAttribute."""
        ...


class TypeForwardedToAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def Destination(self) -> typing.Type:
        ...

    def __init__(self, destination: typing.Type) -> None:
        ...


class AccessedThroughPropertyAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def PropertyName(self) -> str:
        ...

    def __init__(self, propertyName: str) -> None:
        ...


class NullablePublicOnlyAttribute(System.Attribute):
    """
    Reserved for use by a compiler for tracking metadata.
    This attribute should not be used by developers in source code.
    """

    @property
    def IncludesInternals(self) -> bool:
        """Indicates whether metadata for internal members is included."""
        ...

    def __init__(self, value: bool) -> None:
        """
        Initializes the attribute.
        
        :param value: Indicates whether metadata for internal members is included.
        """
        ...


class NullableContextAttribute(System.Attribute):
    """
    Reserved for use by a compiler for tracking metadata.
    This attribute should not be used by developers in source code.
    """

    @property
    def Flag(self) -> int:
        """Flag specifying metadata related to nullable reference types."""
        ...

    def __init__(self, value: int) -> None:
        """
        Initializes the attribute.
        
        :param value: The flag value.
        """
        ...


class IStrongBox(metaclass=abc.ABCMeta):
    """Defines a property for accessing the value that an object references."""


class StrongBox(typing.Generic[System_Runtime_CompilerServices_StrongBox_T], System.Object, System.Runtime.CompilerServices.IStrongBox):
    """Holds a reference to a value."""

    @property
    def Value(self) -> System_Runtime_CompilerServices_StrongBox_T:
        """Gets the strongly typed value associated with the StrongBox{T}This is explicitly exposed as a field instead of a property to enable loading the address of the field."""
        ...

    @overload
    def __init__(self) -> None:
        """Initializes a new StrongBox which can receive a value when used in a reference call."""
        ...

    @overload
    def __init__(self, value: System_Runtime_CompilerServices_StrongBox_T) -> None:
        """
        Initializes a new StrongBox{T} with the specified value.
        
        :param value: A value that the StrongBox{T} will reference.
        """
        ...


class DependencyAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def DependentAssembly(self) -> str:
        ...

    @property
    def LoadHint(self) -> int:
        """This property contains the int value of a member of the System.Runtime.CompilerServices.LoadHint enum."""
        ...

    def __init__(self, dependentAssemblyArgument: str, loadHintArgument: System.Runtime.CompilerServices.LoadHint) -> None:
        ...


class InterpolatedStringHandlerArgumentAttribute(System.Attribute):
    """Indicates which arguments to a method involving an interpolated string handler should be passed to that handler."""

    @property
    def Arguments(self) -> typing.List[str]:
        """Gets the names of the arguments that should be passed to the handler."""
        ...

    @overload
    def __init__(self, argument: str) -> None:
        """
        Initializes a new instance of the InterpolatedStringHandlerArgumentAttribute class.
        
        :param argument: The name of the argument that should be passed to the handler.
        """
        ...

    @overload
    def __init__(self, *arguments: str) -> None:
        """
        Initializes a new instance of the InterpolatedStringHandlerArgumentAttribute class.
        
        :param arguments: The names of the arguments that should be passed to the handler.
        """
        ...


class AsyncMethodBuilderAttribute(System.Attribute):
    """
    Indicates the type of the async method builder that should be used by a language compiler to
    build the attributed async method or to build the attributed type when used as the return type
    of an async method.
    """

    @property
    def BuilderType(self) -> typing.Type:
        """Gets the Type of the associated builder."""
        ...

    def __init__(self, builderType: typing.Type) -> None:
        """
        Initializes the AsyncMethodBuilderAttribute.
        
        :param builderType: The Type of the associated builder.
        """
        ...


class TypeForwardedFromAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def AssemblyFullName(self) -> str:
        ...

    def __init__(self, assemblyFullName: str) -> None:
        ...


class SwitchExpressionException(System.InvalidOperationException):
    """
    Indicates that a switch expression that was non-exhaustive failed to match its input
    at runtime, e.g. in the C# 8 expression 3 switch { 4 => 5 }.
    The exception optionally contains an object representing the unmatched value.
    """

    @property
    def UnmatchedValue(self) -> System.Object:
        ...

    @property
    def Message(self) -> str:
        ...

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, innerException: System.Exception) -> None:
        ...

    @overload
    def __init__(self, unmatchedValue: typing.Any) -> None:
        ...

    @overload
    def __init__(self, message: str) -> None:
        ...

    @overload
    def __init__(self, message: str, innerException: System.Exception) -> None:
        ...

    def GetObjectData(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        """Obsoletions.LegacyFormatterImplMessage"""
        warnings.warn("Obsoletions.LegacyFormatterImplMessage", DeprecationWarning)


class FixedBufferAttribute(System.Attribute):
    """Indicates that a field should be treated as containing a fixed number of elements of the specified primitive type."""

    @property
    def ElementType(self) -> typing.Type:
        ...

    @property
    def Length(self) -> int:
        ...

    def __init__(self, elementType: typing.Type, length: int) -> None:
        ...


class INotifyCompletion(metaclass=abc.ABCMeta):
    """Represents an operation that will schedule continuations when the operation completes."""


class ICriticalNotifyCompletion(System.Runtime.CompilerServices.INotifyCompletion, metaclass=abc.ABCMeta):
    """Represents an awaiter used to schedule continuations when an await operation completes."""


class YieldAwaitable:
    """This class has no documentation."""

    class YieldAwaiter(System.Runtime.CompilerServices.ICriticalNotifyCompletion, System.Runtime.CompilerServices.IStateMachineBoxAwareAwaiter):
        """Provides an awaiter that switches into a target environment."""

        @property
        def IsCompleted(self) -> bool:
            """Gets whether a yield is not required."""
            ...

        def GetResult(self) -> None:
            """Ends the await operation."""
            ...

        def OnCompleted(self, continuation: typing.Callable[[], None]) -> None:
            """
            Posts the  back to the current context.
            
            :param continuation: The action to invoke asynchronously.
            """
            ...

        def UnsafeOnCompleted(self, continuation: typing.Callable[[], None]) -> None:
            """
            Posts the  back to the current context.
            
            :param continuation: The action to invoke asynchronously.
            """
            ...

    def GetAwaiter(self) -> System.Runtime.CompilerServices.YieldAwaitable.YieldAwaiter:
        """
        Gets an awaiter for this YieldAwaitable.
        
        :returns: An awaiter for this awaitable.
        """
        ...


class ExtensionAttribute(System.Attribute):
    """Indicates that a method is an extension method, or that a class or assembly contains extension methods."""


class SuppressIldasmAttribute(System.Attribute):
    """Obsoletions.SuppressIldasmAttributeMessage"""

    def __init__(self) -> None:
        ...


class DisablePrivateReflectionAttribute(System.Attribute):
    """Obsoletions.DisablePrivateReflectionAttributeMessage"""

    def __init__(self) -> None:
        ...


class ValueTaskAwaiter(typing.Generic[System_Runtime_CompilerServices_ValueTaskAwaiter_TResult], System.Runtime.CompilerServices.ICriticalNotifyCompletion, System.Runtime.CompilerServices.IStateMachineBoxAwareAwaiter):
    """Provides an awaiter for a ValueTask{TResult}."""

    @property
    def IsCompleted(self) -> bool:
        """Gets whether the ValueTask has completed."""
        ...

    @overload
    def GetResult(self) -> None:
        """Gets the result of the ValueTask."""
        ...

    @overload
    def GetResult(self) -> System_Runtime_CompilerServices_ValueTaskAwaiter_TResult:
        """Gets the result of the ValueTask."""
        ...

    @overload
    def OnCompleted(self, continuation: typing.Callable[[], None]) -> None:
        """Schedules the continuation action for this ValueTask."""
        ...

    @overload
    def OnCompleted(self, continuation: typing.Callable[[], None]) -> None:
        """Schedules the continuation action for this ValueTask."""
        ...

    @overload
    def UnsafeOnCompleted(self, continuation: typing.Callable[[], None]) -> None:
        """Schedules the continuation action for this ValueTask."""
        ...

    @overload
    def UnsafeOnCompleted(self, continuation: typing.Callable[[], None]) -> None:
        """Schedules the continuation action for this ValueTask."""
        ...


class InternalsVisibleToAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def AssemblyName(self) -> str:
        ...

    @property
    def AllInternalsVisible(self) -> bool:
        ...

    def __init__(self, assemblyName: str) -> None:
        ...


class DefaultDependencyAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def LoadHint(self) -> int:
        """This property contains the int value of a member of the System.Runtime.CompilerServices.LoadHint enum."""
        ...

    def __init__(self, loadHintArgument: System.Runtime.CompilerServices.LoadHint) -> None:
        ...


class SpecialNameAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class AsyncIteratorStateMachineAttribute(System.Runtime.CompilerServices.StateMachineAttribute):
    """Indicates whether a method is an asynchronous iterator."""

    def __init__(self, stateMachineType: typing.Type) -> None:
        """
        Initializes a new instance of the AsyncIteratorStateMachineAttribute class.
        
        :param stateMachineType: The type object for the underlying state machine type that's used to implement a state machine method.
        """
        ...


class RuntimeHelpers(System.Object):
    """This class has no documentation."""

    OffsetToStringData: int
    """OffsetToStringData has been deprecated. Use string.GetPinnableReference() instead."""

    @staticmethod
    def AllocateTypeAssociatedMemory(type: typing.Type, size: int) -> System.IntPtr:
        ...

    @staticmethod
    def Box(target: int, type: System.RuntimeTypeHandle) -> System.Object:
        """
        Create a boxed object of the specified type from the data located at the target reference.
        
        :param target: The target data
        :param type: The type of box to create.
        :returns: A boxed object containing the specified data.
        """
        ...

    def CleanupCode(self, userData: typing.Any, exceptionThrown: bool) -> None:
        ...

    @staticmethod
    def CreateSpan(fldHandle: System.RuntimeFieldHandle) -> System.ReadOnlySpan[System_Runtime_CompilerServices_RuntimeHelpers_CreateSpan_T]:
        """
        Provide a fast way to access constant data stored in a module as a ReadOnlySpan{T}
        
        :param fldHandle: A field handle that specifies the location of the data to be referred to by the ReadOnlySpan{T}. The Rva of the field must be aligned on a natural boundary of type T
        :returns: A ReadOnlySpan{T} of the data stored in the field.
        """
        ...

    @staticmethod
    def EnsureSufficientExecutionStack() -> None:
        ...

    @staticmethod
    def Equals(o1: typing.Any, o2: typing.Any) -> bool:
        ...

    @staticmethod
    def ExecuteCodeWithGuaranteedCleanup(code: typing.Callable[[System.Object], None], backoutCode: typing.Callable[[System.Object, bool], None], userData: typing.Any) -> None:
        """Obsoletions.ConstrainedExecutionRegionMessage"""
        warnings.warn("Obsoletions.ConstrainedExecutionRegionMessage", DeprecationWarning)

    @staticmethod
    def GetHashCode(o: typing.Any) -> int:
        ...

    @staticmethod
    def GetObjectValue(obj: typing.Any) -> System.Object:
        ...

    @staticmethod
    def GetSubArray(array: typing.List[System_Runtime_CompilerServices_RuntimeHelpers_GetSubArray_T], range: System.Range) -> typing.List[System_Runtime_CompilerServices_RuntimeHelpers_GetSubArray_T]:
        """Slices the specified array using the specified range."""
        ...

    @staticmethod
    def GetUninitializedObject(type: typing.Type) -> System.Object:
        ...

    @staticmethod
    def InitializeArray(array: System.Array, fldHandle: System.RuntimeFieldHandle) -> None:
        ...

    @staticmethod
    def IsReferenceOrContainsReferences() -> bool:
        ...

    @staticmethod
    def PrepareConstrainedRegions() -> None:
        """Obsoletions.ConstrainedExecutionRegionMessage"""
        warnings.warn("Obsoletions.ConstrainedExecutionRegionMessage", DeprecationWarning)

    @staticmethod
    def PrepareConstrainedRegionsNoOP() -> None:
        """Obsoletions.ConstrainedExecutionRegionMessage"""
        warnings.warn("Obsoletions.ConstrainedExecutionRegionMessage", DeprecationWarning)

    @staticmethod
    def PrepareContractedDelegate(d: System.Delegate) -> None:
        """Obsoletions.ConstrainedExecutionRegionMessage"""
        warnings.warn("Obsoletions.ConstrainedExecutionRegionMessage", DeprecationWarning)

    @staticmethod
    def PrepareDelegate(d: System.Delegate) -> None:
        ...

    @staticmethod
    @overload
    def PrepareMethod(method: System.RuntimeMethodHandle) -> None:
        ...

    @staticmethod
    @overload
    def PrepareMethod(method: System.RuntimeMethodHandle, instantiation: typing.List[System.RuntimeTypeHandle]) -> None:
        ...

    @staticmethod
    def ProbeForSufficientStack() -> None:
        """Obsoletions.ConstrainedExecutionRegionMessage"""
        warnings.warn("Obsoletions.ConstrainedExecutionRegionMessage", DeprecationWarning)

    @staticmethod
    def RunClassConstructor(type: System.RuntimeTypeHandle) -> None:
        ...

    @staticmethod
    def RunModuleConstructor(module: System.ModuleHandle) -> None:
        ...

    @staticmethod
    def SizeOf(type: System.RuntimeTypeHandle) -> int:
        """
        Get the size of an object of the given type.
        
        :param type: The type to get the size of.
        :returns: The size of instances of the type.
        """
        ...

    def TryCode(self, userData: typing.Any) -> None:
        ...

    @staticmethod
    def TryEnsureSufficientExecutionStack() -> bool:
        ...


class ITuple(metaclass=abc.ABCMeta):
    """This interface is required for types that want to be indexed into by dynamic patterns."""


class RuntimeCompatibilityAttribute(System.Attribute):
    """Specifies whether to enable various legacy or new opt-in behaviors."""

    @property
    def WrapNonExceptionThrows(self) -> bool:
        ...

    def __init__(self) -> None:
        ...


class ContractHelper(System.Object):
    """This class has no documentation."""

    @staticmethod
    def RaiseContractFailedEvent(failureKind: System.Diagnostics.Contracts.ContractFailureKind, userMessage: str, conditionText: str, innerException: System.Exception) -> str:
        """
        Rewriter will call this method on a contract failure to allow listeners to be notified.
        The method should not perform any failure (assert/throw) itself.
        This method has 3 functions:
        1. Call any contract hooks (such as listeners to Contract failed events)
        2. Determine if the listeners deem the failure as handled (then resultFailureMessage should be set to null)
        3. Produce a localized resultFailureMessage used in advertising the failure subsequently.
        On exit: null if the event was handled and should not trigger a failure.
                 Otherwise, returns the localized failure message.
        """
        ...

    @staticmethod
    def TriggerFailure(kind: System.Diagnostics.Contracts.ContractFailureKind, displayMessage: str, userMessage: str, conditionText: str, innerException: System.Exception) -> None:
        """Rewriter calls this method to get the default failure behavior."""
        ...


class NullableAttribute(System.Attribute):
    """
    Reserved for use by a compiler for tracking metadata.
    This attribute should not be used by developers in source code.
    """

    @property
    def NullableFlags(self) -> typing.List[int]:
        """Flags specifying metadata related to nullable reference types."""
        ...

    @overload
    def __init__(self, value: int) -> None:
        """
        Initializes the attribute.
        
        :param value: The flags value.
        """
        ...

    @overload
    def __init__(self, value: typing.List[int]) -> None:
        """
        Initializes the attribute.
        
        :param value: The flags value.
        """
        ...


class CompilerFeatureRequiredAttribute(System.Attribute):
    """Indicates that compiler support for a particular feature is required for the location where this attribute is applied."""

    @property
    def FeatureName(self) -> str:
        """The name of the compiler feature."""
        ...

    @property
    def IsOptional(self) -> bool:
        """If true, the compiler can choose to allow access to the location where this attribute is applied if it does not understand FeatureName."""
        ...

    RefStructs: str = ...
    """The FeatureName used for the ref structs C# feature."""

    RequiredMembers: str = ...
    """The FeatureName used for the required members C# feature."""

    def __init__(self, featureName: str) -> None:
        ...


class MethodCodeType(System.Enum):
    """This class has no documentation."""

    IL = ...

    Native = ...

    OPTIL = ...

    Runtime = ...


class ReferenceAssemblyAttribute(System.Attribute):
    """Identifies an assembly as a reference assembly, which contains metadata but no executable code."""

    @property
    def Description(self) -> str:
        ...

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, description: str) -> None:
        ...


class DefaultInterpolatedStringHandler:
    """Provides a handler used by the language compiler to process interpolated strings into string instances."""

    @overload
    def __init__(self, literalLength: int, formattedCount: int) -> None:
        """
        Creates a handler used to translate an interpolated string into a string.
        
        :param literalLength: The number of constant characters outside of interpolation expressions in the interpolated string.
        :param formattedCount: The number of interpolation expressions in the interpolated string.
        """
        ...

    @overload
    def __init__(self, literalLength: int, formattedCount: int, provider: System.IFormatProvider) -> None:
        """
        Creates a handler used to translate an interpolated string into a string.
        
        :param literalLength: The number of constant characters outside of interpolation expressions in the interpolated string.
        :param formattedCount: The number of interpolation expressions in the interpolated string.
        :param provider: An object that supplies culture-specific formatting information.
        """
        ...

    @overload
    def __init__(self, literalLength: int, formattedCount: int, provider: System.IFormatProvider, initialBuffer: System.Span[str]) -> None:
        """
        Creates a handler used to translate an interpolated string into a string.
        
        :param literalLength: The number of constant characters outside of interpolation expressions in the interpolated string.
        :param formattedCount: The number of interpolation expressions in the interpolated string.
        :param provider: An object that supplies culture-specific formatting information.
        :param initialBuffer: A buffer temporarily transferred to the handler for use as part of its formatting.  Contents may be overwritten.
        """
        ...

    @overload
    def AppendFormatted(self, value: System_Runtime_CompilerServices_DefaultInterpolatedStringHandler_AppendFormatted_T) -> None:
        ...

    @overload
    def AppendFormatted(self, value: System_Runtime_CompilerServices_DefaultInterpolatedStringHandler_AppendFormatted_T, format: str) -> None:
        """
        Writes the specified value to the handler.
        
        :param value: The value to write.
        :param format: The format string.
        """
        ...

    @overload
    def AppendFormatted(self, value: System_Runtime_CompilerServices_DefaultInterpolatedStringHandler_AppendFormatted_T, alignment: int) -> None:
        """
        Writes the specified value to the handler.
        
        :param value: The value to write.
        :param alignment: Minimum number of characters that should be written for this value.  If the value is negative, it indicates left-aligned and the required minimum is the absolute value.
        """
        ...

    @overload
    def AppendFormatted(self, value: System_Runtime_CompilerServices_DefaultInterpolatedStringHandler_AppendFormatted_T, alignment: int, format: str) -> None:
        """
        Writes the specified value to the handler.
        
        :param value: The value to write.
        :param alignment: Minimum number of characters that should be written for this value.  If the value is negative, it indicates left-aligned and the required minimum is the absolute value.
        :param format: The format string.
        """
        ...

    @overload
    def AppendFormatted(self, value: System.ReadOnlySpan[str]) -> None:
        ...

    @overload
    def AppendFormatted(self, value: System.ReadOnlySpan[str], alignment: int = 0, format: str = None) -> None:
        """
        Writes the specified string of chars to the handler.
        
        :param value: The span to write.
        :param alignment: Minimum number of characters that should be written for this value.  If the value is negative, it indicates left-aligned and the required minimum is the absolute value.
        :param format: The format string.
        """
        ...

    @overload
    def AppendFormatted(self, value: str) -> None:
        ...

    @overload
    def AppendFormatted(self, value: str, alignment: int = 0, format: str = None) -> None:
        """
        Writes the specified value to the handler.
        
        :param value: The value to write.
        :param alignment: Minimum number of characters that should be written for this value.  If the value is negative, it indicates left-aligned and the required minimum is the absolute value.
        :param format: The format string.
        """
        ...

    @overload
    def AppendFormatted(self, value: typing.Any, alignment: int = 0, format: str = None) -> None:
        ...

    def AppendLiteral(self, value: str) -> None:
        """
        Writes the specified string to the handler.
        
        :param value: The string to write.
        """
        ...

    def ToString(self) -> str:
        """
        Gets the built string.
        
        :returns: The built string.
        """
        ...

    def ToStringAndClear(self) -> str:
        """
        Gets the built string and clears the handler.
        
        :returns: The built string.
        """
        ...


class TaskAwaiter(typing.Generic[System_Runtime_CompilerServices_TaskAwaiter_TResult], System.Runtime.CompilerServices.ICriticalNotifyCompletion, System.Runtime.CompilerServices.ITaskAwaiter):
    """Provides an awaiter for awaiting a Task{TResult}."""

    @property
    def IsCompleted(self) -> bool:
        """Gets whether the task being awaited is completed."""
        ...

    @overload
    def GetResult(self) -> None:
        """Ends the await on the completed Task."""
        ...

    @overload
    def GetResult(self) -> System_Runtime_CompilerServices_TaskAwaiter_TResult:
        """
        Ends the await on the completed Task{TResult}.
        
        :returns: The result of the completed Task{TResult}.
        """
        ...

    @overload
    def OnCompleted(self, continuation: typing.Callable[[], None]) -> None:
        """
        Schedules the continuation onto the Task associated with this TaskAwaiter.
        
        :param continuation: The action to invoke when the await operation completes.
        """
        ...

    @overload
    def OnCompleted(self, continuation: typing.Callable[[], None]) -> None:
        """
        Schedules the continuation onto the Task associated with this TaskAwaiter.
        
        :param continuation: The action to invoke when the await operation completes.
        """
        ...

    @overload
    def UnsafeOnCompleted(self, continuation: typing.Callable[[], None]) -> None:
        """
        Schedules the continuation onto the Task associated with this TaskAwaiter.
        
        :param continuation: The action to invoke when the await operation completes.
        """
        ...

    @overload
    def UnsafeOnCompleted(self, continuation: typing.Callable[[], None]) -> None:
        """
        Schedules the continuation onto the Task associated with this TaskAwaiter.
        
        :param continuation: The action to invoke when the await operation completes.
        """
        ...


class ConfiguredTaskAwaitable(typing.Generic[System_Runtime_CompilerServices_ConfiguredTaskAwaitable_TResult]):
    """Provides an awaitable object that allows for configured awaits on Task{TResult}."""

    @overload
    def GetAwaiter(self) -> System.Runtime.CompilerServices.ConfiguredTaskAwaitable.ConfiguredTaskAwaiter:
        """
        Gets an awaiter for this awaitable.
        
        :returns: The awaiter.
        """
        ...

    @overload
    def GetAwaiter(self) -> System.Runtime.CompilerServices.ConfiguredTaskAwaitable.ConfiguredTaskAwaiter:
        """
        Gets an awaiter for this awaitable.
        
        :returns: The awaiter.
        """
        ...


class FixedAddressValueTypeAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class CompilationRelaxationsAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def CompilationRelaxations(self) -> int:
        ...

    @overload
    def __init__(self, relaxations: int) -> None:
        ...

    @overload
    def __init__(self, relaxations: System.Runtime.CompilerServices.CompilationRelaxations) -> None:
        ...


class InlineArrayAttribute(System.Attribute):
    """Indicates that the instance's storage is sequentially replicated "length" times."""

    @property
    def Length(self) -> int:
        """Gets the number of sequential fields to replicate in the inline array type."""
        ...

    def __init__(self, length: int) -> None:
        """
        Creates a new InlineArrayAttribute instance with the specified length.
        
        :param length: The number of sequential fields to replicate in the inline array type.
        """
        ...


class ConfiguredAsyncDisposable:
    """Provides a type that can be used to configure how awaits on an IAsyncDisposable are performed."""

    def DisposeAsync(self) -> System.Runtime.CompilerServices.ConfiguredValueTaskAwaitable:
        """
        Asynchronously releases the unmanaged resources used by the System.Runtime.CompilerServices.ConfiguredAsyncDisposable.
        
        :returns: A task that represents the asynchronous dispose operation.
        """
        ...


class MethodImplAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def MethodCodeType(self) -> System.Runtime.CompilerServices.MethodCodeType:
        ...

    @property
    def Value(self) -> int:
        """This property contains the int value of a member of the System.Runtime.CompilerServices.MethodImplOptions enum."""
        ...

    @overload
    def __init__(self, methodImplOptions: System.Runtime.CompilerServices.MethodImplOptions) -> None:
        ...

    @overload
    def __init__(self, value: int) -> None:
        ...

    @overload
    def __init__(self) -> None:
        ...


class CompilerGlobalScopeAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class MetadataUpdateOriginalTypeAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def OriginalType(self) -> typing.Type:
        ...

    def __init__(self, originalType: typing.Type) -> None:
        """
        This attribute is emitted by Roslyn when a type that is marked with (or derives
        from a type that is marked with) CreateNewOnMetadataUpdateAttribute is updated
        during a hot reload session.  The OriginalType points to the original version
        of the updated type.  The next update of the type will have the same OriginalType. Frameworks that provide support for hot reload by implementing a
        Reflection.Metadata.MetadataUpdateHandlerAttribute may use this
        attribute to relate an updated type to its original version.
        
        :param originalType: The original type that was updated
        """
        ...


class DiscardableAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class CallerArgumentExpressionAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def ParameterName(self) -> str:
        ...

    def __init__(self, parameterName: str) -> None:
        ...


class IsByRefLikeAttribute(System.Attribute):
    """
    Reserved for use by a compiler for tracking metadata.
    This attribute should not be used by developers in source code.
    """

    def __init__(self) -> None:
        """Initializes the attribute."""
        ...


class SkipLocalsInitAttribute(System.Attribute):
    """
    Used to indicate to the compiler that the .locals init
    flag should not be set in method headers.
    """

    def __init__(self) -> None:
        ...


class ConfiguredCancelableAsyncEnumerable(typing.Generic[System_Runtime_CompilerServices_ConfiguredCancelableAsyncEnumerable_T]):
    """Provides an awaitable async enumerable that enables cancelable iteration and configured awaits."""

    class Enumerator:
        """Provides an awaitable async enumerator that enables cancelable iteration and configured awaits."""

        @property
        def Current(self) -> System_Runtime_CompilerServices_ConfiguredCancelableAsyncEnumerable_T:
            """Gets the element in the collection at the current position of the enumerator."""
            ...

        def DisposeAsync(self) -> System.Runtime.CompilerServices.ConfiguredValueTaskAwaitable:
            """
            Performs application-defined tasks associated with freeing, releasing, or
            resetting unmanaged resources asynchronously.
            """
            ...

        def MoveNextAsync(self) -> System.Runtime.CompilerServices.ConfiguredValueTaskAwaitable[bool]:
            """
            Advances the enumerator asynchronously to the next element of the collection.
            
            :returns: A ConfiguredValueTaskAwaitable{Boolean} that will complete with a result of true if the enumerator was successfully advanced to the next element, or false if the enumerator has passed the end of the collection.
            """
            ...

    def ConfigureAwait(self, continueOnCapturedContext: bool) -> System.Runtime.CompilerServices.ConfiguredCancelableAsyncEnumerable[System_Runtime_CompilerServices_ConfiguredCancelableAsyncEnumerable_T]:
        """
        Configures how awaits on the tasks returned from an async iteration will be performed.
        
        :param continueOnCapturedContext: Whether to capture and marshal back to the current context.
        :returns: The configured enumerable.
        """
        ...

    def GetAsyncEnumerator(self) -> System.Runtime.CompilerServices.ConfiguredCancelableAsyncEnumerable.Enumerator:
        """
        Returns an enumerator that iterates asynchronously through collections that enables cancelable iteration and configured awaits.
        
        :returns: An enumerator for the System.Runtime.CompilerServices.ConfiguredCancelableAsyncEnumerable`1 class.
        """
        ...

    def WithCancellation(self, cancellationToken: System.Threading.CancellationToken) -> System.Runtime.CompilerServices.ConfiguredCancelableAsyncEnumerable[System_Runtime_CompilerServices_ConfiguredCancelableAsyncEnumerable_T]:
        """
        Sets the CancellationToken to be passed to IAsyncEnumerable{T}.GetAsyncEnumerator(CancellationToken) when iterating.
        
        :param cancellationToken: The CancellationToken to use.
        :returns: The configured enumerable.
        """
        ...


class ICastable(metaclass=abc.ABCMeta):
    """
    Support for dynamic interface casting. Specifically implementing this interface on a type will allow the
    type to support interfaces (for the purposes of casting and interface dispatch) that do not appear in its
    interface map.
    """


class RequiresLocationAttribute(System.Attribute):
    """
    Reserved for use by a compiler for tracking metadata.
    This attribute should not be used by developers in source code.
    """

    def __init__(self) -> None:
        """Initializes the attribute."""
        ...


class _EventContainer(typing.Generic[System_Runtime_CompilerServices__EventContainer_Callable, System_Runtime_CompilerServices__EventContainer_ReturnType]):
    """This class is used to provide accurate autocomplete on events and cannot be imported."""

    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> System_Runtime_CompilerServices__EventContainer_ReturnType:
        """Fires the event."""
        ...

    def __iadd__(self, item: System_Runtime_CompilerServices__EventContainer_Callable) -> None:
        """Registers an event handler."""
        ...

    def __isub__(self, item: System_Runtime_CompilerServices__EventContainer_Callable) -> None:
        """Unregisters an event handler."""
        ...



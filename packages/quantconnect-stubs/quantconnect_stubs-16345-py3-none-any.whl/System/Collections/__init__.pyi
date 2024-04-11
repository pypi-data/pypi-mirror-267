from typing import overload
import abc
import typing
import warnings

import System
import System.Collections
import System.Globalization
import System.Runtime.Serialization


class IStructuralComparable(metaclass=abc.ABCMeta):
    """This class has no documentation."""


class IEnumerable(metaclass=abc.ABCMeta):
    """This class has no documentation."""


class ICollection(System.Collections.IEnumerable, metaclass=abc.ABCMeta):
    """This class has no documentation."""


class IList(System.Collections.ICollection, metaclass=abc.ABCMeta):
    """This class has no documentation."""


class IComparer(metaclass=abc.ABCMeta):
    """This class has no documentation."""


class IEnumerator(metaclass=abc.ABCMeta):
    """This class has no documentation."""


class ArrayList(System.Object, System.Collections.IList, System.ICloneable):
    """Implements the IList interface using an array whose size is dynamically increased as required."""

    @property
    def Capacity(self) -> int:
        ...

    @property
    def Count(self) -> int:
        ...

    @property
    def IsFixedSize(self) -> bool:
        ...

    @property
    def IsReadOnly(self) -> bool:
        ...

    @property
    def IsSynchronized(self) -> bool:
        ...

    @property
    def SyncRoot(self) -> System.Object:
        ...

    def __getitem__(self, index: int) -> typing.Any:
        ...

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, capacity: int) -> None:
        ...

    @overload
    def __init__(self, c: System.Collections.ICollection) -> None:
        ...

    def __setitem__(self, index: int, value: typing.Any) -> None:
        ...

    @staticmethod
    def Adapter(list: System.Collections.IList) -> System.Collections.ArrayList:
        ...

    def Add(self, value: typing.Any) -> int:
        ...

    def AddRange(self, c: System.Collections.ICollection) -> None:
        ...

    @overload
    def BinarySearch(self, index: int, count: int, value: typing.Any, comparer: System.Collections.IComparer) -> int:
        ...

    @overload
    def BinarySearch(self, value: typing.Any) -> int:
        ...

    @overload
    def BinarySearch(self, value: typing.Any, comparer: System.Collections.IComparer) -> int:
        ...

    def Clear(self) -> None:
        ...

    def Clone(self) -> System.Object:
        ...

    def Contains(self, item: typing.Any) -> bool:
        ...

    @overload
    def CopyTo(self, array: System.Array) -> None:
        ...

    @overload
    def CopyTo(self, array: System.Array, arrayIndex: int) -> None:
        ...

    @overload
    def CopyTo(self, index: int, array: System.Array, arrayIndex: int, count: int) -> None:
        ...

    @staticmethod
    @overload
    def FixedSize(list: System.Collections.IList) -> System.Collections.IList:
        ...

    @staticmethod
    @overload
    def FixedSize(list: System.Collections.ArrayList) -> System.Collections.ArrayList:
        ...

    @overload
    def GetEnumerator(self) -> System.Collections.IEnumerator:
        ...

    @overload
    def GetEnumerator(self, index: int, count: int) -> System.Collections.IEnumerator:
        ...

    def GetRange(self, index: int, count: int) -> System.Collections.ArrayList:
        ...

    @overload
    def IndexOf(self, value: typing.Any) -> int:
        ...

    @overload
    def IndexOf(self, value: typing.Any, startIndex: int) -> int:
        ...

    @overload
    def IndexOf(self, value: typing.Any, startIndex: int, count: int) -> int:
        ...

    def Insert(self, index: int, value: typing.Any) -> None:
        ...

    def InsertRange(self, index: int, c: System.Collections.ICollection) -> None:
        ...

    @overload
    def LastIndexOf(self, value: typing.Any) -> int:
        ...

    @overload
    def LastIndexOf(self, value: typing.Any, startIndex: int) -> int:
        ...

    @overload
    def LastIndexOf(self, value: typing.Any, startIndex: int, count: int) -> int:
        ...

    @staticmethod
    @overload
    def ReadOnly(list: System.Collections.IList) -> System.Collections.IList:
        ...

    @staticmethod
    @overload
    def ReadOnly(list: System.Collections.ArrayList) -> System.Collections.ArrayList:
        ...

    def Remove(self, obj: typing.Any) -> None:
        ...

    def RemoveAt(self, index: int) -> None:
        ...

    def RemoveRange(self, index: int, count: int) -> None:
        ...

    @staticmethod
    def Repeat(value: typing.Any, count: int) -> System.Collections.ArrayList:
        ...

    @overload
    def Reverse(self) -> None:
        ...

    @overload
    def Reverse(self, index: int, count: int) -> None:
        ...

    def SetRange(self, index: int, c: System.Collections.ICollection) -> None:
        ...

    @overload
    def Sort(self) -> None:
        ...

    @overload
    def Sort(self, comparer: System.Collections.IComparer) -> None:
        ...

    @overload
    def Sort(self, index: int, count: int, comparer: System.Collections.IComparer) -> None:
        ...

    @staticmethod
    @overload
    def Synchronized(list: System.Collections.IList) -> System.Collections.IList:
        ...

    @staticmethod
    @overload
    def Synchronized(list: System.Collections.ArrayList) -> System.Collections.ArrayList:
        ...

    @overload
    def ToArray(self) -> typing.List[System.Object]:
        ...

    @overload
    def ToArray(self, type: typing.Type) -> System.Array:
        ...

    def TrimToSize(self) -> None:
        ...


class IHashCodeProvider(metaclass=abc.ABCMeta):
    """
    Provides a mechanism for a Hashtable user to override the default
    GetHashCode() function on Objects, providing their own hash function.
    
    IHashCodeProvider has been deprecated. Use IEqualityComparer instead.
    """


class IDictionary(System.Collections.ICollection, metaclass=abc.ABCMeta):
    """This class has no documentation."""


class IDictionaryEnumerator(System.Collections.IEnumerator, metaclass=abc.ABCMeta):
    """This class has no documentation."""


class ListDictionaryInternal(System.Object, System.Collections.IDictionary):
    """
    Implements IDictionary using a singly linked list.
    Recommended for collections that typically include fewer than 10 items.
    """

    @property
    def Count(self) -> int:
        ...

    @property
    def Keys(self) -> System.Collections.ICollection:
        ...

    @property
    def IsReadOnly(self) -> bool:
        ...

    @property
    def IsFixedSize(self) -> bool:
        ...

    @property
    def IsSynchronized(self) -> bool:
        ...

    @property
    def SyncRoot(self) -> System.Object:
        ...

    @property
    def Values(self) -> System.Collections.ICollection:
        ...

    def __getitem__(self, key: typing.Any) -> typing.Any:
        ...

    def __init__(self) -> None:
        ...

    def __setitem__(self, key: typing.Any, value: typing.Any) -> None:
        ...

    def Add(self, key: typing.Any, value: typing.Any) -> None:
        ...

    def Clear(self) -> None:
        ...

    def Contains(self, key: typing.Any) -> bool:
        ...

    def CopyTo(self, array: System.Array, index: int) -> None:
        ...

    def GetEnumerator(self) -> System.Collections.IDictionaryEnumerator:
        ...

    def Remove(self, key: typing.Any) -> None:
        ...


class Comparer(System.Object, System.Collections.IComparer, System.Runtime.Serialization.ISerializable):
    """Compares two objects for equivalence, where string comparisons are case-sensitive."""

    Default: System.Collections.Comparer = ...

    DefaultInvariant: System.Collections.Comparer = ...

    def __init__(self, culture: System.Globalization.CultureInfo) -> None:
        ...

    def Compare(self, a: typing.Any, b: typing.Any) -> int:
        ...

    def GetObjectData(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        """Obsoletions.LegacyFormatterImplMessage"""
        warnings.warn("Obsoletions.LegacyFormatterImplMessage", DeprecationWarning)


class IStructuralEquatable(metaclass=abc.ABCMeta):
    """This class has no documentation."""


class IEqualityComparer(metaclass=abc.ABCMeta):
    """This class has no documentation."""


class Hashtable(System.Object, System.Collections.IDictionary, System.Runtime.Serialization.ISerializable, System.Runtime.Serialization.IDeserializationCallback, System.ICloneable):
    """This class has no documentation."""

    @property
    def hcp(self) -> System.Collections.IHashCodeProvider:
        """
        This property is protected.
        
        Hashtable.hcp has been deprecated. Use the EqualityComparer property instead.
        """
        warnings.warn("Hashtable.hcp has been deprecated. Use the EqualityComparer property instead.", DeprecationWarning)

    @property
    def comparer(self) -> System.Collections.IComparer:
        """
        This property is protected.
        
        Hashtable.comparer has been deprecated. Use the KeyComparer properties instead.
        """
        warnings.warn("Hashtable.comparer has been deprecated. Use the KeyComparer properties instead.", DeprecationWarning)

    @property
    def EqualityComparer(self) -> System.Collections.IEqualityComparer:
        """This property is protected."""
        ...

    @property
    def IsReadOnly(self) -> bool:
        ...

    @property
    def IsFixedSize(self) -> bool:
        ...

    @property
    def IsSynchronized(self) -> bool:
        ...

    @property
    def Keys(self) -> System.Collections.ICollection:
        ...

    @property
    def Values(self) -> System.Collections.ICollection:
        ...

    @property
    def SyncRoot(self) -> System.Object:
        ...

    @property
    def Count(self) -> int:
        ...

    def __getitem__(self, key: typing.Any) -> typing.Any:
        ...

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, capacity: int) -> None:
        ...

    @overload
    def __init__(self, capacity: int, loadFactor: float) -> None:
        ...

    @overload
    def __init__(self, capacity: int, loadFactor: float, equalityComparer: System.Collections.IEqualityComparer) -> None:
        ...

    @overload
    def __init__(self, equalityComparer: System.Collections.IEqualityComparer) -> None:
        ...

    @overload
    def __init__(self, capacity: int, equalityComparer: System.Collections.IEqualityComparer) -> None:
        ...

    @overload
    def __init__(self, d: System.Collections.IDictionary) -> None:
        ...

    @overload
    def __init__(self, d: System.Collections.IDictionary, loadFactor: float) -> None:
        ...

    @overload
    def __init__(self, d: System.Collections.IDictionary, equalityComparer: System.Collections.IEqualityComparer) -> None:
        ...

    @overload
    def __init__(self, d: System.Collections.IDictionary, loadFactor: float, equalityComparer: System.Collections.IEqualityComparer) -> None:
        ...

    @overload
    def __init__(self, hcp: System.Collections.IHashCodeProvider, comparer: System.Collections.IComparer) -> None:
        """This constructor has been deprecated. Use Hashtable(IEqualityComparer) instead."""
        ...

    @overload
    def __init__(self, capacity: int, hcp: System.Collections.IHashCodeProvider, comparer: System.Collections.IComparer) -> None:
        """This constructor has been deprecated. Use Hashtable(int, IEqualityComparer) instead."""
        ...

    @overload
    def __init__(self, d: System.Collections.IDictionary, hcp: System.Collections.IHashCodeProvider, comparer: System.Collections.IComparer) -> None:
        """This constructor has been deprecated. Use Hashtable(IDictionary, IEqualityComparer) instead."""
        ...

    @overload
    def __init__(self, capacity: int, loadFactor: float, hcp: System.Collections.IHashCodeProvider, comparer: System.Collections.IComparer) -> None:
        """This constructor has been deprecated. Use Hashtable(int, float, IEqualityComparer) instead."""
        ...

    @overload
    def __init__(self, d: System.Collections.IDictionary, loadFactor: float, hcp: System.Collections.IHashCodeProvider, comparer: System.Collections.IComparer) -> None:
        """This constructor has been deprecated. Use Hashtable(IDictionary, float, IEqualityComparer) instead."""
        ...

    @overload
    def __init__(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        """
        This method is protected.
        
        Obsoletions.LegacyFormatterImplMessage
        """
        ...

    def __setitem__(self, key: typing.Any, value: typing.Any) -> None:
        ...

    def Add(self, key: typing.Any, value: typing.Any) -> None:
        ...

    def Clear(self) -> None:
        ...

    def Clone(self) -> System.Object:
        ...

    def Contains(self, key: typing.Any) -> bool:
        ...

    def ContainsKey(self, key: typing.Any) -> bool:
        ...

    def ContainsValue(self, value: typing.Any) -> bool:
        ...

    def CopyTo(self, array: System.Array, arrayIndex: int) -> None:
        ...

    def GetEnumerator(self) -> System.Collections.IDictionaryEnumerator:
        ...

    def GetHash(self, key: typing.Any) -> int:
        """This method is protected."""
        ...

    def GetObjectData(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        """Obsoletions.LegacyFormatterImplMessage"""
        warnings.warn("Obsoletions.LegacyFormatterImplMessage", DeprecationWarning)

    def KeyEquals(self, item: typing.Any, key: typing.Any) -> bool:
        """This method is protected."""
        ...

    def OnDeserialization(self, sender: typing.Any) -> None:
        ...

    def Remove(self, key: typing.Any) -> None:
        ...

    @staticmethod
    def Synchronized(table: System.Collections.Hashtable) -> System.Collections.Hashtable:
        ...


class DictionaryEntry:
    """This class has no documentation."""

    @property
    def Key(self) -> System.Object:
        ...

    @property
    def Value(self) -> System.Object:
        ...

    def __init__(self, key: typing.Any, value: typing.Any) -> None:
        ...

    def Deconstruct(self, key: typing.Optional[typing.Any], value: typing.Optional[typing.Any]) -> typing.Union[None, typing.Any, typing.Any]:
        ...

    def ToString(self) -> str:
        ...


class StructuralComparisons(System.Object):
    """This class has no documentation."""

    StructuralComparer: System.Collections.IComparer

    StructuralEqualityComparer: System.Collections.IEqualityComparer


class BitArray(System.Object, System.Collections.ICollection, System.ICloneable):
    """This class has no documentation."""

    @property
    def Length(self) -> int:
        ...

    @property
    def Count(self) -> int:
        ...

    @property
    def SyncRoot(self) -> System.Object:
        ...

    @property
    def IsSynchronized(self) -> bool:
        ...

    @property
    def IsReadOnly(self) -> bool:
        ...

    def __getitem__(self, index: int) -> bool:
        ...

    @overload
    def __init__(self, length: int) -> None:
        ...

    @overload
    def __init__(self, length: int, defaultValue: bool) -> None:
        ...

    @overload
    def __init__(self, bytes: typing.List[int]) -> None:
        ...

    @overload
    def __init__(self, values: typing.List[bool]) -> None:
        ...

    @overload
    def __init__(self, values: typing.List[int]) -> None:
        ...

    @overload
    def __init__(self, bits: System.Collections.BitArray) -> None:
        ...

    def __setitem__(self, index: int, value: bool) -> None:
        ...

    def And(self, value: System.Collections.BitArray) -> System.Collections.BitArray:
        ...

    def Clone(self) -> System.Object:
        ...

    def CopyTo(self, array: System.Array, index: int) -> None:
        ...

    def Get(self, index: int) -> bool:
        ...

    def GetEnumerator(self) -> System.Collections.IEnumerator:
        ...

    def HasAllSet(self) -> bool:
        """
        Determines whether all bits in the BitArray are set to true.
        
        :returns: true if every bit in the BitArray is set to true, or if BitArray is empty; otherwise, false.
        """
        ...

    def HasAnySet(self) -> bool:
        """
        Determines whether any bit in the BitArray is set to true.
        
        :returns: true if BitArray is not empty and at least one of its bit is set to true; otherwise, false.
        """
        ...

    def LeftShift(self, count: int) -> System.Collections.BitArray:
        ...

    def Not(self) -> System.Collections.BitArray:
        ...

    def Or(self, value: System.Collections.BitArray) -> System.Collections.BitArray:
        ...

    def RightShift(self, count: int) -> System.Collections.BitArray:
        ...

    def Set(self, index: int, value: bool) -> None:
        ...

    def SetAll(self, value: bool) -> None:
        ...

    def Xor(self, value: System.Collections.BitArray) -> System.Collections.BitArray:
        ...



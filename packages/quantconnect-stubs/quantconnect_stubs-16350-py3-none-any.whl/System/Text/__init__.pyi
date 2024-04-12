from typing import overload
import abc
import typing

import System
import System.Collections.Generic
import System.Globalization
import System.IO
import System.Runtime.Serialization
import System.Text

System_Text_Rune = typing.Any

System_Text_StringBuilder_AppendFormat_TArg0 = typing.TypeVar("System_Text_StringBuilder_AppendFormat_TArg0")
System_Text_StringBuilder_AppendFormat_TArg1 = typing.TypeVar("System_Text_StringBuilder_AppendFormat_TArg1")
System_Text_StringBuilder_AppendFormat_TArg2 = typing.TypeVar("System_Text_StringBuilder_AppendFormat_TArg2")
System_Text_StringBuilder_AppendJoin_T = typing.TypeVar("System_Text_StringBuilder_AppendJoin_T")
System_Text_StringBuilder_AppendFormatted_AppendInterpolatedStringHandler_T = typing.TypeVar("System_Text_StringBuilder_AppendFormatted_AppendInterpolatedStringHandler_T")


class DecoderFallbackBuffer(System.Object, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    @abc.abstractmethod
    def Remaining(self) -> int:
        ...

    def Fallback(self, bytesUnknown: typing.List[int], index: int) -> bool:
        ...

    def GetNextChar(self) -> str:
        ...

    def MovePrevious(self) -> bool:
        ...

    def Reset(self) -> None:
        ...


class DecoderFallback(System.Object, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    ReplacementFallback: System.Text.DecoderFallback

    ExceptionFallback: System.Text.DecoderFallback

    @property
    @abc.abstractmethod
    def MaxCharCount(self) -> int:
        ...

    def CreateFallbackBuffer(self) -> System.Text.DecoderFallbackBuffer:
        ...


class DecoderExceptionFallback(System.Text.DecoderFallback):
    """This class has no documentation."""

    @property
    def MaxCharCount(self) -> int:
        ...

    def CreateFallbackBuffer(self) -> System.Text.DecoderFallbackBuffer:
        ...

    def Equals(self, value: typing.Any) -> bool:
        ...

    def GetHashCode(self) -> int:
        ...


class DecoderExceptionFallbackBuffer(System.Text.DecoderFallbackBuffer):
    """This class has no documentation."""

    @property
    def Remaining(self) -> int:
        ...

    def Fallback(self, bytesUnknown: typing.List[int], index: int) -> bool:
        ...

    def GetNextChar(self) -> str:
        ...

    def MovePrevious(self) -> bool:
        ...


class DecoderFallbackException(System.ArgumentException):
    """This class has no documentation."""

    @property
    def BytesUnknown(self) -> typing.List[int]:
        ...

    @property
    def Index(self) -> int:
        ...

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, message: str) -> None:
        ...

    @overload
    def __init__(self, message: str, innerException: System.Exception) -> None:
        ...

    @overload
    def __init__(self, message: str, bytesUnknown: typing.List[int], index: int) -> None:
        ...


class EncoderFallbackBuffer(System.Object, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    @abc.abstractmethod
    def Remaining(self) -> int:
        ...

    @overload
    def Fallback(self, charUnknown: str, index: int) -> bool:
        ...

    @overload
    def Fallback(self, charUnknownHigh: str, charUnknownLow: str, index: int) -> bool:
        ...

    def GetNextChar(self) -> str:
        ...

    def MovePrevious(self) -> bool:
        ...

    def Reset(self) -> None:
        ...


class EncoderFallback(System.Object, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    ReplacementFallback: System.Text.EncoderFallback

    ExceptionFallback: System.Text.EncoderFallback

    @property
    @abc.abstractmethod
    def MaxCharCount(self) -> int:
        ...

    def CreateFallbackBuffer(self) -> System.Text.EncoderFallbackBuffer:
        ...


class EncodingProvider(System.Object, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...

    @overload
    def GetEncoding(self, name: str) -> System.Text.Encoding:
        ...

    @overload
    def GetEncoding(self, codepage: int) -> System.Text.Encoding:
        ...

    @overload
    def GetEncoding(self, name: str, encoderFallback: System.Text.EncoderFallback, decoderFallback: System.Text.DecoderFallback) -> System.Text.Encoding:
        ...

    @overload
    def GetEncoding(self, codepage: int, encoderFallback: System.Text.EncoderFallback, decoderFallback: System.Text.DecoderFallback) -> System.Text.Encoding:
        ...

    def GetEncodings(self) -> System.Collections.Generic.IEnumerable[System.Text.EncodingInfo]:
        ...


class NormalizationForm(System.Enum):
    """This class has no documentation."""

    FormC = 1

    FormD = 2

    FormKC = 5

    FormKD = 6


class Decoder(System.Object, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    def Fallback(self) -> System.Text.DecoderFallback:
        ...

    @property
    def FallbackBuffer(self) -> System.Text.DecoderFallbackBuffer:
        ...

    def __init__(self) -> None:
        """This method is protected."""
        ...

    @overload
    def Convert(self, bytes: typing.List[int], byteIndex: int, byteCount: int, chars: typing.List[str], charIndex: int, charCount: int, flush: bool, bytesUsed: typing.Optional[int], charsUsed: typing.Optional[int], completed: typing.Optional[bool]) -> typing.Union[None, int, int, bool]:
        ...

    @overload
    def Convert(self, bytes: typing.Any, byteCount: int, chars: typing.Any, charCount: int, flush: bool, bytesUsed: typing.Optional[int], charsUsed: typing.Optional[int], completed: typing.Optional[bool]) -> typing.Union[None, int, int, bool]:
        ...

    @overload
    def Convert(self, bytes: System.ReadOnlySpan[int], chars: System.Span[str], flush: bool, bytesUsed: typing.Optional[int], charsUsed: typing.Optional[int], completed: typing.Optional[bool]) -> typing.Union[None, int, int, bool]:
        ...

    @overload
    def GetCharCount(self, bytes: typing.List[int], index: int, count: int) -> int:
        ...

    @overload
    def GetCharCount(self, bytes: typing.List[int], index: int, count: int, flush: bool) -> int:
        ...

    @overload
    def GetCharCount(self, bytes: typing.Any, count: int, flush: bool) -> int:
        ...

    @overload
    def GetCharCount(self, bytes: System.ReadOnlySpan[int], flush: bool) -> int:
        ...

    @overload
    def GetChars(self, bytes: typing.List[int], byteIndex: int, byteCount: int, chars: typing.List[str], charIndex: int) -> int:
        ...

    @overload
    def GetChars(self, bytes: typing.List[int], byteIndex: int, byteCount: int, chars: typing.List[str], charIndex: int, flush: bool) -> int:
        ...

    @overload
    def GetChars(self, bytes: typing.Any, byteCount: int, chars: typing.Any, charCount: int, flush: bool) -> int:
        ...

    @overload
    def GetChars(self, bytes: System.ReadOnlySpan[int], chars: System.Span[str], flush: bool) -> int:
        ...

    def Reset(self) -> None:
        ...


class Encoder(System.Object, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    def Fallback(self) -> System.Text.EncoderFallback:
        ...

    @property
    def FallbackBuffer(self) -> System.Text.EncoderFallbackBuffer:
        ...

    def __init__(self) -> None:
        """This method is protected."""
        ...

    @overload
    def Convert(self, chars: typing.List[str], charIndex: int, charCount: int, bytes: typing.List[int], byteIndex: int, byteCount: int, flush: bool, charsUsed: typing.Optional[int], bytesUsed: typing.Optional[int], completed: typing.Optional[bool]) -> typing.Union[None, int, int, bool]:
        ...

    @overload
    def Convert(self, chars: typing.Any, charCount: int, bytes: typing.Any, byteCount: int, flush: bool, charsUsed: typing.Optional[int], bytesUsed: typing.Optional[int], completed: typing.Optional[bool]) -> typing.Union[None, int, int, bool]:
        ...

    @overload
    def Convert(self, chars: System.ReadOnlySpan[str], bytes: System.Span[int], flush: bool, charsUsed: typing.Optional[int], bytesUsed: typing.Optional[int], completed: typing.Optional[bool]) -> typing.Union[None, int, int, bool]:
        ...

    @overload
    def GetByteCount(self, chars: typing.List[str], index: int, count: int, flush: bool) -> int:
        ...

    @overload
    def GetByteCount(self, chars: typing.Any, count: int, flush: bool) -> int:
        ...

    @overload
    def GetByteCount(self, chars: System.ReadOnlySpan[str], flush: bool) -> int:
        ...

    @overload
    def GetBytes(self, chars: typing.List[str], charIndex: int, charCount: int, bytes: typing.List[int], byteIndex: int, flush: bool) -> int:
        ...

    @overload
    def GetBytes(self, chars: typing.Any, charCount: int, bytes: typing.Any, byteCount: int, flush: bool) -> int:
        ...

    @overload
    def GetBytes(self, chars: System.ReadOnlySpan[str], bytes: System.Span[int], flush: bool) -> int:
        ...

    def Reset(self) -> None:
        ...


class EncodingInfo(System.Object):
    """This class has no documentation."""

    @property
    def CodePage(self) -> int:
        """Get the encoding codepage number"""
        ...

    @property
    def Name(self) -> str:
        """Get the encoding name"""
        ...

    @property
    def DisplayName(self) -> str:
        """Get the encoding display name"""
        ...

    def __init__(self, provider: System.Text.EncodingProvider, codePage: int, name: str, displayName: str) -> None:
        """
        Construct an EncodingInfo object.
        
        :param provider: The EncodingProvider object which created this EncodingInfo object
        :param codePage: The encoding codepage
        :param name: The encoding name
        :param displayName: The encoding display name
        """
        ...

    def Equals(self, value: typing.Any) -> bool:
        """
        Compare this EncodingInfo object to other object.
        
        :param value: The other object to compare with this object
        :returns: True if the value object is EncodingInfo object and has a codepage equals to this EncodingInfo object codepage. Otherwise, it returns False.
        """
        ...

    def GetEncoding(self) -> System.Text.Encoding:
        """
        Get the Encoding object match the information in the EncodingInfo object
        
        :returns: The Encoding object.
        """
        ...

    def GetHashCode(self) -> int:
        """
        Get a hashcode representing the current EncodingInfo object.
        
        :returns: The integer value representing the hash code of the EncodingInfo object.
        """
        ...


class Encoding(System.Object, System.ICloneable):
    """This class has no documentation."""

    Default: System.Text.Encoding

    @property
    def Preamble(self) -> System.ReadOnlySpan[int]:
        ...

    @property
    def BodyName(self) -> str:
        ...

    @property
    def EncodingName(self) -> str:
        ...

    @property
    def HeaderName(self) -> str:
        ...

    @property
    def WebName(self) -> str:
        ...

    @property
    def WindowsCodePage(self) -> int:
        ...

    @property
    def IsBrowserDisplay(self) -> bool:
        ...

    @property
    def IsBrowserSave(self) -> bool:
        ...

    @property
    def IsMailNewsDisplay(self) -> bool:
        ...

    @property
    def IsMailNewsSave(self) -> bool:
        ...

    @property
    def IsSingleByte(self) -> bool:
        ...

    @property
    def EncoderFallback(self) -> System.Text.EncoderFallback:
        ...

    @property
    def DecoderFallback(self) -> System.Text.DecoderFallback:
        ...

    @property
    def IsReadOnly(self) -> bool:
        ...

    ASCII: System.Text.Encoding

    Latin1: System.Text.Encoding
    """Gets an encoding for the Latin1 character set (ISO-8859-1)."""

    @property
    def CodePage(self) -> int:
        ...

    Unicode: System.Text.Encoding

    BigEndianUnicode: System.Text.Encoding

    UTF7: System.Text.Encoding
    """Obsoletions.SystemTextEncodingUTF7Message"""

    UTF8: System.Text.Encoding

    UTF32: System.Text.Encoding

    @overload
    def __init__(self) -> None:
        """This method is protected."""
        ...

    @overload
    def __init__(self, codePage: int) -> None:
        """This method is protected."""
        ...

    @overload
    def __init__(self, codePage: int, encoderFallback: System.Text.EncoderFallback, decoderFallback: System.Text.DecoderFallback) -> None:
        """This method is protected."""
        ...

    def Clone(self) -> System.Object:
        ...

    @staticmethod
    @overload
    def Convert(srcEncoding: System.Text.Encoding, dstEncoding: System.Text.Encoding, bytes: typing.List[int]) -> typing.List[int]:
        ...

    @staticmethod
    @overload
    def Convert(srcEncoding: System.Text.Encoding, dstEncoding: System.Text.Encoding, bytes: typing.List[int], index: int, count: int) -> typing.List[int]:
        ...

    @staticmethod
    def CreateTranscodingStream(innerStream: System.IO.Stream, innerStreamEncoding: System.Text.Encoding, outerStreamEncoding: System.Text.Encoding, leaveOpen: bool = False) -> System.IO.Stream:
        """
        Creates a Stream which serves to transcode data between an inner Encoding
        and an outer Encoding, similar to Convert.
        
        :param innerStream: The Stream to wrap.
        :param innerStreamEncoding: The Encoding associated with .
        :param outerStreamEncoding: The Encoding associated with the Stream returned by this method.
        :param leaveOpen: true if disposing the Stream returned by this method should not dispose .
        :returns: A Stream which transcodes the contents of  as .
        """
        ...

    def Equals(self, value: typing.Any) -> bool:
        ...

    @overload
    def GetByteCount(self, chars: typing.List[str]) -> int:
        ...

    @overload
    def GetByteCount(self, s: str) -> int:
        ...

    @overload
    def GetByteCount(self, chars: typing.List[str], index: int, count: int) -> int:
        ...

    @overload
    def GetByteCount(self, s: str, index: int, count: int) -> int:
        ...

    @overload
    def GetByteCount(self, chars: typing.Any, count: int) -> int:
        ...

    @overload
    def GetByteCount(self, chars: System.ReadOnlySpan[str]) -> int:
        ...

    @overload
    def GetBytes(self, chars: typing.List[str]) -> typing.List[int]:
        ...

    @overload
    def GetBytes(self, chars: typing.List[str], index: int, count: int) -> typing.List[int]:
        ...

    @overload
    def GetBytes(self, chars: typing.List[str], charIndex: int, charCount: int, bytes: typing.List[int], byteIndex: int) -> int:
        ...

    @overload
    def GetBytes(self, s: str) -> typing.List[int]:
        ...

    @overload
    def GetBytes(self, s: str, index: int, count: int) -> typing.List[int]:
        ...

    @overload
    def GetBytes(self, s: str, charIndex: int, charCount: int, bytes: typing.List[int], byteIndex: int) -> int:
        ...

    @overload
    def GetBytes(self, chars: typing.Any, charCount: int, bytes: typing.Any, byteCount: int) -> int:
        ...

    @overload
    def GetBytes(self, chars: System.ReadOnlySpan[str], bytes: System.Span[int]) -> int:
        ...

    @overload
    def GetCharCount(self, bytes: typing.List[int]) -> int:
        ...

    @overload
    def GetCharCount(self, bytes: typing.List[int], index: int, count: int) -> int:
        ...

    @overload
    def GetCharCount(self, bytes: typing.Any, count: int) -> int:
        ...

    @overload
    def GetCharCount(self, bytes: System.ReadOnlySpan[int]) -> int:
        ...

    @overload
    def GetChars(self, bytes: typing.List[int]) -> typing.List[str]:
        ...

    @overload
    def GetChars(self, bytes: typing.List[int], index: int, count: int) -> typing.List[str]:
        ...

    @overload
    def GetChars(self, bytes: typing.List[int], byteIndex: int, byteCount: int, chars: typing.List[str], charIndex: int) -> int:
        ...

    @overload
    def GetChars(self, bytes: typing.Any, byteCount: int, chars: typing.Any, charCount: int) -> int:
        ...

    @overload
    def GetChars(self, bytes: System.ReadOnlySpan[int], chars: System.Span[str]) -> int:
        ...

    def GetDecoder(self) -> System.Text.Decoder:
        ...

    def GetEncoder(self) -> System.Text.Encoder:
        ...

    @staticmethod
    @overload
    def GetEncoding(codepage: int) -> System.Text.Encoding:
        ...

    @staticmethod
    @overload
    def GetEncoding(codepage: int, encoderFallback: System.Text.EncoderFallback, decoderFallback: System.Text.DecoderFallback) -> System.Text.Encoding:
        ...

    @staticmethod
    @overload
    def GetEncoding(name: str) -> System.Text.Encoding:
        ...

    @staticmethod
    @overload
    def GetEncoding(name: str, encoderFallback: System.Text.EncoderFallback, decoderFallback: System.Text.DecoderFallback) -> System.Text.Encoding:
        ...

    @staticmethod
    def GetEncodings() -> typing.List[System.Text.EncodingInfo]:
        """
        Get the EncodingInfo list from the runtime and all registered encoding providers
        
        :returns: The list of the EncodingProvider objects.
        """
        ...

    def GetHashCode(self) -> int:
        ...

    def GetMaxByteCount(self, charCount: int) -> int:
        ...

    def GetMaxCharCount(self, byteCount: int) -> int:
        ...

    def GetPreamble(self) -> typing.List[int]:
        ...

    @overload
    def GetString(self, bytes: typing.Any, byteCount: int) -> str:
        ...

    @overload
    def GetString(self, bytes: System.ReadOnlySpan[int]) -> str:
        ...

    @overload
    def GetString(self, bytes: typing.List[int]) -> str:
        ...

    @overload
    def GetString(self, bytes: typing.List[int], index: int, count: int) -> str:
        ...

    @overload
    def IsAlwaysNormalized(self) -> bool:
        ...

    @overload
    def IsAlwaysNormalized(self, form: System.Text.NormalizationForm) -> bool:
        ...

    @staticmethod
    def RegisterProvider(provider: System.Text.EncodingProvider) -> None:
        ...

    def TryGetBytes(self, chars: System.ReadOnlySpan[str], bytes: System.Span[int], bytesWritten: typing.Optional[int]) -> typing.Union[bool, int]:
        """
        Encodes into a span of bytes a set of characters from the specified read-only span if the destination is large enough.
        
        :param chars: The span containing the set of characters to encode.
        :param bytes: The byte span to hold the encoded bytes.
        :param bytesWritten: Upon successful completion of the operation, the number of bytes encoded into .
        :returns: true if all of the characters were encoded into the destination; false if the destination was too small to contain all the encoded bytes.
        """
        ...

    def TryGetChars(self, bytes: System.ReadOnlySpan[int], chars: System.Span[str], charsWritten: typing.Optional[int]) -> typing.Union[bool, int]:
        """
        Decodes into a span of chars a set of bytes from the specified read-only span if the destination is large enough.
        
        :param bytes: A read-only span containing the sequence of bytes to decode.
        :param chars: The character span receiving the decoded bytes.
        :param charsWritten: Upon successful completion of the operation, the number of chars decoded into .
        :returns: true if all of the characters were decoded into the destination; false if the destination was too small to contain all the decoded chars.
        """
        ...


class UnicodeEncoding(System.Text.Encoding):
    """This class has no documentation."""

    CharSize: int = 2

    @property
    def Preamble(self) -> System.ReadOnlySpan[int]:
        ...

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, bigEndian: bool, byteOrderMark: bool) -> None:
        ...

    @overload
    def __init__(self, bigEndian: bool, byteOrderMark: bool, throwOnInvalidBytes: bool) -> None:
        ...

    def Equals(self, value: typing.Any) -> bool:
        ...

    @overload
    def GetByteCount(self, chars: typing.List[str], index: int, count: int) -> int:
        ...

    @overload
    def GetByteCount(self, s: str) -> int:
        ...

    @overload
    def GetByteCount(self, chars: typing.Any, count: int) -> int:
        ...

    @overload
    def GetBytes(self, s: str, charIndex: int, charCount: int, bytes: typing.List[int], byteIndex: int) -> int:
        ...

    @overload
    def GetBytes(self, chars: typing.List[str], charIndex: int, charCount: int, bytes: typing.List[int], byteIndex: int) -> int:
        ...

    @overload
    def GetBytes(self, chars: typing.Any, charCount: int, bytes: typing.Any, byteCount: int) -> int:
        ...

    @overload
    def GetCharCount(self, bytes: typing.List[int], index: int, count: int) -> int:
        ...

    @overload
    def GetCharCount(self, bytes: typing.Any, count: int) -> int:
        ...

    @overload
    def GetChars(self, bytes: typing.List[int], byteIndex: int, byteCount: int, chars: typing.List[str], charIndex: int) -> int:
        ...

    @overload
    def GetChars(self, bytes: typing.Any, byteCount: int, chars: typing.Any, charCount: int) -> int:
        ...

    def GetDecoder(self) -> System.Text.Decoder:
        ...

    def GetEncoder(self) -> System.Text.Encoder:
        ...

    def GetHashCode(self) -> int:
        ...

    def GetMaxByteCount(self, charCount: int) -> int:
        ...

    def GetMaxCharCount(self, byteCount: int) -> int:
        ...

    def GetPreamble(self) -> typing.List[int]:
        ...

    def GetString(self, bytes: typing.List[int], index: int, count: int) -> str:
        ...


class CompositeFormat(System.Object):
    """Represents a parsed composite format string."""

    @property
    def Format(self) -> str:
        """Gets the original composite format string used to create this CompositeFormat instance."""
        ...

    @property
    def MinimumArgumentCount(self) -> int:
        """Gets the minimum number of arguments that must be passed to a formatting operation using this CompositeFormat."""
        ...

    @staticmethod
    def Parse(format: str) -> System.Text.CompositeFormat:
        """
        Parse the composite format string .
        
        :param format: The string to parse.
        :returns: The parsed CompositeFormat.
        """
        ...


class Rune(System.IComparable[System_Text_Rune], System.IEquatable[System_Text_Rune]):
    """Represents a Unicode scalar value ([ U+0000..U+D7FF ], inclusive; or [ U+E000..U+10FFFF ], inclusive)."""

    @property
    def IsAscii(self) -> bool:
        """
        Returns true if and only if this scalar value is ASCII ([ U+0000..U+007F ])
        and therefore representable by a single UTF-8 code unit.
        """
        ...

    @property
    def IsBmp(self) -> bool:
        """
        Returns true if and only if this scalar value is within the BMP ([ U+0000..U+FFFF ])
        and therefore representable by a single UTF-16 code unit.
        """
        ...

    @property
    def Plane(self) -> int:
        """Returns the Unicode plane (0 to 16, inclusive) which contains this scalar."""
        ...

    ReplacementChar: System.Text.Rune
    """A Rune instance that represents the Unicode replacement character U+FFFD."""

    @property
    def Utf16SequenceLength(self) -> int:
        """
        Returns the length in code units (char) of the
        UTF-16 sequence required to represent this scalar value.
        """
        ...

    @property
    def Utf8SequenceLength(self) -> int:
        """
        Returns the length in code units of the
        UTF-8 sequence required to represent this scalar value.
        """
        ...

    @property
    def Value(self) -> int:
        """Returns the Unicode scalar value as an integer."""
        ...

    @overload
    def __init__(self, ch: str) -> None:
        """Creates a Rune from the provided UTF-16 code unit."""
        ...

    @overload
    def __init__(self, highSurrogate: str, lowSurrogate: str) -> None:
        """Creates a Rune from the provided UTF-16 surrogate pair."""
        ...

    @overload
    def __init__(self, value: int) -> None:
        """Creates a Rune from the provided Unicode scalar value."""
        ...

    @overload
    def __init__(self, value: int) -> None:
        """Creates a Rune from the provided Unicode scalar value."""
        ...

    def CompareTo(self, other: System.Text.Rune) -> int:
        ...

    @staticmethod
    def DecodeFromUtf16(source: System.ReadOnlySpan[str], result: typing.Optional[System.Text.Rune], charsConsumed: typing.Optional[int]) -> typing.Union[int, System.Text.Rune, int]:
        """
        Decodes the Rune at the beginning of the provided UTF-16 source buffer.
        
        :returns: If the source buffer begins with a valid UTF-16 encoded scalar value, returns , and outs via  the decoded  and via  the number of s used in the input buffer to encode the .  If the source buffer is empty or contains only a standalone UTF-16 high surrogate character, returns , and outs via  and via  the length of the input buffer.  If the source buffer begins with an ill-formed UTF-16 encoded scalar value, returns , and outs via  and via  the number of s used in the input buffer to encode the ill-formed sequence. This method returns the int value of a member of the System.Buffers.OperationStatus enum.
        """
        ...

    @staticmethod
    def DecodeFromUtf8(source: System.ReadOnlySpan[int], result: typing.Optional[System.Text.Rune], bytesConsumed: typing.Optional[int]) -> typing.Union[int, System.Text.Rune, int]:
        """
        Decodes the Rune at the beginning of the provided UTF-8 source buffer.
        
        :returns: If the source buffer begins with a valid UTF-8 encoded scalar value, returns , and outs via  the decoded  and via  the number of s used in the input buffer to encode the .  If the source buffer is empty or contains only a partial UTF-8 subsequence, returns , and outs via  and via  the length of the input buffer.  If the source buffer begins with an ill-formed UTF-8 encoded scalar value, returns , and outs via  and via  the number of s used in the input buffer to encode the ill-formed sequence. This method returns the int value of a member of the System.Buffers.OperationStatus enum.
        """
        ...

    @staticmethod
    def DecodeLastFromUtf16(source: System.ReadOnlySpan[str], result: typing.Optional[System.Text.Rune], charsConsumed: typing.Optional[int]) -> typing.Union[int, System.Text.Rune, int]:
        """
        Decodes the Rune at the end of the provided UTF-16 source buffer.
        
        :returns: This method returns the int value of a member of the System.Buffers.OperationStatus enum.
        """
        ...

    @staticmethod
    def DecodeLastFromUtf8(source: System.ReadOnlySpan[int], value: typing.Optional[System.Text.Rune], bytesConsumed: typing.Optional[int]) -> typing.Union[int, System.Text.Rune, int]:
        """
        Decodes the Rune at the end of the provided UTF-8 source buffer.
        
        :returns: This method returns the int value of a member of the System.Buffers.OperationStatus enum.
        """
        ...

    def EncodeToUtf16(self, destination: System.Span[str]) -> int:
        """
        Encodes this Rune to a UTF-16 destination buffer.
        
        :param destination: The buffer to which to write this value as UTF-16.
        :returns: The number of chars written to .
        """
        ...

    def EncodeToUtf8(self, destination: System.Span[int]) -> int:
        """
        Encodes this Rune to a UTF-8 destination buffer.
        
        :param destination: The buffer to which to write this value as UTF-8.
        :returns: The number of bytes written to .
        """
        ...

    @overload
    def Equals(self, obj: typing.Any) -> bool:
        ...

    @overload
    def Equals(self, other: System.Text.Rune) -> bool:
        ...

    def GetHashCode(self) -> int:
        ...

    @staticmethod
    def GetNumericValue(value: System.Text.Rune) -> float:
        ...

    @staticmethod
    def GetRuneAt(input: str, index: int) -> System.Text.Rune:
        """
        Gets the Rune which begins at index  in
        string .
        """
        ...

    @staticmethod
    def GetUnicodeCategory(value: System.Text.Rune) -> int:
        """:returns: This method returns the int value of a member of the System.Globalization.UnicodeCategory enum."""
        ...

    @staticmethod
    def IsControl(value: System.Text.Rune) -> bool:
        ...

    @staticmethod
    def IsDigit(value: System.Text.Rune) -> bool:
        ...

    @staticmethod
    def IsLetter(value: System.Text.Rune) -> bool:
        ...

    @staticmethod
    def IsLetterOrDigit(value: System.Text.Rune) -> bool:
        ...

    @staticmethod
    def IsLower(value: System.Text.Rune) -> bool:
        ...

    @staticmethod
    def IsNumber(value: System.Text.Rune) -> bool:
        ...

    @staticmethod
    def IsPunctuation(value: System.Text.Rune) -> bool:
        ...

    @staticmethod
    def IsSeparator(value: System.Text.Rune) -> bool:
        ...

    @staticmethod
    def IsSymbol(value: System.Text.Rune) -> bool:
        ...

    @staticmethod
    def IsUpper(value: System.Text.Rune) -> bool:
        ...

    @staticmethod
    @overload
    def IsValid(value: int) -> bool:
        """
        Returns true iff  is a valid Unicode scalar
        value, i.e., is in [ U+0000..U+D7FF ], inclusive; or [ U+E000..U+10FFFF ], inclusive.
        """
        ...

    @staticmethod
    @overload
    def IsValid(value: int) -> bool:
        """
        Returns true iff  is a valid Unicode scalar
        value, i.e., is in [ U+0000..U+D7FF ], inclusive; or [ U+E000..U+10FFFF ], inclusive.
        """
        ...

    @staticmethod
    def IsWhiteSpace(value: System.Text.Rune) -> bool:
        ...

    @staticmethod
    def ToLower(value: System.Text.Rune, culture: System.Globalization.CultureInfo) -> System.Text.Rune:
        ...

    @staticmethod
    def ToLowerInvariant(value: System.Text.Rune) -> System.Text.Rune:
        ...

    def ToString(self) -> str:
        """Returns a string representation of this Rune instance."""
        ...

    @staticmethod
    def ToUpper(value: System.Text.Rune, culture: System.Globalization.CultureInfo) -> System.Text.Rune:
        ...

    @staticmethod
    def ToUpperInvariant(value: System.Text.Rune) -> System.Text.Rune:
        ...

    @staticmethod
    @overload
    def TryCreate(ch: str, result: typing.Optional[System.Text.Rune]) -> typing.Union[bool, System.Text.Rune]:
        ...

    @staticmethod
    @overload
    def TryCreate(highSurrogate: str, lowSurrogate: str, result: typing.Optional[System.Text.Rune]) -> typing.Union[bool, System.Text.Rune]:
        """
        Attempts to create a Rune from the provided UTF-16 surrogate pair.
        Returns false if the input values don't represent a well-formed UTF-16surrogate pair.
        """
        ...

    @staticmethod
    @overload
    def TryCreate(value: int, result: typing.Optional[System.Text.Rune]) -> typing.Union[bool, System.Text.Rune]:
        """Attempts to create a Rune from the provided input value."""
        ...

    @staticmethod
    @overload
    def TryCreate(value: int, result: typing.Optional[System.Text.Rune]) -> typing.Union[bool, System.Text.Rune]:
        """Attempts to create a Rune from the provided input value."""
        ...

    def TryEncodeToUtf16(self, destination: System.Span[str], charsWritten: typing.Optional[int]) -> typing.Union[bool, int]:
        """
        Encodes this Rune to a UTF-16 destination buffer.
        
        :param destination: The buffer to which to write this value as UTF-16.
        :param charsWritten: The number of chars written to , or 0 if the destination buffer is not large enough to contain the output.
        :returns: True if the value was written to the buffer; otherwise, false.
        """
        ...

    def TryEncodeToUtf8(self, destination: System.Span[int], bytesWritten: typing.Optional[int]) -> typing.Union[bool, int]:
        """
        Encodes this Rune to a destination buffer as UTF-8 bytes.
        
        :param destination: The buffer to which to write this value as UTF-8.
        :param bytesWritten: The number of bytes written to , or 0 if the destination buffer is not large enough to contain the output.
        :returns: True if the value was written to the buffer; otherwise, false.
        """
        ...

    @staticmethod
    def TryGetRuneAt(input: str, index: int, value: typing.Optional[System.Text.Rune]) -> typing.Union[bool, System.Text.Rune]:
        """
        Attempts to get the Rune which begins at index  in
        string .
        
        :returns: true if a scalar value was successfully extracted from the specified index, false if a value could not be extracted due to invalid data.
        """
        ...


class StringRuneEnumerator(typing.Iterable[System.Text.Rune]):
    """This class has no documentation."""

    @property
    def Current(self) -> System.Text.Rune:
        ...

    def GetEnumerator(self) -> System.Text.StringRuneEnumerator:
        ...

    def MoveNext(self) -> bool:
        ...


class UTF8Encoding(System.Text.Encoding):
    """This class has no documentation."""

    @property
    def Preamble(self) -> System.ReadOnlySpan[int]:
        ...

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, encoderShouldEmitUTF8Identifier: bool) -> None:
        ...

    @overload
    def __init__(self, encoderShouldEmitUTF8Identifier: bool, throwOnInvalidBytes: bool) -> None:
        ...

    def Equals(self, value: typing.Any) -> bool:
        ...

    @overload
    def GetByteCount(self, chars: typing.List[str], index: int, count: int) -> int:
        ...

    @overload
    def GetByteCount(self, chars: str) -> int:
        ...

    @overload
    def GetByteCount(self, chars: typing.Any, count: int) -> int:
        ...

    @overload
    def GetByteCount(self, chars: System.ReadOnlySpan[str]) -> int:
        ...

    @overload
    def GetBytes(self, s: str, charIndex: int, charCount: int, bytes: typing.List[int], byteIndex: int) -> int:
        ...

    @overload
    def GetBytes(self, chars: typing.List[str], charIndex: int, charCount: int, bytes: typing.List[int], byteIndex: int) -> int:
        ...

    @overload
    def GetBytes(self, chars: typing.Any, charCount: int, bytes: typing.Any, byteCount: int) -> int:
        ...

    @overload
    def GetBytes(self, chars: System.ReadOnlySpan[str], bytes: System.Span[int]) -> int:
        ...

    @overload
    def GetCharCount(self, bytes: typing.List[int], index: int, count: int) -> int:
        ...

    @overload
    def GetCharCount(self, bytes: typing.Any, count: int) -> int:
        ...

    @overload
    def GetCharCount(self, bytes: System.ReadOnlySpan[int]) -> int:
        ...

    @overload
    def GetChars(self, bytes: typing.List[int], byteIndex: int, byteCount: int, chars: typing.List[str], charIndex: int) -> int:
        ...

    @overload
    def GetChars(self, bytes: typing.Any, byteCount: int, chars: typing.Any, charCount: int) -> int:
        ...

    @overload
    def GetChars(self, bytes: System.ReadOnlySpan[int], chars: System.Span[str]) -> int:
        ...

    def GetDecoder(self) -> System.Text.Decoder:
        ...

    def GetEncoder(self) -> System.Text.Encoder:
        ...

    def GetHashCode(self) -> int:
        ...

    def GetMaxByteCount(self, charCount: int) -> int:
        ...

    def GetMaxCharCount(self, byteCount: int) -> int:
        ...

    def GetPreamble(self) -> typing.List[int]:
        ...

    def GetString(self, bytes: typing.List[int], index: int, count: int) -> str:
        ...

    def TryGetBytes(self, chars: System.ReadOnlySpan[str], bytes: System.Span[int], bytesWritten: typing.Optional[int]) -> typing.Union[bool, int]:
        ...

    def TryGetChars(self, bytes: System.ReadOnlySpan[int], chars: System.Span[str], charsWritten: typing.Optional[int]) -> typing.Union[bool, int]:
        ...


class UTF7Encoding(System.Text.Encoding):
    """This class has no documentation."""

    @overload
    def __init__(self) -> None:
        """Obsoletions.SystemTextEncodingUTF7Message"""
        ...

    @overload
    def __init__(self, allowOptionals: bool) -> None:
        """Obsoletions.SystemTextEncodingUTF7Message"""
        ...

    def Equals(self, value: typing.Any) -> bool:
        ...

    @overload
    def GetByteCount(self, chars: typing.List[str], index: int, count: int) -> int:
        ...

    @overload
    def GetByteCount(self, s: str) -> int:
        ...

    @overload
    def GetByteCount(self, chars: typing.Any, count: int) -> int:
        ...

    @overload
    def GetBytes(self, s: str, charIndex: int, charCount: int, bytes: typing.List[int], byteIndex: int) -> int:
        ...

    @overload
    def GetBytes(self, chars: typing.List[str], charIndex: int, charCount: int, bytes: typing.List[int], byteIndex: int) -> int:
        ...

    @overload
    def GetBytes(self, chars: typing.Any, charCount: int, bytes: typing.Any, byteCount: int) -> int:
        ...

    @overload
    def GetCharCount(self, bytes: typing.List[int], index: int, count: int) -> int:
        ...

    @overload
    def GetCharCount(self, bytes: typing.Any, count: int) -> int:
        ...

    @overload
    def GetChars(self, bytes: typing.List[int], byteIndex: int, byteCount: int, chars: typing.List[str], charIndex: int) -> int:
        ...

    @overload
    def GetChars(self, bytes: typing.Any, byteCount: int, chars: typing.Any, charCount: int) -> int:
        ...

    def GetDecoder(self) -> System.Text.Decoder:
        ...

    def GetEncoder(self) -> System.Text.Encoder:
        ...

    def GetHashCode(self) -> int:
        ...

    def GetMaxByteCount(self, charCount: int) -> int:
        ...

    def GetMaxCharCount(self, byteCount: int) -> int:
        ...

    def GetString(self, bytes: typing.List[int], index: int, count: int) -> str:
        ...


class Ascii(System.Object):
    """This class has no documentation."""

    @staticmethod
    @overload
    def Equals(left: System.ReadOnlySpan[int], right: System.ReadOnlySpan[int]) -> bool:
        """
        Determines whether the provided buffers contain equal ASCII characters.
        
        :param left: The buffer to compare with .
        :param right: The buffer to compare with .
        :returns: true if the corresponding elements in  and  were equal and ASCII. false otherwise.
        """
        ...

    @staticmethod
    @overload
    def Equals(left: System.ReadOnlySpan[int], right: System.ReadOnlySpan[str]) -> bool:
        ...

    @staticmethod
    @overload
    def Equals(left: System.ReadOnlySpan[str], right: System.ReadOnlySpan[int]) -> bool:
        ...

    @staticmethod
    @overload
    def Equals(left: System.ReadOnlySpan[str], right: System.ReadOnlySpan[str]) -> bool:
        ...

    @staticmethod
    @overload
    def EqualsIgnoreCase(left: System.ReadOnlySpan[int], right: System.ReadOnlySpan[int]) -> bool:
        """
        Determines whether the provided buffers contain equal ASCII characters, ignoring case considerations.
        
        :param left: The buffer to compare with .
        :param right: The buffer to compare with .
        :returns: true if the corresponding elements in  and  were equal ignoring case considerations and ASCII. false otherwise.
        """
        ...

    @staticmethod
    @overload
    def EqualsIgnoreCase(left: System.ReadOnlySpan[int], right: System.ReadOnlySpan[str]) -> bool:
        ...

    @staticmethod
    @overload
    def EqualsIgnoreCase(left: System.ReadOnlySpan[str], right: System.ReadOnlySpan[int]) -> bool:
        ...

    @staticmethod
    @overload
    def EqualsIgnoreCase(left: System.ReadOnlySpan[str], right: System.ReadOnlySpan[str]) -> bool:
        ...

    @staticmethod
    def FromUtf16(source: System.ReadOnlySpan[str], destination: System.Span[int], bytesWritten: typing.Optional[int]) -> typing.Union[int, int]:
        """
        Copies text from a source buffer to a destination buffer, converting
        from UTF-16 to ASCII during the copy.
        
        :param source: The source buffer from which UTF-16 text is read.
        :param destination: The destination buffer to which ASCII text is written.
        :param bytesWritten: The number of bytes actually written to . It's the same as the number of chars actually read from .
        :returns: An OperationStatus describing the result of the operation. This method returns the int value of a member of the System.Buffers.OperationStatus enum.
        """
        ...

    @staticmethod
    @overload
    def IsValid(value: System.ReadOnlySpan[int]) -> bool:
        """
        Determines whether the provided value contains only ASCII bytes.
        
        :param value: The value to inspect.
        :returns: True if  contains only ASCII bytes or is empty; False otherwise.
        """
        ...

    @staticmethod
    @overload
    def IsValid(value: System.ReadOnlySpan[str]) -> bool:
        """
        Determines whether the provided value contains only ASCII chars.
        
        :param value: The value to inspect.
        :returns: True if  contains only ASCII chars or is empty; False otherwise.
        """
        ...

    @staticmethod
    @overload
    def IsValid(value: int) -> bool:
        """
        Determines whether the provided value is ASCII byte.
        
        :param value: The value to inspect.
        :returns: True if  is ASCII, False otherwise.
        """
        ...

    @staticmethod
    @overload
    def IsValid(value: str) -> bool:
        """
        Determines whether the provided value is ASCII char.
        
        :param value: The value to inspect.
        :returns: True if  is ASCII, False otherwise.
        """
        ...

    @staticmethod
    @overload
    def ToLower(source: System.ReadOnlySpan[int], destination: System.Span[int], bytesWritten: typing.Optional[int]) -> typing.Union[int, int]:
        """
        Copies text from a source buffer to a destination buffer, converting
        ASCII letters to lowercase during the copy.
        
        :param source: The source buffer from which ASCII text is read.
        :param destination: The destination buffer to which lowercase text is written.
        :param bytesWritten: The number of bytes actually written to . It's the same as the number of bytes actually read from .
        :returns: An OperationStatus describing the result of the operation. This method returns the int value of a member of the System.Buffers.OperationStatus enum.
        """
        ...

    @staticmethod
    @overload
    def ToLower(source: System.ReadOnlySpan[str], destination: System.Span[str], charsWritten: typing.Optional[int]) -> typing.Union[int, int]:
        """
        Copies text from a source buffer to a destination buffer, converting
        ASCII letters to lowercase during the copy.
        
        :param source: The source buffer from which ASCII text is read.
        :param destination: The destination buffer to which lowercase text is written.
        :param charsWritten: The number of characters actually written to . It's the same as the number of characters actually read from .
        :returns: An OperationStatus describing the result of the operation. This method returns the int value of a member of the System.Buffers.OperationStatus enum.
        """
        ...

    @staticmethod
    @overload
    def ToLower(source: System.ReadOnlySpan[int], destination: System.Span[str], charsWritten: typing.Optional[int]) -> typing.Union[int, int]:
        """
        Copies text from a source buffer to a destination buffer, converting
        ASCII letters to lowercase during the copy.
        
        :param source: The source buffer from which ASCII text is read.
        :param destination: The destination buffer to which lowercase text is written.
        :param charsWritten: The number of characters actually written to . It's the same as the number of bytes actually read from .
        :returns: An OperationStatus describing the result of the operation. This method returns the int value of a member of the System.Buffers.OperationStatus enum.
        """
        ...

    @staticmethod
    @overload
    def ToLower(source: System.ReadOnlySpan[str], destination: System.Span[int], bytesWritten: typing.Optional[int]) -> typing.Union[int, int]:
        """
        Copies text from a source buffer to a destination buffer, converting
        ASCII letters to lowercase during the copy.
        
        :param source: The source buffer from which ASCII text is read.
        :param destination: The destination buffer to which lowercase text is written.
        :param bytesWritten: The number of bytes actually written to . It's the same as the number of characters actually read from .
        :returns: An OperationStatus describing the result of the operation. This method returns the int value of a member of the System.Buffers.OperationStatus enum.
        """
        ...

    @staticmethod
    @overload
    def ToLowerInPlace(value: System.Span[int], bytesWritten: typing.Optional[int]) -> typing.Union[int, int]:
        """
        Performs in-place uppercase conversion.
        
        :param value: The ASCII text buffer.
        :param bytesWritten: The number of processed bytes.
        :returns: An OperationStatus describing the result of the operation. This method returns the int value of a member of the System.Buffers.OperationStatus enum.
        """
        ...

    @staticmethod
    @overload
    def ToLowerInPlace(value: System.Span[str], charsWritten: typing.Optional[int]) -> typing.Union[int, int]:
        """
        Performs in-place uppercase conversion.
        
        :param value: The ASCII text buffer.
        :param charsWritten: The number of processed characters.
        :returns: An OperationStatus describing the result of the operation. This method returns the int value of a member of the System.Buffers.OperationStatus enum.
        """
        ...

    @staticmethod
    @overload
    def ToUpper(source: System.ReadOnlySpan[int], destination: System.Span[int], bytesWritten: typing.Optional[int]) -> typing.Union[int, int]:
        """
        Copies text from a source buffer to a destination buffer, converting
        ASCII letters to uppercase during the copy.
        
        :param source: The source buffer from which ASCII text is read.
        :param destination: The destination buffer to which uppercase text is written.
        :param bytesWritten: The number of bytes actually written to . It's the same as the number of bytes actually read from .
        :returns: An OperationStatus describing the result of the operation. This method returns the int value of a member of the System.Buffers.OperationStatus enum.
        """
        ...

    @staticmethod
    @overload
    def ToUpper(source: System.ReadOnlySpan[str], destination: System.Span[str], charsWritten: typing.Optional[int]) -> typing.Union[int, int]:
        """
        Copies text from a source buffer to a destination buffer, converting
        ASCII letters to uppercase during the copy.
        
        :param source: The source buffer from which ASCII text is read.
        :param destination: The destination buffer to which uppercase text is written.
        :param charsWritten: The number of characters actually written to . It's the same as the number of characters actually read from .
        :returns: An OperationStatus describing the result of the operation. This method returns the int value of a member of the System.Buffers.OperationStatus enum.
        """
        ...

    @staticmethod
    @overload
    def ToUpper(source: System.ReadOnlySpan[int], destination: System.Span[str], charsWritten: typing.Optional[int]) -> typing.Union[int, int]:
        """
        Copies text from a source buffer to a destination buffer, converting
        ASCII letters to uppercase during the copy.
        
        :param source: The source buffer from which ASCII text is read.
        :param destination: The destination buffer to which uppercase text is written.
        :param charsWritten: The number of characters actually written to . It's the same as the number of bytes actually read from .
        :returns: An OperationStatus describing the result of the operation. This method returns the int value of a member of the System.Buffers.OperationStatus enum.
        """
        ...

    @staticmethod
    @overload
    def ToUpper(source: System.ReadOnlySpan[str], destination: System.Span[int], bytesWritten: typing.Optional[int]) -> typing.Union[int, int]:
        """
        Copies text from a source buffer to a destination buffer, converting
        ASCII letters to uppercase during the copy.
        
        :param source: The source buffer from which ASCII text is read.
        :param destination: The destination buffer to which uppercase text is written.
        :param bytesWritten: The number of bytes actually written to . It's the same as the number of characters actually read from .
        :returns: An OperationStatus describing the result of the operation. This method returns the int value of a member of the System.Buffers.OperationStatus enum.
        """
        ...

    @staticmethod
    @overload
    def ToUpperInPlace(value: System.Span[int], bytesWritten: typing.Optional[int]) -> typing.Union[int, int]:
        """
        Performs in-place lowercase conversion.
        
        :param value: The ASCII text buffer.
        :param bytesWritten: The number of processed bytes.
        :returns: An OperationStatus describing the result of the operation. This method returns the int value of a member of the System.Buffers.OperationStatus enum.
        """
        ...

    @staticmethod
    @overload
    def ToUpperInPlace(value: System.Span[str], charsWritten: typing.Optional[int]) -> typing.Union[int, int]:
        """
        Performs in-place lowercase conversion.
        
        :param value: The ASCII text buffer.
        :param charsWritten: The number of processed characters.
        :returns: An OperationStatus describing the result of the operation. This method returns the int value of a member of the System.Buffers.OperationStatus enum.
        """
        ...

    @staticmethod
    def ToUtf16(source: System.ReadOnlySpan[int], destination: System.Span[str], charsWritten: typing.Optional[int]) -> typing.Union[int, int]:
        """
        Copies text from a source buffer to a destination buffer, converting
        from ASCII to UTF-16 during the copy.
        
        :param source: The source buffer from which ASCII text is read.
        :param destination: The destination buffer to which UTF-16 text is written.
        :param charsWritten: The number of chars actually written to . It's the same as the number of bytes actually read from
        :returns: An OperationStatus describing the result of the operation. This method returns the int value of a member of the System.Buffers.OperationStatus enum.
        """
        ...

    @staticmethod
    @overload
    def Trim(value: System.ReadOnlySpan[int]) -> System.Range:
        """
        Trims all leading and trailing ASCII whitespaces from the buffer.
        
        :param value: The ASCII buffer.
        :returns: The Range of the untrimmed data.
        """
        ...

    @staticmethod
    @overload
    def Trim(value: System.ReadOnlySpan[str]) -> System.Range:
        ...

    @staticmethod
    @overload
    def TrimEnd(value: System.ReadOnlySpan[int]) -> System.Range:
        """
        Trims all trailing ASCII whitespaces from the buffer.
        
        :param value: The ASCII buffer.
        :returns: The Range of the untrimmed data.
        """
        ...

    @staticmethod
    @overload
    def TrimEnd(value: System.ReadOnlySpan[str]) -> System.Range:
        ...

    @staticmethod
    @overload
    def TrimStart(value: System.ReadOnlySpan[int]) -> System.Range:
        """
        Trims all leading ASCII whitespaces from the buffer.
        
        :param value: The ASCII buffer.
        :returns: The Range of the untrimmed data.
        """
        ...

    @staticmethod
    @overload
    def TrimStart(value: System.ReadOnlySpan[str]) -> System.Range:
        ...


class ASCIIEncoding(System.Text.Encoding):
    """This class has no documentation."""

    @property
    def IsSingleByte(self) -> bool:
        ...

    def __init__(self) -> None:
        ...

    @overload
    def GetByteCount(self, chars: typing.List[str], index: int, count: int) -> int:
        ...

    @overload
    def GetByteCount(self, chars: str) -> int:
        ...

    @overload
    def GetByteCount(self, chars: typing.Any, count: int) -> int:
        ...

    @overload
    def GetByteCount(self, chars: System.ReadOnlySpan[str]) -> int:
        ...

    @overload
    def GetBytes(self, chars: str, charIndex: int, charCount: int, bytes: typing.List[int], byteIndex: int) -> int:
        ...

    @overload
    def GetBytes(self, chars: typing.List[str], charIndex: int, charCount: int, bytes: typing.List[int], byteIndex: int) -> int:
        ...

    @overload
    def GetBytes(self, chars: typing.Any, charCount: int, bytes: typing.Any, byteCount: int) -> int:
        ...

    @overload
    def GetBytes(self, chars: System.ReadOnlySpan[str], bytes: System.Span[int]) -> int:
        ...

    @overload
    def GetCharCount(self, bytes: typing.List[int], index: int, count: int) -> int:
        ...

    @overload
    def GetCharCount(self, bytes: typing.Any, count: int) -> int:
        ...

    @overload
    def GetCharCount(self, bytes: System.ReadOnlySpan[int]) -> int:
        ...

    @overload
    def GetChars(self, bytes: typing.List[int], byteIndex: int, byteCount: int, chars: typing.List[str], charIndex: int) -> int:
        ...

    @overload
    def GetChars(self, bytes: typing.Any, byteCount: int, chars: typing.Any, charCount: int) -> int:
        ...

    @overload
    def GetChars(self, bytes: System.ReadOnlySpan[int], chars: System.Span[str]) -> int:
        ...

    def GetDecoder(self) -> System.Text.Decoder:
        ...

    def GetEncoder(self) -> System.Text.Encoder:
        ...

    def GetMaxByteCount(self, charCount: int) -> int:
        ...

    def GetMaxCharCount(self, byteCount: int) -> int:
        ...

    def GetString(self, bytes: typing.List[int], byteIndex: int, byteCount: int) -> str:
        ...

    def TryGetBytes(self, chars: System.ReadOnlySpan[str], bytes: System.Span[int], bytesWritten: typing.Optional[int]) -> typing.Union[bool, int]:
        ...

    def TryGetChars(self, bytes: System.ReadOnlySpan[int], chars: System.Span[str], charsWritten: typing.Optional[int]) -> typing.Union[bool, int]:
        ...


class EncoderReplacementFallback(System.Text.EncoderFallback):
    """This class has no documentation."""

    @property
    def DefaultString(self) -> str:
        ...

    @property
    def MaxCharCount(self) -> int:
        ...

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, replacement: str) -> None:
        ...

    def CreateFallbackBuffer(self) -> System.Text.EncoderFallbackBuffer:
        ...

    def Equals(self, value: typing.Any) -> bool:
        ...

    def GetHashCode(self) -> int:
        ...


class EncoderReplacementFallbackBuffer(System.Text.EncoderFallbackBuffer):
    """This class has no documentation."""

    @property
    def Remaining(self) -> int:
        ...

    def __init__(self, fallback: System.Text.EncoderReplacementFallback) -> None:
        ...

    @overload
    def Fallback(self, charUnknown: str, index: int) -> bool:
        ...

    @overload
    def Fallback(self, charUnknownHigh: str, charUnknownLow: str, index: int) -> bool:
        ...

    def GetNextChar(self) -> str:
        ...

    def MovePrevious(self) -> bool:
        ...

    def Reset(self) -> None:
        ...


class StringBuilder(System.Object, System.Runtime.Serialization.ISerializable):
    """This class has no documentation."""

    class ChunkEnumerator:
        """
        ChunkEnumerator supports both the IEnumerable and IEnumerator pattern so foreach
        works (see GetChunks).  It needs to be public (so the compiler can use it
        when building a foreach statement) but users typically don't use it explicitly.
        (which is why it is a nested type).
        """

        @property
        def Current(self) -> System.ReadOnlyMemory[str]:
            """Implements the IEnumerator pattern."""
            ...

        def GetEnumerator(self) -> System.Text.StringBuilder.ChunkEnumerator:
            """Implement IEnumerable.GetEnumerator() to return  'this' as the IEnumerator"""
            ...

        def MoveNext(self) -> bool:
            """Implements the IEnumerator pattern."""
            ...

    class AppendInterpolatedStringHandler:
        """Provides a handler used by the language compiler to append interpolated strings into StringBuilder instances."""

        @overload
        def __init__(self, literalLength: int, formattedCount: int, stringBuilder: System.Text.StringBuilder) -> None:
            """
            Creates a handler used to append an interpolated string into a StringBuilder.
            
            :param literalLength: The number of constant characters outside of interpolation expressions in the interpolated string.
            :param formattedCount: The number of interpolation expressions in the interpolated string.
            :param stringBuilder: The associated StringBuilder to which to append.
            """
            ...

        @overload
        def __init__(self, literalLength: int, formattedCount: int, stringBuilder: System.Text.StringBuilder, provider: System.IFormatProvider) -> None:
            """
            Creates a handler used to translate an interpolated string into a string.
            
            :param literalLength: The number of constant characters outside of interpolation expressions in the interpolated string.
            :param formattedCount: The number of interpolation expressions in the interpolated string.
            :param stringBuilder: The associated StringBuilder to which to append.
            :param provider: An object that supplies culture-specific formatting information.
            """
            ...

        @overload
        def AppendFormatted(self, value: System_Text_StringBuilder_AppendFormatted_AppendInterpolatedStringHandler_T) -> None:
            ...

        @overload
        def AppendFormatted(self, value: System_Text_StringBuilder_AppendFormatted_AppendInterpolatedStringHandler_T, format: str) -> None:
            """
            Writes the specified value to the handler.
            
            :param value: The value to write.
            :param format: The format string.
            """
            ...

        @overload
        def AppendFormatted(self, value: System_Text_StringBuilder_AppendFormatted_AppendInterpolatedStringHandler_T, alignment: int) -> None:
            """
            Writes the specified value to the handler.
            
            :param value: The value to write.
            :param alignment: Minimum number of characters that should be written for this value.  If the value is negative, it indicates left-aligned and the required minimum is the absolute value.
            """
            ...

        @overload
        def AppendFormatted(self, value: System_Text_StringBuilder_AppendFormatted_AppendInterpolatedStringHandler_T, alignment: int, format: str) -> None:
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

    @property
    def Capacity(self) -> int:
        ...

    @property
    def MaxCapacity(self) -> int:
        """Gets the maximum capacity this builder is allowed to have."""
        ...

    @property
    def Length(self) -> int:
        """Gets or sets the length of this builder."""
        ...

    def __getitem__(self, index: int) -> str:
        ...

    @overload
    def __init__(self) -> None:
        """Initializes a new instance of the StringBuilder class."""
        ...

    @overload
    def __init__(self, capacity: int) -> None:
        """
        Initializes a new instance of the StringBuilder class.
        
        :param capacity: The initial capacity of this builder.
        """
        ...

    @overload
    def __init__(self, value: str) -> None:
        """
        Initializes a new instance of the StringBuilder class.
        
        :param value: The initial contents of this builder.
        """
        ...

    @overload
    def __init__(self, value: str, capacity: int) -> None:
        """
        Initializes a new instance of the StringBuilder class.
        
        :param value: The initial contents of this builder.
        :param capacity: The initial capacity of this builder.
        """
        ...

    @overload
    def __init__(self, value: str, startIndex: int, length: int, capacity: int) -> None:
        """
        Initializes a new instance of the StringBuilder class.
        
        :param value: The initial contents of this builder.
        :param startIndex: The index to start in .
        :param length: The number of characters to read in .
        :param capacity: The initial capacity of this builder.
        """
        ...

    @overload
    def __init__(self, capacity: int, maxCapacity: int) -> None:
        """
        Initializes a new instance of the StringBuilder class.
        
        :param capacity: The initial capacity of this builder.
        :param maxCapacity: The maximum capacity of this builder.
        """
        ...

    def __setitem__(self, index: int, value: str) -> None:
        ...

    @overload
    def Append(self, value: str, repeatCount: int) -> System.Text.StringBuilder:
        """
        Appends a character 0 or more times to the end of this builder.
        
        :param value: The character to append.
        :param repeatCount: The number of times to append .
        """
        ...

    @overload
    def Append(self, value: typing.List[str], startIndex: int, charCount: int) -> System.Text.StringBuilder:
        """
        Appends a range of characters to the end of this builder.
        
        :param value: The characters to append.
        :param startIndex: The index to start in .
        :param charCount: The number of characters to read in .
        """
        ...

    @overload
    def Append(self, value: str) -> System.Text.StringBuilder:
        """
        Appends a string to the end of this builder.
        
        :param value: The string to append.
        """
        ...

    @overload
    def Append(self, value: str, startIndex: int, count: int) -> System.Text.StringBuilder:
        """
        Appends part of a string to the end of this builder.
        
        :param value: The string to append.
        :param startIndex: The index to start in .
        :param count: The number of characters to read in .
        """
        ...

    @overload
    def Append(self, value: System.Text.StringBuilder) -> System.Text.StringBuilder:
        ...

    @overload
    def Append(self, value: System.Text.StringBuilder, startIndex: int, count: int) -> System.Text.StringBuilder:
        ...

    @overload
    def Append(self, value: bool) -> System.Text.StringBuilder:
        ...

    @overload
    def Append(self, value: str) -> System.Text.StringBuilder:
        ...

    @overload
    def Append(self, value: int) -> System.Text.StringBuilder:
        ...

    @overload
    def Append(self, value: int) -> System.Text.StringBuilder:
        ...

    @overload
    def Append(self, value: int) -> System.Text.StringBuilder:
        ...

    @overload
    def Append(self, value: int) -> System.Text.StringBuilder:
        ...

    @overload
    def Append(self, value: int) -> System.Text.StringBuilder:
        ...

    @overload
    def Append(self, value: float) -> System.Text.StringBuilder:
        ...

    @overload
    def Append(self, value: float) -> System.Text.StringBuilder:
        ...

    @overload
    def Append(self, value: float) -> System.Text.StringBuilder:
        ...

    @overload
    def Append(self, value: int) -> System.Text.StringBuilder:
        ...

    @overload
    def Append(self, value: int) -> System.Text.StringBuilder:
        ...

    @overload
    def Append(self, value: int) -> System.Text.StringBuilder:
        ...

    @overload
    def Append(self, value: typing.Any) -> System.Text.StringBuilder:
        ...

    @overload
    def Append(self, value: typing.List[str]) -> System.Text.StringBuilder:
        ...

    @overload
    def Append(self, value: System.ReadOnlySpan[str]) -> System.Text.StringBuilder:
        ...

    @overload
    def Append(self, value: System.ReadOnlyMemory[str]) -> System.Text.StringBuilder:
        ...

    @overload
    def Append(self, handler: System.Text.StringBuilder.AppendInterpolatedStringHandler) -> System.Text.StringBuilder:
        """
        Appends the specified interpolated string to this instance.
        
        :param handler: The interpolated string to append.
        :returns: A reference to this instance after the append operation has completed.
        """
        ...

    @overload
    def Append(self, provider: System.IFormatProvider, handler: System.Text.StringBuilder.AppendInterpolatedStringHandler) -> System.Text.StringBuilder:
        """
        Appends the specified interpolated string to this instance.
        
        :param provider: An object that supplies culture-specific formatting information.
        :param handler: The interpolated string to append.
        :returns: A reference to this instance after the append operation has completed.
        """
        ...

    @overload
    def Append(self, value: typing.Any, valueCount: int) -> System.Text.StringBuilder:
        """
        Appends a character buffer to this builder.
        
        :param value: The pointer to the start of the buffer.
        :param valueCount: The number of characters in the buffer.
        """
        ...

    @overload
    def AppendFormat(self, format: str, arg0: typing.Any) -> System.Text.StringBuilder:
        ...

    @overload
    def AppendFormat(self, format: str, arg0: typing.Any, arg1: typing.Any) -> System.Text.StringBuilder:
        ...

    @overload
    def AppendFormat(self, format: str, arg0: typing.Any, arg1: typing.Any, arg2: typing.Any) -> System.Text.StringBuilder:
        ...

    @overload
    def AppendFormat(self, format: str, *args: typing.Any) -> System.Text.StringBuilder:
        ...

    @overload
    def AppendFormat(self, provider: System.IFormatProvider, format: str, arg0: typing.Any) -> System.Text.StringBuilder:
        ...

    @overload
    def AppendFormat(self, provider: System.IFormatProvider, format: str, arg0: typing.Any, arg1: typing.Any) -> System.Text.StringBuilder:
        ...

    @overload
    def AppendFormat(self, provider: System.IFormatProvider, format: str, arg0: typing.Any, arg1: typing.Any, arg2: typing.Any) -> System.Text.StringBuilder:
        ...

    @overload
    def AppendFormat(self, provider: System.IFormatProvider, format: str, *args: typing.Any) -> System.Text.StringBuilder:
        ...

    @overload
    def AppendFormat(self, provider: System.IFormatProvider, format: System.Text.CompositeFormat, arg0: System_Text_StringBuilder_AppendFormat_TArg0) -> System.Text.StringBuilder:
        """
        Appends the string returned by processing a composite format string, which contains zero or more format items, to this instance.
        Each format item is replaced by the string representation of any of the arguments using a specified format provider.
        
        :param provider: An object that supplies culture-specific formatting information.
        :param format: A CompositeFormat.
        :param arg0: The first object to format.
        :returns: A reference to this instance after the append operation has completed.
        """
        ...

    @overload
    def AppendFormat(self, provider: System.IFormatProvider, format: System.Text.CompositeFormat, arg0: System_Text_StringBuilder_AppendFormat_TArg0, arg1: System_Text_StringBuilder_AppendFormat_TArg1) -> System.Text.StringBuilder:
        """
        Appends the string returned by processing a composite format string, which contains zero or more format items, to this instance.
        Each format item is replaced by the string representation of any of the arguments using a specified format provider.
        
        :param provider: An object that supplies culture-specific formatting information.
        :param format: A CompositeFormat.
        :param arg0: The first object to format.
        :param arg1: The second object to format.
        :returns: A reference to this instance after the append operation has completed.
        """
        ...

    @overload
    def AppendFormat(self, provider: System.IFormatProvider, format: System.Text.CompositeFormat, arg0: System_Text_StringBuilder_AppendFormat_TArg0, arg1: System_Text_StringBuilder_AppendFormat_TArg1, arg2: System_Text_StringBuilder_AppendFormat_TArg2) -> System.Text.StringBuilder:
        """
        Appends the string returned by processing a composite format string, which contains zero or more format items, to this instance.
        Each format item is replaced by the string representation of any of the arguments using a specified format provider.
        
        :param provider: An object that supplies culture-specific formatting information.
        :param format: A CompositeFormat.
        :param arg0: The first object to format.
        :param arg1: The second object to format.
        :param arg2: The third object to format.
        :returns: A reference to this instance after the append operation has completed.
        """
        ...

    @overload
    def AppendFormat(self, provider: System.IFormatProvider, format: System.Text.CompositeFormat, *args: typing.Any) -> System.Text.StringBuilder:
        """
        Appends the string returned by processing a composite format string, which contains zero or more format items, to this instance.
        Each format item is replaced by the string representation of any of the arguments using a specified format provider.
        
        :param provider: An object that supplies culture-specific formatting information.
        :param format: A CompositeFormat.
        :param args: An array of objects to format.
        :returns: A reference to this instance after the append operation has completed.
        """
        ...

    @overload
    def AppendFormat(self, provider: System.IFormatProvider, format: System.Text.CompositeFormat, args: System.ReadOnlySpan[System.Object]) -> System.Text.StringBuilder:
        """
        Appends the string returned by processing a composite format string, which contains zero or more format items, to this instance.
        Each format item is replaced by the string representation of any of the arguments using a specified format provider.
        
        :param provider: An object that supplies culture-specific formatting information.
        :param format: A CompositeFormat.
        :param args: A span of objects to format.
        :returns: A reference to this instance after the append operation has completed.
        """
        ...

    @overload
    def AppendJoin(self, separator: str, *values: typing.Any) -> System.Text.StringBuilder:
        ...

    @overload
    def AppendJoin(self, separator: str, values: System.Collections.Generic.IEnumerable[System_Text_StringBuilder_AppendJoin_T]) -> System.Text.StringBuilder:
        ...

    @overload
    def AppendJoin(self, separator: str, *values: str) -> System.Text.StringBuilder:
        ...

    @overload
    def AppendJoin(self, separator: str, *values: typing.Any) -> System.Text.StringBuilder:
        ...

    @overload
    def AppendJoin(self, separator: str, values: System.Collections.Generic.IEnumerable[System_Text_StringBuilder_AppendJoin_T]) -> System.Text.StringBuilder:
        ...

    @overload
    def AppendJoin(self, separator: str, *values: str) -> System.Text.StringBuilder:
        ...

    @overload
    def AppendLine(self) -> System.Text.StringBuilder:
        ...

    @overload
    def AppendLine(self, value: str) -> System.Text.StringBuilder:
        ...

    @overload
    def AppendLine(self, handler: System.Text.StringBuilder.AppendInterpolatedStringHandler) -> System.Text.StringBuilder:
        """
        Appends the specified interpolated string followed by the default line terminator to the end of the current StringBuilder object.
        
        :param handler: The interpolated string to append.
        :returns: A reference to this instance after the append operation has completed.
        """
        ...

    @overload
    def AppendLine(self, provider: System.IFormatProvider, handler: System.Text.StringBuilder.AppendInterpolatedStringHandler) -> System.Text.StringBuilder:
        """
        Appends the specified interpolated string followed by the default line terminator to the end of the current StringBuilder object.
        
        :param provider: An object that supplies culture-specific formatting information.
        :param handler: The interpolated string to append.
        :returns: A reference to this instance after the append operation has completed.
        """
        ...

    def Clear(self) -> System.Text.StringBuilder:
        ...

    @overload
    def CopyTo(self, sourceIndex: int, destination: typing.List[str], destinationIndex: int, count: int) -> None:
        ...

    @overload
    def CopyTo(self, sourceIndex: int, destination: System.Span[str], count: int) -> None:
        ...

    def EnsureCapacity(self, capacity: int) -> int:
        """
        Ensures that the capacity of this builder is at least the specified value.
        
        :param capacity: The new capacity for this builder.
        """
        ...

    @overload
    def Equals(self, sb: System.Text.StringBuilder) -> bool:
        """
        Determines if the contents of this builder are equal to the contents of another builder.
        
        :param sb: The other builder.
        """
        ...

    @overload
    def Equals(self, span: System.ReadOnlySpan[str]) -> bool:
        """
        Determines if the contents of this builder are equal to the contents of ReadOnlySpan{Char}.
        
        :param span: The ReadOnlySpan{Char}.
        """
        ...

    def GetChunks(self) -> System.Text.StringBuilder.ChunkEnumerator:
        """
        GetChunks returns ChunkEnumerator that follows the IEnumerable pattern and
        thus can be used in a C# 'foreach' statements to retrieve the data in the StringBuilder
        as chunks (ReadOnlyMemory) of characters.  An example use is:
        
             foreach (ReadOnlyMemory<char> chunk in sb.GetChunks())
                foreach (char c in chunk.Span)
                    { /* operation on c }
        
        It is undefined what happens if the StringBuilder is modified while the chunk
        enumeration is incomplete.  StringBuilder is also not thread-safe, so operating
        on it with concurrent threads is illegal.  Finally the ReadOnlyMemory chunks returned
        are NOT guaranteed to remain unchanged if the StringBuilder is modified, so do
        not cache them for later use either.  This API's purpose is efficiently extracting
        the data of a CONSTANT StringBuilder.
        
        Creating a ReadOnlySpan from a ReadOnlyMemory  (the .Span property) is expensive
        compared to the fetching of the character, so create a local variable for the SPAN
        if you need to use it in a nested for statement.  For example
        
           foreach (ReadOnlyMemory<char> chunk in sb.GetChunks())
           {
                var span = chunk.Span;
                for (int i = 0; i < span.Length; i++)
                    { /* operation on span[i] */ }
           }
        """
        ...

    @overload
    def Insert(self, index: int, value: str, count: int) -> System.Text.StringBuilder:
        """
        Inserts a string 0 or more times into this builder at the specified position.
        
        :param index: The index to insert in this builder.
        :param value: The string to insert.
        :param count: The number of times to insert the string.
        """
        ...

    @overload
    def Insert(self, index: int, value: str) -> System.Text.StringBuilder:
        ...

    @overload
    def Insert(self, index: int, value: bool) -> System.Text.StringBuilder:
        ...

    @overload
    def Insert(self, index: int, value: int) -> System.Text.StringBuilder:
        ...

    @overload
    def Insert(self, index: int, value: int) -> System.Text.StringBuilder:
        ...

    @overload
    def Insert(self, index: int, value: int) -> System.Text.StringBuilder:
        ...

    @overload
    def Insert(self, index: int, value: str) -> System.Text.StringBuilder:
        ...

    @overload
    def Insert(self, index: int, value: typing.List[str]) -> System.Text.StringBuilder:
        ...

    @overload
    def Insert(self, index: int, value: typing.List[str], startIndex: int, charCount: int) -> System.Text.StringBuilder:
        ...

    @overload
    def Insert(self, index: int, value: int) -> System.Text.StringBuilder:
        ...

    @overload
    def Insert(self, index: int, value: int) -> System.Text.StringBuilder:
        ...

    @overload
    def Insert(self, index: int, value: float) -> System.Text.StringBuilder:
        ...

    @overload
    def Insert(self, index: int, value: float) -> System.Text.StringBuilder:
        ...

    @overload
    def Insert(self, index: int, value: float) -> System.Text.StringBuilder:
        ...

    @overload
    def Insert(self, index: int, value: int) -> System.Text.StringBuilder:
        ...

    @overload
    def Insert(self, index: int, value: int) -> System.Text.StringBuilder:
        ...

    @overload
    def Insert(self, index: int, value: int) -> System.Text.StringBuilder:
        ...

    @overload
    def Insert(self, index: int, value: typing.Any) -> System.Text.StringBuilder:
        ...

    @overload
    def Insert(self, index: int, value: System.ReadOnlySpan[str]) -> System.Text.StringBuilder:
        ...

    def Remove(self, startIndex: int, length: int) -> System.Text.StringBuilder:
        """Removes a range of characters from this builder."""
        ...

    @overload
    def Replace(self, oldValue: str, newValue: str) -> System.Text.StringBuilder:
        """
        Replaces all instances of one string with another in this builder.
        
        :param oldValue: The string to replace.
        :param newValue: The string to replace  with.
        """
        ...

    @overload
    def Replace(self, oldValue: System.ReadOnlySpan[str], newValue: System.ReadOnlySpan[str]) -> System.Text.StringBuilder:
        """
        Replaces all instances of one read-only character span with another in this builder.
        
        :param oldValue: The read-only character span to replace.
        :param newValue: The read-only character span to replace  with.
        """
        ...

    @overload
    def Replace(self, oldValue: str, newValue: str, startIndex: int, count: int) -> System.Text.StringBuilder:
        """
        Replaces all instances of one string with another in part of this builder.
        
        :param oldValue: The string to replace.
        :param newValue: The string to replace  with.
        :param startIndex: The index to start in this builder.
        :param count: The number of characters to read in this builder.
        """
        ...

    @overload
    def Replace(self, oldValue: System.ReadOnlySpan[str], newValue: System.ReadOnlySpan[str], startIndex: int, count: int) -> System.Text.StringBuilder:
        """
        Replaces all instances of one read-only character span with another in part of this builder.
        
        :param oldValue: The read-only character span to replace.
        :param newValue: The read-only character span to replace  with.
        :param startIndex: The index to start in this builder.
        :param count: The number of characters to read in this builder.
        """
        ...

    @overload
    def Replace(self, oldChar: str, newChar: str) -> System.Text.StringBuilder:
        """
        Replaces all instances of one character with another in this builder.
        
        :param oldChar: The character to replace.
        :param newChar: The character to replace  with.
        """
        ...

    @overload
    def Replace(self, oldChar: str, newChar: str, startIndex: int, count: int) -> System.Text.StringBuilder:
        """
        Replaces all instances of one character with another in this builder.
        
        :param oldChar: The character to replace.
        :param newChar: The character to replace  with.
        :param startIndex: The index to start in this builder.
        :param count: The number of characters to read in this builder.
        """
        ...

    @overload
    def ToString(self) -> str:
        ...

    @overload
    def ToString(self, startIndex: int, length: int) -> str:
        """
        Creates a string from a substring of this builder.
        
        :param startIndex: The index to start in this builder.
        :param length: The number of characters to read in this builder.
        """
        ...


class DecoderReplacementFallback(System.Text.DecoderFallback):
    """This class has no documentation."""

    @property
    def DefaultString(self) -> str:
        ...

    @property
    def MaxCharCount(self) -> int:
        ...

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, replacement: str) -> None:
        ...

    def CreateFallbackBuffer(self) -> System.Text.DecoderFallbackBuffer:
        ...

    def Equals(self, value: typing.Any) -> bool:
        ...

    def GetHashCode(self) -> int:
        ...


class DecoderReplacementFallbackBuffer(System.Text.DecoderFallbackBuffer):
    """This class has no documentation."""

    @property
    def Remaining(self) -> int:
        ...

    def __init__(self, fallback: System.Text.DecoderReplacementFallback) -> None:
        ...

    def Fallback(self, bytesUnknown: typing.List[int], index: int) -> bool:
        ...

    def GetNextChar(self) -> str:
        ...

    def MovePrevious(self) -> bool:
        ...

    def Reset(self) -> None:
        ...


class UTF32Encoding(System.Text.Encoding):
    """This class has no documentation."""

    @property
    def Preamble(self) -> System.ReadOnlySpan[int]:
        ...

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, bigEndian: bool, byteOrderMark: bool) -> None:
        ...

    @overload
    def __init__(self, bigEndian: bool, byteOrderMark: bool, throwOnInvalidCharacters: bool) -> None:
        ...

    def Equals(self, value: typing.Any) -> bool:
        ...

    @overload
    def GetByteCount(self, chars: typing.List[str], index: int, count: int) -> int:
        ...

    @overload
    def GetByteCount(self, s: str) -> int:
        ...

    @overload
    def GetByteCount(self, chars: typing.Any, count: int) -> int:
        ...

    @overload
    def GetBytes(self, s: str, charIndex: int, charCount: int, bytes: typing.List[int], byteIndex: int) -> int:
        ...

    @overload
    def GetBytes(self, chars: typing.List[str], charIndex: int, charCount: int, bytes: typing.List[int], byteIndex: int) -> int:
        ...

    @overload
    def GetBytes(self, chars: typing.Any, charCount: int, bytes: typing.Any, byteCount: int) -> int:
        ...

    @overload
    def GetCharCount(self, bytes: typing.List[int], index: int, count: int) -> int:
        ...

    @overload
    def GetCharCount(self, bytes: typing.Any, count: int) -> int:
        ...

    @overload
    def GetChars(self, bytes: typing.List[int], byteIndex: int, byteCount: int, chars: typing.List[str], charIndex: int) -> int:
        ...

    @overload
    def GetChars(self, bytes: typing.Any, byteCount: int, chars: typing.Any, charCount: int) -> int:
        ...

    def GetDecoder(self) -> System.Text.Decoder:
        ...

    def GetEncoder(self) -> System.Text.Encoder:
        ...

    def GetHashCode(self) -> int:
        ...

    def GetMaxByteCount(self, charCount: int) -> int:
        ...

    def GetMaxCharCount(self, byteCount: int) -> int:
        ...

    def GetPreamble(self) -> typing.List[int]:
        ...

    def GetString(self, bytes: typing.List[int], index: int, count: int) -> str:
        ...


class SpanLineEnumerator:
    """Enumerates the lines of a ReadOnlySpan{Char}."""

    @property
    def Current(self) -> System.ReadOnlySpan[str]:
        """Gets the line at the current position of the enumerator."""
        ...

    def GetEnumerator(self) -> System.Text.SpanLineEnumerator:
        """Returns this instance as an enumerator."""
        ...

    def MoveNext(self) -> bool:
        """
        Advances the enumerator to the next line of the span.
        
        :returns: True if the enumerator successfully advanced to the next line; false if the enumerator has advanced past the end of the span.
        """
        ...


class SpanRuneEnumerator:
    """This class has no documentation."""

    @property
    def Current(self) -> System.Text.Rune:
        ...

    def GetEnumerator(self) -> System.Text.SpanRuneEnumerator:
        ...

    def MoveNext(self) -> bool:
        ...


class EncoderExceptionFallback(System.Text.EncoderFallback):
    """This class has no documentation."""

    @property
    def MaxCharCount(self) -> int:
        ...

    def __init__(self) -> None:
        ...

    def CreateFallbackBuffer(self) -> System.Text.EncoderFallbackBuffer:
        ...

    def Equals(self, value: typing.Any) -> bool:
        ...

    def GetHashCode(self) -> int:
        ...


class EncoderExceptionFallbackBuffer(System.Text.EncoderFallbackBuffer):
    """This class has no documentation."""

    @property
    def Remaining(self) -> int:
        ...

    def __init__(self) -> None:
        ...

    @overload
    def Fallback(self, charUnknown: str, index: int) -> bool:
        ...

    @overload
    def Fallback(self, charUnknownHigh: str, charUnknownLow: str, index: int) -> bool:
        ...

    def GetNextChar(self) -> str:
        ...

    def MovePrevious(self) -> bool:
        ...


class EncoderFallbackException(System.ArgumentException):
    """This class has no documentation."""

    @property
    def CharUnknown(self) -> str:
        ...

    @property
    def CharUnknownHigh(self) -> str:
        ...

    @property
    def CharUnknownLow(self) -> str:
        ...

    @property
    def Index(self) -> int:
        ...

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, message: str) -> None:
        ...

    @overload
    def __init__(self, message: str, innerException: System.Exception) -> None:
        ...

    def IsUnknownSurrogate(self) -> bool:
        ...



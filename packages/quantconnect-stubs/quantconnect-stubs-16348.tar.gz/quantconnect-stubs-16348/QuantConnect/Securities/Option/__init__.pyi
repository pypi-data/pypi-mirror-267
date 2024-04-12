from typing import overload
import abc
import datetime
import typing
import warnings

import QuantConnect
import QuantConnect.Data
import QuantConnect.Data.Market
import QuantConnect.Interfaces
import QuantConnect.Orders
import QuantConnect.Orders.Fees
import QuantConnect.Orders.Fills
import QuantConnect.Orders.OptionExercise
import QuantConnect.Orders.Slippage
import QuantConnect.Securities
import QuantConnect.Securities.Future
import QuantConnect.Securities.Interfaces
import QuantConnect.Securities.Option
import QuantConnect.Securities.Positions
import System
import System.Collections.Generic

QuantConnect_Securities_Option_OptionStrategy_LegData = typing.Any
GeneralizedBlackScholesProcess = typing.Any
IPricingEngine = typing.Any


class IOptionPriceModel(metaclass=abc.ABCMeta):
    """Defines a model used to calculate the theoretical price of an option contract."""


class OptionStrategy(System.Object):
    """Option strategy specification class. Describes option strategy and its parameters for trading."""

    class LegData(QuantConnect.Orders.Leg, metaclass=abc.ABCMeta):
        """Defines common properties between OptionLegData and UnderlyingLegData"""

        def Invoke(self, underlyingHandler: typing.Callable[[QuantConnect.Securities.Option.OptionStrategy.UnderlyingLegData], None], optionHandler: typing.Callable[[QuantConnect.Securities.Option.OptionStrategy.OptionLegData], None]) -> None:
            """Invokes the correct handler based on the runtime type."""
            ...

    class OptionLegData(QuantConnect_Securities_Option_OptionStrategy_LegData):
        """This class is a POCO containing basic data for the option legs of the strategy"""

        @property
        def Right(self) -> int:
            """
            Option right (type) of the option leg
            
            This property contains the int value of a member of the QuantConnect.OptionRight enum.
            """
            ...

        @property
        def Expiration(self) -> datetime.datetime:
            """Expiration date of the leg"""
            ...

        @property
        def Strike(self) -> float:
            """Strike price of the leg"""
            ...

        @staticmethod
        def Create(quantity: int, symbol: typing.Union[QuantConnect.Symbol, str], orderPrice: typing.Optional[float] = None) -> QuantConnect.Securities.Option.OptionStrategy.OptionLegData:
            """Creates a new instance of OptionLegData from the specified parameters"""
            ...

        def Invoke(self, underlyingHandler: typing.Callable[[QuantConnect.Securities.Option.OptionStrategy.UnderlyingLegData], None], optionHandler: typing.Callable[[QuantConnect.Securities.Option.OptionStrategy.OptionLegData], None]) -> None:
            """Invokes the"""
            ...

    class UnderlyingLegData(QuantConnect_Securities_Option_OptionStrategy_LegData):
        """This class is a POCO containing basic data for the underlying leg of the strategy"""

        @staticmethod
        @overload
        def Create(quantity: int, symbol: typing.Union[QuantConnect.Symbol, str], orderPrice: typing.Optional[float] = None) -> QuantConnect.Securities.Option.OptionStrategy.UnderlyingLegData:
            """Creates a new instance of UnderlyingLegData for the specified  of underlying shares."""
            ...

        @staticmethod
        @overload
        def Create(quantity: int, orderPrice: typing.Optional[float] = None) -> QuantConnect.Securities.Option.OptionStrategy.UnderlyingLegData:
            """Creates a new instance of UnderlyingLegData for the specified  of underlying shares."""
            ...

        def Invoke(self, underlyingHandler: typing.Callable[[QuantConnect.Securities.Option.OptionStrategy.UnderlyingLegData], None], optionHandler: typing.Callable[[QuantConnect.Securities.Option.OptionStrategy.OptionLegData], None]) -> None:
            """Invokes the"""
            ...

    @property
    def Name(self) -> str:
        """Option strategy name"""
        ...

    @property
    def CanonicalOption(self) -> QuantConnect.Symbol:
        """The canonical Option symbol of the strategy"""
        ...

    @property
    def Underlying(self) -> QuantConnect.Symbol:
        """Underlying symbol of the strategy"""
        ...

    @property
    def OptionLegs(self) -> System.Collections.Generic.List[QuantConnect.Securities.Option.OptionStrategy.OptionLegData]:
        """Option strategy legs"""
        ...

    @property
    def UnderlyingLegs(self) -> System.Collections.Generic.List[QuantConnect.Securities.Option.OptionStrategy.UnderlyingLegData]:
        """Option strategy underlying legs (usually 0 or 1 legs)"""
        ...


class OptionStrategies(System.Object):
    """
    Provides methods for creating popular OptionStrategy instances.
    These strategies can be directly bought and sold via:
        QCAlgorithm.Buy(OptionStrategy strategy, int quantity)
        QCAlgorithm.Sell(OptionStrategy strategy, int quantity)
    
    See also OptionStrategyDefinitions
    """

    @staticmethod
    def BearCallSpread(canonicalOption: typing.Union[QuantConnect.Symbol, str], leg1Strike: float, leg2Strike: float, expiration: typing.Union[datetime.datetime, datetime.date]) -> QuantConnect.Securities.Option.OptionStrategy:
        """
        Method creates new Bear Call Spread strategy, that consists of two calls with the same expiration but different strikes.
        The strike price of the short call is below the strike of the long call. This is a credit spread.
        
        :param canonicalOption: Option symbol
        :param leg1Strike: The strike price of the short call
        :param leg2Strike: The strike price of the long call
        :param expiration: Option expiration date
        :returns: Option strategy specification.
        """
        ...

    @staticmethod
    def BearPutSpread(canonicalOption: typing.Union[QuantConnect.Symbol, str], leg1Strike: float, leg2Strike: float, expiration: typing.Union[datetime.datetime, datetime.date]) -> QuantConnect.Securities.Option.OptionStrategy:
        """
        Method creates new Bear Put Spread strategy, that consists of two puts with the same expiration but different strikes.
        The strike price of the short put is below the strike of the long put. This is a debit spread.
        
        :param canonicalOption: Option symbol
        :param leg1Strike: The strike price of the long put
        :param leg2Strike: The strike price of the short put
        :param expiration: Option expiration date
        :returns: Option strategy specification.
        """
        ...

    @staticmethod
    def BullCallSpread(canonicalOption: typing.Union[QuantConnect.Symbol, str], leg1Strike: float, leg2Strike: float, expiration: typing.Union[datetime.datetime, datetime.date]) -> QuantConnect.Securities.Option.OptionStrategy:
        """
        Method creates new Bull Call Spread strategy, that consists of two calls with the same expiration but different strikes.
        The strike price of the short call is higher than the strike of the long call. This is a debit spread.
        
        :param canonicalOption: Option symbol
        :param leg1Strike: The strike price of the long call
        :param leg2Strike: The strike price of the short call
        :param expiration: Option expiration date
        :returns: Option strategy specification.
        """
        ...

    @staticmethod
    def BullPutSpread(canonicalOption: typing.Union[QuantConnect.Symbol, str], leg1Strike: float, leg2Strike: float, expiration: typing.Union[datetime.datetime, datetime.date]) -> QuantConnect.Securities.Option.OptionStrategy:
        """
        Method creates new Bull Put Spread strategy, that consists of two puts with the same expiration but different strikes.
        The strike price of the short put is above the strike of the long put. This is a credit spread.
        
        :param canonicalOption: Option symbol
        :param leg1Strike: The strike price of the short put
        :param leg2Strike: The strike price of the long put
        :param expiration: Option expiration date
        :returns: Option strategy specification.
        """
        ...

    @staticmethod
    def ButterflyCall(canonicalOption: typing.Union[QuantConnect.Symbol, str], higherStrike: float, middleStrike: float, lowerStrike: float, expiration: typing.Union[datetime.datetime, datetime.date]) -> QuantConnect.Securities.Option.OptionStrategy:
        """
        Creates a new Butterfly Call strategy that consists of two short calls at a middle strike,
        and one long call each at a lower and upper strike.
        The upper and lower strikes must both be equidistant from the middle strike.
        
        :param canonicalOption: Option symbol
        :param higherStrike: The upper strike price of the long call
        :param middleStrike: The middle strike price of the two short calls
        :param lowerStrike: The lower strike price of the long call
        :param expiration: Option expiration date
        :returns: Option strategy specification.
        """
        ...

    @staticmethod
    def ButterflyPut(canonicalOption: typing.Union[QuantConnect.Symbol, str], higherStrike: float, middleStrike: float, lowerStrike: float, expiration: typing.Union[datetime.datetime, datetime.date]) -> QuantConnect.Securities.Option.OptionStrategy:
        """
        Creates a new Butterfly Put strategy that consists of two short puts at a middle strike,
        and one long put each at a lower and upper strike.
        The upper and lower strikes must both be equidistant from the middle strike.
        
        :param canonicalOption: Option symbol
        :param higherStrike: The upper strike price of the long put
        :param middleStrike: The middle strike price of the two short puts
        :param lowerStrike: The lower strike price of the long put
        :param expiration: Option expiration date
        :returns: Option strategy specification.
        """
        ...

    @staticmethod
    def CallButterfly(canonicalOption: typing.Union[QuantConnect.Symbol, str], higherStrike: float, middleStrike: float, lowerStrike: float, expiration: typing.Union[datetime.datetime, datetime.date]) -> QuantConnect.Securities.Option.OptionStrategy:
        """
        Method creates new Call Butterfly strategy, that consists of two short calls at a middle strike, and one long call each at a lower and upper strike.
        The upper and lower strikes must both be equidistant from the middle strike.
        
        :param canonicalOption: Option symbol
        :param higherStrike: The upper strike price of the long call
        :param middleStrike: The middle strike price of the two short calls
        :param lowerStrike: The lower strike price of the long call
        :param expiration: Option expiration date
        :returns: Option strategy specification.
        """
        ...

    @staticmethod
    def CallCalendarSpread(canonicalOption: typing.Union[QuantConnect.Symbol, str], strike: float, nearExpiration: typing.Union[datetime.datetime, datetime.date], farExpiration: typing.Union[datetime.datetime, datetime.date]) -> QuantConnect.Securities.Option.OptionStrategy:
        """
        Creates new Call Calendar Spread strategy which consists of a short and a long call
        with the same strikes but with the long call having a further expiration date.
        
        :param canonicalOption: Option symbol
        :param strike: The strike price of the both legs
        :param nearExpiration: Near expiration date for the short option
        :param farExpiration: Far expiration date for the long option
        :returns: Option strategy specification.
        """
        ...

    @staticmethod
    def CoveredCall(canonicalOption: typing.Union[QuantConnect.Symbol, str], strike: float, expiration: typing.Union[datetime.datetime, datetime.date]) -> QuantConnect.Securities.Option.OptionStrategy:
        """
        Creates a Covered Call strategy that consists of selling one call contract and buying 1 lot of the underlying.
        
        :param canonicalOption: Option symbol
        :param strike: The strike price for the call option contract
        :param expiration: The expiration date for the call option contract
        :returns: Option strategy specification.
        """
        ...

    @staticmethod
    def CoveredPut(canonicalOption: typing.Union[QuantConnect.Symbol, str], strike: float, expiration: typing.Union[datetime.datetime, datetime.date]) -> QuantConnect.Securities.Option.OptionStrategy:
        """
        Creates a Covered Put strategy that consists of selling 1 put contract and 1 lot of the underlying.
        
        :param canonicalOption: Option symbol
        :param strike: The strike price for the put option contract
        :param expiration: The expiration date for the put option contract
        :returns: Option strategy specification.
        """
        ...

    @staticmethod
    def IronCondor(canonicalOption: typing.Union[QuantConnect.Symbol, str], longPutStrike: float, shortPutStrike: float, shortCallStrike: float, longCallStrike: float, expiration: typing.Union[datetime.datetime, datetime.date]) -> QuantConnect.Securities.Option.OptionStrategy:
        """
        Creates a new Iron Condor strategy which consists of a long put, a short put, a short call and a long option,
        all with the same expiration date and with increasing strikes prices in the mentioned order.
        
        :param canonicalOption: Option symbol
        :param longPutStrike: Long put option strike price
        :param shortPutStrike: Short put option strike price
        :param shortCallStrike: Short call option strike price
        :param longCallStrike: Long call option strike price
        :param expiration: Expiration date for all the options
        :returns: Option strategy specification.
        """
        ...

    @staticmethod
    def NakedCall(canonicalOption: typing.Union[QuantConnect.Symbol, str], strike: float, expiration: typing.Union[datetime.datetime, datetime.date]) -> QuantConnect.Securities.Option.OptionStrategy:
        """
        Creates a Naked Call strategy that consists of selling 1 call contract.
        
        :param canonicalOption: Option symbol
        :param strike: The strike price for the call option contract
        :param expiration: The expiration date for the call option contract
        :returns: Option strategy specification.
        """
        ...

    @staticmethod
    def NakedPut(canonicalOption: typing.Union[QuantConnect.Symbol, str], strike: float, expiration: typing.Union[datetime.datetime, datetime.date]) -> QuantConnect.Securities.Option.OptionStrategy:
        """
        Creates a Naked Put strategy that consists of selling 1 put contract.
        
        :param canonicalOption: Option symbol
        :param strike: The strike price for the put option contract
        :param expiration: The expiration date for the put option contract
        :returns: Option strategy specification.
        """
        ...

    @staticmethod
    def ProtectiveCall(canonicalOption: typing.Union[QuantConnect.Symbol, str], strike: float, expiration: typing.Union[datetime.datetime, datetime.date]) -> QuantConnect.Securities.Option.OptionStrategy:
        """
        Creates a Protective Call strategy that consists of buying one call contract and selling 1 lot of the underlying.
        
        :param canonicalOption: Option symbol
        :param strike: The strike price for the call option contract
        :param expiration: The expiration date for the call option contract
        :returns: Option strategy specification.
        """
        ...

    @staticmethod
    def ProtectivePut(canonicalOption: typing.Union[QuantConnect.Symbol, str], strike: float, expiration: typing.Union[datetime.datetime, datetime.date]) -> QuantConnect.Securities.Option.OptionStrategy:
        """
        Creates a Protective Put strategy that consists of buying 1 put contract and 1 lot of the underlying.
        
        :param canonicalOption: Option symbol
        :param strike: The strike price for the put option contract
        :param expiration: The expiration date for the put option contract
        :returns: Option strategy specification.
        """
        ...

    @staticmethod
    def PutButterfly(canonicalOption: typing.Union[QuantConnect.Symbol, str], higherStrike: float, middleStrike: float, lowerStrike: float, expiration: typing.Union[datetime.datetime, datetime.date]) -> QuantConnect.Securities.Option.OptionStrategy:
        """
        Method creates new Put Butterfly strategy, that consists of two short puts at a middle strike, and one long put each at a lower and upper strike.
        The upper and lower strikes must both be equidistant from the middle strike.
        
        :param canonicalOption: Option symbol
        :param higherStrike: The upper strike price of the long put
        :param middleStrike: The middle strike price of the two short puts
        :param lowerStrike: The lower strike price of the long put
        :param expiration: Option expiration date
        :returns: Option strategy specification.
        """
        ...

    @staticmethod
    def PutCalendarSpread(canonicalOption: typing.Union[QuantConnect.Symbol, str], strike: float, nearExpiration: typing.Union[datetime.datetime, datetime.date], farExpiration: typing.Union[datetime.datetime, datetime.date]) -> QuantConnect.Securities.Option.OptionStrategy:
        """
        Creates new Put Calendar Spread strategy which consists of a short and a long put
        with the same strikes but with the long put having a further expiration date.
        
        :param canonicalOption: Option symbol
        :param strike: The strike price of the both legs
        :param nearExpiration: Near expiration date for the short option
        :param farExpiration: Far expiration date for the long option
        :returns: Option strategy specification.
        """
        ...

    @staticmethod
    def ShortButterflyCall(canonicalOption: typing.Union[QuantConnect.Symbol, str], higherStrike: float, middleStrike: float, lowerStrike: float, expiration: typing.Union[datetime.datetime, datetime.date]) -> QuantConnect.Securities.Option.OptionStrategy:
        """
        Creates a new Butterfly Call strategy that consists of two long calls at a middle strike,
        and one short call each at a lower and upper strike.
        The upper and lower strikes must both be equidistant from the middle strike.
        
        :param canonicalOption: Option symbol
        :param higherStrike: The upper strike price of the short call
        :param middleStrike: The middle strike price of the two long calls
        :param lowerStrike: The lower strike price of the short call
        :param expiration: Option expiration date
        :returns: Option strategy specification.
        """
        ...

    @staticmethod
    def ShortButterflyPut(canonicalOption: typing.Union[QuantConnect.Symbol, str], higherStrike: float, middleStrike: float, lowerStrike: float, expiration: typing.Union[datetime.datetime, datetime.date]) -> QuantConnect.Securities.Option.OptionStrategy:
        """
        Creates a new Butterfly Put strategy that consists of two long puts at a middle strike,
        and one short put each at a lower and upper strike.
        The upper and lower strikes must both be equidistant from the middle strike.
        
        :param canonicalOption: Option symbol
        :param higherStrike: The upper strike price of the short put
        :param middleStrike: The middle strike price of the two long puts
        :param lowerStrike: The lower strike price of the short put
        :param expiration: Option expiration date
        :returns: Option strategy specification.
        """
        ...

    @staticmethod
    def ShortCallCalendarSpread(canonicalOption: typing.Union[QuantConnect.Symbol, str], strike: float, nearExpiration: typing.Union[datetime.datetime, datetime.date], farExpiration: typing.Union[datetime.datetime, datetime.date]) -> QuantConnect.Securities.Option.OptionStrategy:
        """
        Creates new Short Call Calendar Spread strategy which consists of a short and a long call
        with the same strikes but with the short call having a further expiration date.
        
        :param canonicalOption: Option symbol
        :param strike: The strike price of the both legs
        :param nearExpiration: Near expiration date for the long option
        :param farExpiration: Far expiration date for the short option
        :returns: Option strategy specification.
        """
        ...

    @staticmethod
    def ShortPutCalendarSpread(canonicalOption: typing.Union[QuantConnect.Symbol, str], strike: float, nearExpiration: typing.Union[datetime.datetime, datetime.date], farExpiration: typing.Union[datetime.datetime, datetime.date]) -> QuantConnect.Securities.Option.OptionStrategy:
        """
        Creates new Short Put Calendar Spread strategy which consists of a short and a long put
        with the same strikes but with the short put having a further expiration date.
        
        :param canonicalOption: Option symbol
        :param strike: The strike price of the both legs
        :param nearExpiration: Near expiration date for the long option
        :param farExpiration: Far expiration date for the short option
        :returns: Option strategy specification.
        """
        ...

    @staticmethod
    def ShortStraddle(canonicalOption: typing.Union[QuantConnect.Symbol, str], strike: float, expiration: typing.Union[datetime.datetime, datetime.date]) -> QuantConnect.Securities.Option.OptionStrategy:
        """
        Creates a Short Straddle strategy that consists of selling a call and a put, both with the same strike price and expiration.
        
        :param canonicalOption: Option symbol
        :param strike: The strike price for the option contracts
        :param expiration: The expiration date for the option contracts
        :returns: Option strategy specification.
        """
        ...

    @staticmethod
    def ShortStrangle(canonicalOption: typing.Union[QuantConnect.Symbol, str], callLegStrike: float, putLegStrike: float, expiration: typing.Union[datetime.datetime, datetime.date]) -> QuantConnect.Securities.Option.OptionStrategy:
        """
        Creates a Short Strangle strategy that consists of selling a call and a put, with the same expiration date and
        the call strike being above the put strike.
        
        :param canonicalOption: Option symbol
        :param callLegStrike: The strike price of the short call
        :param putLegStrike: The strike price of the short put
        :param expiration: Option expiration date
        :returns: Option strategy specification.
        """
        ...

    @staticmethod
    def Straddle(canonicalOption: typing.Union[QuantConnect.Symbol, str], strike: float, expiration: typing.Union[datetime.datetime, datetime.date]) -> QuantConnect.Securities.Option.OptionStrategy:
        """
        Method creates new Straddle strategy, that is a combination of buying a call and buying a put, both with the same strike price and expiration.
        
        :param canonicalOption: Option symbol
        :param strike: The strike price of the both legs
        :param expiration: Option expiration date
        :returns: Option strategy specification.
        """
        ...

    @staticmethod
    def Strangle(canonicalOption: typing.Union[QuantConnect.Symbol, str], callLegStrike: float, putLegStrike: float, expiration: typing.Union[datetime.datetime, datetime.date]) -> QuantConnect.Securities.Option.OptionStrategy:
        """
        Method creates new Strangle strategy, that buying a call option and a put option with the same expiration date
        The strike price of the call is above the strike of the put.
        
        :param canonicalOption: Option symbol
        :param callLegStrike: The strike price of the long call
        :param putLegStrike: The strike price of the long put
        :param expiration: Option expiration date
        :returns: Option strategy specification.
        """
        ...


class OptionPriceModelResult(System.Object):
    """Result type for IOptionPriceModel.Evaluate"""

    # Cannot convert to Python: None: QuantConnect.Securities.Option.OptionPriceModelResult
    """Represents the zero option price and greeks."""

    @property
    def TheoreticalPrice(self) -> float:
        """Gets the theoretical price as computed by the IOptionPriceModel"""
        ...

    @property
    def ImpliedVolatility(self) -> float:
        """Gets the implied volatility of the option contract"""
        ...

    @property
    def Greeks(self) -> QuantConnect.Data.Market.Greeks:
        """Gets the various sensitivities as computed by the IOptionPriceModel"""
        ...

    @overload
    def __init__(self, theoreticalPrice: float, greeks: QuantConnect.Data.Market.Greeks) -> None:
        """
        Initializes a new instance of the OptionPriceModelResult class
        
        :param theoreticalPrice: The theoretical price computed by the price model
        :param greeks: The sensitivities (greeks) computed by the price model
        """
        ...

    @overload
    def __init__(self, theoreticalPrice: float, impliedVolatility: typing.Callable[[], float], greeks: typing.Callable[[], QuantConnect.Data.Market.Greeks]) -> None:
        """
        Initializes a new instance of the OptionPriceModelResult class with lazy calculations of implied volatility and greeks
        
        :param theoreticalPrice: The theoretical price computed by the price model
        :param impliedVolatility: The calculated implied volatility
        :param greeks: The sensitivities (greeks) computed by the price model
        """
        ...


class OptionExchange(QuantConnect.Securities.SecurityExchange):
    """Option exchange class - information and helper tools for option exchange properties"""

    @property
    def TradingDaysPerYear(self) -> int:
        """Number of trading days per year for this security, 252."""
        ...

    def __init__(self, exchangeHours: QuantConnect.Securities.SecurityExchangeHours) -> None:
        """
        Initializes a new instance of the OptionExchange class using the specified
        exchange hours to determine open/close times
        
        :param exchangeHours: Contains the weekly exchange schedule plus holidays
        """
        ...


class OptionPortfolioModel(QuantConnect.Securities.SecurityPortfolioModel):
    """
    Provides an implementation of ISecurityPortfolioModel for options that supports
    default fills as well as option exercising.
    """

    def ProcessExerciseFill(self, portfolio: QuantConnect.Securities.SecurityPortfolioManager, security: QuantConnect.Securities.Security, order: QuantConnect.Orders.Order, fill: QuantConnect.Orders.OrderEvent) -> None:
        """
        Processes exercise/assignment event to the portfolio
        
        :param portfolio: The algorithm's portfolio
        :param security: Option security
        :param order: The order object to be applied
        :param fill: The order event fill object to be applied
        """
        ...

    def ProcessFill(self, portfolio: QuantConnect.Securities.SecurityPortfolioManager, security: QuantConnect.Securities.Security, fill: QuantConnect.Orders.OrderEvent) -> None:
        """
        Performs application of an OrderEvent to the portfolio
        
        :param portfolio: The algorithm's portfolio
        :param security: Option security
        :param fill: The order event fill object to be applied
        """
        ...


class OptionCache(QuantConnect.Securities.SecurityCache):
    """Option specific caching support"""


class EmptyOptionChainProvider(System.Object, QuantConnect.Interfaces.IOptionChainProvider):
    """An implementation of IOptionChainProvider that always returns an empty list of contracts"""

    def GetOptionContractList(self, symbol: typing.Union[QuantConnect.Symbol, str], date: typing.Union[datetime.datetime, datetime.date]) -> System.Collections.Generic.IEnumerable[QuantConnect.Symbol]:
        """
        Gets the list of option contracts for a given underlying symbol
        
        :param symbol: The underlying symbol
        :param date: The date for which to request the option chain (only used in backtesting)
        :returns: The list of option contracts.
        """
        ...


class IQLDividendYieldEstimator(metaclass=abc.ABCMeta):
    """
    Defines QuantLib dividend yield estimator for option pricing model. User may define his own estimators,
    including those forward and backward looking ones.
    """


class ConstantQLDividendYieldEstimator(System.Object, QuantConnect.Securities.Option.IQLDividendYieldEstimator):
    """Class implements default flat dividend yield curve estimator, implementing IQLDividendYieldEstimator."""

    def __init__(self, dividendYield: float = 0.00) -> None:
        """Constructor initializes class with constant dividend yield."""
        ...

    def Estimate(self, security: QuantConnect.Securities.Security, slice: QuantConnect.Data.Slice, contract: QuantConnect.Data.Market.OptionContract) -> float:
        """
        Returns current flat estimate of the dividend yield
        
        :param security: The option security object
        :param slice: The current data slice. This can be used to access other information available to the algorithm
        :param contract: The option contract to evaluate
        :returns: The estimate.
        """
        ...


class OptionAssignmentResult(System.Object):
    """Data transfer object class"""

    Null: QuantConnect.Securities.Option.OptionAssignmentResult
    """No option assignment should take place"""

    @property
    def Quantity(self) -> float:
        """The amount of option holdings to trigger the assignment for"""
        ...

    @property
    def Tag(self) -> str:
        """The tag that will be used in the order for the option assignment"""
        ...

    def __init__(self, quantity: float, tag: str) -> None:
        """
        Creates a new instance
        
        :param quantity: The quantity to assign
        :param tag: The order tag to use
        """
        ...


class IOptionAssignmentModel(metaclass=abc.ABCMeta):
    """The option assignment model emulates exercising of short option positions in the portfolio."""

    def GetAssignment(self, parameters: QuantConnect.Securities.Option.OptionAssignmentParameters) -> QuantConnect.Securities.Option.OptionAssignmentResult:
        """
        Get's the option assignments to generate if any
        
        :param parameters: The option assignment parameters data transfer class
        :returns: The option assignment result.
        """
        ...


class OptionSymbolProperties(QuantConnect.Securities.SymbolProperties):
    """Represents common properties for a specific option contract"""

    @property
    def ContractUnitOfTrade(self) -> int:
        """
        When the holder of an equity option exercises one contract, or when the writer of an equity option is assigned
        an exercise notice on one contract, this unit of trade, usually 100 shares of the underlying security, changes hands.
        """
        ...

    @property
    def MinimumPriceVariation(self) -> float:
        """
        Overridable minimum price variation, required for index options contracts with
        variable sized quoted prices depending on the premium of the option.
        """
        ...

    @overload
    def __init__(self, description: str, quoteCurrency: str, contractMultiplier: float, pipSize: float, lotSize: float) -> None:
        """Creates an instance of the OptionSymbolProperties class"""
        ...

    @overload
    def __init__(self, properties: QuantConnect.Securities.SymbolProperties) -> None:
        """Creates an instance of the OptionSymbolProperties class from SymbolProperties class"""
        ...


class Option(QuantConnect.Securities.Security, QuantConnect.Securities.IDerivativeSecurity, QuantConnect.Interfaces.IOptionPrice):
    """Option Security Object Implementation for Option Assets"""

    DefaultSettlementDays: int = 1
    """The default number of days required to settle an equity sale"""

    DefaultSettlementTime: datetime.timedelta = ...
    """The default time of day for settlement"""

    @property
    def IsOptionChain(self) -> bool:
        """Returns true if this is the option chain security, false if it is a specific option contract"""
        ...

    @property
    def IsOptionContract(self) -> bool:
        """Returns true if this is a specific option contract security, false if it is the option chain security"""
        ...

    @property
    def StrikePrice(self) -> float:
        """Gets the strike price"""
        ...

    @property
    def ScaledStrikePrice(self) -> float:
        """Gets the strike price multiplied by the strike multiplier"""
        ...

    @property
    def Expiry(self) -> datetime.datetime:
        """Gets the expiration date"""
        ...

    @property
    def Right(self) -> int:
        """
        Gets the right being purchased (call [right to buy] or put [right to sell])
        
        This property contains the int value of a member of the QuantConnect.OptionRight enum.
        """
        ...

    @property
    def Style(self) -> int:
        """
        Gets the option style
        
        This property contains the int value of a member of the QuantConnect.OptionStyle enum.
        """
        ...

    @property
    def BidPrice(self) -> float:
        """Gets the most recent bid price if available"""
        ...

    @property
    def AskPrice(self) -> float:
        """Gets the most recent ask price if available"""
        ...

    @property
    def ContractUnitOfTrade(self) -> int:
        """
        When the holder of an equity option exercises one contract, or when the writer of an equity option is assigned
        an exercise notice on one contract, this unit of trade, usually 100 shares of the underlying security, changes hands.
        """
        ...

    @property
    def ContractMultiplier(self) -> int:
        """The contract multiplier for the option security"""
        ...

    @property
    def ExerciseSettlement(self) -> int:
        """
        Specifies if option contract has physical or cash settlement on exercise
        
        This property contains the int value of a member of the QuantConnect.SettlementType enum.
        """
        ...

    @property
    def Underlying(self) -> QuantConnect.Securities.Security:
        """Gets or sets the underlying security object."""
        ...

    @property
    def PriceModel(self) -> QuantConnect.Securities.Option.IOptionPriceModel:
        """Gets or sets the price model for this option security"""
        ...

    @property
    def OptionExerciseModel(self) -> QuantConnect.Orders.OptionExercise.IOptionExerciseModel:
        """Fill model used to produce fill events for this security"""
        ...

    @property
    def OptionAssignmentModel(self) -> QuantConnect.Securities.Option.IOptionAssignmentModel:
        """The automatic option assignment model"""
        ...

    @property
    def EnableGreekApproximation(self) -> bool:
        """
        When enabled, approximates Greeks if corresponding pricing model didn't calculate exact numbers
        
        This property has been deprecated. Please use QLOptionPriceModel.EnableGreekApproximation instead.
        """
        warnings.warn("This property has been deprecated. Please use QLOptionPriceModel.EnableGreekApproximation instead.", DeprecationWarning)

    @property
    def ContractFilter(self) -> QuantConnect.Securities.IDerivativeSecurityFilter:
        """Gets or sets the contract filter"""
        ...

    @overload
    def __init__(self, exchangeHours: QuantConnect.Securities.SecurityExchangeHours, config: QuantConnect.Data.SubscriptionDataConfig, quoteCurrency: QuantConnect.Securities.Cash, symbolProperties: QuantConnect.Securities.Option.OptionSymbolProperties, currencyConverter: QuantConnect.Securities.ICurrencyConverter, registeredTypes: QuantConnect.Securities.IRegisteredSecurityDataTypesProvider) -> None:
        """
        Constructor for the option security
        
        :param exchangeHours: Defines the hours this exchange is open
        :param config: The subscription configuration for this security
        :param quoteCurrency: The cash object that represent the quote currency
        :param symbolProperties: The symbol properties for this security
        :param currencyConverter: Currency converter used to convert CashAmount instances into units of the account currency
        :param registeredTypes: Provides all data types registered in the algorithm
        """
        ...

    @overload
    def __init__(self, symbol: typing.Union[QuantConnect.Symbol, str], exchangeHours: QuantConnect.Securities.SecurityExchangeHours, quoteCurrency: QuantConnect.Securities.Cash, symbolProperties: QuantConnect.Securities.Option.OptionSymbolProperties, currencyConverter: QuantConnect.Securities.ICurrencyConverter, registeredTypes: QuantConnect.Securities.IRegisteredSecurityDataTypesProvider, securityCache: QuantConnect.Securities.SecurityCache, underlying: QuantConnect.Securities.Security) -> None:
        """
        Constructor for the option security
        
        :param symbol: The symbol of the security
        :param exchangeHours: Defines the hours this exchange is open
        :param quoteCurrency: The cash object that represent the quote currency
        :param symbolProperties: The symbol properties for this security
        :param currencyConverter: Currency converter used to convert CashAmount instances into units of the account currency
        :param registeredTypes: Provides all data types registered in the algorithm
        :param securityCache: Cache to store security information
        :param underlying: Future underlying security
        """
        ...

    @overload
    def __init__(self, symbol: typing.Union[QuantConnect.Symbol, str], quoteCurrency: QuantConnect.Securities.Cash, symbolProperties: QuantConnect.Securities.SymbolProperties, exchange: QuantConnect.Securities.SecurityExchange, cache: QuantConnect.Securities.SecurityCache, portfolioModel: QuantConnect.Securities.ISecurityPortfolioModel, fillModel: QuantConnect.Orders.Fills.IFillModel, feeModel: QuantConnect.Orders.Fees.IFeeModel, slippageModel: QuantConnect.Orders.Slippage.ISlippageModel, settlementModel: QuantConnect.Securities.ISettlementModel, volatilityModel: QuantConnect.Securities.IVolatilityModel, buyingPowerModel: QuantConnect.Securities.IBuyingPowerModel, dataFilter: QuantConnect.Securities.Interfaces.ISecurityDataFilter, priceVariationModel: QuantConnect.Securities.IPriceVariationModel, currencyConverter: QuantConnect.Securities.ICurrencyConverter, registeredTypesProvider: QuantConnect.Securities.IRegisteredSecurityDataTypesProvider, underlying: QuantConnect.Securities.Security) -> None:
        """
        Creates instance of the Option class.
        
        This method is protected.
        """
        ...

    def EvaluatePriceModel(self, slice: QuantConnect.Data.Slice, contract: QuantConnect.Data.Market.OptionContract) -> QuantConnect.Securities.Option.OptionPriceModelResult:
        """
        For this option security object, evaluates the specified option
        contract to compute a theoretical price, IV and greeks
        
        :param slice: The current data slice. This can be used to access other information available to the algorithm
        :param contract: The option contract to evaluate
        :returns: An instance of OptionPriceModelResult containing the theoretical price of the specified option contract.
        """
        ...

    def GetAggregateExerciseAmount(self) -> float:
        """
        Aggregate exercise amount or aggregate contract value. It is the total amount of cash one will pay (or receive) for the shares of the
        underlying stock if he/she decides to exercise (or is assigned an exercise notice). This amount is not the premium paid or received for an equity option.
        """
        ...

    @overload
    def GetExerciseQuantity(self) -> float:
        """
        Returns the directional quantity of underlying shares that are going to change hands on exercise/assignment of all
        contracts held by this account, taking into account the contract's Right as well as the contract's current
        ContractUnitOfTrade, which may have recently changed due to a split/reverse split in the underlying security.
        """
        ...

    @overload
    def GetExerciseQuantity(self, exerciseOrderQuantity: float) -> float:
        """
        Returns the directional quantity of underlying shares that are going to change hands on exercise/assignment of the
        specified , taking into account the contract's Right as well
        as the contract's current ContractUnitOfTrade, which may have recently changed due to a split/reverse
        split in the underlying security.
        """
        ...

    def GetIntrinsicValue(self, underlyingPrice: float) -> float:
        """Intrinsic value function of the option"""
        ...

    def GetPayOff(self, underlyingPrice: float) -> float:
        """
        Option payoff function at expiration time
        
        :param underlyingPrice: The price of the underlying
        """
        ...

    def IsAutoExercised(self, underlyingPrice: float) -> bool:
        """Checks if option is eligible for automatic exercise on expiration"""
        ...

    def OutOfTheMoneyAmount(self, underlyingPrice: float) -> float:
        """
        Option out of the money function
        
        :param underlyingPrice: The price of the underlying
        """
        ...

    def SetDataNormalizationMode(self, mode: QuantConnect.DataNormalizationMode) -> None:
        """Sets the data normalization mode to be used by this security"""
        ...

    @overload
    def SetFilter(self, minStrike: int, maxStrike: int) -> None:
        """
        Sets the ContractFilter to a new instance of the filter
        using the specified min and max strike values. Contracts with expirations further than 35
        days out will also be filtered.
        
        :param minStrike: The min strike rank relative to market price, for example, -1 would put a lower bound of one strike under market price, where a +1 would put a lower bound of one strike over market price
        :param maxStrike: The max strike rank relative to market place, for example, -1 would put an upper bound of on strike under market price, where a +1 would be an upper bound of one strike over market price
        """
        ...

    @overload
    def SetFilter(self, minExpiry: datetime.timedelta, maxExpiry: datetime.timedelta) -> None:
        """
        Sets the ContractFilter to a new instance of the filter
        using the specified min and max strike and expiration range values
        
        :param minExpiry: The minimum time until expiry to include, for example, TimeSpan.FromDays(10) would exclude contracts expiring in less than 10 days
        :param maxExpiry: The maximum time until expiry to include, for example, TimeSpan.FromDays(10) would exclude contracts expiring in more than 10 days
        """
        ...

    @overload
    def SetFilter(self, minStrike: int, maxStrike: int, minExpiry: datetime.timedelta, maxExpiry: datetime.timedelta) -> None:
        """
        Sets the ContractFilter to a new instance of the filter
        using the specified min and max strike and expiration range values
        
        :param minStrike: The min strike rank relative to market price, for example, -1 would put a lower bound of one strike under market price, where a +1 would put a lower bound of one strike over market price
        :param maxStrike: The max strike rank relative to market place, for example, -1 would put an upper bound of on strike under market price, where a +1 would be an upper bound of one strike over market price
        :param minExpiry: The minimum time until expiry to include, for example, TimeSpan.FromDays(10) would exclude contracts expiring in less than 10 days
        :param maxExpiry: The maximum time until expiry to include, for example, TimeSpan.FromDays(10) would exclude contracts expiring in more than 10 days
        """
        ...

    @overload
    def SetFilter(self, minStrike: int, maxStrike: int, minExpiryDays: int, maxExpiryDays: int) -> None:
        """
        Sets the ContractFilter to a new instance of the filter
        using the specified min and max strike and expiration range values
        
        :param minStrike: The min strike rank relative to market price, for example, -1 would put a lower bound of one strike under market price, where a +1 would put a lower bound of one strike over market price
        :param maxStrike: The max strike rank relative to market place, for example, -1 would put an upper bound of on strike under market price, where a +1 would be an upper bound of one strike over market price
        :param minExpiryDays: The minimum time, expressed in days, until expiry to include, for example, 10 would exclude contracts expiring in less than 10 days
        :param maxExpiryDays: The maximum time, expressed in days, until expiry to include, for example, 10 would exclude contracts expiring in more than 10 days
        """
        ...

    @overload
    def SetFilter(self, universeFunc: typing.Callable[[QuantConnect.Securities.OptionFilterUniverse], QuantConnect.Securities.OptionFilterUniverse]) -> None:
        """
        Sets the ContractFilter to a new universe selection function
        
        :param universeFunc: new universe selection function
        """
        ...

    @overload
    def SetFilter(self, universeFunc: typing.Any) -> None:
        """
        Sets the ContractFilter to a new universe selection function
        
        :param universeFunc: new universe selection function
        """
        ...

    @overload
    def SetOptionAssignmentModel(self, pyObject: typing.Any) -> None:
        """
        Sets the automatic option assignment model
        
        :param pyObject: The option assignment model to use
        """
        ...

    @overload
    def SetOptionAssignmentModel(self, optionAssignmentModel: QuantConnect.Securities.Option.IOptionAssignmentModel) -> None:
        """
        Sets the automatic option assignment model
        
        :param optionAssignmentModel: The option assignment model to use
        """
        ...

    @overload
    def SetOptionExerciseModel(self, pyObject: typing.Any) -> None:
        """
        Sets the option exercise model
        
        :param pyObject: The option exercise model to use
        """
        ...

    @overload
    def SetOptionExerciseModel(self, optionExerciseModel: QuantConnect.Orders.OptionExercise.IOptionExerciseModel) -> None:
        """
        Sets the option exercise model
        
        :param optionExerciseModel: The option exercise model to use
        """
        ...


class OptionAssignmentParameters(System.Object):
    """The option assignment parameters data transfer class"""

    @property
    def Option(self) -> QuantConnect.Securities.Option.Option:
        """The option to evaluate option assignments for"""
        ...

    def __init__(self, option: QuantConnect.Securities.Option.Option) -> None:
        """
        Creates a new instance
        
        :param option: The target option
        """
        ...


class NullOptionAssignmentModel(System.Object, QuantConnect.Securities.Option.IOptionAssignmentModel):
    """The null option assignment model, that will disable automatic order assignment"""

    def GetAssignment(self, parameters: QuantConnect.Securities.Option.OptionAssignmentParameters) -> QuantConnect.Securities.Option.OptionAssignmentResult:
        """
        Get's the option assignments to generate if any
        
        :param parameters: The option assignment parameters data transfer object
        :returns: The option assignment result.
        """
        ...


class OptionSymbol(System.Object):
    """Static class contains common utility methods specific to symbols representing the option contracts"""

    @staticmethod
    def GetLastDayOfTrading(symbol: typing.Union[QuantConnect.Symbol, str]) -> datetime.datetime:
        """
        Returns the last trading date for the option contract
        
        :param symbol: Option symbol
        """
        ...

    @staticmethod
    def IsOptionContractExpired(symbol: typing.Union[QuantConnect.Symbol, str], currentTimeUtc: typing.Union[datetime.datetime, datetime.date]) -> bool:
        """
        Returns true if the option contract is expired at the specified time
        
        :param symbol: The option contract symbol
        :param currentTimeUtc: The current time (UTC)
        :returns: True if the option contract is expired at the specified time, false otherwise.
        """
        ...

    @staticmethod
    def IsStandard(symbol: typing.Union[QuantConnect.Symbol, str]) -> bool:
        """
        Returns true if the option is a standard contract that expires 3rd Friday of the month
        
        :param symbol: Option symbol
        """
        ...

    @staticmethod
    def IsStandardContract(symbol: typing.Union[QuantConnect.Symbol, str]) -> bool:
        """
        Returns true if the option is a standard contract that expires 3rd Friday of the month
        
        :param symbol: Option symbol
        """
        ...

    @staticmethod
    def IsWeekly(symbol: typing.Union[QuantConnect.Symbol, str]) -> bool:
        """
        Returns true if the option is a weekly contract that expires on Friday , except 3rd Friday of the month
        
        :param symbol: Option symbol
        """
        ...

    @staticmethod
    def MapToUnderlying(optionTicker: str, securityType: QuantConnect.SecurityType) -> str:
        """
        Maps the option ticker to it's underlying
        
        :param optionTicker: The option ticker to map
        :param securityType: The security type of the option or underlying
        :returns: The underlying ticker.
        """
        ...


class IQLUnderlyingVolatilityEstimator(metaclass=abc.ABCMeta):
    """
    Defines QuantLib underlying volatility estimator for option pricing model. User may define his own estimators,
    including those forward and backward looking ones.
    """


class IQLRiskFreeRateEstimator(metaclass=abc.ABCMeta):
    """Defines QuantLib risk free rate estimator for option pricing model."""


class QLOptionPriceModel(System.Object, QuantConnect.Securities.Option.IOptionPriceModel):
    """Provides QuantLib(QL) implementation of IOptionPriceModel to support major option pricing models, available in QL."""

    @property
    def EnableGreekApproximation(self) -> bool:
        """
        When enabled, approximates Greeks if corresponding pricing model didn't calculate exact numbers.
        The default value is true.
        """
        ...

    @property
    def VolatilityEstimatorWarmedUp(self) -> bool:
        """True if volatility model is warmed up, i.e. has generated volatility value different from zero, otherwise false."""
        ...

    @property
    def AllowedOptionStyles(self) -> System.Collections.Generic.IReadOnlyCollection[QuantConnect.OptionStyle]:
        """
        List of option styles supported by the pricing model.
        By default, both American and European option styles are supported.
        """
        ...

    @overload
    def __init__(self, pricingEngineFunc: typing.Callable[[GeneralizedBlackScholesProcess], IPricingEngine], underlyingVolEstimator: QuantConnect.Securities.Option.IQLUnderlyingVolatilityEstimator = None, riskFreeRateEstimator: QuantConnect.Securities.Option.IQLRiskFreeRateEstimator = None, dividendYieldEstimator: QuantConnect.Securities.Option.IQLDividendYieldEstimator = None, allowedOptionStyles: typing.List[QuantConnect.OptionStyle] = None) -> None:
        """
        Method constructs QuantLib option price model with necessary estimators of underlying volatility, risk free rate, and underlying dividend yield
        
        :param pricingEngineFunc: Function modeled stochastic process, and returns new pricing engine to run calculations for that option
        :param underlyingVolEstimator: The underlying volatility estimator
        :param riskFreeRateEstimator: The risk free rate estimator
        :param dividendYieldEstimator: The underlying dividend yield estimator
        :param allowedOptionStyles: List of option styles supported by the pricing model. It defaults to both American and European option styles
        """
        ...

    @overload
    def __init__(self, pricingEngineFunc: typing.Callable[[QuantConnect.Symbol, GeneralizedBlackScholesProcess], IPricingEngine], underlyingVolEstimator: QuantConnect.Securities.Option.IQLUnderlyingVolatilityEstimator = None, riskFreeRateEstimator: QuantConnect.Securities.Option.IQLRiskFreeRateEstimator = None, dividendYieldEstimator: QuantConnect.Securities.Option.IQLDividendYieldEstimator = None, allowedOptionStyles: typing.List[QuantConnect.OptionStyle] = None) -> None:
        """
        Method constructs QuantLib option price model with necessary estimators of underlying volatility, risk free rate, and underlying dividend yield
        
        :param pricingEngineFunc: Function takes option and modeled stochastic process, and returns new pricing engine to run calculations for that option
        :param underlyingVolEstimator: The underlying volatility estimator
        :param riskFreeRateEstimator: The risk free rate estimator
        :param dividendYieldEstimator: The underlying dividend yield estimator
        :param allowedOptionStyles: List of option styles supported by the pricing model. It defaults to both American and European option styles
        """
        ...

    def Evaluate(self, security: QuantConnect.Securities.Security, slice: QuantConnect.Data.Slice, contract: QuantConnect.Data.Market.OptionContract) -> QuantConnect.Securities.Option.OptionPriceModelResult:
        """
        Evaluates the specified option contract to compute a theoretical price, IV and greeks
        
        :param security: The option security object
        :param slice: The current data slice. This can be used to access other information available to the algorithm
        :param contract: The option contract to evaluate
        :returns: An instance of OptionPriceModelResult containing the theoretical price of the specified option contract.
        """
        ...

    def ImpliedVolatilityEstimation(self, price: float, initialGuess: float, timeTillExpiry: float, riskFreeDiscount: float, forwardPrice: float, payoff: typing.Any, black: typing.Optional[typing.Any]) -> typing.Union[float, typing.Any]:
        """
        An implied volatility approximation by Newton-Raphson method. Return 0 if result is not converged
        
        This method is protected.
        
        :param price: current price of the option
        :param initialGuess: initial guess of the IV
        :param timeTillExpiry: time till option contract expiry
        :param riskFreeDiscount: risk free rate discount factor
        :param forwardPrice: future value of underlying price
        :param payoff: payoff structure of the option contract
        :param black: black calculator instance
        :returns: implied volatility estimation.
        """
        ...


class OptionPriceModels(System.Object):
    """Static class contains definitions of major option pricing models that can be used in LEAN"""

    @staticmethod
    def AdditiveEquiprobabilities() -> QuantConnect.Securities.Option.IOptionPriceModel:
        """
        Pricing engine for European and American vanilla options using binomial trees. Additive Equiprobabilities model.
        QuantLib reference: http://quantlib.org/reference/class_quant_lib_1_1_f_d_european_engine.html
        
        :returns: New option price model instance.
        """
        ...

    @staticmethod
    def BaroneAdesiWhaley() -> QuantConnect.Securities.Option.IOptionPriceModel:
        """
        Barone-Adesi and Whaley pricing engine for American options (1987)
        QuantLib reference: http://quantlib.org/reference/class_quant_lib_1_1_barone_adesi_whaley_approximation_engine.html
        
        :returns: New option price model instance.
        """
        ...

    @staticmethod
    def BinomialCoxRossRubinstein() -> QuantConnect.Securities.Option.IOptionPriceModel:
        """
        Pricing engine for European and American vanilla options using binomial trees. Cox-Ross-Rubinstein(CRR) model.
        QuantLib reference: http://quantlib.org/reference/class_quant_lib_1_1_f_d_european_engine.html
        
        :returns: New option price model instance.
        """
        ...

    @staticmethod
    def BinomialJarrowRudd() -> QuantConnect.Securities.Option.IOptionPriceModel:
        """
        Pricing engine for European and American vanilla options using binomial trees. Jarrow-Rudd model.
        QuantLib reference: http://quantlib.org/reference/class_quant_lib_1_1_f_d_european_engine.html
        
        :returns: New option price model instance.
        """
        ...

    @staticmethod
    def BinomialJoshi() -> QuantConnect.Securities.Option.IOptionPriceModel:
        """
        Pricing engine for European and American vanilla options using binomial trees. Joshi model.
        QuantLib reference: http://quantlib.org/reference/class_quant_lib_1_1_f_d_european_engine.html
        
        :returns: New option price model instance.
        """
        ...

    @staticmethod
    def BinomialLeisenReimer() -> QuantConnect.Securities.Option.IOptionPriceModel:
        """
        Pricing engine for European and American vanilla options using binomial trees. Leisen-Reimer model.
        QuantLib reference: http://quantlib.org/reference/class_quant_lib_1_1_f_d_european_engine.html
        
        :returns: New option price model instance.
        """
        ...

    @staticmethod
    def BinomialTian() -> QuantConnect.Securities.Option.IOptionPriceModel:
        """
        Pricing engine for European and American vanilla options using binomial trees. Tian model.
        QuantLib reference: http://quantlib.org/reference/class_quant_lib_1_1_f_d_european_engine.html
        
        :returns: New option price model instance.
        """
        ...

    @staticmethod
    def BinomialTrigeorgis() -> QuantConnect.Securities.Option.IOptionPriceModel:
        """
        Pricing engine for European and American vanilla options using binomial trees. Trigeorgis model.
        QuantLib reference: http://quantlib.org/reference/class_quant_lib_1_1_f_d_european_engine.html
        
        :returns: New option price model instance.
        """
        ...

    @staticmethod
    def BjerksundStensland() -> QuantConnect.Securities.Option.IOptionPriceModel:
        """
        Bjerksund and Stensland pricing engine for American options (1993)
        QuantLib reference: http://quantlib.org/reference/class_quant_lib_1_1_bjerksund_stensland_approximation_engine.html
        
        :returns: New option price model instance.
        """
        ...

    @staticmethod
    def BlackScholes() -> QuantConnect.Securities.Option.IOptionPriceModel:
        """
        Pricing engine for European vanilla options using analytical formula.
        QuantLib reference: http://quantlib.org/reference/class_quant_lib_1_1_analytic_european_engine.html
        
        :returns: New option price model instance.
        """
        ...

    @staticmethod
    def CrankNicolsonFD() -> QuantConnect.Securities.Option.IOptionPriceModel:
        """
        Pricing engine for European and American options using finite-differences.
        QuantLib reference: http://quantlib.org/reference/class_quant_lib_1_1_f_d_european_engine.html
        
        :returns: New option price model instance.
        """
        ...

    @staticmethod
    def Create(priceEngineName: str, riskFree: float, allowedOptionStyles: typing.List[QuantConnect.OptionStyle] = None) -> QuantConnect.Securities.Option.IOptionPriceModel:
        """
        Creates pricing engine by engine type name.
        
        :param priceEngineName: QL price engine name
        :param riskFree: The risk free rate
        :param allowedOptionStyles: List of option styles supported by the pricing model. It defaults to both American and European option styles
        :returns: New option price model instance of specific engine.
        """
        ...

    @staticmethod
    def Integral() -> QuantConnect.Securities.Option.IOptionPriceModel:
        """
        Pricing engine for European vanilla options using integral approach.
        QuantLib reference: http://quantlib.org/reference/class_quant_lib_1_1_integral_engine.html
        
        :returns: New option price model instance.
        """
        ...


class OptionStrategyPositionGroupBuyingPowerModel(QuantConnect.Securities.Positions.PositionGroupBuyingPowerModel):
    """Option strategy buying power model"""

    def __init__(self, optionStrategy: QuantConnect.Securities.Option.OptionStrategy) -> None:
        """
        Creates a new instance for a target option strategy
        
        :param optionStrategy: The option strategy to model
        """
        ...

    def GetContemplatedGroupsInitialMargin(self, portfolio: QuantConnect.Securities.SecurityPortfolioManager, contemplatedGroups: QuantConnect.Securities.Positions.PositionGroupCollection, ordersPositions: System.Collections.Generic.List[QuantConnect.Securities.Positions.IPosition]) -> float:
        """
        Gets the initial margin required for the specified contemplated position group.
        Used by GetReservedBuyingPowerImpact to get the contemplated groups margin.
        
        This method is protected.
        """
        ...

    def GetInitialMarginRequiredForOrder(self, parameters: QuantConnect.Securities.Positions.PositionGroupInitialMarginForOrderParameters) -> QuantConnect.Securities.InitialMargin:
        """
        Gets the total margin required to execute the specified order in units of the account currency including fees
        
        :param parameters: An object containing the portfolio, the security and the order
        :returns: The total margin in terms of the currency quoted in the order.
        """
        ...

    def GetInitialMarginRequirement(self, parameters: QuantConnect.Securities.Positions.PositionGroupInitialMarginParameters) -> QuantConnect.Securities.InitialMargin:
        """
        The margin that must be held in order to increase the position by the provided quantity
        
        :param parameters: An object containing the security and quantity
        """
        ...

    def GetMaintenanceMargin(self, parameters: QuantConnect.Securities.Positions.PositionGroupMaintenanceMarginParameters) -> QuantConnect.Securities.MaintenanceMargin:
        """
        Gets the margin currently allocated to the specified holding
        
        :param parameters: An object containing the security
        :returns: The maintenance margin required for the.
        """
        ...

    def ToString(self) -> str:
        """
        Returns a string that represents the current object.
        
        :returns: A string that represents the current object.
        """
        ...


class OptionMarginModel(QuantConnect.Securities.SecurityMarginModel):
    """Represents a simple option margin model."""

    def __init__(self, requiredFreeBuyingPowerPercent: float = 0) -> None:
        """
        Initializes a new instance of the OptionMarginModel
        
        :param requiredFreeBuyingPowerPercent: The percentage used to determine the required unused buying power for the account.
        """
        ...

    def GetInitialMarginRequiredForOrder(self, parameters: QuantConnect.Securities.InitialMarginRequiredForOrderParameters) -> QuantConnect.Securities.InitialMargin:
        """
        Gets the total margin required to execute the specified order in units of the account currency including fees
        
        :param parameters: An object containing the portfolio, the security and the order
        :returns: The total margin in terms of the currency quoted in the order.
        """
        ...

    def GetInitialMarginRequirement(self, parameters: QuantConnect.Securities.InitialMarginParameters) -> QuantConnect.Securities.InitialMargin:
        """
        The margin that must be held in order to increase the position by the provided quantity
        
        :returns: The initial margin required for the provided security and quantity.
        """
        ...

    def GetLeverage(self, security: QuantConnect.Securities.Security) -> float:
        """
        Gets the current leverage of the security
        
        :param security: The security to get leverage for
        :returns: The current leverage in the security.
        """
        ...

    def GetMaintenanceMargin(self, parameters: QuantConnect.Securities.MaintenanceMarginParameters) -> QuantConnect.Securities.MaintenanceMargin:
        """
        Gets the margin currently alloted to the specified holding
        
        :param parameters: An object containing the security
        :returns: The maintenance margin required for the provided holdings quantity/cost/value.
        """
        ...

    def SetLeverage(self, security: QuantConnect.Securities.Security, leverage: float) -> None:
        """
        Sets the leverage for the applicable securities, i.e, options.
        
        :param leverage: The new leverage
        """
        ...


class CurrentPriceOptionPriceModel(System.Object, QuantConnect.Securities.Option.IOptionPriceModel):
    """
    Provides a default implementation of IOptionPriceModel that does not compute any
    greeks and uses the current price for the theoretical price.
    This is a stub implementation until the real models are implemented
    """

    def Evaluate(self, security: QuantConnect.Securities.Security, slice: QuantConnect.Data.Slice, contract: QuantConnect.Data.Market.OptionContract) -> QuantConnect.Securities.Option.OptionPriceModelResult:
        """
        Creates a new OptionPriceModelResult containing the current Security.Price
        and a default, empty instance of first Order Greeks
        
        :param security: The option security object
        :param slice: The current data slice. This can be used to access other information available to the algorithm
        :param contract: The option contract to evaluate
        :returns: An instance of OptionPriceModelResult containing the theoretical price of the specified option contract.
        """
        ...


class FedRateQLRiskFreeRateEstimator(System.Object, QuantConnect.Securities.Option.IQLRiskFreeRateEstimator):
    """Class implements Fed's US primary credit rate as risk free rate, implementing IQLRiskFreeRateEstimator."""

    def Estimate(self, security: QuantConnect.Securities.Security, slice: QuantConnect.Data.Slice, contract: QuantConnect.Data.Market.OptionContract) -> float:
        """
        Returns current flat estimate of the risk free rate
        
        :param security: The option security object
        :param slice: The current data slice. This can be used to access other information available to the algorithm
        :param contract: The option contract to evaluate
        :returns: The estimate.
        """
        ...


class DefaultOptionAssignmentModel(System.Object, QuantConnect.Securities.Option.IOptionAssignmentModel):
    """
    The option assignment model emulates exercising of short option positions in the portfolio.
    Simulator implements basic no-arb argument: when time value of the option contract is close to zero
    it assigns short legs getting profit close to expiration dates in deep ITM positions. User algorithm then receives
    assignment event from LEAN. Simulator randomly scans for arbitrage opportunities every two hours or so.
    """

    def __init__(self, requiredInTheMoneyPercent: float = 0.05, priorExpiration: typing.Optional[datetime.timedelta] = None) -> None:
        """
        Creates a new instance
        
        :param requiredInTheMoneyPercent: The percent in the money the option has to be to trigger the option assignment
        :param priorExpiration: For OptionStyle.American, the time span prior to expiration were we will try to evaluate option assignment
        """
        ...

    def GetAssignment(self, parameters: QuantConnect.Securities.Option.OptionAssignmentParameters) -> QuantConnect.Securities.Option.OptionAssignmentResult:
        """
        Get's the option assignments to generate if any
        
        :param parameters: The option assignment parameters data transfer class
        :returns: The option assignment result.
        """
        ...


class ConstantQLRiskFreeRateEstimator(System.Object, QuantConnect.Securities.Option.IQLRiskFreeRateEstimator):
    """Class implements default flat risk free curve, implementing IQLRiskFreeRateEstimator."""

    def __init__(self, riskFreeRate: float = 0.01) -> None:
        """Constructor initializes class with risk free rate constant"""
        ...

    def Estimate(self, security: QuantConnect.Securities.Security, slice: QuantConnect.Data.Slice, contract: QuantConnect.Data.Market.OptionContract) -> float:
        """
        Returns current flat estimate of the risk free rate
        
        :param security: The option security object
        :param slice: The current data slice. This can be used to access other information available to the algorithm
        :param contract: The option contract to evaluate
        :returns: The estimate.
        """
        ...


class OptionHolding(QuantConnect.Securities.SecurityHolding):
    """Option holdings implementation of the base securities class"""

    def __init__(self, security: QuantConnect.Securities.Option.Option, currencyConverter: QuantConnect.Securities.ICurrencyConverter) -> None:
        """
        Option Holding Class constructor
        
        :param security: The option security being held
        :param currencyConverter: A currency converter instance
        """
        ...


class ConstantQLUnderlyingVolatilityEstimator(System.Object, QuantConnect.Securities.Option.IQLUnderlyingVolatilityEstimator):
    """
    Class implements default underlying constant volatility estimator (IQLUnderlyingVolatilityEstimator.), that projects the underlying own volatility
    model into corresponding option pricing model.
    """

    @property
    def IsReady(self) -> bool:
        """Indicates whether volatility model has been warmed ot not"""
        ...

    def Estimate(self, security: QuantConnect.Securities.Security, slice: QuantConnect.Data.Slice, contract: QuantConnect.Data.Market.OptionContract) -> float:
        """
        Returns current estimate of the underlying volatility
        
        :param security: The option security object
        :param slice: The current data slice. This can be used to access other information available to the algorithm
        :param contract: The option contract to evaluate
        :returns: The estimate.
        """
        ...


class OptionDataFilter(QuantConnect.Securities.SecurityDataFilter):
    """Option packet by packet data filtering mechanism for dynamically detecting bad ticks."""


class FuturesOptionsMarginModel(QuantConnect.Securities.Future.FutureMarginModel):
    """
    Defines a margin model for future options (an option with a future as its underlying).
    We re-use the FutureMarginModel implementation and multiply its results
    by 1.5x to simulate the increased margins seen for future options.
    """

    @property
    def InitialOvernightMarginRequirement(self) -> float:
        """Initial Overnight margin requirement for the contract effective from the date of change"""
        ...

    @property
    def MaintenanceOvernightMarginRequirement(self) -> float:
        """Maintenance Overnight margin requirement for the contract effective from the date of change"""
        ...

    @property
    def InitialIntradayMarginRequirement(self) -> float:
        """Initial Intraday margin for the contract effective from the date of change"""
        ...

    @property
    def MaintenanceIntradayMarginRequirement(self) -> float:
        """Maintenance Intraday margin requirement for the contract effective from the date of change"""
        ...

    def __init__(self, requiredFreeBuyingPowerPercent: float = 0, futureOption: QuantConnect.Securities.Option.Option = None) -> None:
        """
        Creates an instance of FutureOptionMarginModel
        
        :param requiredFreeBuyingPowerPercent: The percentage used to determine the required unused buying power for the account.
        :param futureOption: Option Security containing a Future security as the underlying
        """
        ...

    def GetInitialMarginRequirement(self, parameters: QuantConnect.Securities.InitialMarginParameters) -> QuantConnect.Securities.InitialMargin:
        """
        The margin that must be held in order to increase the position by the provided quantity
        
        :param parameters: An object containing the security and quantity of shares
        :returns: The initial margin required for the option (i.e. the equity required to enter a position for this option).
        """
        ...

    def GetMaintenanceMargin(self, parameters: QuantConnect.Securities.MaintenanceMarginParameters) -> QuantConnect.Securities.MaintenanceMargin:
        """
        Gets the margin currently alloted to the specified holding.
        
        :param parameters: An object containing the security
        :returns: The maintenance margin required for the option.
        """
        ...

    @staticmethod
    def GetMarginRequirement(option: QuantConnect.Securities.Option.Option, underlyingRequirement: float, positionSide: QuantConnect.PositionSide = ...) -> int:
        """
        Get's the margin requirement for a future option based on the underlying future margin requirement and the position side to trade.
        FOPs margin requirement is an 'S' curve based on the underlying requirement around it's current price, see https://en.wikipedia.org/wiki/Logistic_function
        
        :param option: The future option contract to trade
        :param underlyingRequirement: The underlying future associated margin requirement
        :param positionSide: The position side to trade, long by default. This is because short positions require higher margin requirements
        """
        ...



from typing import overload
import abc
import datetime
import typing

import QuantConnect
import QuantConnect.Interfaces
import QuantConnect.Lean.Engine.DataFeeds
import QuantConnect.Lean.Engine.RealTime
import QuantConnect.Lean.Engine.Results
import QuantConnect.Lean.Engine.Setup
import QuantConnect.Lean.Engine.TransactionHandlers
import QuantConnect.Packets
import QuantConnect.Util
import System
import System.Collections.Generic


class AlgorithmSetupException(System.Exception):
    """Defines an exception generated in the course of invoking ISetupHandler.Setup"""

    @overload
    def __init__(self, message: str) -> None:
        """
        Initializes a new instance of the AlgorithmSetupException class
        
        :param message: The error message
        """
        ...

    @overload
    def __init__(self, message: str, inner: System.Exception) -> None:
        """
        Initializes a new instance of the AlgorithmSetupException class
        
        :param message: The error message
        :param inner: The inner exception being wrapped
        """
        ...


class SetupHandlerParameters(System.Object):
    """Defines the parameters for ISetupHandler"""

    @property
    def UniverseSelection(self) -> QuantConnect.Lean.Engine.DataFeeds.UniverseSelection:
        """Gets the universe selection"""
        ...

    @property
    def Algorithm(self) -> QuantConnect.Interfaces.IAlgorithm:
        """Gets the algorithm"""
        ...

    @property
    def Brokerage(self) -> QuantConnect.Interfaces.IBrokerage:
        """Gets the Brokerage"""
        ...

    @property
    def AlgorithmNodePacket(self) -> QuantConnect.Packets.AlgorithmNodePacket:
        """Gets the algorithm node packet"""
        ...

    @property
    def ResultHandler(self) -> QuantConnect.Lean.Engine.Results.IResultHandler:
        """Gets the algorithm node packet"""
        ...

    @property
    def TransactionHandler(self) -> QuantConnect.Lean.Engine.TransactionHandlers.ITransactionHandler:
        """Gets the TransactionHandler"""
        ...

    @property
    def RealTimeHandler(self) -> QuantConnect.Lean.Engine.RealTime.IRealTimeHandler:
        """Gets the RealTimeHandler"""
        ...

    @property
    def DataCacheProvider(self) -> QuantConnect.Interfaces.IDataCacheProvider:
        """Gets the DataCacheProvider"""
        ...

    @property
    def MapFileProvider(self) -> QuantConnect.Interfaces.IMapFileProvider:
        """The map file provider instance of the algorithm"""
        ...

    def __init__(self, universeSelection: QuantConnect.Lean.Engine.DataFeeds.UniverseSelection, algorithm: QuantConnect.Interfaces.IAlgorithm, brokerage: QuantConnect.Interfaces.IBrokerage, algorithmNodePacket: QuantConnect.Packets.AlgorithmNodePacket, resultHandler: QuantConnect.Lean.Engine.Results.IResultHandler, transactionHandler: QuantConnect.Lean.Engine.TransactionHandlers.ITransactionHandler, realTimeHandler: QuantConnect.Lean.Engine.RealTime.IRealTimeHandler, dataCacheProvider: QuantConnect.Interfaces.IDataCacheProvider, mapFileProvider: QuantConnect.Interfaces.IMapFileProvider) -> None:
        """
        Creates a new instance
        
        :param universeSelection: The universe selection instance
        :param algorithm: Algorithm instance
        :param brokerage: New brokerage output instance
        :param algorithmNodePacket: Algorithm job task
        :param resultHandler: The configured result handler
        :param transactionHandler: The configured transaction handler
        :param realTimeHandler: The configured real time handler
        :param dataCacheProvider: The configured data cache provider
        :param mapFileProvider: The map file provider
        """
        ...


class ISetupHandler(System.IDisposable, metaclass=abc.ABCMeta):
    """Interface to setup the algorithm. Pass in a raw algorithm, return one with portfolio, cash, etc already preset."""


class BaseSetupHandler(System.Object):
    """
    Base class that provides shared code for
    the ISetupHandler implementations
    """

    AlgorithmCreationTimeout: datetime.timedelta
    """Get the maximum time that the creation of an algorithm can take"""

    @staticmethod
    def GetConfiguredDataFeeds() -> System.Collections.Generic.Dictionary[QuantConnect.SecurityType, System.Collections.Generic.List[QuantConnect.TickType]]:
        """Get the available data feeds from config.json,"""
        ...

    @staticmethod
    def InitializeDebugging(algorithmNodePacket: QuantConnect.Packets.AlgorithmNodePacket, workerThread: QuantConnect.Util.WorkerThread) -> bool:
        """
        Initialize the debugger
        
        :param algorithmNodePacket: The algorithm node packet
        :param workerThread: The worker thread instance to use
        """
        ...

    @staticmethod
    def LoadBacktestJobAccountCurrency(algorithm: QuantConnect.Interfaces.IAlgorithm, job: QuantConnect.Packets.BacktestNodePacket) -> None:
        """Sets the account currency the algorithm should use if set in the job packet"""
        ...

    @staticmethod
    def LoadBacktestJobCashAmount(algorithm: QuantConnect.Interfaces.IAlgorithm, job: QuantConnect.Packets.BacktestNodePacket) -> None:
        """Sets the initial cash for the algorithm if set in the job packet."""
        ...

    @staticmethod
    def SetBrokerageTradingDayPerYear(algorithm: QuantConnect.Interfaces.IAlgorithm) -> None:
        """
        Set the number of trading days per year based on the specified brokerage model.
        
        :param algorithm: The algorithm instance
        :returns: The number of trading days per year. For specific brokerages (Coinbase, Binance, Bitfinex, Bybit, FTX, Kraken), the value is 365. For other brokerages, the default value is 252.
        """
        ...

    @staticmethod
    def SetupCurrencyConversions(algorithm: QuantConnect.Interfaces.IAlgorithm, universeSelection: QuantConnect.Lean.Engine.DataFeeds.UniverseSelection) -> None:
        """
        Will first check and add all the required conversion rate securities
        and later will seed an initial value to them.
        
        :param algorithm: The algorithm instance
        :param universeSelection: The universe selection instance
        """
        ...


class BrokerageSetupHandler(System.Object, QuantConnect.Lean.Engine.Setup.ISetupHandler):
    """Defines a set up handler that initializes the algorithm instance using values retrieved from the user's brokerage account"""

    MaxAllocationLimitConfig: str = "max-allocation-limit"
    """Max allocation limit configuration variable name"""

    @property
    def WorkerThread(self) -> QuantConnect.Util.WorkerThread:
        """The worker thread instance the setup handler should use"""
        ...

    @property
    def Errors(self) -> System.Collections.Generic.List[System.Exception]:
        """Any errors from the initialization stored here:"""
        ...

    @property
    def MaximumRuntime(self) -> datetime.timedelta:
        """Get the maximum runtime for this algorithm job."""
        ...

    @property
    def StartingPortfolioValue(self) -> float:
        """Algorithm starting capital for statistics calculations"""
        ...

    @property
    def StartingDate(self) -> datetime.datetime:
        """Start date for analysis loops to search for data."""
        ...

    @property
    def MaxOrders(self) -> int:
        """Maximum number of orders for the algorithm run -- applicable for backtests only."""
        ...

    def __init__(self) -> None:
        """Initializes a new BrokerageSetupHandler"""
        ...

    def CreateAlgorithmInstance(self, algorithmNodePacket: QuantConnect.Packets.AlgorithmNodePacket, assemblyPath: str) -> QuantConnect.Interfaces.IAlgorithm:
        """
        Create a new instance of an algorithm from a physical dll path.
        
        :param algorithmNodePacket: Details of the task required
        :param assemblyPath: The path to the assembly's location
        :returns: A new instance of IAlgorithm, or throws an exception if there was an error.
        """
        ...

    def CreateBrokerage(self, algorithmNodePacket: QuantConnect.Packets.AlgorithmNodePacket, uninitializedAlgorithm: QuantConnect.Interfaces.IAlgorithm, factory: typing.Optional[QuantConnect.Interfaces.IBrokerageFactory]) -> typing.Union[QuantConnect.Interfaces.IBrokerage, QuantConnect.Interfaces.IBrokerageFactory]:
        """
        Creates the brokerage as specified by the job packet
        
        :param algorithmNodePacket: Job packet
        :param uninitializedAlgorithm: The algorithm instance before Initialize has been called
        :param factory: The brokerage factory
        :returns: The brokerage instance, or throws if error creating instance.
        """
        ...

    def Dispose(self) -> None:
        """Performs application-defined tasks associated with freeing, releasing, or resetting unmanaged resources."""
        ...

    def GetOpenOrders(self, algorithm: QuantConnect.Interfaces.IAlgorithm, resultHandler: QuantConnect.Lean.Engine.Results.IResultHandler, transactionHandler: QuantConnect.Lean.Engine.TransactionHandlers.ITransactionHandler, brokerage: QuantConnect.Interfaces.IBrokerage) -> None:
        """
        Get the open orders from a brokerage. Adds Orders.Order and Orders.OrderTicket to the transaction handler
        
        This method is protected.
        
        :param algorithm: Algorithm instance
        :param resultHandler: The configured result handler
        :param transactionHandler: The configurated transaction handler
        :param brokerage: Brokerage output instance
        """
        ...

    def LoadExistingHoldingsAndOrders(self, brokerage: QuantConnect.Interfaces.IBrokerage, algorithm: QuantConnect.Interfaces.IAlgorithm, parameters: QuantConnect.Lean.Engine.Setup.SetupHandlerParameters) -> bool:
        """This method is protected."""
        ...

    def Setup(self, parameters: QuantConnect.Lean.Engine.Setup.SetupHandlerParameters) -> bool:
        """
        Primary entry point to setup a new algorithm
        
        :param parameters: The parameters object to use
        :returns: True on successfully setting up the algorithm state, or false on error.
        """
        ...


class BacktestingSetupHandler(System.Object, QuantConnect.Lean.Engine.Setup.ISetupHandler):
    """Backtesting setup handler processes the algorithm initialize method and sets up the internal state of the algorithm class."""

    @property
    def WorkerThread(self) -> QuantConnect.Util.WorkerThread:
        """The worker thread instance the setup handler should use"""
        ...

    @property
    def Errors(self) -> System.Collections.Generic.List[System.Exception]:
        """Internal errors list from running the setup procedures."""
        ...

    @property
    def MaximumRuntime(self) -> datetime.timedelta:
        """Maximum runtime of the algorithm in seconds."""
        ...

    @property
    def StartingPortfolioValue(self) -> float:
        """Starting capital according to the users initialize routine."""
        ...

    @property
    def StartingDate(self) -> datetime.datetime:
        """Start date for analysis loops to search for data."""
        ...

    @property
    def MaxOrders(self) -> int:
        """Maximum number of orders for this backtest."""
        ...

    def __init__(self) -> None:
        """Initialize the backtest setup handler."""
        ...

    def CreateAlgorithmInstance(self, algorithmNodePacket: QuantConnect.Packets.AlgorithmNodePacket, assemblyPath: str) -> QuantConnect.Interfaces.IAlgorithm:
        """
        Create a new instance of an algorithm from a physical dll path.
        
        :param algorithmNodePacket: Details of the task required
        :param assemblyPath: The path to the assembly's location
        :returns: A new instance of IAlgorithm, or throws an exception if there was an error.
        """
        ...

    def CreateBrokerage(self, algorithmNodePacket: QuantConnect.Packets.AlgorithmNodePacket, uninitializedAlgorithm: QuantConnect.Interfaces.IAlgorithm, factory: typing.Optional[QuantConnect.Interfaces.IBrokerageFactory]) -> typing.Union[QuantConnect.Interfaces.IBrokerage, QuantConnect.Interfaces.IBrokerageFactory]:
        """
        Creates a new BacktestingBrokerage instance
        
        :param algorithmNodePacket: Job packet
        :param uninitializedAlgorithm: The algorithm instance before Initialize has been called
        :param factory: The brokerage factory
        :returns: The brokerage instance, or throws if error creating instance.
        """
        ...

    def Dispose(self) -> None:
        """Performs application-defined tasks associated with freeing, releasing, or resetting unmanaged resources."""
        ...

    def Setup(self, parameters: QuantConnect.Lean.Engine.Setup.SetupHandlerParameters) -> bool:
        """
        Setup the algorithm cash, dates and data subscriptions as desired.
        
        :param parameters: The parameters object to use
        :returns: Boolean true on successfully initializing the algorithm.
        """
        ...


class ConsoleSetupHandler(QuantConnect.Lean.Engine.Setup.BacktestingSetupHandler):
    """
    Kept for backwards compatibility-
    
    Should use BacktestingSetupHandler instead
    """



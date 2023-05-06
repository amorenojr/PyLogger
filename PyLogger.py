from datetime import datetime
from enum import Enum, auto
from pathlib import Path
from os import remove

class EnumLogLevel(Enum):
    """
    Enumerated type representing the log level.
    """

    Info = auto()
    """Info Level"""

    Debug = auto()
    """Info Level"""

    Warning = auto()
    """Warning Level"""

    Error = auto()
    """Error Level"""

    Critical = auto()
    """Critical Level"""

    Verbose = auto()
    """Verbose Level"""

class PyLogger:

    @property
    def LogFilePath(self) -> Path:
        """Log file path."""
        return self.__LogFilePath

    @LogFilePath.setter
    def LogFilePath(self, value: Path):
        self.__LogFilePath = value

    # https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal#answer-21786287
    LogLevelColorMap = [["\x1b[1;37;40m","\x1b[0m"], # Info
                        ["\x1b[1;32;40m","\x1b[0m"], # Debug
                        ["\x1b[1;33;40m","\x1b[0m"], # Warning
                        ["\x1b[1;31;40m","\x1b[0m"], # Error
                        ["\x1b[5;30;41m","\x1b[0m"], # Critical
                        ["\x1b[1;34;40m","\x1b[0m"]] # Verbose


    def __init__(self, logFilePath: str | Path) -> None:
        self.LogFilePath = Path(logFilePath) if isinstance(logFilePath, str) else logFilePath
        if self.LogFilePath.exists():
            remove(str(self.LogFilePath))
        self.__Queue = []
        self.LogStartTime = datetime.now()
        self.RecordStartTime = self.LogStartTime
        self.Info("Log Started.")

    def __del__(self):
        self.Info("Log Ended (Total run-time {TotalRunTime}).".format(TotalRunTime = datetime.now() - self.LogStartTime))

    def __AppendLog(self, msg: str, printOut: bool, logLevel: EnumLogLevel, report: bool = True):

        self.__Queue.append("{LogMsg}".format(LogMsg = msg))

        if report:
            self.RecordEndTime = datetime.now()
            self.ElapsedTime = self.RecordEndTime - self.RecordStartTime
            ElapsedTimeStr = datetime.utcfromtimestamp(self.ElapsedTime.total_seconds()).strftime("%H:%M:%S.%f")
            self.__Queue.insert(0, "{TimeStamp} ({ElapsedTime}) {LogLevel}: ".format(TimeStamp = self.RecordEndTime.strftime('%Y-%m-%d %H:%M:%S'),
                                                                                    LogLevel = self.__GetLevelStr(logLevel),
                                                                                    ElapsedTime = ElapsedTimeStr))
            logMsg = "".join(self.__Queue)
            with open(self.LogFilePath, "a", encoding="utf-8") as file:
                file.writelines(logMsg + "\n")
            self.__Queue.clear()
            self.RecordStartTime = self.RecordEndTime
        
        if printOut:
            ColorPrefix = self.LogLevelColorMap[logLevel.value][0]
            ColorSuffix = self.LogLevelColorMap[logLevel.value][1]
            print("{ColorPrefix}{msg}{ColorSuffix}".format(ColorPrefix = ColorPrefix, msg = msg, ColorSuffix = ColorSuffix), end = ("\n" if report else ""))


    def __GetLevelStr(self, logLevel: EnumLogLevel) -> str:
        match logLevel:
            case EnumLogLevel.Info:
                return "[I]"
            case EnumLogLevel.Debug:
                return "[D]"
            case EnumLogLevel.Warning:
                return "[W]"
            case EnumLogLevel.Error:
                return "[E]"
            case EnumLogLevel.Critical:
                return "[C]"
            case EnumLogLevel.Verbose:
                return "[V]"
            case _:
                return None


    def Info(self, msg: str, report: bool = True, printOut: bool = True):
        self.__AppendLog(msg, printOut, EnumLogLevel.Info, report)


    def Debug(self, msg: str, report: bool = True, printOut: bool = True):
        self.__AppendLog(msg, printOut, EnumLogLevel.Debug, report)


    def Warning(self, msg: str, report: bool = True, printOut: bool = True):
        self.__AppendLog(msg, printOut, EnumLogLevel.Warning, report)


    def Error(self, msg: str, report: bool = True, printOut: bool = True):
        self.__AppendLog(msg, printOut, EnumLogLevel.Error, report)


    def Critical(self, msg: str, report: bool = True, printOut: bool = True):
        self.__AppendLog(msg, printOut, EnumLogLevel.Critical, report)


    def Verbose(self, msg: str, report: bool = True, printOut: bool = True):
        self.__AppendLog(msg, printOut, EnumLogLevel.Verbose, report)

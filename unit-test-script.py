from PyLogger import PyLogger
import os

LogFilePath = os.path.basename(__file__).replace(".py", ".log")

logger = PyLogger(LogFilePath)

logger.Info("This is an info log.")
logger.Debug("This is an debug log.")
logger.Warning("This is an warning log.")
logger.Error("This is an error log.")
logger.Critical("This is an critical log.")
logger.Verbose("This is an verbose log.")

logger = None
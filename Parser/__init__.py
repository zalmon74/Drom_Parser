from pathlib import Path
import sys

from .Parser import DromParser
from .Errors import Errors
import GET_Parameters as getparameters
import Output_Parameters as outputparameters
import Settings as settingparameters
import ConstantsUrls


# Добавляем в путь сбора модуль с параметрами
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))



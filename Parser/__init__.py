from pathlib import Path
import sys

from .Parser import DromParser
import GET_Parameters as getparameters

# Добавляем в путь сбора модуль с параметрами
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))





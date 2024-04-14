# these lines below make sure the package user doesn't have to import the package as 
# `from classifyspectraltype.fetch_exoplanet_data import fetch_data` but rather 
# `from classifyspectraltype import fetch_data etc.`

from src.classifyspectraltype.boxplot_table_function import make_boxplot_and_table # ignore
from src.classifyspectraltype.clean_confidence_intervals import clean_confidence_intervals # ignore
from src.classifyspectraltype.fetch_exoplanet_dataset import fetch_data # ignore
from src.classifyspectraltype.split_cross_val import split_cross_val # ignore
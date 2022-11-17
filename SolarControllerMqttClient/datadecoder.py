from io import StringIO

import config
import log
import pandas as pd

logger = log.get_module_logger("datadecoder")


def decode(csvString):
    logger.debug("Decoding data")
    result = {}
    csvStringIO = StringIO(config.csvheader + "\n" + csvString)
    df = pd.read_csv(csvStringIO, sep="\t")
    for column in df:
        name = df[column].name
        val = df[column].values[0]
        result[name] = val
    return result
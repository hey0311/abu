# 基础库导入

from __future__ import print_function
from __future__ import division

import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib inline

import os
import sys
# 使用insert 0即只使用github，避免交叉使用了pip安装的abupy，导致的版本不一致问题
sys.path.insert(0, os.path.abspath('../'))
import abupy

# 使用沙盒数据，目的是和书中一样的数据环境
abupy.env.enable_example_env_ipython()
from abupy import AbuFactorAtrNStop, AbuFactorPreAtrNStop, AbuFactorCloseAtrNStop, AbuFactorBuyBreak, ABuProgress
from abupy import abu, EMarketTargetType, AbuMetricsBase, ABuSymbolPd, tl, get_price, ABuMarketDrawing, ABuKLUtil
# btc是比特币symbol代号
btc = ABuSymbolPd.make_kl_df('btc', start='2013-09-01', end='2017-07-26')
# ltc是莱特币symbol代号
ltc = ABuSymbolPd.make_kl_df('ltc', start='2014-03-19', end='2017-07-26')
# btc.tail(7)
# ABuMarketDrawing.plot_simple_two_stock({'btc': btc, 'ltc': ltc})
btc365 = btc[-365:]
ltc365 = ltc[-365:]
# print(ABuKLUtil.date_week_wave({'btc': btc, 'btc365':btc365, 'ltc':ltc, 'ltc365':ltc365}))
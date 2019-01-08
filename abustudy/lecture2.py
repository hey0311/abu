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

from abupy import AbuFactorBuyBreak, AbuFactorSellBreak

# buy_factors 60日向上突破，42日向上突破两个因子
buy_factors = [{'xd': 60, 'class': AbuFactorBuyBreak},
               {'xd': 42, 'class': AbuFactorBuyBreak}]
# 使用120天向下突破为卖出信号
sell_factor1 = {'xd': 120, 'class': AbuFactorSellBreak}

from abupy import AbuFactorAtrNStop
from abupy import ABuPickTimeExecute, AbuBenchmark, AbuCapital

# 趋势跟踪策略止盈要大于止损设置值，这里0.5，3.0
sell_factor2 = {'stop_loss_n': 0.5, 'stop_win_n': 3.0,
                'class': AbuFactorAtrNStop}

# 两个卖出因子策略并行同时生效
sell_factors = [sell_factor1, sell_factor2]
benchmark = AbuBenchmark()
capital = AbuCapital(1000000, benchmark)
orders_pd, action_pd, _ = ABuPickTimeExecute.do_symbols_with_same_factors(['usTSLA'],
                                                                          benchmark,
                                                                          buy_factors,
                                                                          sell_factors,
                                                                          capital, show=True)

from abupy import AbuFactorPreAtrNStop

# 暴跌止损卖出因子形成dict
sell_factor3 = {'class': AbuFactorPreAtrNStop, 'pre_atr_n': 1.0}
# 三个卖出因子同时生效，组成sell_factors
sell_factors = [sell_factor1, sell_factor2, sell_factor3]
capital = AbuCapital(1000000, benchmark)
orders_pd, action_pd, _ = ABuPickTimeExecute.do_symbols_with_same_factors(['usTSLA'],
                                                                          benchmark,
                                                                          buy_factors,
                                                                          sell_factors,
                                                                          capital,
                                                                           show=True)

from abupy import AbuFactorCloseAtrNStop

# 保护止盈卖出因子组成dict
sell_factor4 = {'class': AbuFactorCloseAtrNStop, 'close_atr_n': 1.5}
# 四个卖出因子同时并行生效
sell_factors = [sell_factor1, sell_factor2, sell_factor3,
                sell_factor4]
capital = AbuCapital(1000000, benchmark)
orders_pd, action_pd, _ = ABuPickTimeExecute.do_symbols_with_same_factors(['usTSLA'],
                                                                          benchmark,
                                                                          buy_factors,
                                                                          sell_factors,
                                                                          capital,
                                                                          show=True)
# 基础库导入
from __future__ import print_function
from __future__ import division
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib inline
import os
import sys
# 使用insert 0即只使用github，避免交叉使用了pip安装的abupy，导致的版本不一致问题
import abupy
# 使用沙盒数据，目的是和书中一样的数据环境
from abupy import AbuFactorAtrNStop, AbuFactorPreAtrNStop, AbuFactorCloseAtrNStop, AbuFactorBuyBreak, ABuProgress,abu, EMarketTargetType, AbuMetricsBase, ABuSymbolPd, tl, get_price, ABuMarketDrawing, ABuKLUtil
if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    warnings.simplefilter('ignore')
    sys.path.insert(0, os.path.abspath('../'))
    abupy.env.enable_example_env_ipython()
# btc是比特币symbol代号
# print('开始加载btc数据...')
# btc = ABuSymbolPd.make_kl_df('btc', start='2013-09-01', end='2017-07-26')
# print('加载btc数据完成!')
# # ltc是莱特币symbol代号
# print('开始加载ltc数据...')
# ltc = ABuSymbolPd.make_kl_df('ltc', start='2014-03-19', end='2017-07-26')
# print('加载ltc数据完成!')
# btc.tail(7)
# ABuMarketDrawing.plot_simple_two_stock({'btc': btc, 'ltc': ltc})
# 设置市场类型为港股
    abupy.env.g_market_target = EMarketTargetType.E_MARKET_TARGET_TC
    #买入因子，卖出因子等依然使用相同的设置，如下所示：
    read_cash = 1000000
    # 买入因子依然延用向上突破因子
    buy_factors = [{'xd': 60, 'class': AbuFactorBuyBreak},
                   {'xd': 42, 'class': AbuFactorBuyBreak}]
    # 卖出因子继续使用上一节使用的因子
    sell_factors = [
        {'stop_loss_n': 1.0, 'stop_win_n': 3.0,
         'class': AbuFactorAtrNStop},
        {'class': AbuFactorPreAtrNStop, 'pre_atr_n': 1.5},
        {'class': AbuFactorCloseAtrNStop, 'close_atr_n': 1.5}
    ]
    # 注意这里把atr资金管理的仓位基数设置为0.5，即50%
    abupy.beta.atr.g_atr_pos_base = 0.5
    abu_result_tuple, kl_pd_manger = abu.run_loop_back(read_cash,
                                                       buy_factors,
                                                       sell_factors,
                                                       start='2013-09-01',
                                                       end='2017-07-26',
                                                       choice_symbols=None)
    ABuProgress.clear_output()
    AbuMetricsBase.show_general(*abu_result_tuple, only_show_returns=True)

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
from abupy import AbuFactorBuyBreak
from abupy import AbuFactorAtrNStop
from abupy import AbuFactorPreAtrNStop
from abupy import AbuFactorCloseAtrNStop
# run_loop_back等一些常用且最外层的方法定义在abu中
from abupy import abu, ABuProgress

# 设置初始资金数
read_cash = 1000000
# 设置选股因子，None为不使用选股因子
stock_pickers = None
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
# 择时股票池
choice_symbols = ['usNOAH', 'usSFUN', 'usBIDU', 'usAAPL', 'usGOOG',
                  'usTSLA', 'usWUBA', 'usVIPS']
# 使用run_loop_back运行策略
abu_result_tuple, kl_pd_manger = abu.run_loop_back(read_cash,
                                                   buy_factors,
                                                   sell_factors,
                                                   stock_pickers,
                                                   choice_symbols=choice_symbols,
                                                   n_folds=2)
ABuProgress.clear_output()

help(abu.run_loop_back)
from abupy import AbuMetricsBase
metrics = AbuMetricsBase(*abu_result_tuple)
metrics.fit_metrics()
metrics.plot_returns_cmp()
metrics.plot_sharp_volatility_cmp()
metrics.plot_effect_mean_day()
metrics.plot_keep_days()
metrics.plot_sell_factors()
metrics.plot_max_draw_down()
from abupy import ABuScalerUtil

class MetricsDemo(AbuMetricsBase):
    """扩展自定义度量类示例"""

    def _metrics_extend_stats(self):
        """
            子类可扩展的metrics方法，子类在此方法中可定义自己需要度量的值:
            本demo示例交易手续费和策略收益之间的度量对比
        """
        commission_df = self.capital.commission.commission_df
        commission_df['commission'] = commission_df.commission.astype(float)
        commission_df['cumsum'] = commission_df.commission.cumsum()
        """
            eg:
                type	date	symbol	commission	cumsum
            0	buy	20141024	usAAPL	19.04	19.04
            0	buy	20141024	usAAPL	19.04	38.08
            0	buy	20141029	usNOAH	92.17	130.25
            0	buy	20141029	usBIDU	7.81	138.06
            0	buy	20141029	usBIDU	7.81	145.87
            0	buy	20141029	usVIPS	60.95	206.82
        """
        # 讲date转换为index
        dates_pd = pd.to_datetime(commission_df.date)
        commission = pd.DataFrame(index=dates_pd)
        """
            eg: commission
            2014-10-24	19.04
            2014-10-24	38.08
            2014-10-29	130.25
            2014-10-29	138.06
            2014-10-29	145.87
            2014-10-29	206.82
            2014-11-03	265.82
            2014-11-11	360.73
        """
        commission['cum'] = commission_df['cumsum'].values
        self.commission_cum = commission['cum']
        self.commission_sum = self.commission_cum[-1]

    def plot_commission(self):
        """
            使用计算好的首先费cumsum序列和策略收益cumsum序列进行可视化对比
            可视化收益曲线和手续费曲线之前的关系
        """
        print('回测周期内手续费共: {:.2f}'.format(self.commission_sum))
        # 使用缩放scaler_xy将两条曲线缩放到同一个级别
        x, y = ABuScalerUtil.scaler_xy(self.commission_cum, self.algorithm_cum_returns, type_look='look_max',
                                       mean_how=True)
        x.plot(label='commission')
        y.plot(label='algorithm returns')
        plt.legend(loc=2)
        plt.show()

metrics = MetricsDemo(*abu_result_tuple)
metrics.fit_metrics()
metrics.plot_commission()
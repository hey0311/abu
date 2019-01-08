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
from abupy import AbuFactorAtrNStop, AbuFactorPreAtrNStop, AbuFactorCloseAtrNStop
from abupy import ABuPickTimeExecute, AbuBenchmark, AbuCapital

# buy_factors 60日向上突破，42日向上突破两个因子
buy_factors = [{'xd': 60, 'class': AbuFactorBuyBreak},
               {'xd': 42, 'class': AbuFactorBuyBreak}]
# 四个卖出因子同时并行生效
sell_factors = [
    {
        'xd': 120,
        'class': AbuFactorSellBreak
    },
    {
        'stop_loss_n': 0.5,
        'stop_win_n': 3.0,
        'class': AbuFactorAtrNStop
    },
    {
        'class': AbuFactorPreAtrNStop,
        'pre_atr_n': 1.0
    },
    {
        'class': AbuFactorCloseAtrNStop,
        'close_atr_n': 1.5
    }]
benchmark = AbuBenchmark()
capital = AbuCapital(1000000, benchmark)

from abupy import AbuSlippageBuyBase, slippage
# 修改买入下跌阀值为0.02
g_open_down_rate = 0.02

class AbuSlippageBuyMean2(AbuSlippageBuyBase):
    """示例日内滑点均价买入类"""

    @slippage.sbb.slippage_limit_up
    def fit_price(self):
        """
        取当天交易日的最高最低均价做为决策价格
        :return: 最终决策的当前交易买入价格
        """
        # TODO 基类提取作为装饰器函数，子类根据需要选择是否装饰，并且添加上根据order的call，put明确细节逻辑
        if self.kl_pd_buy.pre_close == 0 or (self.kl_pd_buy.open / self.kl_pd_buy.pre_close) < (1 - g_open_down_rate):
            # 开盘就下跌一定比例阀值，放弃单子
            return np.inf
        # 买入价格为当天均价，即最高，最低的平均，也可使用高开低收平均等方式计算
        self.buy_price = np.mean([self.kl_pd_buy['high'], self.kl_pd_buy['low']])
        # 返回最终的决策价格
        return self.buy_price

from abupy import AbuSlippageBuyBase, slippage
# 修改买入下跌阀值为0.02
g_open_down_rate = 0.02

class AbuSlippageBuyMean2(AbuSlippageBuyBase):
    """示例日内滑点均价买入类"""

    @slippage.sbb.slippage_limit_up
    def fit_price(self):
        """
        取当天交易日的最高最低均价做为决策价格
        :return: 最终决策的当前交易买入价格
        """
        # TODO 基类提取作为装饰器函数，子类根据需要选择是否装饰，并且添加上根据order的call，put明确细节逻辑
        if self.kl_pd_buy.pre_close == 0 or (self.kl_pd_buy.open / self.kl_pd_buy.pre_close) < (1 - g_open_down_rate):
            # 开盘就下跌一定比例阀值，放弃单子
            return np.inf
        # 买入价格为当天均价，即最高，最低的平均，也可使用高开低收平均等方式计算
        self.buy_price = np.mean([self.kl_pd_buy['high'], self.kl_pd_buy['low']])
        # 返回最终的决策价格
        return self.buy_price

# 针对60使用AbuSlippageBuyMean2
buy_factors2 = [{'slippage': AbuSlippageBuyMean2, 'xd': 60,
                 'class': AbuFactorBuyBreak},
                {'xd': 42, 'class': AbuFactorBuyBreak}]
capital = AbuCapital(1000000, benchmark)
orders_pd, action_pd, _ = ABuPickTimeExecute.do_symbols_with_same_factors(['usTSLA'],
                                                                          benchmark,
                                                                          buy_factors2,
                                                                          sell_factors,
                                                                          capital,
                                                                          show=True)
capital.commission.commission_df
def calc_commission_us2(trade_cnt, price):
    """
        手续费统一7美元
    """
    return 7

# 构造一个字典key='buy_commission_func', value=自定义的手续费方法函数
commission_dict = {'buy_commission_func': calc_commission_us2}
# 将commission_dict做为参数传入AbuCapital
capital = AbuCapital(1000000, benchmark, user_commission_dict=commission_dict)
# 除了手续费自定义外，回测其它设置不变，show=False不可视化回测交易
orders_pd, action_pd, _ = ABuPickTimeExecute.do_symbols_with_same_factors(['usTSLA'],
                                                                          benchmark,
                                                                          buy_factors2,
                                                                          sell_factors,
                                                                          capital,
                                                                          show=False)
# 回测完成后查看手续费情况
capital.commission.commission_df
# 卖出字典key='sell_commission_func', 指向同一个手续费方法，当然也可以定义不同的方法
commission_dict = {'buy_commission_func': calc_commission_us2, 'sell_commission_func': calc_commission_us2}
# 将commission_dict做为参数传入AbuCapital
capital = AbuCapital(1000000, benchmark, user_commission_dict=commission_dict)
# 除了手续费自定义外，回测其它设置不变，show=False不可视化回测交易
orders_pd, action_pd, _ = ABuPickTimeExecute.do_symbols_with_same_factors(['usTSLA'],
                                                                          benchmark,
                                                                          buy_factors2,
                                                                          sell_factors,
                                                                          capital,
                                                                          show=False)
# 回测完成后查看手续费情况
capital.commission.commission_df
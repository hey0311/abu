import math

import abupy
from abupy import abu, EMarketTargetType, AbuMetricsBase, ABuMarketDrawing, ABuProgress, ABuSymbolPd, get_price, \
    ABuIndustries, AbuDataParseWrap, SupportMixin, ABuNetWork
from abupy import EMarketDataFetchMode, EDataCacheType, EMarketSourceType, FuturesBaseMarket, TCBaseMarket, ABuDateUtil

from abupy.MarketBu.ABuDataFeed import OkexApi
abupy.env.g_data_fetch_mode = EMarketDataFetchMode.E_DATA_FETCH_FORCE_NET
# ABuSymbolPd.make_kl_df('usBIDU').tail()
abupy.env.g_private_data_source = OkexApi
btc=ABuSymbolPd.make_kl_df('btc')
print(btc)
ABuMarketDrawing.plot_candle_form_klpd(btc)
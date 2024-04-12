# tushare-interface
将tushare接口封装在类中，并提供限流、重试功能

#### 安装教程
1.  pip install tushare-interface
2.  在.bashrc中添加环境变量：
-   export TUSHARE_TOKEN='xxxxxxxxxx'  该api从tushare.pro网站购买
-   export TUSHARE_POINTS='120', 设置你的实际积分，将据此设定每分钟可访问接口的次数，需要注意的是，与网站上说明的不同，120积分实际只支持10次查询/分钟

#### 使用说明

1.  from tushare_interface import interfaceTuShare as pro
2.  package内有实例化对象: interfaceTuShare, 
-   如果环境变量已经设置好，import后即可使用
-   如果环境变量未设置，可通过setToken函数设置从htp://tushare.pro获得的token; 以及
-   通过setPoints函数设置积分，最低120
3.  interfaceTuShare还可以使用setRetry设置重试次数（最少0次）和重试间隔（以秒为单位，最低1秒）
4.  如果发现请求后出现流控告警，可以通过setTimesPerMinutus直接设置每分钟发送请求的数量，最低1次/分钟。
5.  调用query接口从tushare下载数据，接口与tushare原始的query保持一致
6.  函数原型
-   setToken(self, token: str) -> None
-   setPoints(self, points: int) -> None:
-   setTimesPerMinutus(self, timesPerMinutus: int) -> None
-   setRetry(self, retrys: int, secondsWaitRetry: int) -> None
-   query(self, func_name: str, **kwds: object) -> pandas.DataFrame | None
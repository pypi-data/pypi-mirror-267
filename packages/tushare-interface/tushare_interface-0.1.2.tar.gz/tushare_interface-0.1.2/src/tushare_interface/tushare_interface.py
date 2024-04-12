"""
Author: polaritec
Date: 2024-04-10 13:42:26
LastEditTime: 2024-04-10 20:24:36
Description:
"""

import os
import logging
import time
import pandas
import tushare as ts

"""
description: Tushare的接口类，可以在控制流量的情况下向tushare请求数据
return {*}
"""


class InterfaceTuShare:
    """
    description: 初始化，从配置文件中读取流量和Token，并将重置次数设置为5
    param {*} self
    return {*}
    """

    def __init__(self) -> None:
        try:
            timesPerMinutusEnv = os.environ.get("TUSHARE_API_PER_MINUTUS")
            if timesPerMinutusEnv is None:
                logging.warning(
                    "环境变量TUSHARE_API_PER_MINUTUS未设置，默认设置为最低等级10"
                )
                timesPerMinutus = 10
            else:
                timesPerMinutus = int(timesPerMinutusEnv)
        except ValueError:
            logging.warning(
                "环境变量TUSHARE_API_PER_MINUTUS应设置为数字，默认设置为最低等级10"
            )
            timesPerMinutus = 10

        if timesPerMinutus == 0:
            logging.warning("timesPerMinutus应设置为大于0的数字，默认设置为最低等级10")
            timesPerMinutus = 10

        self.__retrys = 4
        self.__secondsWaitRetry = 1

        self.__intervalMicroSecond = (
            60 * 1000
        ) / timesPerMinutus  # 计算两次发送之间的最小间隔

        token = os.environ.get("TUSHARE_TOKEN")  # 从环境变量中获取token, 并获取接口句柄
        if token is None:
            logging.critical(
                "TuShare的Token未能从环境变量TUSHARE_TOKEN中获取, 无法建立tushare接口"
            )
            self.__interface = None
        else:
            self.__interface = ts.pro_api(token)

        self.__prevMicroSeconds = 0  # 之前一次发送的时间戳

    """
    description: 重新设置Token
    param {*} self
    param {str} token
    return {*}
    """

    def setToken(self, token: str) -> None:
        if not isinstance(token, str):
            raise TypeError(
                "Expected a string for the token, got: {}".format(type(token))
            )

        if len(token) != 56:
            raise ValueError("Expected a string of length 56, got: {}".format(token))

        self.__interface = ts.pro_api(token)

    def setTimesPerMinutus(self, timesPerMinutus: int) -> None:
        if not isinstance(timesPerMinutus, int):
            raise TypeError(
                "Expected a integer for the timesPerMinutus, got: {}".format(
                    type(timesPerMinutus)
                )
            )

        if timesPerMinutus < 1:
            raise ValueError(
                "Expected an integer greater than or equal to 1, got: {}".format(
                    timesPerMinutus
                )
            )

        self.__intervalMicroSecond = (
            60 * 1000
        ) / timesPerMinutus  # 计算两次发送之间的最小间隔

    """
    description: 重新设置重试次数和重试等待时间
    param {*} self
    param {int} retrys: 如果第一次失败，自动重试几次，设置为0表示只尝试发送一次，不会重试。
    param {int} secondsWaitRetry: 发送失败后，等待n秒重试
    return {*}
    """

    def setRetry(self, retrys: int, secondsWaitRetry: int) -> None:
        if not isinstance(retrys, int):
            raise TypeError(
                "Expected a integer for the retry, got: {}".format(type(retrys))
            )

        if retrys < 0:
            raise ValueError(
                "Expected an integer greater than or equal to 1, got: {}".format(retrys)
            )

        if not isinstance(secondsWaitRetry, int):
            raise TypeError(
                "Expected a integer for the secondsWaitRetry, got: {}".format(
                    type(secondsWaitRetry)
                )
            )

        if secondsWaitRetry < 1:
            raise ValueError(
                "Expected an integer greater than or equal to 1, got: {}".format(
                    secondsWaitRetry
                )
            )

        self.__retrys = retrys
        self.__secondsWaitRetry = secondsWaitRetry

    """
    description: 从tushare服务器抓取信息
    param {*} self
    param {str} func_name: 接口名称，详见https://tushare.pro/document/2
    param {object} kwds: 接口参数
    return {*}
    """

    def query(self, func_name: str, **kwds: object) -> pandas.DataFrame | None:
        if self.__interface is None:  # 如果初始化时interface没有建立，直接返回None
            return None

        # 计算距离上次发送请求有多久
        currentMicroSeconds = time.perf_counter_ns() / (1000 * 1000)
        # 计算还需要延时多久
        delayMicroSecond = self.__intervalMicroSecond - (
            currentMicroSeconds - self.__prevMicroSeconds
        )
        if delayMicroSecond > 0:  # 如果需要延时，则发起定时器sleep
            logging.info("Sleep %d seconds", delayMicroSecond / 1000)
            time.sleep(delayMicroSecond / 1000)

        retrys = self.__retrys + 1

        while retrys:
            try:
                self.__prevMicroSeconds = time.perf_counter_ns() / (
                    1000 * 1000
                )  # 记录当前发送的时间戳
                return self.__interface.query(func_name, **kwds)
            except Exception as e:
                if str(e).find("接口不存在") != -1:
                    logging.critical("Tushare: 调用的接口%s不存在", func_name)
                    return None
                else:
                    logging.warning(
                        "Tushare: %s。 等待%d秒后自动重试",
                        str(e),
                        self.__secondsWaitRetry,
                    )
                    retrys = retrys - 1
                    if retrys != 0:
                        time.sleep(
                            self.__secondsWaitRetry
                        )  # 如果依然出错，则sleep n秒后重复发送

        return None


interfaceTuShare = InterfaceTuShare()

import unittest
import datetime
import os
import time
import sys
from pathlib import Path

# 获取当前文件的绝对路径
current_path = Path(__file__).resolve().parent
# 构造src目录的绝对路径
src_path = current_path.parent / "src"

# 将src目录添加到sys.path中
sys.path.append(str(src_path))

from tushare_interface.tushare_interface import interfaceTuShare as pro  # noqa: E402


# 测试前，请将TUSHARE_POINTS设置为120 !!!


class MyTest(unittest.TestCase):
    def setUp(self):
        # 测试前的设置工作
        pass

    def tearDown(self):
        # 测试后的清理工作
        pass

    def test_00_env(self):
        pointsEnv = os.environ.get("TUSHARE_POINTS")
        points = int(pointsEnv)
        if points >= 15000:
            timesPerMinutus = 1000
        elif points >= 10000:
            timesPerMinutus = 1000
        elif points >= 5000:
            timesPerMinutus = 500
        elif points >= 2000:
            timesPerMinutus = 200
        else:
            timesPerMinutus = 10

        self.assertEqual(
            pro._InterfaceTuShare__intervalMicroSecond,
            (60 * 1000) / timesPerMinutus,
        )

    def test_01_queryOnce(self):
        start_date = "20240101"
        end_date = (datetime.date.today() + datetime.timedelta(days=28)).strftime(
            "%Y%m%d"
        )
        df = pro.query(
            func_name="new_share",
            exchange="SSE",
            start_date=start_date,
            end_date=end_date,
            fields="ts_code,sub_code,name,ipo_date",
            is_open="1",
        )
        self.assertIsNotNone(df)  # 使用断言方法验证预期结果

    def test_02_setToken_1(self):
        with self.assertRaises(TypeError):
            pro.setToken(1)

    def test_03_setToken_2(self):
        with self.assertRaises(ValueError):
            pro.setToken("1")

    def test_04_setToken_3(self):
        pro.setToken("12345678901234567890123456789012345678901234567890123456")
        start_date = "20240101"
        end_date = (datetime.date.today() + datetime.timedelta(days=28)).strftime(
            "%Y%m%d"
        )
        df = pro.query(
            func_name="new_share",
            exchange="SSE",
            start_date=start_date,
            end_date=end_date,
            fields="ts_code,sub_code,name,ipo_date",
            is_open="1",
        )
        self.assertIsNone(df)

    def test_05_setToken_4(self):
        token = os.environ.get("TUSHARE_TOKEN")
        pro.setToken(token)
        start_date = "20240101"
        end_date = (datetime.date.today() + datetime.timedelta(days=28)).strftime(
            "%Y%m%d"
        )
        df = pro.query(
            func_name="new_share",
            exchange="SSE",
            start_date=start_date,
            end_date=end_date,
            fields="ts_code,sub_code,name,ipo_date",
            is_open="1",
        )
        self.assertIsNotNone(df)  # 使用断言方法验证预期结果

    def test_06_setTimesPerMinutus_1(self):
        with self.assertRaises(TypeError):
            pro.setTimesPerMinutus("1")

    def test_07_setTimesPerMinutus_2(self):
        with self.assertRaises(ValueError):
            pro.setTimesPerMinutus(0)

    def test_08_setTimesPerMinutus_3(self):
        pro.setTimesPerMinutus(5)
        self.assertEqual(pro._InterfaceTuShare__intervalMicroSecond, 12 * 1000)

    def test_09_setRetry_1(self):
        with self.assertRaises(TypeError):
            pro.setRetry(1)

    def test_10_setRetry_2(self):
        with self.assertRaises(TypeError):
            pro.setRetry("1", 1)

    def test_11_setRetry_3(self):
        with self.assertRaises(ValueError):
            pro.setRetry(-1, 1)

    def test_12_setRetry_4(self):
        with self.assertRaises(TypeError):
            pro.setRetry(0, "1")

    def test_13_setRetry_5(self):
        with self.assertRaises(ValueError):
            pro.setRetry(-1, 0)

    def test_14_setRetry_6(self):
        pro.setRetry(0, 1)
        self.assertEqual(pro._InterfaceTuShare__retrys, 0)

    def test_15_setRetry_7(self):
        pro.setRetry(0, 1)
        self.assertEqual(pro._InterfaceTuShare__secondsWaitRetry, 1)

    def test_16_setRetry_setTimesPerMinutus_1(self):
        pro.setRetry(1, 1)

        start_date = "20240101"
        end_date = (datetime.date.today() + datetime.timedelta(days=28)).strftime(
            "%Y%m%d"
        )
        startSeconds = time.perf_counter_ns() / (1000 * 1000 * 1000)
        for i in range(6):
            pro.query(
                func_name="new_share",
                exchange="SSE",
                start_date=start_date,
                end_date=end_date,
                fields="ts_code,sub_code,name,ipo_date",
                is_open="1",
            )

        endSeconds = time.perf_counter_ns() / (1000 * 1000 * 1000)
        duration = endSeconds - startSeconds
        self.assertGreaterEqual(duration, 60)

    def test_17_setRetry_setTimesPerMinutus_2(self):
        pro.setToken("12345678901234567890123456789012345678901234567890123456")
        pro.setTimesPerMinutus(5)
        pro.setRetry(10, 2)

        start_date = "20240101"
        end_date = (datetime.date.today() + datetime.timedelta(days=28)).strftime(
            "%Y%m%d"
        )
        startSeconds = time.perf_counter_ns() / (1000 * 1000 * 1000)
        pro.query(
            func_name="new_share",
            exchange="SSE",
            start_date=start_date,
            end_date=end_date,
            fields="ts_code,sub_code,name,ipo_date",
            is_open="1",
        )

        endSeconds = time.perf_counter_ns() / (1000 * 1000 * 1000)
        duration = endSeconds - startSeconds
        self.assertGreaterEqual(duration, 20)

    def test_18_setPoints_1(self):
        with self.assertRaises(TypeError):
            pro.setPoints("1")

    def test_19_setPoints_2(self):
        with self.assertRaises(ValueError):
            pro.setPoints(119)

    def test_20_setPoints_3(self):
        pro.setPoints(2000)
        self.assertEqual(pro._InterfaceTuShare__intervalMicroSecond, 60 * 1000 / 200)


if __name__ == "__main__":
    unittest.main()

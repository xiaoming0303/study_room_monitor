# -*- coding: utf-8 -*-
"""
generate_data.py —— 模拟智能终端，生成书房24小时温湿度数据

对应2023年6月浙江选考第14题场景：
智能终端（树莓派等）连接温湿度传感器，定时采集数据并保存。

运行方式：在项目根目录执行  python generate_data.py
生成结果：data/env_data.csv（时间、温度、湿度）
"""
import csv
import random
from datetime import datetime, timedelta


def generate_data():
    # 从24小时前开始，每10分钟采集一次
    start = datetime.now().replace(second=0, microsecond=0) - timedelta(hours=24)
    rows = []
    for i in range(24 * 6):          # 24小时 × 每小时6次 = 144条记录
        t = start + timedelta(minutes=10 * i)
        # 模拟采集：温度在22~28℃波动，湿度在40~65%波动
        temp = round(random.uniform(22.0, 28.0), 1)
        humi = round(random.uniform(40.0, 65.0), 1)
        rows.append([t.strftime("%Y-%m-%d %H:%M"), temp, humi])

    with open("data/env_data.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["time", "temp", "humi"])   # 表头
        writer.writerows(rows)

    print(f"已生成 {len(rows)} 条温湿度数据 → data/env_data.csv")


if __name__ == "__main__":
    generate_data()

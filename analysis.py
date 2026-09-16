# -*- coding: utf-8 -*-
"""
analysis.py —— 数据分析与可视化（pandas + matplotlib）

对应2023年6月浙江选考第14题第(5)问思路：
"利用pandas对导出的CSV数据进行分析统计，并用matplotlib绘制图表"

功能：
  1. pandas 读取CSV，统计温度、湿度的最大值/最小值/平均值
  2. 按小时分组，求每小时最大湿度（真题考法）
  3. matplotlib 绘制温湿度双Y轴变化曲线，保存为图片

运行方式：在项目根目录执行  python analysis.py
生成结果：static/images/env_chart.png
"""
import pandas as pd
import matplotlib.pyplot as plt

# 中文字体设置（Windows 使用 SimHei）
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False


def analyze():
    # 1. pandas 读取CSV数据
    df = pd.read_csv("data/env_data.csv", encoding="utf-8")
    df["time"] = pd.to_datetime(df["time"])
    df["hour"] = df["time"].dt.hour          # 提取小时，用于分组统计

    # 2. 基本统计
    print("数据条数:", len(df))
    print("温度统计:\n", df["temp"].describe())
    print("湿度统计:\n", df["humi"].describe())

    # 3. 真题考点：按小时分组，求每小时最大湿度
    humi_hour_max = df.groupby("hour")["humi"].max()
    print("每小时最大湿度:\n", humi_hour_max)

    # 4. matplotlib 绘制双Y轴折线图（温度、湿度单位不同，用两个Y轴）
    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(df["time"], df["temp"], color="red", linewidth=1.5, label="温度(℃)")
    ax1.set_xlabel("时间")
    ax1.set_ylabel("温度(℃)", color="red")
    ax1.tick_params(axis="y", labelcolor="red")

    ax2 = ax1.twinx()                        # 生成共用X轴的第二个Y轴
    ax2.plot(df["time"], df["humi"], color="blue", linewidth=1.5, label="湿度(%)")
    ax2.set_ylabel("湿度(%)", color="blue")
    ax2.tick_params(axis="y", labelcolor="blue")

    # 合并两条曲线的图例
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

    plt.title("书房24小时温湿度变化曲线")
    plt.grid(axis="x", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig("static/images/env_chart.png", dpi=150)
    print("图表已保存 → static/images/env_chart.png")


if __name__ == "__main__":
    analyze()

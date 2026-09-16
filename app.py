# -*- coding: utf-8 -*-
"""
app.py —— 书房温湿度监控系统（Flask 服务器端程序）

对应2023年6月浙江选考第14题场景：用户通过浏览器查看温湿度数据。
考点覆盖：
  · @app.route 路由  · render_template 模板渲染
  · request.args 获取GET参数（对应2023年1月真题：智能终端上传数据）
  · csv文件读写  · pandas 数据分析

运行方式：在项目根目录执行  python app.py
浏览器访问：http://127.0.0.1:5000
"""
import csv
from datetime import datetime

from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

CSV_FILE = "data/env_data.csv"


def read_df():
    """用 pandas 读取温湿度数据文件"""
    return pd.read_csv(CSV_FILE, encoding="utf-8")


def is_normal(temp, humi):
    """判断温湿度是否正常（对应真题：异常时蜂鸣器报警）"""
    if 20.0 <= temp <= 28.0 and 40.0 <= humi <= 65.0:
        return "正常"
    return "异常"


@app.route("/")
def index():
    """首页：显示最新温湿度、报警状态、24小时统计"""
    df = read_df()
    latest = df.iloc[-1].to_dict()           # 最新一条记录
    stats = {
        "temp_max": df["temp"].max(),
        "temp_min": df["temp"].min(),
        "temp_avg": round(df["temp"].mean(), 1),
        "humi_max": df["humi"].max(),
        "humi_min": df["humi"].min(),
        "humi_avg": round(df["humi"].mean(), 1),
    }
    return render_template("index.html",
                           latest=latest, stats=stats,
                           status=is_normal(latest["temp"], latest["humi"]))


@app.route("/history")
def history():
    """历史数据：温湿度曲线图 + 最近30条记录表格"""
    df = read_df()
    records = df.tail(30).to_dict("records")
    return render_template("history.html", records=records)


@app.route("/upload")
def upload():
    """模拟智能终端上传数据（GET参数方式）
    访问示例：http://127.0.0.1:5000/upload?temp=26.5&humi=55
    对应2023年1月真题：request.args 获取 URL 中的查询参数
    """
    temp = request.args.get("temp")
    humi = request.args.get("humi")
    if temp is None or humi is None:
        return "参数错误：请使用 /upload?temp=温度&humi=湿度"

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([now, float(temp), float(humi)])
    return f"上传成功：temp={temp}℃, humi={humi}%"


if __name__ == "__main__":
    # host=127.0.0.1 本机访问；改成 0.0.0.0 可让局域网其他设备访问
    app.run(host="127.0.0.1", port=5000, debug=True)

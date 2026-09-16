# 书房温湿度监控系统（高考生水平 Flask 项目）

对应 **2023年6月浙江信息技术选考第14题** 场景：小华搭建书房环境监控系统，监测温湿度，
用户通过浏览器查看实时和历史数据。本项目用 **Flask + pandas + matplotlib** 完整复现。

## 项目功能

| 功能 | 说明 | 对应考点 |
| --- | --- | --- |
| 首页 `/` | 显示最新温湿度、正常/异常报警状态、24小时统计 | Flask路由、模板渲染、pandas统计 |
| 历史数据 `/history` | 温湿度曲线图 + 最近记录表格 | matplotlib绘图、Jinja2循环 |
| 数据上传 `/upload` | 模拟智能终端上传数据（GET参数） | `request.args`（2023年1月真题考法） |

## 文件结构

```
study_room_monitor/
├── app.py               # Flask服务器端主程序
├── generate_data.py     # 模拟智能终端：生成24小时温湿度数据
├── analysis.py          # pandas统计 + matplotlib绘图
├── requirements.txt     # 依赖清单
├── data/
│   └── env_data.csv     # 温湿度历史数据（自动生成）
├── static/images/
│   └── env_chart.png    # matplotlib生成的曲线图（自动生成）
└── templates/
    ├── index.html       # 首页模板
    └── history.html     # 历史数据模板
```

## 运行步骤

1. 安装依赖（只需一次）
   ```
   pip install -r requirements.txt
   ```

2. 生成模拟数据（模拟智能终端采集24小时数据）
   ```
   python generate_data.py
   ```

3. 数据分析与绘图（pandas + matplotlib）
   ```
   python analysis.py
   ```

4. 启动Web服务器
   ```
   python app.py
   ```

5. 浏览器访问 http://127.0.0.1:5000

6. 模拟智能终端上传一条数据
   ```
   浏览器打开：http://127.0.0.1:5000/upload?temp=26.5&humi=55
   ```

## 与高考真题的对应关系

- `@app.route`、`app.run(host, port)` —— 2023.6真题第(3)问：写出访问URL
- B/S架构：浏览器是客户端，Flask程序是服务器端程序 —— 2023.6真题第(1)(2)问
- `request.args` 获取GET参数 —— 2023.1真题：`/toserv?h=60&id=1`
- pandas分组统计 + matplotlib绘图 —— 2023.6真题第(5)问
- 温湿度超范围报警 —— 2023.6真题：异常蜂鸣报警

## 高考生学习要点

- Flask只用了：路由、render_template、request，全部在考纲范围内
- 数据存储用CSV文件，没有用数据库（符合高考要求）
- pandas用了：read_csv、max/min/mean、groupby
- matplotlib用了：双Y轴折线图（温度和湿度单位不同，需要两个Y轴）

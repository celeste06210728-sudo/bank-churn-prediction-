# 银行信用卡客户流失预测项目

本项目通过 SQL 数据提取与清洗、Python 机器学习建模、Excel 自动化报表生成、Power BI 交互式可视化，端到端展示数据分析与商业智能能力。

## 技术栈

| 工具 | 用途 |
|------|------|
| SQL | 数据查询、清洗、特征初步加工 |
| Python | 数据预处理、随机森林模型训练、批量预测 |
| Excel | 自动化业务报表（预测明细、高风险客户名单、汇总统计） |
| Power BI | 交互式仪表板（KPI 监控、风险分布、混淆矩阵、维度下钻） |

## 项目结构
bank-churn-prediction/
├── data/
│   ├── BankChurners.csv
│   ├── credit_card_customers.csv
│   ├── import_into_sql.py
│   └── SQL.sql
├── output/
│   ├── rf_model.pkl
│   ├── encoders.pkl
│   ├── feature_cols.pk
│   ├── roc_curve.png
│   ├── feature_importance.png
│   ├── feature_importance.csv
│   ├── predictions.csv
│   ├── churn_prediction_report.xlsx
│   └── credit_card_customers_processed.csv
├── BankChurnAnalysis.py   # 数据处理 + 模型训练
├── PredictChurn.py        # 加载模型批量预测
├── GenerateExcel.py       # 生成 Excel 业务报表
├── Presentation.pbix      # Power BI 仪表板
├── requirements.txt
└── README.md


## 项目流程

### 1. SQL — 数据准备

通过 SQL 脚本完成数据导入、清洗与初步特征加工：

- `import_into_sql.py`：将原始数据写入数据库
- `SQL.sql`：数据查询、去重、字段清洗、基础特征计算

### 2. Python — 建模与预测

- **数据处理**：删除无关列，类别特征 LabelEncoder 编码，训练/测试集切分，避免数据泄漏
- **模型训练**：RandomForestClassifier，`class_weight="balanced"` 处理类别不平衡
- **模型评估**：ROC-AUC = 0.986，特征重要性可视化
- **持久化**：模型、编码器、特征列名保存为 `rf_model.pkl` / `encoders.pkl` / `feature_cols.pkl`
- **批量预测**：输出 `predictions.csv`，包含 `predicted_churn` 与 `churn_probability`

### 3. Excel — 自动化报表

`GenerateExcel.py` 自动产出 Excel 报表，包含：

- 预测明细（客户级流失概率与风险标签）
- 高风险客户名单（概率 ≥ 0.7）
- 汇总统计（总客户数、预测流失数、流失率等）

### 4. Power BI — 可视化看板

基于 `output/` 下文件构建交互式仪表板，核心页面：

- **概览**：总客户数、预测流失数、预测流失率、高风险客户数
- **风险等级分布**：按流失概率划分低/中/高风险
- **实际 vs 预测流失对比**：验证模型表现
- **混淆矩阵**：TP = 1540, FP = 44, FN = 87, TN = 8456，准确率 98.71%，召回率 94.65%，精确率 97.22%
- **维度分析**：按年龄、收入、教育、卡片类别、不活跃月数等下钻
- **特征重要性**：Top 20 驱动因素

## 快速开始

bash
pip install -r requirements.txt
python BankChurnAnalysis.py
python PredictChurn.py
python GenerateExcel.py

三步跑完即可在 `output/` 目录下获得所有结果文件，直接接入 Excel 和 Power BI。

## 数据集

数据来源：[Credit Card Customers](https://www.kaggle.com/datasets/sakshigoyal7/credit-card-customers)，包含约 10,127 条信用卡客户记录，涵盖人口统计、账户活跃度、消费行为等字段。

## 核心结果

| 指标 | 数值 |
|------|------|
| 总客户数 | 10,127 |
| 预测流失数 | 1,780 |
| 预测流失率 | 17.58% |
| 高风险客户数（概率 ≥ 0.7） | 1,584 |
| 高风险客户占比 | 15.64% |
| ROC-AUC | 0.986 |

**说明：** 预测流失数基于模型预测标签 `predicted_churn = 1`，高风险客户数基于概率阈值 `churn_probability >= 0.7`，两者口径不同，因此数值不完全一致。

### 关键发现

模型特征重要性显示，交易行为与账户使用强度是流失的核心驱动因素。Top 8 特征：

`Total_Trans_Amt`、`Total_Trans_Ct`、`Total_Revolving_Bal`、`Total_Ct_Chng_Q4_Q1`、`Avg_Utilization_Ratio`、`Total_Amt_Chng_Q4_Q1`、`Total_Relationship_Count`、`Months_Inactive_12_mon`

交易活跃度下降、额度使用变化和账户不活跃是客户流失的预警信号。

## License

MIT
-- 信用卡客户流失分析
CREATE DATABASE IF NOT EXISTS bank_chum
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_0900_ai_ci;

USE bank_chum;
SELECT COUNT(*) AS 总人数 FROM credit_card_customers;

SELECT
    Attrition_Flag,
    COUNT(*) AS 人数,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM credit_card_customers), 2) AS 占比
FROM credit_card_customers
GROUP BY Attrition_Flag;

SELECT
    Gender,
    Attrition_Flag,
    COUNT(*) AS 人数,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(PARTITION BY Gender), 2) AS 组内占比
FROM credit_card_customers
GROUP BY Gender, Attrition_Flag
ORDER BY Gender, Attrition_Flag;

WITH age_grouped AS (
    SELECT
        Attrition_Flag,
        CASE
            WHEN Customer_Age < 30 THEN 'Under 30'
            WHEN Customer_Age BETWEEN 30 AND 39 THEN '30-39'
            WHEN Customer_Age BETWEEN 40 AND 49 THEN '40-49'
            WHEN Customer_Age BETWEEN 50 AND 59 THEN '50-59'
            ELSE '60+'
        END AS 年龄组
    FROM credit_card_customers
)
SELECT
    年龄组,
    Attrition_Flag,
    COUNT(*) AS 人数,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(PARTITION BY 年龄组), 2) AS 组内占比
FROM age_grouped
GROUP BY 年龄组, Attrition_Flag
ORDER BY 年龄组, Attrition_Flag;

SELECT
    Attrition_Flag,
    ROUND(AVG(Total_Trans_Ct), 2) AS 平均交易次数,
    ROUND(AVG(Total_Trans_Amt), 2) AS 平均交易金额,
    ROUND(AVG(Credit_Limit), 2) AS 平均信用额度,
    ROUND(AVG(Total_Revolving_Bal), 2) AS 平均循环余额,
    ROUND(AVG(Avg_Utilization_Ratio), 4) AS 平均使用率
FROM credit_card_customers
GROUP BY Attrition_Flag;

SELECT
    Income_Category,
    Attrition_Flag,
    COUNT(*) AS 人数,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(PARTITION BY Income_Category), 2) AS 组内占比
FROM credit_card_customers
GROUP BY Income_Category, Attrition_Flag
ORDER BY Income_Category, Attrition_Flag;

SELECT '教育程度' AS 维度, Education_Level AS 分组, Attrition_Flag,
    COUNT(*) AS 人数,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(PARTITION BY Education_Level), 2) AS 组内占比
FROM credit_card_customers
GROUP BY Education_Level, Attrition_Flag
UNION ALL
SELECT '婚姻状况' AS 维度, Marital_Status AS 分组, Attrition_Flag,
    COUNT(*) AS 人数,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(PARTITION BY Marital_Status), 2) AS 组内占比
FROM credit_card_customers
GROUP BY Marital_Status, Attrition_Flag
UNION ALL
SELECT '卡等级' AS 维度, Card_Category AS 分组, Attrition_Flag,
    COUNT(*) AS 人数,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(PARTITION BY Card_Category), 2) AS 组内占比
FROM credit_card_customers
GROUP BY Card_Category, Attrition_Flag
ORDER BY 维度, 分组, Attrition_Flag;

SELECT
    Months_Inactive_12_mon AS 不活跃月数,
    Attrition_Flag,
    COUNT(*) AS 人数,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(PARTITION BY Months_Inactive_12_mon), 2) AS 组内占比
FROM credit_card_customers
GROUP BY Months_Inactive_12_mon, Attrition_Flag
ORDER BY Months_Inactive_12_mon, Attrition_Flag;

SELECT
    Contacts_Count_12_mon AS 联系次数,
    Attrition_Flag,
    COUNT(*) AS 人数,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(PARTITION BY Contacts_Count_12_mon), 2) AS 组内占比
FROM credit_card_customers
GROUP BY Contacts_Count_12_mon, Attrition_Flag
ORDER BY Contacts_Count_12_mon, Attrition_Flag;
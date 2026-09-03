 import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

df = pd.read_csv('data/BankChurners.csv')

df = df.loc[:, ~df.columns.str.startswith('Naive_Bayes')]

print(f'CSV行数: {df.shape[0]}')
print(f'CSV列名: {df.columns.tolist()}')

password = os.getenv("DB_PASSWORD", "your_password")
engine = create_engine(f'mysql+pymysql://root:{password}@localhost:3306/bank_churn?charset=utf8mb4')

df.to_sql('credit_card_customers', con=engine, if_exists='replace', index=False)

print('导入完成！')

with engine.connect() as conn:
    result = conn.execute(text('SELECT COUNT(*) FROM credit_card_customers'))
    print(f'数据库行数: {result.fetchone()[0]}')
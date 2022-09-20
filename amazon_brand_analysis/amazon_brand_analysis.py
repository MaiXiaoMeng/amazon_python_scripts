import os
import sys
import time
import timeit
import pandas as pd

pd.set_option('max_colwidth', 20)
pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
MAIN_DF = pd.DataFrame()
OUT_EXCEL = '关键词查找_数据.xlsx'

if __name__ == '__main__':
    # 品牌分析数据命名 US_2021-06-20_2021-06-26.csv
    asin = input('请输入要查询的ASIN:\n')
    asin = asin if len(asin) > 5 else 'B094NMF611'
    print(f'正在查询ASIN: {asin} 相关的关键词数据,请耐心等候...')
    start = timeit.default_timer()
    folder = repr(os.path.dirname(os.path.realpath(sys.executable)))[1:-1]
    if 'virtualenvs' in folder or 'Python37' in folder:
        folder = sys.path[0]
    for file_name in os.listdir(f'{folder}/品牌分析数据'):
        if '.csv' in file_name:
            print(f'正在读取 {file_name} 文件的数据')
            file_list = file_name[:-4].split('_')
            df = pd.read_csv(f'品牌分析数据/{file_name}', header=1)
            df = df[(df['#1 已点击的 ASIN'] == asin) | (df['#2 已点击的 ASIN'] == asin) | (df['#3 已点击的 ASIN'] == asin)]
            df_col_name = df.columns.tolist()
            df_col_name.insert(0, '开始时间')
            df_col_name.insert(1, '结束时间')
            df = df.reindex(columns=df_col_name)
            df['开始时间'] = pd.to_datetime(file_list[1]).date()
            df['结束时间'] = pd.to_datetime(file_list[2]).date()
            MAIN_DF = pd.concat([MAIN_DF, df])
    MAIN_DF.to_excel(OUT_EXCEL)

    stop = timeit.default_timer()
    print(f'输出文件名称: {OUT_EXCEL} ASIN: {asin} 数据总行数: {len(MAIN_DF)}')
    input(f'数据处理完成，共耗时: {time.strftime("%H:%M:%S", time.gmtime(stop - start))}')

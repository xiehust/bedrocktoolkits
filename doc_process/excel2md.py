# pip install tabulate openpyxl pandas
import os
import glob
import openpyxl
import argparse
import pandas as pd
from tabulate import tabulate

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_path', type=str, default='./excels', help='input path')
    parser.add_argument('--output_path', type=str, default='./output/', help='output path')
    args = parser.parse_args()
    input_path = args.input_path
    output_path = args.output_path

    # 打开Excel文件
    # xlsx_files = glob.glob(os.path.join(input_path, '*.xlsx'))
    
    #create a folder if it doesn't exist
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    # list all csv files in folder 
    csv_files = glob.glob(os.path.join(input_path, '*.csv'))
    print(f"csv_files: {csv_files}")
    # 遍历每个 .xlsx 文件
    for xlsx_file in csv_files:
        xlsx_file_name = os.path.basename(xlsx_file)
        print(f"processing {xlsx_file_name}")
        try:
            # workbook = openpyxl.load_workbook(xlsx_file)

            # for worksheet in workbook.worksheets:
            df = pd.read_csv(xlsx_file)
            # df = pd.DataFrame(worksheet.values)
            df = df.dropna(how='all', axis=0).dropna(how='all', axis=1)
            markdown_table = df.to_markdown(index=False)
            json_table = df.to_json(orient='records')
            # header = df.loc[0].values
            # print(f"header: {header}")

            # # for i, row in df[1:].iterrows():
            # data = [ str(item).replace('\n', ';') for item in row.values]
            # row_df = pd.DataFrame([data], columns=header)
            # markdown_table = row_df.to_markdown(index=False)
                
            # 写入Markdown文件
            filename = f"{output_path}/{xlsx_file_name}_.md"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(markdown_table)
                
            # Json文件
            filename2 = f"{output_path}/{xlsx_file_name}_.json"
            with open(filename2, 'w', encoding='utf-8') as f:
                f.write(json_table)

            print(f'已将第{xlsx_file_name}数据写入文件 {filename}')
        except Exception as e:
            print(str(e))
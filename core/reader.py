import logging
from docx import Document

def readox(temp_path : str):

    print("读取模板文件...",end="")
    doc = Document(temp_path)
    print("成功")

    return doc

import logging
from docx import Document

def readox(temp_path : str):

    logging.info("读取模板文件...")
    doc = Document(temp_path)
    logging.info("成功")

    return doc

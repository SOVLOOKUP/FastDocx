import re, logging

def process(doc,somethinglist:list,imgpath :str):
    """
    doc Document文件对象   
    something list

    >>>[{
        "key":"锚点标记",
        "type":"text/img/tab/br",
        "value":"文本"/[img_path,width,height]/[rows,cols]
        },
        ...]
    """
    # 遍历一遍
    for paragraph in doc.paragraphs:
        # 如果碰到锚点
        rer = re.findall(r"{{.*?}}",paragraph.text)
        if rer != None:
            # 根据锚点信息
            for i in rer:
                # 查找输入字典
                sth = list(filter(lambda x:x["key"] == i.strip(r"{{").strip(r"}}"),somethinglist))
                # 字典中没有这条锚点信息
                if sth == []:
                    logging.warning(f"缺失模板信息 {i} 的key，跳过")
                    continue
                
                sth = sth[0]
                # 映射出输入信息中的字段
                # ikey = sth["key"]
                itype = sth["type"]
                ivalue = sth["value"]

                # 判断输入是什么类型
                TEXT = (itype == "text")
                PICTURE = (itype == ("img" or "picture"))
                TAB = (itype == ("tab" or "table"))
                BREAK = (itype == ("br" or "break"))

                # 替换文本，对一段文字也有效
                if TEXT:
                    # paragraph.runs[-1].add_text(something["value"])
                    paragraph.text = re.sub(i,ivalue,paragraph.text)
                    continue
                
                # 删除锚点文本
                paragraph.text = re.sub(i,"",paragraph.text)

                # 在末尾添加图片
                # params:
                # [img_path,width,height]
                # todo 碰到http开头的自动下载并插入
                if PICTURE:
                    paragraph.add_run().add_picture(*ivalue)
                    # paragraph.runs[-1].add_picture(path)
                
                # 在末尾添加表格
                # params:
                # [rows,cols]
                if TAB:
                    paragraph.add_run().add_tab(*ivalue)

                # 添加换行
                if BREAK:
                    paragraph.add_run().add_break()
    return doc



import logging
from .reader import readox
from .engine import process
from .writer import writedox
import os

class WordCore(object):
    """
    word 模板自动生成

    basepath -- tmp -- {id} -- template.docx
             |              |
             |              |- index.json
             |              |
             |              |- img -- 1.img
             |                     |
             |                     |- 2.img
             |- out

    BasePath = "D:\Desktop\自动word\workspace"
    index = {
        # 12位id，模板解析任务的唯一标识
        "id":"111111111111",
        "taskname":"测试任务",
        "author":"GoNorth",
        "version":"V0.0.1",
        "description":"这是一个测试任务，一帆风顺🤩",
        # 模板解析的内容
        "word":[{
            # 输出word名称
            "name":"1.docx",
            # 具体锚点替换内容
            "content":[{
                "key" : "这里插入表1",
                "type" : "text",
                "value" : "我是替换文字！！！"
                },
                # 其他关键字锚点
                ]
            },
            # 其他生成的word
        ]}
    """
    def __init__(self,basepath : str,index : dict):
        # if index == "":
        #     with open(os.path.join(basepath,"index.json")) as f:
        #         index = json.loads(f.read())
        if basepath.endswith("/") == False:
            basepath = basepath+"/"
            
        self.basepath = basepath
        self.id = index["id"]
        self.taskname = index["taskname"]
        self.author = index["author"]
        self.version = index["version"]
        self.description = index["description"]
        # self.readpath = os.path.join(self.basepath,"/tmp",self.id+"/template.docx")
        self.readpath = self.basepath+self.id+"/tmp/"
        # self.outpath = os.path.join(self.basepath,"/out",self.id)
        self.outpath = self.basepath+self.id+"/out/"

        # 检查项目资源;项目目录，没有就创建
        if os.path.exists(self.readpath) == False:
            os.makedirs(self.readpath)
        if os.path.exists(self.outpath) == False:
            os.makedirs(self.outpath)

        # todo 校验并下载，重构self.word
        if os.path.exists(self.readpath+"template.docx") == False:
            logging.error("没有找到工作资源！")
        # 输出自述信息
        logging.info(f"""
        任务ID\t\t|\t{self.id}
        任务名称\t|\t{self.taskname}
        作者\t\t|\t{self.author}
        版本\t\t|\t{self.version}
        任务描述\t|\t{self.description}
        """)

        self.word = index["word"]

        # 加载模板
        self.template = readox(self.readpath+"template.docx")
    

    def process(self):
        logging.info("#"*16+f"{self.id}任务开始"+"#"*16)

        for word_content in self.word:
            name = word_content["name"]
            content = word_content["content"]

            logging.info("gen "+name)
            # 使用模板和内容组成新文档
            newdoc = process(self.template,content)

            # 保存新文档
            writedox(newdoc,self.outpath + name)


        logging.info("#"*16+f"{self.id}任务结束"+"#"*16)
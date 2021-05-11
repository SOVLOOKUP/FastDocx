import logging, httpx, os, json, string, random
from .reader import readox
from .engine import process
from .writer import writedox
from .download import download

class WordCore(object):
    """[summary]
    Args:
        basepath : 工作区目录
        log_level : logging.DEBUG/INFO/WARNING
    """
    def __init__(self, basepath : str, log_level=logging.INFO):
        logging.basicConfig(level=log_level,
                    format='%(levelname)s: %(message)s')  
                    # format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')  
        logging.info("""
##############################################
##                                          ##
##           Welcome to FastDocx!!          ##
##                                          ##
##        Author      sovlookup             ##
##        Mail     805408477@qq.com         ##
##        Github  sovlookup/FastDocx        ##
##                                          ##
##############################################
        """)
        if basepath.endswith("/") == False:
            basepath = basepath+"/"

        self.basepath = basepath
    
    def verify(self, config : dict or str, thread_num:int):
        logging.info("校验中...")
        if type(config) == str and config.startswith("http"):
            # 下载config.json
            config = json.loads(httpx.get(config).content)

        id = config.get("id")
        if id == None:
            logging.error("资源地址不正确或已失效！")
            return False
        
        word = config.get("word")
        if word == None:
            logging.error("资源无效！")
            return False
        
        self.id = id 

        self.readpath = self.basepath+self.id+"/tmp/"
        self.outpath = self.basepath+self.id+"/out/"

        # 检查项目资源;项目目录，没有就创建
        if os.path.exists(self.readpath) == False:
            os.makedirs(self.readpath)
        if os.path.exists(self.outpath) == False:
            os.makedirs(self.outpath)

        if os.path.exists(self.readpath+"template.docx") == False:
            tmplate_url = config.get("template",False)
            if tmplate_url == False:
                logging.error("没有找到工作资源！")
                return False
            if tmplate_url.strip().startswith("http") == False:
                logging.error("资源地址错误！")
                return False
            
            # 下载到 self.readpath+"template.docx"
            with httpx.stream("GET", tmplate_url) as response:
                with open(self.readpath+"template.docx","wb+") as f:
                    for chunk in response.iter_bytes():
                        f.write(chunk)

        if os.path.exists(self.readpath + "img/") == False:
            os.makedirs(self.readpath + "img/")

        # 下载img
        msg = [
        # {
        #     "content":["GET","https://baidu.com"],
        #     "todo": print("sssssssssssssssssssssssssss")
        # },
        ]
        for part in word:
            for section in part.get("content"):
                value = section.get("value")
                if type(value) == list:
                    if (type(value[0]) == str) and (value[0].startswith("http")):
                        # 下载并保存到readpath/img/ 返回名字
                        name = ''.join(random.sample(string.ascii_letters + string.digits, 12)) + ".png"
                        msg.append({
                            "content":["GET",value[0]],
                            "path": self.readpath + "img/" + name
                        })

                        value[0] = self.readpath + "img/"+name
        
        logging.info(f"同步资源...共{len(msg)}个项目")
        download(msg, thread_num)
        
        # # 保存config.json
        # with open(self.readpath+"config.json","w+") as f:
        #     f.write(json.dumps(config))

        self.word = word
        self.config = config

    def load(self, config : dict, thread_num:int = 1):
        """[summary]

        Args:
            config : config
            thread_num (int, optional): [下载线程数]. Defaults to 1.
        """

        if self.verify(config=config,thread_num=thread_num):
            logging.warning("加载失败！！！")
            return

        self.taskname = self.config.get("taskname","")
        self.author = self.config.get("author","")
        self.version = self.config.get("version","")
        self.description = self.config.get("description","")
        
        # 输出自述信息
        logging.info(f"""
        任务ID\t\t|\t{self.id}
        任务名称\t|\t{self.taskname}
        作者\t\t|\t{self.author}
        版本\t\t|\t{self.version}
        任务描述\t|\t{self.description}
        """)

        # 加载模板
        self.template = readox(self.readpath+"template.docx")

        return self

    def process(self) -> bool:
        logging.info("#"*16+f"{self.id}任务开始"+"#"*16)

        for word_content in self.word:
            name = word_content["name"]
            content = word_content["content"]

            logging.info("gen "+name)
            # 使用模板和内容组成新文档
            newdoc = process(self.template,content,self.readpath+"img/")

            # 保存新文档
            writedox(newdoc,self.outpath + name)


        logging.info("#"*16+f"{self.id}任务结束"+"#"*16)
        return True
import logging, httpx, os, json, string, random, shutil
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
##              Version 0.2.1               ##
##                                          ##
##        Author      sovlookup             ##
##        Mail      gonorth@qq.com          ##
##        Github  sovlookup/FastDocx        ##
##                                          ##
##############################################
        """)
        if basepath.endswith("/") == False:
            basepath = basepath+"/"

        self.basepath = basepath
    
    def verify(self, config: dict) -> bool:
        logging.info("校验中...")

        self.config = config
        self.id :str = config.get("id")
        self.word :dict = config.get("word")
        self.template :str = self.config.get("template")

        if self.id == None:
            logging.error("配置中没有找到id！")
            return False
        
        if self.word == None:
            logging.error("配置中没有找到word！")
            return False
        
        if self.template == None:
            logging.error("配置中没有找到template！")
            return False

        self.readpath = self.basepath+self.id+"/tmp/"
        self.outpath = self.basepath+self.id+"/out/"
        self.templatepath = self.readpath+"template.docx"

        # 检查项目资源;项目目录，没有就创建
        if os.path.exists(self.readpath) == False:
            os.makedirs(self.readpath)
        if os.path.exists(self.outpath) == False:
            os.makedirs(self.outpath)
        if os.path.exists(self.readpath + "img/") == False:
            os.makedirs(self.readpath + "img/")

        return True

    def load(self, config , thread_num:int = 1):
        """[summary]

        Args:
            config : path | url | dict
            thread_num (int, optional): [下载线程数]. Defaults to 1.
        """
        # url
        if type(config) == str and config.startswith("http"):
            _config = json.loads(httpx.get(config).content)
        # dict
        elif type(config) == dict:
            _config = config
        # path
        elif type(config) == str:
            with open(config,'r') as f:
                _config = json.load(f)
        else:
            logging.error("config格式错误，支持url，filepath，dict")
        
        if self.verify(config = _config):
            logging.info("资源加载中...")
            # 下载word模版
            if self.template.strip().startswith("http"):
                with httpx.stream("GET", self.template) as response:
                    with open(self.templatepath,"wb+") as f:
                        for chunk in response.iter_bytes():
                            f.write(chunk)
            # 本地word模版
            elif os.path.exists(self.template):
                shutil.copyfile(self.template, self.templatepath)
            else:
                logging.error("template资源地址错误，仅支持本地文件和网址")

            # 下载img
            msg = []
            for part in self.word:
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

        else:
            logging.error("加载失败！！！")
            raise RuntimeError('verifyError')

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
        self.template = readox(self.templatepath)

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

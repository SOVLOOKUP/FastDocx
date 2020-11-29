from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices, QIcon, QIconEngine
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QApplication, QListWidgetItem, QInputDialog, QFileDialog
from .form import Ui_MainWindow
import httpx, json, os
from fastdocx import WordCore
from .style import stype
# class CommonHelper:
#   def __init__(self):
#     pass
 
#   @staticmethod
#   def readQss(style):
#     with open(style, 'r') as f:
#         return f.read()

# todo:获取输出、改造为迭代器提高效率
class item(QListWidgetItem):
  def __init__(self, name :str, icon: str, id: str, author: str, version: str, config: str, description: str,tmpdir: str, parent = None):
    super(item, self).__init__(parent)
    self.tmpdir = tmpdir
    self.setText(name)
    iconame = icon.split("/")[-1]
    with httpx.stream("GET", icon) as response:
      with open(self.tmpdir+iconame,"wb+") as f:
          for chunk in response.iter_bytes():
              f.write(chunk)
    self.setIcon(QIcon(self.tmpdir+iconame))
    self.setToolTip(f"ID:{id}\n作者:{author}\n版本:{version}")
    self.config = config
    self.description = description
    self.name = name
    self.version = version
    self.author = author
  
  def __next__():
    pass
  
  def __iter__():
    pass

  
class fastdocx(QMainWindow, Ui_MainWindow):
    def __init__(self,tmpdir:str = "./tmp/",source_url:str = "https://v.gonorth.top:444/file/index.json", parent = None):
        super(fastdocx, self).__init__(parent)
        # 重连10次
        self._time = 10
        self.source_url = source_url
        self.tmpdir = tmpdir
        self.setupUi(self)
        try:
          self.setWindowIcon(QIcon('icon.ico'))
        except:
          pass
        self.setWindowTitle('FastDocx')
        self.workdirButton.clicked.connect(self.workdirButtonClicked)
        self.process.clicked.connect(self.startProcess)
        self.listWidget.itemClicked.connect(self.setDetails)
        self.source.triggered.connect(self.setSourse)
        self.about.triggered.connect(self.aboutOpenWeb)
        # self.myinit()

    # todo:修复打开bug
    def aboutOpenWeb(self):
      QDesktopServices.openUrl(QUrl("https://github.com/sovlookup"))

    def setDetails(self, item):
      self.name.setText(item.name)
      self.author.setText(item.author)
      self.version.setText(item.version)
      self.description.setText(item.description)
      self.config = item.config
    
    def setSourse(self):
      text, ok = QInputDialog.getText(self,"自定义源地址","设置源地址:")
      if ok and str(text).startswith("http"):
        self.source_url = str(text)
        
    def workdirButtonClicked(self):
      dir = QFileDialog.getExistingDirectory(self, "输出文件夹", "./") 
      self.workdir.setText(dir)
      self.word = WordCore(dir)

    def startProcess(self):
      self.process.setText("处理中...")
      try:
        status = self.word.load(self.config).process()
        if status:
          QMessageBox.information(self,"成功","运行成功请查看输出目录!")
      except AttributeError:
        QMessageBox.warning(self,"检查","请选择任务和输出文件夹！")
      except httpx.ConnectTimeout:
        try:
          self.word.load(self.config).process()
        except httpx.ConnectTimeout:
          QMessageBox.warning(self,"超时","请检查网络连接")
      finally:
        self.process.setText("开始任务")


    def myinit(self):
      if os.path.exists(self.tmpdir) == False:
        os.makedirs(self.tmpdir)
      for item in self.download():
        self.listWidget.addItem(item)

    def download(self):
      try:
        source = json.loads(httpx.get(self.source_url).content)

        for k,v in source.items():
          yield item("\n"+v.get("taskname")+"\n",v.get("icon"),k,v.get("author"),v.get("version"),v.get("config"),v.get("description"),self.tmpdir)
      except httpx.ConnectTimeout:
        if self._time == 0:
          pass
        self.download()
        self._time -= 1


def ui():
  """可视化界面
  """
  app = QApplication([])
  widget = fastdocx()
  # qssStyle = CommonHelper.readQss('./qss/black.qss')
  widget.setStyleSheet(stype)
  widget.show()
  widget.myinit()
  app.exec_()



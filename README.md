# FastDocx

FastDocx是一个自动化模块 帮助你快速依据模板生成word文档

## 安装
`pip install fastdocx -i https://pypi.org/simple`
## 示例

一行代码开启GUI界面，点击开始一键生成

```py
import fastdocx
fastdocx.ui()
```
![](https://s1.ax1x.com/2020/10/24/BZDFVe.png)
或者运行下面这段代码，目录下会自动生成word

```py
from fastdocx import WordCore

workspace = r"./"

(WordCore(workspace)
.load("https://v.gonorth.top:444/file/111111111111/config.json")
.process()
)
```

让我们看看`config.json`中是哪些内容

```py
{
    # 任务配置信息
    # 12位id，模板解析任务的唯一标识
    "id":"111111111111",
    # 任务名称
    "taskname":"测试任务",
    # 任务作者
    "author":"GoNorth",
    # 任务版本
    "version":"V0.0.1",
    # 任务描述
    "description":"这是一个测试任务，一帆风顺🤩",
    # 模板地址 URL/PATH
    "template":"https://v.gonorth.top:444/file/111111111111/template.docx",
    # 模板解析的内容
    "word":[{
        # 输出word名称
        "name":"1.docx",
        # 具体替换内容
        "content":[{
            # 将定位替换模板中{{A}}
            "key" : "A",
            # 类型 text/img/tab/br
            "type" : "text",
            # 支持填入返回str的函数
            "value" : "我是替换上去的标题"
            },{
            "key" : "B",
            "type" : "img",
            # 图片value支持 [path/stream/url,width,height]
            "value" : ["https://v.gonorth.top:444/file/111111111111/img/2.png"]
            },
            # 还可以加入其他关键字
            ]
        },
        # 继续填写其他生成的word内容
    ]
}
```

可以看到使用FastDocx可以利用json模板的方式，随时随地便捷地创建成批的Word文档

## 特点
 -  工作空间支持
 -  一键化解析，书写方便
 -  Gen your word everywhere，可以传入云端配置脚本随处生成
 -  支持json配置
 -  能够插入图片、表格、空行
 -  动态解析，字典中能传入函数作为内容
 -  高性能异步多线程下载引擎

## 设计

### 工作空间目录
    workspace -- {id} -- tmp -- template.docx     # word模板
                      |      |
                      |      |- index.json        # json配置信息
                      |      |
                      |      |- img -- 1.img      # 供插入的图片文件
                      |             |
                      |             |- 2.img      
                      |- out                      # 输出文件夹


## 高级使用

你可以根据下面的dict自定义输入，就像第一个例子里一样，你可以将这个json托管到cdn，由此你就能随处生成你的word文档

```py
from fastdocx import WordCore

basepath = r"./"

config = {
        "id":"111111111111",
        "taskname":"测试任务",
        "author":"GoNorth",
        "version":"V0.0.1",
        "description":"这是一个测试任务，一帆风顺🤩",
        "template":"https://v.gonorth.top:444/file/111111111111/template.docx",
        "word":[{
            "name":"out.docx",
            "content":[{
                "key" : "A",
                "type" : "text",
                "value" : "我是替换上去的标题"
                },{
                "key" : "B",
                "type" : "img",
                "value" : ["https://v.gonorth.top:444/file/111111111111/img/2.png"]
                }
                ]
            }
        ]}

(WordCore(basepath)
.load(config)
.process()
)
```

高级用法，你可以直接传入函数调用该模块

```py
from fastdocx import WordCore

basepath = r"./"

config = {
        "id":"111111111111",
        "taskname":"测试任务",
        "author":"GoNorth",
        "version":"V0.0.1",
        "description":"这是一个测试任务，一帆风顺🤩",
        "template":"https://v.gonorth.top:444/file/111111111111/template.docx",
        "word":[{
            "name":"out.docx",
            "content":[{
                "key" : "A",
                "type" : "text",
                "value" : lambda :"动态函数传入"
                },{
                "key" : "B",
                "type" : "img",
                "value" : [io.b]
                }
                ]
            }
        ]}

(WordCore(basepath)
.load(config)
.process()
)
```

## TODO

1. [x] PyQT GUI集成
2. [x] download 模块
3. [x] 遇到url自动下载图片并插入
4. [ ] 更好的图片支持（图例等）
5. [ ] 表格支持

# FastDocx

根据字典自动解析模板生成word文档

## 示例

运行`main.py`试试看，`example/out`会自动生成word

## 特点
 -  工作空间支持
 -  根据字典解析，书写方便
 -  支持json配置
 -  能够插入图片、表格、空行
 -  动态解析，能传入函数作为内容

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

### 配置字典示例

```py
{
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
            "key" : "A",
            "type" : "text",
            # 支持填入返回str的函数
            "value" : "我是替换上去的标题"
            },{
            "key" : "B",
            "type" : "img",
            # [path/stream/url,width,height]
            "value" : ["2.png"]
            },
          # 其他关键字锚点
          ]
      },
      # 其他生成的word
  ]
}
```
## 用法
1. 用模板语法书写word文档
2. 编写index.json、准备工作空间
3. `WordCore(basepath,index).process()`运行

## TODO

1. [ ] PyQT GUI集成
2. [x] download 模块
3. [ ] 遇到url自动下载图片并插入
4. [ ] 更好的图片支持（图例等）
5. [ ] 表格支持

# FastDocx

根据json自动解析模板生成word文档

## 特点
 -  工作空间支持
 -  根据json解析，书写方便
 -  能够插入图片、表格、空行

## 设计

### 工作空间目录
    workspace -- {id} -- tmp -- template.docx     # word模板
                      |      |
                      |      |- index.json        # json信息
                      |      |
                      |      |- img -- 1.img      # 供插入的图片文件
                      |             |
                      |             |- 2.img      
                      |- out                      # 输出文件夹

### index.json示例

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
          "key" : "这里插入表1",
          "type" : "text",
          "value" : "我是替换文字！！！"
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
2. [ ] download 模块
3. [ ] 更好的图片支持（图例等）
4. [ ] 表格支持
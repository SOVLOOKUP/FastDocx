from core.core import WordCore

basepath = r"./example"

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
            "key" : "A",
            "type" : "text",
            "value" : "我是替换上去的标题"
            },{
            "key" : "B",
            "type" : "img",
            "value" : ["2.png"]
            },
            # 其他关键字锚点
            ]
        },
        # 其他生成的word
    ]}

WordCore(basepath,index).process()
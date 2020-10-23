from fastdocx import WordCore

basepath = r"./"

(WordCore(basepath)
.load("https://v.gonorth.top:444/file/111111111111/config.json")
.process()
)
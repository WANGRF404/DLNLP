#Part 1

import os
from collections import Counter
import jieba
import re
import matplotlib.pyplot as plt

#导入语料库
txt = []
# 指定文件夹路径
folder_path = 'd:/Machine Learning/zipflaw_corpus/'

# 遍历文件夹中的所有文件
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path):
        with open(file_path, 'r', encoding='gb18030', errors='ignore') as file:
            content = file.read()
            txt.append(content)
txt = ''.join(txt)

# #加入要去除的标点符号
# extra_characters = open("d:/Machine Learning/zipflaw_corpus/cn_punctuation.txt", "r", encoding="gb18030", errors='ignore').read()

#利用jieba分词
words = jieba.lcut(txt)

#设置初始字典
counts = {}

#遍历计数
for word in words:
    counts[word] = counts.get(word,0)+1

#返回遍历得分所有键与值
items = list(counts.items())
print(len(items))

#根据词出现次序进行排序
items.sort(key=lambda x: x[1], reverse=True)
#sort_list用于绘图时的数据列表
sort_list = sorted(counts.values(), reverse=True)

#将数据写入txt文本
file = open('data1.txt', mode='w',encoding='utf-8')

#输出词语与词频
for i in range(10963):
    word, count = items[i]
    print("{0:<10}{1:>5}".format(word,count))

    #写入txt文件
    new_context = word + "   " + str(count) + '\n'
    file.write(new_context)

file.close()
result = open('re_match.txt', mode='w',encoding='utf-8')

#存正则匹配的数组
sentences = []

#正则匹配：人物说的内容
for i in re.finditer("“(.+)(\？|\！)”", txt):
    message = i.group(1)
    sentences.append(message)

#计数计数和并保存到re_match.txt
c = Counter(sentences)
for k, v in c.most_common(51):
    print(k, v)
    context = k + "   " + str(v) + '\n'
    result.write(context)

result.close()

#用matplotlib验证Zipf-Law
plt.title('Zipf-Law',fontsize=18)
plt.xlabel('rank',fontsize=18)  #排名
plt.ylabel('freq',fontsize=18) #频度
plt.yticks([pow(10,i) for i in range(0,4)])  # 设置y刻度
plt.xticks([pow(10,i) for i in range(0,4)])  # 设置x刻度
x = [i for i in range(len(sort_list))]
plt.yscale('log')#设置纵坐标的缩放
plt.xscale('log')
plt.plot(x, sort_list , 'r')
plt.savefig('./Zipf_Law.jpg')
plt.show()
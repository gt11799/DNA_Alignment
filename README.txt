DNA_Alignment
=============

compute the DNA alignment, and check spelling of given word.

算法课作业，要计算DNA的匹配。

- - - - - - - - - - - - - - -

alignmentCompute.py是使用Dynamic programming 计算字符串匹配的四个基本模块。

HumanEyelessProtein.txt 是人类致盲的蛋白质的序列

FruitflyEyelessProtein.txt 是果蝇致盲的蛋白质的序列

score_PAM50.txt 是给定的匹配定分标准，比如A与C匹配是－5，A与A匹配是10，诸如此类

ConsensusPAXDomain.txt 是通用蛋白质序列，上述两个蛋白质local匹配后的序列，再跟通用蛋白质序列匹配，看看相同的地方是否是蛋白质。

- - - - - - - - - - - - - - -

eyelessProteinAlign.py 是计算上述两个蛋白质匹配度的文档。匹配出的蛋白质再跟通用蛋白质匹配。为了验证结论，把通用蛋白质的序列打乱，跟通用蛋白质匹配，得出的分数跟前者对比。

- - - - - - - - - - - - - - -

statistical_hypothesis.py 是用统计方法去验证结论。把果蝇的蛋白质序列打乱，再跟人类的蛋白质去匹配，如此匹配1000次，可以得到一个正态分布。发现人类和果蝇的匹配所得到的分数在48倍的标准差的位置。这种事件是巧合的概率是0.（已经超过了python的精度）
其中还捎带着计算了一下大乐透的概率，比中大乐透的概率还要低。
scoring_distribuion.p 是数据缓存文档。里面存放着一个字典

- - - - - - - - - - - - - - -

spelling_correction.py
既然已经使用了字符串匹配，也可以进行拼写检查。从字典中读出正确的拼写，然后返回编辑距离为固定值的所有单词。
其中引用了Edit Distance，其中也有模块去寻找scoring matrix。

word_list.txt
里面含有7万多个正确拼写单词

- - - - - - - - - - - - - - -

test_afficiency.py
是测试模块效率的模块，跟本项目基本没有关系。
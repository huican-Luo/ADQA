# ADQA
构建基于老年痴呆领域知识图谱的问答系统。参考[https://github.com/zhihao-chen/QASystemOnMedicalGraph](https://github.com/zhihao-chen/QASystemOnMedicalGraph)

从知识爬虫-知识图谱问答功能构建。搭建一个小型的老年痴呆知识图谱(仅仅爬取老年痴呆第一层关系知识)，能够简单的实现基于老年痴呆的医疗知识问答。(麻雀虽小，五脏俱全)

# 项目运行方式
运行环境：Python3.7      数据库：neo4j
1、数据爬取：python climb_Alzheimer'_disease.py
2、搭建知识图谱：python build_AD_graph.py
3、启动问答测试：python AD_QA.py

# 老年痴呆知识图谱
数据来源：寻医问药网。

**知识图谱结构如下：**

**1.1 知识图谱实体类型**

| 实体类型     | 中文含义 | 举例                |
| ------------ | -------- | ------------------ |
| AD           | 疾病     | 老年痴呆           |
| Alias        | 别名     | 阿尔兹海默症        |
| Cause        | 病因     | 脑栓塞             |
| Diagnosis    | 诊断     | 抑郁症             |
| Infect_people| 患病人群 | 老年人             |
| Inspect_Type | 检查类型 | 海马像检查          |
| Department   | 所属科室 | 内科，神经内科      |
| Symptom      | 症状     | 记性不好，找不到方向|
| Nursing_Type | 护理种类 | 一般护理            |
| Prevent      | 预防     | 适度运动           |
| Prevent_Type | 预防种类 | 健康教育           |
| Neopathy     | 并发症   | 便秘               |
| Drug         | 药品     | 盐酸多奈哌齐片     |
| Treat        | 治疗     | 强化记忆           |
| Treat_type   | 治疗种类 | 心理治疗，药物治疗  |

**1.2 知识图谱疾病属性**

| 疾病属性  | 中文含义 |
| --------- | -------- | 
| cure_rate | 发病人群 | 
| describe  | 疾病描述 | 
| food      | 饮食方式 |
|infect_rate| 患病概率 | 
| infect_way| 传染性   |
| insurance | 医保情况 |
| money     | 花销     | 
| name      | 名称     | 
| nursing   | 护理     | 
| period    | 周期     | 

# 问题意图识别
贝叶斯分类 + 规则方法
分类模型预测的意图+基于规则筛选的意图，最终返回所有意图答案，所以往往有两个意图的答案返回。解决办法是训练一个精确的分类模型或者放弃分类器预测的方法，又或者对结果综合打分选择一个意图。一共识别20种意图类别，由于种类较多，自己训练效果不理想，故借用 [ https://github.com/zhihao-chen/QASystemOnMedicalGraph ] 的7分类模型+自定义规则筛选方法

# 总结
1、本项目构建简单，但麻雀虽小，五脏俱全，能够了解知识图谱建立过程。

2、对老年痴呆知识图谱的构建知识较少，可以收集更多层级的知识。

3、意图识别更多基于自定义规则，扩展性差。

4、实体识别方法有待改进。

#!/usr/bin/env python3
# coding: utf-8
from py2neo import Graph


class AnswerSearching:
    def __init__(self):
        self.graph = Graph("http://localhost:7474", username="neo4j", password="123456789")
        self.top_num = 10

    """
    根据不同的实体和意图构造cypher查询语句 
    data: {"AD":[], "Alias":[], "neopathy":[], "Symptom":[], "Cause":[], "intentions":[] }
    """
    def question_parser(self, data):
        sqls = []
        if data:
            for intent in data["intentions"]:
                sql_ = {}
                sql_["intention"] = intent
                sql = []
                if data.get("AD"):
                    sql = self.transfer_to_sql("AD", data["AD"], intent)
                elif data.get("Alias"):
                    sql = self.transfer_to_sql("Alias", data["Alias"], intent)
                elif data.get("Neopathy"):
                    sql = self.transfer_to_sql("Neopathy", data["Neopathy"], intent)
                elif data.get("Symptom"):
                    sql = self.transfer_to_sql("Symptom", data["Symptom"], intent)
                elif data.get("Cause"):
                    sql = self.transfer_to_sql("Cause", data["Cause"], intent)

                if sql:
                    sql_['sql'] = sql
                    sqls.append(sql_) # 存放字典结构 [ { 'intention': [] ,'sql' : [] }、 { 'intention': [],'sql' : [] }  ]
        return sqls

    """
    将问题转变为cypher查询语句
    """
    def transfer_to_sql(self, label, entities, intent):
        if not entities: # 没有实体返回空列表
            return []
        sql = []

        # 查询症状
        if intent == "query_symptom" and label == "AD":
            sql = ["MATCH (d:AD)-[:Has_Symptoms]->(s) WHERE d.name='{0}' RETURN d.name,s.name".format(e)
                   for e in entities]
        if intent == "query_symptom" and label == "Alias":
            sql = ["MATCH (a:Alias)<-[:Alias_Is]-(d:AD)-[:HAS_SYMPTOM]->(s) WHERE a.name='{0}' return " \
                   "d.name,s.name".format(e) for e in entities]

        # 查询治疗方法
        if intent == "query_cureway" and label == "AD":
            sql = ["MATCH (n)<-[:Has_Treat_Way]-(d:AD) WHERE d.name='{0}' return d.name,n.name".format(e) for e in entities]
        if intent == "query_cureway" and label == "Alias":
            sql = ["MATCH (n)<-[:Has_Treat_Way]-(d:AD)-[]->(a:Alias) WHERE a.name='{0}' return d.name" \
                   "n.name".format(e) for e in entities]
        if intent == "query_cureway" and label == "Symptom":
            sql = ["MATCH (n)<-[:Has_Treat_Way]-(d:AD)-[]->(s:Symptoms) WHERE s.name='{0}' " \
                   "return d.name, n.name".format(e) for e in entities]
        if intent == "query_cureway" and label == "Neopathy":
            sql = ["MATCH (n)<-[:Has_Treat_Way]-(d:AD)-[]->(c:Neopathy) WHERE c.name='{0}' " \
                   "return d.name, n.name".format(e) for e in entities]

        # 查询治疗药物
        if intent == "query_curedrug" and label == "AD":
            sql = ["MATCH (n)<-[:Has_Drug]-(d:AD) WHERE d.name='{0}' return d.name,n.name".format(e) for e in entities]
        if intent == "query_curedrug" and label == "Alias":
            sql = ["MATCH (n)<-[:Has_Drug]-(d:AD)-[]->(a:Alias) WHERE a.name='{0}' return d.name" \
                   "n.name".format(e) for e in entities]
        if intent == "query_curedrug" and label == "Symptom":
            sql = ["MATCH (n)<-[:Has_Drug]-(d:AD)-[]->(s:Symptoms) WHERE s.name='{0}' " \
                   "return d.name, n.name".format(e) for e in entities]
        if intent == "query_curedrug" and label == "Neopathy":
            sql = ["MATCH (n)<-[:Has_Drug]-(d:AD)-[]->(c:Neopathy) WHERE c.name='{0}' " \
                   "return d.name, n.name".format(e) for e in entities]

        # 查询治疗周期
        if intent == "query_period" and label == "AD":
            sql = ["MATCH (d:AD) WHERE d.name='{0}' return d.name,d.period".format(e) for e in entities]
        if intent == "query_period" and label == "Alias":
            sql = ["MATCH (d:AD)-[]->(a:Alias) WHERE a.name='{0}' return d.name,d.period".format(e)
                   for e in entities]
        if intent == "query_period" and label == "Symptom":
            sql = ["MATCH (d:AD)-[]->(s:Symptoms) WHERE s.name='{0}' return d.name,d.period".format(e)
                   for e in entities]
        if intent == "query_period" and label == "Neopathy":
            sql = ["MATCH (d:AD)-[]->(c:Neopathy) WHERE c.name='{0}' return d.name,d.period".format(e) for e in entities]

        # 查询治愈率
        if intent == "query_rate" and label == "AD":
            sql = ["MATCH (d:AD) WHERE d.name='{0}' return d.name,d.cure_rate".format(e) for e in entities]
        if intent == "query_rate" and label == "Alias":
            sql = ["MATCH (d:AD)-[]->(a:Alias) WHERE a.name='{0}' return d.name,d.cure_rate".format(e)
                   for e in entities]
        if intent == "query_rate" and label == "Symptom":
            sql = ["MATCH (d:AD)-[]->(s:Symptoms) WHERE s.name='{0}' return d.name,d.cure_rate".format(e)
                   for e in entities]
        if intent == "query_rate" and label == "Neopathy":
            sql = ["MATCH (d:AD)-[]->(c:Neopathy) WHERE c.name='{0}' return d.name," \
                   "d.cure_rate".format(e) for e in entities]

        # 查询检查项目
        if intent == "query_checklist" and label == "AD":
            sql = ["MATCH (d:AD)-[]-(a:Inspect_Type) WHERE d.name='{0}' return d.name,a.name".format(e) for e in entities]
        if intent == "query_checklist" and label == "Alias":
            sql = ["MATCH (a:Inspect_Type)-[]-(d:AD)-[]->(i:Alias) WHERE i.name='{0}' return d.name,a.name".format(e) for e in entities]
        if intent == "query_checklist" and label == "Symptom":
            sql = ["MATCH (a:Inspect_Type)-[]-(d:AD)-[]->(s:Symptoms) WHERE s.name='{0}' return d.name,a.name".format(e) for e in entities]
        if intent == "query_checklist" and label == "Neopathy":
            sql = ["MATCH (a:Inspect_Type)-[]-(d:Disease)-[]->(c:Neopathy) WHERE c.name='{0}' return d.name," \
                   "a.name".format(e) for e in entities]

        # 查询科室
        if intent == "query_department" and label == "AD":
            sql = ["MATCH (d:AD)-[:Department_Is ]->(n) WHERE d.name='{0}' return d.name," \
                   "n.name".format(e) for e in entities]
        if intent == "query_department" and label == "Alias":
            sql = ["MATCH (n)<-[:Department_Is]-(d:AD)-[:Alias_Is]->(a:Alias) WHERE a.name='{0}' " \
                   "return d.name,n.name".format(e) for e in entities]
        if intent == "query_department" and label == "Symptom":
            sql = ["MATCH (n)<-[:Department_Is]-(d:AD)-[:Has_Symptoms]->(s:Symptoms) WHERE s.name='{0}' " \
                   "return d.name,n.name".format(e) for e in entities]
        if intent == "query_department" and label == "Neopathy":
            sql = ["MATCH (n)<-[:Department_Is]-(d:AD)-[:Has_Neopathy]->(c:Neopathy) WHERE " \
                   "c.name='{0}' return d.name,n.name".format(e) for e in entities]

        # 已知症状，查询疾病
        if intent == "query_disease" and label == "Symptom":
            sql = ["MATCH (d:AD)-[]->(s:Symptoms) WHERE s.name='{0}' return " \
                   "d.name".format(e) for e in entities]

        # 查询病因
        if intent == "query_cause" and label == "AD":
            sql = ["MATCH (d:AD)-[]->(n:Cause) WHERE d.name='{0}' return " \
                   "d.name,n.name".format(e) for e in entities]
        if intent == "query_cause" and label == "Alias":
            sql = ["MATCH (n)<-[:Has_Cause]-(d:AD)-[:Alias_Is]->(a:Alias) WHERE a.name='{0}' " \
                   "return d.name,n.name".format(e) for e in entities]

        # 查询疾病描述
        if intent == "disease_describe" and label == "AD":
            sql = ["MATCH (d:AD) WHERE d.name='{0}' return d.name,d.describe".format(e) for e in entities]
        if intent == "disease_describe" and label == "Alias":
            sql = ["MATCH (d:AD)-[]->(a:Alias) WHERE a.name='{0}' return d.name,d.describe".format(e) for e in entities]
        if intent == "disease_describe" and label == "Symptom":
            sql = ["MATCH (d:AD)-[]->(s:Symptoms) WHERE s.name='{0}' return d.name,d.describe".format(e) for e in entities]
        if intent == "disease_describe" and label == "Neopathy":
            sql = ["MATCH (d:AD)-[]->(c:Neopathy) WHERE c.name='{0}' return d.name,d.describe".format(e) for e in entities]

        # 查询疾病别称
        if intent == "query_alias" and label == "AD":
            sql = ["MATCH (d:AD)-[]->(n:Alias) WHERE d.name='{0}' return d.name,n.name".format(e) for e in entities]

        # 查询疾病医保情况
        if intent == "query_insurance" and label == "AD":
            sql = ["MATCH (d:AD) WHERE d.name='{0}' return d.name,d.insurance".format(e) for e in entities]
        if intent == "disease_describe" and label == "Alias":
            sql = ["MATCH (d:AD)-[]->(a:Alias) WHERE a.name='{0}' return d.name,d.insurance".format(e) for e in entities]

        # 查询患病概率
        if intent == "query_infect_rate" and label == "AD":
            sql = ["MATCH (d:AD) WHERE d.name='{0}' return d.name,d.infect_rate".format(e) for e in entities]
        if intent == "query_infect_rate" and label == "Alias":
            sql = ["MATCH (d:AD)-[]->(a:Alias) WHERE a.name='{0}' return d.name,d.infect_rate".format(e) for e in entities]

        # 查询患病人群
        if intent == "query_infect_people" and label == "AD":
            sql = ["MATCH (n:Infect_People)<-[]-(d:AD) WHERE d.name='{0}' return d.name,n.name".format(e) for e in entities]
        if intent == "query_infect_people" and label == "Alias":
            sql = ["MATCH (n:Infect_People)-[]-(d:AD)-[]->(a:Alias) WHERE a.name='{0}' return d.name,n.name".format(e) for e in entities]

        # 查询传染性
        if intent == "query_infect_way" and label == "AD":
            sql = ["MATCH (d:AD) WHERE d.name='{0}' return d.name,d.infect_way".format(e) for e in entities]
        if intent == "query_infect_way" and label == "Alias":
            sql = ["MATCH (d:AD)-[]->(a:Alias) WHERE a.name='{0}' return d.name,d.infect_way".format(e) for e in entities]

        # 查询花销
        if intent == "query_money" and label == "AD":
            sql = ["MATCH (d:AD) WHERE d.name='{0}' return d.name,d.money".format(e) for e in entities]
        if intent == "query_money" and label == "Alias":
            sql = ["MATCH (d:AD)-[]->(a:Alias) WHERE a.name='{0}' return d.name,d.money".format(e) for e in entities]

        # 查询预防措施
        if intent == "query_prevent" and label == "AD":
            sql = ["MATCH (d:AD)-[]->(n:Prevent) WHERE d.name='{0}' return d.name,n.name".format(e) for e in entities]
        if intent == "query_prevent" and label == "Alias":
            sql = ["MATCH (n:Prevent)<-[]-(d:AD)-[]->(a:Alias) WHERE a.name='{0}' return d.name,n.name".format(e) for e in entities]

        # 查询疾病护理
        if intent == "query_nursing" and label == "AD":
            sql = ["MATCH (d:AD) WHERE d.name='{0}' return d.name,d.nursing".format(e) for e in entities]
        if intent == "query_prevent" and label == "Alias":
            sql = ["MATCH (d:AD)-[]->(a:Alias) WHERE a.name='{0}' return d.name,d.nursing".format(e) for e in entities]

        # 查询疾病饮食
        if intent == "query_food" and label == "AD":
            sql = ["MATCH (d:AD) WHERE d.name='{0}' return d.name,d.food".format(e) for e in entities]
        if intent == "query_food" and label == "Alias":
            sql = ["MATCH (d:AD)-[]->(a:Alias) WHERE a.name='{0}' return d.name,d.food".format(e) for e in entities]

        return sql

    """
    执行cypher查询，返回结果
    """
    def searching(self, sqls):
        final_answers = []
        for sql_ in sqls:
            intent = sql_['intention']
            queries = sql_['sql']
            answers = []
            for query in queries:
                ress = self.graph.run(query).data() # 返回列表，元素为字典格式
                answers += ress
            final_answer = self.answer_template(intent, answers)
            if final_answer:
                final_answers.append(final_answer)
        return final_answers

    """
    根据不同意图，返回不同模板的答案
    """
    def answer_template(self, intent, answers):
        final_answer = ""
        if not answers:
            return ""
        # 查询症状
        if intent == "query_symptom":
            disease_dic = {}
            for data in answers:
                d = data['d.name'] # 疾病名称
                s = data['s.name'] # 症状名称
                if d not in disease_dic:
                    disease_dic[d] = [s] # { " ": [] }
                else:
                    disease_dic[d].append(s)
            i = 0
            for k, v in disease_dic.items():  # [(m1,n1),(m2,n2),...]
                if i >= 10:
                    break
                final_answer += "{0}疾病的症状有：{1}\n".format(k, '、'.join(list(set(v)))) # 注意 += 说明答案在不断累加
                i += 1

        # 已知症状查询疾病概率
        if intent == "query_disease":
            disease_freq = {}
            for data in answers:
                d = data["d.name"]
                disease_freq[d] = disease_freq.get(d, 0) + 1 # 疾病名字次数累加
            n = len(disease_freq.keys())
            freq = sorted(disease_freq.items(), key=lambda x: x[1], reverse=True) # 按照次数排序
            for d, v in freq[:10]:
                final_answer += "疾病为{0}的概率为：{1}\n".format(d, v/10) # 这里简单的根据疾病名称出现的次数进行回答

        # 查询治疗方法
        if intent == "query_cureway":
            disease_tre = {}
            for data in answers: # 治疗方式
                disease = data['d.name']
                treat = data["n.name"]
                if disease not in disease_tre:
                    disease_tre[disease] = [treat]
                else:
                    disease_tre[disease].append(treat)
            i = 0
            for d, v in disease_tre.items():
                if i >= 20:
                    break
                final_answer += "{0}疾病的治疗方法有：{1}；\n".format(d,  '、'.join(v))
                i += 1

        # 查询治疗药物
        if intent == "query_curedrug":
            disease_drg = {}
            for data in answers[:2]:
                disease = data['d.name']
                drug = data["n.name"] # 前两个为药品
                if disease not in disease_drg:
                    disease_drg[disease] = [drug]
                else:
                    disease_drg[disease].append(drug)
            i = 0
            for d, v in disease_drg.items():
                if i >= 20:
                    break
                final_answer += "{0}疾病的可用药品包括：{1}\n".format(d, '、'.join(v))
                i += 1

        # 查询治愈周期
        if intent == "query_period":
            disease_dic = {}
            for data in answers:
                d = data['d.name']
                p = data['d.period']
                if d not in disease_dic:
                    disease_dic[d] = [p]
                else:
                    disease_dic[d].append(p)
            i = 0
            for k, v in disease_dic.items():
                if i >= 10:
                    break
                final_answer += "{0}疾病的治愈周期为：{1}\n".format(k, ','.join(list(set(v))))
                i += 1

        # 查询治愈率
        if intent == "query_rate":
            disease_dic = {}
            for data in answers:
                d = data['d.name']
                r = data['d.cure_rate']
                if d not in disease_dic:
                    disease_dic[d] = [r]
                else:
                    disease_dic[d].append(r)
            i = 0
            for k, v in disease_dic.items():
                if i >= 10:
                    break
                final_answer += "{0}疾病的治愈率为：{1}\n".format(k, ','.join(list(set(v))))
                i += 1

        # 查询检查项目
        if intent == "query_checklist":
            disease_dic = {}
            for data in answers:
                d = data['d.name']
                r = data['a.name']
                if d not in disease_dic:
                    disease_dic[d] = [r]
                else:
                    disease_dic[d].append(r)
            i = 0
            for k, v in disease_dic.items():
                if i >= 10:
                    break
                final_answer += "{0}疾病的检查项目有：{1}\n".format(k, '、'.join(list(set(v))))
                i += 1

        # 查询科室
        if intent == "query_department":
            disease_dic = {}
            for data in answers:
                d = data['d.name']
                r = data['n.name']
                if d not in disease_dic:
                    disease_dic[d] = [r]
                else:
                    disease_dic[d].append(r)
            i = 0
            for k, v in disease_dic.items():
                if i >= 10:
                    break
                final_answer += "{0}疾病所属科室有：{1}\n".format(k, '、'.join(list(set(v))))
                i += 1

        # 查询病因
        if intent == "query_cause":
            disease_dic = {}
            for data in answers:
                d = data['d.name']
                r = data['n.name']
                if d not in disease_dic:
                    disease_dic[d] = [r]
                else:
                    disease_dic[d].append(r)
            i = 0
            for k, v in disease_dic.items():
                if i >= 10:
                    break
                final_answer += "{0}疾病的病因可能为：{1}\n".format(k, '、'.join(list(set(v))))
                i += 1

        # 查询别称
        if intent == "query_alias":
            disease_dic = {}
            for data in answers:
                d = data['d.name']
                r = data['n.name']
                if d not in disease_dic:
                    disease_dic[d] = [r]
                else:
                    disease_dic[d].append(r)
            i = 0
            for k, v in disease_dic.items():
                if i >= 10:
                    break
                final_answer += "{0}疾病的别称为：{1}\n".format(k, '、'.join(list(set(v))))
                i += 1

        # 查询医保
        if intent == "query_insurance":
            disease_dic = {}
            for data in answers:
                d = data['d.name']
                r = data['d.insurance']
                if d not in disease_dic:
                    disease_dic[d] = [r]
                else:
                    disease_dic[d].append(r)
            i = 0
            for k, v in disease_dic.items():
                if i >= 10:
                    break
                final_answer += "{0}疾病的医保情况为：{1}\n".format(k, '、'.join(list(set(v))))
                i += 1

        # 查询患病概率
        if intent == "query_infect_rate":
            disease_dic = {}
            for data in answers:
                d = data['d.name']
                r = data['d.infect_rate']
                if d not in disease_dic:
                    disease_dic[d] = [r]
                else:
                    disease_dic[d].append(r)
            i = 0
            for k, v in disease_dic.items():
                if i >= 10:
                    break
                final_answer += "{0}疾病的患病概率为：{1}\n".format(k, '、'.join(list(set(v))))
                i += 1

        # 查询患病人群
        if intent == "query_infect_people":
            disease_dic = {}
            for data in answers:
                d = data['d.name']
                r = data['n.name']
                if d not in disease_dic:
                    disease_dic[d] = [r]
                else:
                    disease_dic[d].append(r)
            i = 0
            for k, v in disease_dic.items():
                if i >= 10:
                    break
                final_answer += "{0}疾病的患病人群为：{1}\n".format(k, '、'.join(list(set(v))))
                i += 1

        # 查询传染性
        if intent == "query_infect_way":
            disease_dic = {}
            for data in answers:
                d = data['d.name']
                r = data['d.infect_way']
                if d not in disease_dic:
                    disease_dic[d] = [r]
                else:
                    disease_dic[d].append(r)
            i = 0
            for k, v in disease_dic.items():
                if i >= 10:
                    break
                final_answer += "{0}疾病：{1}\n".format(k, '、'.join(list(set(v))))
                i += 1

        # 查询花销情况
        if intent == "query_money":
            disease_dic = {}
            for data in answers:
                d = data['d.name']
                r = data['d.money']
                if d not in disease_dic:
                    disease_dic[d] = [r]
                else:
                    disease_dic[d].append(r)
            i = 0
            for k, v in disease_dic.items():
                if i >= 10:
                    break
                final_answer += "{0}疾病的花销情况：{1}\n".format(k, '、'.join(list(set(v))))
                i += 1

        # 查询预防措施
        if intent == "query_prevent":
            disease_dic = {}
            for data in answers:
                d = data['d.name']
                r = data['n.name']
                if d not in disease_dic:
                    disease_dic[d] = [r]
                else:
                    disease_dic[d].append(r)
            i = 0
            for k, v in disease_dic.items():
                if i >= 10:
                    break
                final_answer += "{0}疾病的预防措施为：{1}\n".format(k, '、'.join(list(set(v))))
                i += 1

        # 查询护理方式
        if intent == "query_nursing":
            disease_dic = {}
            for data in answers:
                d = data['d.name']
                r = data['d.nursing']
                if d not in disease_dic:
                    disease_dic[d] = [r]
                else:
                    disease_dic[d].append(r)
            i = 0
            for k, v in disease_dic.items():
                if i >= 10:
                    break
                final_answer += "{0}疾病的护理方式为：{1}\n".format(k, '、'.join(list(set(v))))
                i += 1

        # 查询护理方式
        if intent == "query_food":
            disease_dic = {}
            for data in answers:
                d = data['d.name']
                r = data['d.food']
                if d not in disease_dic:
                    disease_dic[d] = [r]
                else:
                    disease_dic[d].append(r)
            i = 0
            for k, v in disease_dic.items():
                if i >= 10:
                    break
                final_answer += "{0}疾病的饮食建议为：{1}\n".format(k, '、'.join(list(set(v))))
                i += 1

        # 查询疾病描述
        if intent == "disease_describe":
            disease_infos = {}
            for data in answers:
                name = data['d.name']
                describe = data['d.describe']
                if name not in disease_infos:
                    disease_infos[name] = [describe]
                else:
                    disease_infos[name].append(describe)
            i = 0
            for k, v in disease_infos.items():
                if i >= 10:
                    break
                message = "{0}疾病的描述信息如下：{1}\n"
                final_answer += message.format(k, ''.join(v))
                i += 1

        return final_answer
#!/usr/bin/env python3
# coding: utf-8
from py2neo import Graph, Node
import pandas as pd
import os


class ADGraph:
    def __init__(self):
        cur_dir = os.path.dirname(__file__)
        self.data_path = os.path.join(cur_dir, 'data/AD.csv')
        self.graph = Graph("http://localhost:7474", username="neo4j", password="123456789")
        self.alias = []  # 别称
        self.infect_people = [] # 传染人群
        self.departments = []  # 科室
        self.drugs = []  # 药品
        self.cause = [] # 病因
        self.prevent = [] # 预防
        self.prevent_type = [] #预防种类
        self.neopathy = [] # 并发症
        self.symptoms = []  # 症状
        self.inspect = [] # 检查
        self.diagnosis = [] # 诊断
        self.treat = [] # 治疗方式
        self.treat_type = [] # 治疗种类
        self.nursing_type = [] # 护理种类
        # 疾病的属性：name, insurance,infect_rate, infect_way, period, cure_rate,money, describe,nursing,food
        self.AD_infos = []
        # 关系
        self.AD_to_alias = []  # AD与别称的关系
        self.AD_to_infect_people = [] # AD与感染人群的关系
        self.AD_to_department = []  # AD与科室关系
        self.AD_to_drug = []  # AD与药品关系
        self.AD_to_cause = []  # AD与病因关系
        self.AD_to_prevent = []  # AD与预防关系
        self.AD_to_prevent_type = [] # AD与预防种类的关系
        self.AD_to_neopathy = []  # AD与并发症关系
        self.AD_to_symptoms = []  # AD与症状的关系
        self.AD_to_inspect = []  # AD与检查的关系
        self.AD_to_diagnosis = []  # AD与诊断的关系
        self.AD_to_treat = []  # AD与治疗方式的关系
        self.AD_to_treat_type = []  # AD与治疗种类的关系
        self.AD_to_nursing_type = []  # AD与护理种类的关系
        self.AD_infos_dict = {}  # 疾病信息/属性


    '''
    读取文件，获得实体，实体关系
    cols = ["name", "insurance", "infect_rate","infect_people","infect_way","department", "period", "cure_rate","drug",
    "money", "describe", "cause","prevent","prevent_type", "neopathy", "symptom", "inspect", "diagnosis", "treat","treat_type",
    "nursing","nursing_type", "food"]
    '''
    def read_file(self):
        all_data = pd.read_csv(self.data_path, encoding='utf-8-sig').loc[:, :].values #按行展开数据
        for data in all_data:
            # 名称
            AD = data[0]
            self.AD_infos_dict["name"] = AD
            # 医保
            insurance = data[2]
            self.AD_infos_dict["insurance"] = insurance
            # 患病概率
            infect_rate = data[3]
            self.AD_infos_dict["infect_rate"] = infect_rate
            # 传染性
            infect_way = data[5]
            self.AD_infos_dict["infect_way"] = infect_way
            # 治疗周期
            period = data[7]
            self.AD_infos_dict["period"] = period
            # 治愈概率
            cure_rate = data[8]
            self.AD_infos_dict["cure_rate"] = cure_rate
            # 治疗金钱
            money = data[10]
            self.AD_infos_dict["money"] = money
            # 概述
            describe = data[11]
            self.AD_infos_dict["describe"] = describe
            # 护理
            nursing = data[21]
            self.AD_infos_dict["nursing"] = nursing
            # 食物
            food = data[23]
            self.AD_infos_dict["food"] = food
            # 疾病别称
            alias = data[1].split()
            for al in alias:
                self.alias.append(al)
                self.AD_to_alias.append([AD, al])
            # 患病人群
            infect_people = data[4]
            self.infect_people.append(infect_people)
            self.AD_to_infect_people.append([AD, infect_people])
            # 科室
            departments = data[6].split()
            for department in departments:
                self.departments.append(department)
                self.AD_to_department.append([AD, department])
            # 药物
            drugs = data[9].split()
            for drug in drugs:
                self.drugs.append(drug)
                self.AD_to_drug.append([AD, drug])
            # 病因
            cause = data[12].split()
            for cau in cause:
                self.cause.append(cau)
                self.AD_to_cause.append([AD, cau])
            # 预防
            prevent = data[13].split()
            for pre in prevent:
                self.prevent.append(pre)
                self.AD_to_prevent.append([AD, pre])
            # 预防种类
            prevent_type = data[14].split()
            for pre_typ in prevent_type:
                self.prevent_type.append(pre_typ)
                self.AD_to_prevent_type.append([AD, pre_typ])
            # 并发症
            neopathy = data[15].split()
            for neo in neopathy:
                self.neopathy.append(neo)
                self.AD_to_neopathy.append([AD, neo])
            # 症状
            symptoms = data[16].split()
            for sym in symptoms[:-1]:
                self.symptoms.append(sym)
                self.AD_to_symptoms.append([AD, sym])
            # 检查
            inspect = data[17].split()
            for ins in inspect:
                self.inspect.append(ins)
                self.AD_to_inspect.append([AD, ins])
            # 诊断
            diagnosis = data[18].split()
            for dig in diagnosis:
                self.diagnosis.append(dig)
                self.AD_to_diagnosis.append([AD, dig])
            # 治疗方式
            treat = data[19].split()
            for tre in treat:
                self.treat.append(tre)
                self.AD_to_treat.append([AD, tre])
            # 治疗种类
            treat_type = data[20].split()
            for tre in treat_type:
                self.treat_type.append(tre)
                self.AD_to_treat_type.append([AD, tre])
            # 护理种类
            nursing_type = data[22].split()
            for nur in nursing_type:
                self.nursing_type.append(nur)
                self.AD_to_nursing_type.append([AD, nur])

    """
    创建知识图谱实体
    """
    def create_graphNodes(self):
        print('开始创建疾病实体、属性节点')
        self.create_diseases_nodes(self.AD_infos_dict) # 创建疾病节点及其属性
        print('开始创建别称实体节点')
        self.create_node("Alias", self.alias)
        print('开始创建易感染群体实体节点')
        self.create_node("Infect_People", self.infect_people)
        print('开始创建部门实体节点')
        self.create_node("Department", self.departments)
        print('开始创建药物实体节点')
        self.create_node("Drug", self.drugs)
        print('开始创建病因实体节点')
        self.create_node("Cause", self.cause)
        print('开始创建预防实体节点')
        self.create_node("Prevent", self.prevent)
        print('开始创建预防种类实体节点')
        self.create_node("Prevent_Type", self.prevent_type)
        print('开始创建并发症实体节点')
        self.create_node("Neopathy", self.neopathy)
        print('开始创建症状实体节点')
        self.create_node("Symptoms", self.symptoms)
        print('开始创建检查实体节点')
        self.create_node("Inspect_Type", self.inspect)
        print('开始创建诊断实体节点')
        self.create_node("Diagnosis", self.diagnosis)
        print('开始创建治疗方式实体节点')
        self.create_node("Treat", self.treat)
        print('开始创建治疗种类实体节点')
        self.create_node("Treat_Type", self.treat_type)
        print('开始创建护理种类实体节点')
        self.create_node("Nursing_Type", self.nursing_type)

    """
    创建知识图谱实体关系
    """
    def create_graphRels(self):
        print('开始创建别称关系')
        self.create_relationship("AD", "Alias", self.AD_to_alias, "Alias_Is", "别称")
        print('开始创建患病人群关系')
        self.create_relationship("AD", "Infect_People", self.AD_to_infect_people, "Infect_People_Is", "患病人群")
        print('开始创建部门关系')
        self.create_relationship("AD", "Department", self.AD_to_department, "Department_Is", "部门")
        print('开始创建药品关系')
        self.create_relationship("AD", "Drug", self.AD_to_drug, "Has_Drug", "药品")
        print('开始创建病因关系')
        self.create_relationship("AD", "Cause", self.AD_to_cause, "Has_Cause", "病因")
        print('开始创建预防方式关系')
        self.create_relationship("AD", "Prevent", self.AD_to_prevent, "Has_Prevent_Way", "预防方式")
        print('开始创建预防种类关系')
        self.create_relationship("AD", "Prevent_Type", self.AD_to_prevent_type, "Has_Prevent_Type", "预防种类")
        print('开始创建并发症关系')
        self.create_relationship("AD", "Neopathy", self.AD_to_neopathy, "Has_Neopathy", "并发症")
        print('开始创建症状关系')
        self.create_relationship("AD", "Symptoms", self.AD_to_symptoms, "Has_Symptoms", "症状")
        print('开始创建检查关系')
        self.create_relationship("AD", "Inspect_Type", self.AD_to_inspect, "Has_Inspect_Type", "检查")
        print('开始创建诊断种类关系')
        self.create_relationship("AD", "Diagnosis", self.AD_to_diagnosis, "Has_Diagnosis_Way", "诊断种类")
        print('开始创建治疗方式关系')
        self.create_relationship("AD", "Treat", self.AD_to_treat, "Has_Treat_Way", "治疗方式")
        print('开始创建治疗种类关系')
        self.create_relationship("AD", "Treat_Type", self.AD_to_treat_type, "Has_Treat_Type", "治疗种类")
        print('开始创建护理种类关系')
        self.create_relationship("AD", "Nursing_Type", self.AD_to_nursing_type, "Has_Nursing_Type", "护理种类")


    """
    创建AD节点属性的方法 insurance,infect_rate, infect_way, period, cure_rate,money, describe,nursing,food
    """
    def create_diseases_nodes(self, AD_info):
        print('开始创建疾病节点及其属性')
        count = 0
        node = Node("AD", name=AD_info['name'], insurance=AD_info['insurance'],infect_rate=AD_info['infect_rate'],
                    infect_way=AD_info['infect_way'],period=AD_info['period'], cure_rate=AD_info['cure_rate'],
                    money=AD_info['money'], describe=AD_info['describe'],nursing=AD_info['nursing'],food=AD_info['food'])
        self.graph.create(node)
        count += 1
        print(count)


    """
    创建节点方法
    """
    def create_node(self, label, nodes):
        count = 0
        for node_name in nodes:
            node = Node(label, name=node_name)
            self.graph.create(node)
            count += 1
            print(count, len(nodes))

    """
    创建实体关系方法
    """
    def create_relationship(self, start_node, end_node, edges, rel_type, rel_name):
        count = 0
        # 去重处理
        set_edges = []
        for edge in edges:
            set_edges.append('###'.join(edge)) #合并
        all = len(set(set_edges))
        for edge in set(set_edges):
            edge = edge.split('###') #拆分
            p = edge[0] # AD
            q = edge[1] # 其他实体
            query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_node, end_node, p, q, rel_type, rel_name)
            try:
                self.graph.run(query)
                count += 1
                print(rel_type, count, all)
            except Exception as e:
                print(e)
        return

if __name__ == "__main__":
    handler = ADGraph()
    handler.read_file()
    handler.create_graphNodes()
    handler.create_graphRels()

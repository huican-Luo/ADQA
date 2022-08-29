#!/usr/bin/env python3
# coding: utf-8
import os
import ahocorasick
from sklearn.externals import joblib
import jieba
import numpy as np
import re
import string
from gensim.models import KeyedVectors
import pandas as pd

class Recognition:
    def __init__(self):
        cur_dir = os.path.dirname(__file__)
        data_dir = './data/'
        # 路径
        self.vocab_path = os.path.join(cur_dir, 'data/vocab.txt') # 词表路径
        self.stopwords_path =os.path.join(cur_dir, 'data/stop_words.utf8') # 停词表路径
        self.stopwords = [w.strip() for w in open(self.stopwords_path, 'r', encoding='utf8') if w.strip()]
        # 意图分类模型文件
        self.tfidf_path = os.path.join(cur_dir, 'model/tfidf_model.m')
        self.nb_path = os.path.join(cur_dir, 'model/intent_reg_model.m')  # 朴素贝叶斯模型
        self.tfidf_model = joblib.load(self.tfidf_path) # 加载模型
        self.nb_model = joblib.load(self.nb_path)
        # 词表路径
        self.AD_path = data_dir + 'AD_vocab.txt'
        self.Alias_path = data_dir + 'Alias_vocab.txt'
        self.symptom_path = data_dir + 'symptom_vocab.txt'
        self.neopathy_path = data_dir + 'neopathy_vocab.txt'
        self.cause_path = data_dir + 'cause_vocab.txt'
        # 5个主要实体
        self.AD_entities = [w.strip() for w in open(self.AD_path, encoding='utf-8-sig') if w.strip()]
        self.Alias_entities = [w.strip() for w in open(self.Alias_path, encoding='utf-8-sig') if w.strip()]
        self.symptom_entities = [w.strip() for w in open(self.symptom_path, encoding='utf-8-sig') if w.strip()]
        self.neopathy_entities = [w.strip() for w in open(self.neopathy_path, encoding='utf-8-sig') if w.strip()]
        self.cause_entities = [w.strip() for w in open(self.cause_path, encoding='utf-8-sig') if w.strip()]
        self.region_words = list(set(self.AD_entities+self.symptom_entities+self.neopathy_entities+self.cause_entities)) # 总的实体
        self.result = {} #提取结果

        # 构造领域actree
        self.AD_tree = self.build_actree(list(set(self.AD_entities)))
        self.Alias_tree = self.build_actree(list(set(self.Alias_entities)))
        self.symptom_tree = self.build_actree(list(set(self.symptom_entities)))
        self.neopathy_tree = self.build_actree(list(set(self.neopathy_entities)))
        self.cause_tree = self.build_actree(list(set(self.cause_entities)))
        # 问题中的疑问、特征词
        self.symptom_qwds = ['什么症状', '哪些症状', '症状有哪些', '症状是什么', '什么表征', '哪些表征', '表征是什么',
                             '什么现象', '哪些现象', '现象有哪些', '症候', '什么表现', '哪些表现', '表现有哪些',
                             '什么行为', '哪些行为', '行为有哪些', '什么状况', '哪些状况', '状况有哪些', '现象是什么',
                             '表现是什么', '行为是什么']  # 询问症状
        self.cureway_qwds = ['怎么办', '怎么治疗', '如何医治', '怎么医治', '怎么治', '怎么医', '如何治',
                             '医治方式', '疗法', '咋治', '咋办', '咋治', '治疗方法']  # 询问治疗方法
        self.curedrug_qwds = ['药', '药品', '用药', '胶囊', '口服液', '炎片', '吃什么药', '用什么药',
                             '买什么药']  # 询问治疗药物
        self.lasttime_qwds = ['周期', '多久', '多长时间', '多少时间', '几天', '几年', '多少天', '多少小时',
                              '几个小时', '多少年', '多久能好', '痊愈', '康复']  # 询问治疗周期
        self.cureprob_qwds = ['多大概率能治好', '多大几率能治好', '治好希望大么', '几率', '几成', '比例',
                              '可能性', '能治', '可治', '可以治', '可以医', '能治好吗', '可以治好吗', '会好吗',
                              '能好吗', '治愈吗']  # 询问治愈率
        self.check_qwds = ['检查什么', '检查项目', '哪些检查', '什么检查', '检查哪些', '项目', '检测什么',
                           '哪些检测', '检测哪些', '化验什么', '哪些化验', '化验哪些', '哪些体检', '怎么查找',
                           '如何查找', '怎么检查', '如何检查', '怎么检测', '如何检测']  # 询问检查项目
        self.belong_qwds = ['属于什么科', '什么科', '科室', '挂什么', '挂哪个', '哪个科', '哪些科','科']  # 询问科室
        self.cause_qwds = ['什么原因', '怎么造成的', '原因是什么', '怎么导致', '诱导', '原因', '造成',
                            '病因是', '病因', '源头', '源头是什么']  # 询问病因
        self.disease_qwds = ['什么病', '啥病', '得了什么', '得了哪种', '怎么回事', '咋回事', '回事',
                            '什么情况', '什么问题', '什么毛病', '啥毛病', '哪种病']  # 询问疾病
        self.alias_qwds = ['又名','别称','叫','叫什么','又名为','称呼'] # 询问别称
        self.insurance_qwds = ['是否有','医保','报销','属于医保'] # 询问医保情况
        self.infect_rate_qwds = ['患病概率','概率','容易','容易得','容易患','几率','几率大不大','几率大不','常见吗','会老年痴呆','会得'] # 询问患病概率
        self.infect_people_qwds = ['人群','什么年龄','针对','年轻人会得','容易患','哪类','哪些人','哪种人','年龄段'] # 询问患病人群
        self.infect_way_qwds = ['传染性','传染','是否传染','染'] # 询问传染性
        self.money_qwds = ['花多少','多少钱','钱','money','要多少','费用','花销'] # 询问花销
        self.prevent_qwds = ['预防','应对','方法','缓解','防止','防治','减缓'] # 询问预防措施
        self.nursing_qwds = ['护理','照顾','康复'] # 询问护理方式
        self.food_qwds = ['吃','营养品','食物','保健品'] # 询问饮食

    """
    构造actree，加速过滤
    """
    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        # 向树中添加单词
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    """
    模式匹配, 得到匹配的词和类型。如老年痴呆别名，并发症，症状，病因
    """
    def entity_reg(self, question):
        for i in self.AD_tree.iter(question): #识别一段话中是否存在AC树中的实体并返回
            word = i[1][1]
            if "AD" not in self.result:
                self.result["AD"] = [word] #值对应的是一个列表
            else:
                self.result["AD"].append(word) #值的列表中添加元素，即实体

        for i in self.Alias_tree.iter(question):
            word = i[1][1]
            if "Alias" not in self.result:
                self.result["Alias"] = [word]
            else:
                self.result["Alias"].append(word)

        for i in self.symptom_tree.iter(question):
            wd = i[1][1]
            if "Symptom" not in self.result:
                self.result["Symptom"] = [wd]
            else:
                self.result["Symptom"].append(wd)

        for i in self.neopathy_tree.iter(question):
            wd = i[1][1]
            if "Neopathy" not in self.result:
                self.result["Neopathy"] = [wd]
            else:
                self.result["Neopathy"].append(wd)

        for i in self.cause_tree.iter(question):
            wd = i[1][1]
            if "Cause" not in self.result:
                self.result["Cause"] = [wd]
            else:
                self.result["Cause"].append(wd)

        return self.result


    """
    当全匹配失败时，就采用相似度计算来找相似的词
    """
    def find_sim_words(self, question):
        jieba.load_userdict(self.vocab_path) # 自定义词库
        sentence = re.sub("[{}]", re.escape(string.punctuation), question) # string.punctuation 返回所有的标点符号
        sentence = re.sub("[，。‘’；：？、！【】]", " ", sentence)
        sentence = sentence.strip()
        words = [w.strip() for w in jieba.cut(sentence) if w.strip() not in self.stopwords and len(w.strip()) >= 2] #问题中提取的实体

        scores_list = []
        for word in words:
            temp_entities = [self.AD_entities,self.Alias_entities, self.neopathy_entities, self.symptom_entities, self.cause_entities]
            for i in range(len(temp_entities)):
                if i == 0:
                    flag = "AD"
                elif i == 1:
                    flag = "Alias"
                elif i == 2:
                    flag = "Neopathy"
                elif i == 3:
                    flag = "Symptom"
                else:
                    flag = "Cause"
                scores = self.simCal(word, temp_entities[i], flag) # 判断问题中的实体与5种类别下的哪个实体最相似
                scores_list.extend(scores)
        sorted_scores = sorted(scores_list, key=lambda k: k[1], reverse=True) # scores里面为元组，第二项是分数
        if sorted_scores:
            self.result[sorted_scores[0][2]] = [sorted_scores[0][0]] # temp1[0][2] 排序当中的第一个元组的标签  temp1[0][0] 排序当中的第一个元组的实体

    """
    计算词语和字典中的词的相似度
    """
    def simCal(self, word, entities, flag):
        word_length = len(word)
        scores = []
        for entity in entities:
            sim_num = 0
            entity_length = len(entity)
            all_length = len(set(entity+word))
            temp = []
            for w in word:
                if w in entity: # 如果字符和在实体中存在，sim_num+1 最后判断相似度之和
                    sim_num += 1

            if sim_num != 0:
                score1 = sim_num / all_length  # overlap score 交并比
                temp.append(score1)

            score2 = 1 - self.editDistanceDP(word, entity) / (word_length + entity_length)  # 编辑距离分数
            if score2:
                temp.append(score2)
            score = sum(temp) / len(temp) # 相似度分数取平均
            if score >= 0.7:  #设置阈值，只有实体相似度大于0.7时才添加在表中，最后进行排序
                scores.append((entity, score, flag))

        scores.sort(key=lambda k: k[1], reverse=True)
        return scores

    """
    采用DP方法计算编辑距离
    """
    def editDistanceDP(self, s1, s2):
        m = len(s1)
        n = len(s2)
        solution = [[0 for j in range(n + 1)] for i in range(m + 1)]
        for i in range(len(s2) + 1):
            solution[0][i] = i
        for i in range(len(s1) + 1):
            solution[i][0] = i

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s1[i - 1] == s2[j - 1]:
                    solution[i][j] = solution[i - 1][j - 1]
                else:
                    solution[i][j] = 1 + min(solution[i][j - 1], min(solution[i - 1][j],
                                                                     solution[i - 1][j - 1]))
        return solution[m][n]

    """
    提取问题的TF-IDF特征
    """
    def tfidf_features(self, text, vectorizer):
        jieba.load_userdict(self.vocab_path)
        words = [w.strip() for w in jieba.cut(text) if w.strip() and w.strip() not in self.stopwords]
        sents = [' '.join(words)] # 先合并成字符串再转换成列表
        tfidf = vectorizer.transform(sents).toarray()
        return tfidf

    """
    提取问题的关键词特征
    """
    def other_features(self, text):
        features = [0] * 7 # 7个问题类别
        for d in self.disease_qwds:
            if d in text:
                features[0] += 1

        for s in self.symptom_qwds:
            if s in text:
                features[1] += 1

        for c in self.cureway_qwds:
            if c in text:
                features[2] += 1

        for c in self.check_qwds:
            if c in text:
                features[3] += 1
        for p in self.lasttime_qwds:
            if p in text:
                features[4] += 1

        for r in self.cureprob_qwds:
            if r in text:
                features[5] += 1

        for d in self.belong_qwds:
            if d in text:
                features[6] += 1

        m = max(features)
        n = min(features)
        normed_features = []
        if m == n:
            normed_features = features
        else:
            for i in features:
                j = (i - n) / (m - n) # 归一化特征
                normed_features.append(j)

        return np.array(normed_features)

    """
    预测意图
    """
    def model_predict(self, x, model):
        pred = model.predict(x)
        return pred

    """
    基于特征词分类
    """
    def check_words(self, wds, sent): # sent是字符类型--问题
        for wd in wds:
            if wd in sent:
                return True
        return False

    # 实体抽取主函数
    def extractor(self, question):
        self.entity_reg(question) # 判断是否提取实体
        if not self.result:
            self.find_sim_words(question)

        types = []  # 实体类型
        for v in self.result.keys():
            types.append(v)

        intentions = []  # 查询意图

        # 意图预测
        tfidf_feature = self.tfidf_features(question, self.tfidf_model)
        other_feature = self.other_features(question) # 问题特征提取
        m = other_feature.shape
        other_feature = np.reshape(other_feature, (1, m[0]))
        feature = np.concatenate((tfidf_feature, other_feature), axis=1) # 特征合并
        predicted = self.model_predict(feature, self.nb_model) # 意图预测
        intentions.append(predicted[0])

        # 已知疾病，查询症状
        if self.check_words(self.symptom_qwds, question) and ('AD' in types or 'Alias' in types): # 症状特征词在问题里存在并且 疾病实体在提取的实体集合types里面
            intention = "query_symptom"
            if intention not in intentions:
                intentions.append(intention)
        # 已知疾病或症状，查询治疗方法
        if self.check_words(self.cureway_qwds, question) and \
                ('AD' in types or 'Alias' in types or 'Symptom' in types or 'Neopathy' in types):
            intention = "query_cureway"
            if intention not in intentions:
                intentions.append(intention)
        # 已知疾病或症状，查询治疗药物
        if self.check_words(self.curedrug_qwds, question) and \
                ('AD' in types or 'Alias' in types or 'Symptom' in types or 'Neopathy' in types):
            intention = "query_curedrug"
            if intention not in intentions:
                intentions.append(intention)
        # 已知疾病，查询治疗周期
        if self.check_words(self.lasttime_qwds, question) and ('AD' in types or 'Alias' in types):
            intention = "query_period"
            if intention not in intentions:
                intentions.append(intention)
        # 已知疾病，查询治愈率
        if self.check_words(self.cureprob_qwds, question) and ('AD' in types or 'Alias' in types):
            intention = "query_rate"
            if intention not in intentions:
                intentions.append(intention)
        # 已知疾病，查询检查项目
        if self.check_words(self.check_qwds, question) and ('AD' in types or 'Alias' in types):
            intention = "query_checklist"
            if intention not in intentions:
                intentions.append(intention)
        # 已知疾病、症状，查询科室
        if self.check_words(self.belong_qwds, question) and \
                ('AD' in types or 'Alias' in types or 'Symptom' in types):
            intention = "query_department"
            if intention not in intentions:
                intentions.append(intention)
        # 已知症状，查询疾病
        if self.check_words(self.disease_qwds, question) and ("Symptom" in types):
            intention = "query_disease"
            if intention not in intentions:
                intentions.append(intention)
        # 已知疾病，查询病因
        if self.check_words(self.cause_qwds, question) and ("AD" in types or 'Alias' in types):
            intention = "query_cause"
            if intention not in intentions:
                intentions.append(intention)
        # 已知疾病，查询别称
        if self.check_words(self.alias_qwds, question) and ("AD" in types):
            intention = "query_alias"
            if intention not in intentions:
                intentions.append(intention)
        # 已知疾病，查询医保
        if self.check_words(self.insurance_qwds, question) and ("AD" in types or 'Alias' in types):
            intention = "query_insurance"
            if intention not in intentions:
                intentions.append(intention)
        # 已知疾病，查询疾病描述
        if self.check_words(self.disease_qwds, question) and ("AD" in types or 'Alias' in types):
            intention = "disease_describe"
            if intention not in intentions:
                intentions.append(intention)
        # 已知疾病，查询患病概率
        if self.check_words(self.infect_rate_qwds, question) and ("AD" in types or 'Alias' in types):
            intention = "query_infect_rate"
            if intention not in intentions:
                intentions.append(intention)
        # 已知疾病，查询疾病患病人群
        if self.check_words(self.infect_people_qwds, question) and ("AD" in types or 'Alias' in types):
            intention = "query_infect_people"
            if intention not in intentions:
                intentions.append(intention)
        # 已知疾病，查询疾病传染性
        if self.check_words(self.infect_way_qwds, question) and ("AD" in types or 'Alias' in types):
            intention = "query_infect_way"
            if intention not in intentions:
                intentions.append(intention)
        # 已知疾病，查询疾病花销
        if self.check_words(self.money_qwds, question) and ("AD" in types or 'Alias' in types):
            intention = "query_money"
            if intention not in intentions:
                intentions.append(intention)
        # 已知疾病，查询疾病预防措施
        if self.check_words(self.prevent_qwds, question) and ("AD" in types or 'Alias' in types):
            intention = "query_prevent"
            if intention not in intentions:
                intentions.append(intention)
        # 已知疾病，查询疾病护理方式
        if self.check_words(self.nursing_qwds, question) and ("AD" in types or 'Alias' in types):
            intention = "query_nursing"
            if intention not in intentions:
                intentions.append(intention)
        # 已知疾病，查询疾病饮食
        if self.check_words(self.food_qwds, question) and ("AD" in types or 'Alias' in types):
            intention = "query_food"
            if intention not in intentions:
                intentions.append(intention)
        # 若没有检测到意图，且已知疾病，则返回疾病的描述
        if not intentions and ('AD' in types or 'Alias' in types):
            intention = "disease_describe"
            if intention not in intentions:
                intentions.append(intention)
        # 若是疾病和症状同时出现，且出现了查询疾病的特征词，则意图为查询疾病
        if self.check_words(self.disease_qwds, question) and ('AD' in types or 'Alias' in types) \
                and ("Symptom" in types or "Neopathy" in types):
            intention = "query_disease"
            if intention not in intentions:
                intentions.append(intention)
        # 若没有识别出实体或意图则调用其它方法
        if not intentions or not types:
            intention = "QA_matching"
            if intention not in intentions:
                intentions.append(intention)

        self.result["intentions"] = intentions

        return self.result
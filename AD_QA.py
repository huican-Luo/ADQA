#!/usr/bin/env python3
# coding: utf-8

from Entity_Intention_recognition import Recognition
from search_answer import AnswerSearching


class KBQA:
    def __init__(self):
        self.extractor = Recognition()
        self.searcher = AnswerSearching()

    def qa_main(self, input_str):
        answer = "Sorry，这个问题我也不知道，我会持续进化的。"
        entities = self.extractor.extractor(input_str)
        if not entities:
            return answer
        sqls = self.searcher.question_parser(entities)
        final_answer = self.searcher.searching(sqls)
        if not final_answer:
            return answer
        else:
            return '\n'.join(final_answer)


if __name__ == "__main__":
    handler = KBQA()
    while True:
        question = input("你可以寻问关于老年痴呆的任何问题，只要我会：")
        if not question:
            break
        answer = handler.qa_main(question)
        print("华佗：\n", answer)
        print("*"*300)

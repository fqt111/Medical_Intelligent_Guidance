"""
	https://github.com/facebookresearch/fastText
"""
# -*- coding: utf-8 -*-
import fasttext
from sklearn.metrics import classification_report

def train():
	model = fasttext.train_supervised("train.txt", lr=0.1, dim=200,
			                 epoch=40, word_ngrams=2,bucket= 2000000, loss='softmax')
	model.save_model("model.bin")


def test():
	classifier = fasttext.load_model("../model.bin")

	#批量测试
	# result = classifier.test("dev_back.txt")
	# #print(classifier.predict("abcde"))
	# print(result)
	
	#单个测试
	real_labels = []
	pred_labels = []
	with open("dev.txt", "r", encoding="utf-8") as reader:
		#print(reader)
		for line in reader:
			#import pdb;pdb.set_trace()
			real_labels.append(line.split()[0])
			pred_labels.append(classifier.predict([line.strip()[1:]])[0][0][0])
	report = classification_report(real_labels, pred_labels)
	print(report)

if __name__ == "__main__":
	# train()
	test()

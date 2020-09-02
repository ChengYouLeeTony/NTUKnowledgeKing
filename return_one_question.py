import random

def return_one(index, index2):
  data_path = "./data_king/"
  # index = int(random.random() * 9)
  new_data_path = data_path + str(index) + '.csv'
  with open(new_data_path , 'r') as f:
    question_list = []
    while True:
      i = f.readline().strip()
      if i=='': break
      question_list.append(i)
    # index2 = int(random.random() * len(question_list))
    one_question = question_list[index2].split(',')
    if len(one_question) == 5:
      question = one_question[0]
      choice_1 = one_question[1]
      choice_2 = one_question[2]
      choice_3 = one_question[3]
      answer = one_question[4]
    return question, choice_1, choice_2, choice_3, answer
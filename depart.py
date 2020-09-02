def depart():
  data_path = "./data_king/"
  with open("king.csv" , 'r') as f:
    count = -1
    while True:
      i = f.readline().strip().strip('★').strip('#').strip(',')
      if '\"' not in i:
        count += 1
        if i=='': break
        if count % 500 == 0:
          f_w = open(data_path + str(int(count / 500)) + '.csv' , 'w')
        f_w.write(i)
        f_w.write('\n')

depart()
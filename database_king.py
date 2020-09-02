import sys
import pymongo
import time
import random

def find_db():
  uri = 'mongodb://heroku_tn484cn6:okmlvoolpgrfiood5dh87v6mlo@ds053148.mlab.com:53148/heroku_tn484cn6'
  client = pymongo.MongoClient(uri)
  db = client.get_default_database()['king']
  return db

def initSeting(userId):
  uri = 'mongodb://heroku_tn484cn6:okmlvoolpgrfiood5dh87v6mlo@ds053148.mlab.com:53148/heroku_tn484cn6'
  client = pymongo.MongoClient(uri)
  db = client.get_default_database()['king']
  try:
    cursor = db.find_one({'userId': userId})
    cursor['userId']
    return True
  except:
    userRemain = [i for i in range(4364)]
    db.insert({'userId': userId, 'userName': "", 'userPoint' : 0, 'userWrong' : 0, 'userRate' : 0, 'userSexual' : 0, 'userRemain' : userRemain, 'userStatus' : "$start"})
    return False

def userStatus(userId):
  db = find_db()
  try:
    cursor = db.find_one({'userId': userId})
    userStatus = cursor['userStatus']
    return userStatus
  except:
    return "un_status"

def userSexual(userId):
  db = find_db()
  try:
    cursor = db.find_one({'userId': userId})
    userSexual = cursor['userSexual']
    return userSexual
  except:
    return "un_status"

def set_userName(userId, userName):
  db = find_db()
  myquery = {'userId': userId}
  db.update(myquery, {'$set': {'userName': userName, 'userStatus' : 'has_name'}})

def set_userSexual(userId, userSexual):
  db = find_db()
  myquery = {'userId': userId}
  db.update(myquery, {'$set': {'userSexual': userSexual}})

def re_userName(userId):
  db = find_db()
  myquery = {'userId': userId}
  db.update(myquery, {'$set': {'userName': "", 'userStatus' : '$start'}})

def index_index2(userId):
  db = find_db()
  cursor = db.find_one({'userId': userId})
  if len(cursor['userRemain']) == 0:
    return "wrong", 0
  which = int(random.random() * len(cursor['userRemain']))
  number = cursor['userRemain'][which]
  print(number)
  del cursor['userRemain'][which]
  myquery = {'userId': userId}
  db.update(myquery, {'$set': {'userRemain' : cursor['userRemain']}})
  index = int(number / 500)
  index2 = int(number % 500)
  return index, index2

def change_status(userId, answer):
  db = find_db()
  myquery = {'userId': userId}
  db.update(myquery, {'$set': {'userStatus' : answer}})

def after_answer(userId, wrongOrCorrect):
  db = find_db()
  myquery = {'userId': userId}
  #答對
  if wrongOrCorrect == 1:
    db.update(myquery, {'$set': {'userStatus' : 'has_name'}, '$inc': {'userPoint': 1}})
  #答錯
  elif wrongOrCorrect == 0:
    db.update(myquery, {'$set': {'userStatus' : 'has_name'}, '$inc': {'userWrong': 1}})
  cursor = db.find_one({'userId': userId})
  userPoint = cursor['userPoint']
  userWrong = cursor['userWrong']
  userRate = int(userPoint / (userPoint + userWrong) * 10000)
  db.update(myquery, {'$set': {'userRate' : userRate}})

def user_point(userId):
  db = find_db()
  try:
    cursor = db.find_one({'userId': userId})
    userPoint = cursor['userPoint']
    userWrong = cursor['userWrong']
    if userPoint != 0 or userWrong != 0:
      userRate = int(userPoint / (userPoint + userWrong) * 10000)
      return userPoint, userWrong, userRate
    else:
      return "wrong", 0, 0
  except:
    return "wrong", 0, 0

def find_max_point():
  db = find_db()
  cursor = db.find({}, {'userName' : 1, "userPoint" : 1, "_id" : 0}).sort([('userPoint' , -1)])
  max_list = []
  max_list_point = []
  for i in range(cursor.count()):
    max_list.append(cursor[i]['userName'])
    max_list_point.append(cursor[i]['userPoint'])
  return max_list, max_list_point

def find_max_rate():
  db = find_db()
  cursor = db.find({}, {'userName' : 1, "userRate" : 1, 'userPoint' : 1, "_id" : 0}).sort([('userRate' , -1)])
  max_list = []
  max_list_rate = []
  for i in range(cursor.count()):
    if cursor[i]['userPoint'] >= 30:
      max_list.append(cursor[i]['userName'])
      max_list_rate.append(cursor[i]['userRate'])
  return max_list, max_list_rate

def user_name(userId):
  db = find_db()
  cursor = db.find_one({'userId': userId})
  return cursor['userName']

def judge_pure_english(keyword):
    return all(ord(c) < 128 for c in keyword)





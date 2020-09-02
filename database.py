import sys
import pymongo
import time
import random
### Standard URI format: mongodb://[dbuser:dbpassword@]host:port/dbname
# uri = 'mongodb://heroku_tn484cn6:okmlvoolpgrfiood5dh87v6mlo@ds053148.mlab.com:53148/heroku_tn484cn6'
# ### Create seed data
# SEED_DATA = [
#     {
#         'location': '公館',
#         'food_kind': '麵',
#         'restaurant': ['右手餐廳'],
#         'menu': ['http://lenadepp123.pixnet.net/blog/post/338123207-%5B%E9%A3%9F%E8%A8%98%5D%E5%8F%B3%E6%89%8B%E9%A4%90%E5%BB%B3thaihand%E2%99%A5%E5%8F%B0%E5%8C%97%E5%85%AC%E9%A4%A8%E6%96%B0%E9%96%8B%E5%B9%95%E6%B3%B0%E5%BC%8F'],
#         'size' : 1,
#         'newtime' : ['Wed May  2 16:17:48 2018'],
#     },
#     {
#         'location': '台大',
#         'food_kind': '飯',
#         'restaurant': ['左手餐廳'],
#         'menu': ['100台北市中正區羅斯福路三段307號'],
#         'size' : 1,
#         'newtime' : ['Wed May  2 16:17:48 2018'],
#     },
#     {
#         'location': '公館',
#         'food_kind': '小吃',
#         'restaurant': ['左右手餐廳'],
#         'menu': ['100台北市中正區羅斯福路三段308號'],
#         'size' : 1,
#         'newtime' : ['Wed May  2 16:17:48 2018'],
#     }
# ]
###############################################################################
# main
###############################################################################
def find_info(db, location, food_kind):
  cursor = db.find_one({'location': location, 'food_kind': food_kind})
  try:
    restaurant_list = cursor["restaurant"]
    menu_list = cursor["menu"]
    index = int(random.random() * cursor["size"])
    return restaurant_list[index], menu_list[index]
  except:
    return "null", "null"


def new_restaurant(db, location, food_kind, restaurant, menu = "null"):
  newtime = time.asctime(time.localtime(time.time()))
  found = True
  try:
      cursor = db.find_one({'location': location, 'food_kind': food_kind})
      cursor["restaurant"]
  except:
    found = False
  #如果地點或種類沒有，直接新增餐廳資訊
  if found == False:
    db.insert({'location': location, 'food_kind': food_kind, 'restaurant': [restaurant], 'menu': [menu], 'size': 1, 'newtime': [newtime]})
    return "已成功新增地點、餐廳"
  else:
    #如果地點種類和餐廳都有，不做任何事
    if restaurant in cursor['restaurant']:
      return "您所欲新增的餐廳已經存在"
    else:
      #如果地點種類已有、餐廳尚未建立，新增餐廳資訊
      query = {'location': location, 'food_kind': food_kind}
      db.update(query, {'$push': {'restaurant': restaurant, 'menu': menu, 'newtime': newtime}, "$inc":{"size":1}})
      return "已成功新增餐廳"

def delete_restaurant(db, location, food_kind, restaurant):
  #只允許刪去單一餐廳
  #先看地點、種類、餐廳存不存在
  cursor = db.find_one({'location': location, 'food_kind': food_kind})
  try:
    restaurant_list = cursor["restaurant"]
    if restaurant in restaurant_list:
      index = restaurant_list.index(restaurant)
      query = {'location': location, 'food_kind': food_kind}
      db.update(query, {'$pull': {'restaurant': restaurant, 'menu': cursor["menu"][index], 'newtime': cursor["newtime"][index]}, "$inc":{"size":-1}})
      return "已成功刪除餐廳"
    else:
      return "查無此餐廳喔"
  except:
    return "查無此餐廳喔"

def update_menu(db, location, food_kind, restaurant, newmenu):
  newtime = time.asctime(time.localtime(time.time()))
  cursor = db.find_one({'location': location, 'food_kind': food_kind})
  try:
    restaurant_list = cursor["restaurant"]
    if restaurant in restaurant_list:
      index = restaurant_list.index(restaurant)
      query = {'location': location, 'food_kind': food_kind}
      db.update(query, {'$pull': {'restaurant': restaurant, 'menu': cursor["menu"][index], 'newtime': cursor["newtime"][index]}})
      db.update(query, {'$push': {'restaurant': restaurant, 'menu': newmenu, 'newtime': newtime}})
      return "已成功更新菜單"
    else:
      return "查無此餐廳喔"
  except:
    return "查無此餐廳喔"

def find_db():
  uri = 'mongodb://heroku_tn484cn6:okmlvoolpgrfiood5dh87v6mlo@ds053148.mlab.com:53148/heroku_tn484cn6'
  client = pymongo.MongoClient(uri)
  db = client.get_default_database()
  return db

# def main(args):

#     client = pymongo.MongoClient(uri)

#     db = client.get_default_database()

#     # First we'll add a few songs. Nothing is required to create the songs
#     # collection; it is created automatically when we insert.

#     food = db['eating']
#     # Note that the insert method can take either an array or a single dict.

#     food.insert_many(SEED_DATA)
#     #宣告區
#     location = '公館'
#     food_kind = '麵'
#     restaurant = "右手餐廳"
#     menu = "test"
#     # update_menu(food, location, food_kind, restaurant, menu)
#     # delete_restaurant(food, location, food_kind, restaurant)
#     find_info(food, location, food_kind)
#     # new_restaurant(food, location, food_kind, restaurant, menu)
#     # newtime = time.asctime(time.localtime(time.time()))
#     # found = True
#     # try:
#     #   cursor = food.find_one({'location': location, 'food_kind': food_kind})
#     #   cursor["restaurant"]
#     # except:
#     #   found = False
#     # #如果地點或種類沒有，直接新增餐廳資訊
#     # if found == False:
#     #   food.insert({'location': location, 'food_kind': food_kind, 'restaurant': restaurant, 'menu': menu, 'size': 1, 'newtime': newtime})
#     #   print("已成功新增地點、餐廳")
#     # else:
#     #   #如果地點種類和餐廳都有，不做任何事
#     #   if restaurant in cursor['restaurant']:
#     #     print("您所欲新增的餐廳已經存在")
#     #   else:
#     #     #如果地點種類已有、餐廳尚未建立，新增餐廳資訊
#     #     query = {'location': location, 'food_kind': food_kind, 'restaurant': {"$nin": [restaurant]}}
#     #     food.update(query, {'$push': {'restaurant': restaurant, 'menu': menu, 'newtime': newtime}, "$inc":{"size":1}})
#     #     print("已成功新增餐廳")



#     # # Finally we run a query which returns all the hits that spent 10 or
#     # # more weeks at number 1.
#     # try:
#     #   cursor = food.find_one({'location': '公館', 'food_kind': '麵'})
#     # except:
#     #   print('查無此資料，請問您要不要自行建立一個呢')

#     # for i in range(len(cursor["restaurant"])):
#     #     print(cursor["restaurant"][i])
#     #     print(cursor["menu"][i])
#     #     print(cursor["newtime"][i])

#     ### Since this is an example, we'll clean up after ourselves.

#     db.drop_collection('eating')

#     ### Only close the connection when your app is terminating

#     client.close()


# if __name__ == '__main__':
#     # print(time.asctime(time.localtime(time.time())))
#     tStart = time.time()
#     main(sys.argv[1:])
#     tStop = time.time()
#     print(tStop - tStart)





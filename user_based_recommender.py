import pandas as pd
from surprise import dump

# 讀取資料
df = pd.read_csv("retail_data_1022_2020.csv", encoding="utf-8")
df['customer_id'] = df['customer_id'].apply(lambda x: str(x))
df['product_code'] = df['product_code'].apply(lambda x: str(x))

# 載入模組
file_name = 'user_based_module'
user_algo = dump.load(file_name)[1]

# 找出相似用戶的Top-N
def getSimilarUsers(top_k, u_id):
    user_inner_id = user_algo.trainset.to_inner_uid(u_id)
    user_neighbors = user_algo.get_neighbors(user_inner_id, k=top_k)
    user_neighbors = (user_algo.trainset.to_raw_uid(inner_id) for inner_id in user_neighbors)
    return list(user_neighbors)

# 刪除list裡的重複值
def deleteDuplicatedElementFromList(l):
    resultList = []
    for item in l:
        if not item in resultList:
            resultList.append(item)
    return resultList


def convertProductCode2Name(L):
    # 推薦列表轉 DataFrame
    recommend_item_df = pd.DataFrame(L, columns=['product_code'])

    # 建立商品Code與Name對應的 Dataframe
    product_code_name_df = pd.DataFrame(
        {'product_code': df['product_code'], 'product_name': df['product_name']}).drop_duplicates()

    # 將兩個 DataFrame做 merge
    recommend_item_df = pd.merge(recommend_item_df, product_code_name_df, on=['product_code'])

    # 商品名輸出成list
    recommend_item_list = list(recommend_item_df['product_name'])
    return recommend_item_list


def userBasedRecommender(customer_id):
    # 建立每個顧客的購買清單 DataFrame
    customer_itemList_df = df.groupby('customer_id', as_index=False).agg(
        {'product_code': lambda x: ' '.join(x).split(' ')})

    # 建立 Top 10 的 similar users list
    similar_users_list = getSimilarUsers(10, customer_id)

    # 建立特定顧客的購買物品list
    customer_items_list = \
    customer_itemList_df[customer_itemList_df['customer_id'] == customer_id]['product_code'].values[0]

    # 建立 similar users 購買物品 list [[A1,A2,.], [B1,B2,..],...]
    similar_user_item_list = []
    for user in similar_users_list:
        item_list = customer_itemList_df[customer_itemList_df['customer_id'] == user]['product_code'].values[0]
        similar_user_item_list.append(item_list)

    # 建立推薦物品list [A1,A2,...,B1,B2,...]
    recommend_list = []
    for l in similar_user_item_list:
        for item in l:
            recommend_list.append(item)
    # 推薦列表中, 刪除已購買過的產品
    for i in customer_items_list:
        if i in recommend_list:
            recommend_list.remove(i)
    # 將推薦商品code_list 轉成 name_list
    recommend_list = convertProductCode2Name(recommend_list)
    recommend_list = deleteDuplicatedElementFromList(recommend_list)
    return recommend_list[:5]

def main(test):
    # 測試 推薦 customer_id = '1'
    # print(userBasedRecommender('1'))
    return userBasedRecommender(test)

if __name__ == '__main__':
    main()
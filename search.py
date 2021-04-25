import pandas as pd
import eel
import sys
import datetime

ITEM_MASTER_CSV_PATH="./item_master.csv"
RECEIPT_FOLDER="./receipt"

class Food_MenuItem:
    def __init__(self, item_code, item_name, price):
        self.item_code = item_code
        self.item_name = item_name
        self.price = price

    def info(self):
        return self.item_name + ': ¥' + str(self.price)

class Order:
    def __init__(self,item_master):
        self.item_order_list=[]
        self.item_count_list=[]
        self.item_master=item_master
        self.set_datetime()
    
    def set_datetime(self):
        self.datetime=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

    def add_item_order(self, item_code, item_count):
        self.item_order_list.append(item_code)
        self.item_count_list.append(item_count)

    def view_item_list(self):
        for item in self.item_order_list:
            print("商品コード:{}".format(item))

    def get_item_data(self,item_code):
            for m in self.item_master:
                if item_code==m.item_code:
                    return m.item_name,m.price

    def input_order(self):
        print("いらっしゃいませ！")
        while True:
            buy_item_code=input("商品番号を入力。注文を完了する場合は、0を入力してください >>> ")
            if int(buy_item_code)!=0:
                check=self.get_item_data(buy_item_code)
                if check!=None:
                    print("{} が注文されました".format(check[0]))
                    buy_item_count=input("購入数を入力してください　>>> ")
                    self.add_item_order(buy_item_code,buy_item_count)
                else:
                    print("「{}」は商品MENUに存在しません".format(buy_item_code))
            else:
                print("商品注文を終了します。")
                break 
    
    def view_order(self):
        number=1
        self.sum_price=0
        self.sum_count=0
        self.receipt_name="receipt_{}.log".format(self.datetime)
        self.write_receipt("-----------------------------------------------")
        self.write_receipt("注文商品一覧\n")
        for item_order,item_count in zip(self.item_order_list,self.item_count_list):
            result=self.get_item_data(item_order)
            self.sum_price+=result[1]*int(item_count)
            self.sum_count+=int(item_count)
            receipt_data="{0}.{2}({1}) : ￥{3:,}　{4}個 = ￥{5:,}".format(number,item_order,result[0],result[1],item_count,int(result[1])*int(item_count))
            self.write_receipt(receipt_data)
            number+=1

        # 合計金額、個数の表示
        self.write_receipt("-----------------------------------------------")
        self.write_receipt("合計金額:￥{:,} {}個".format(self.sum_price,self.sum_count))

    def input_change_money(self):
        while True:
            self.money = input("投入金額を入力してください >>> ")
            self.change_money = int(self.money) - self.sum_price
            if self.change_money>=0:
                print("投入金額は" + str(self.money) + '円です')
                print("お釣りは" + str(self.change_money) + '円です')
                break
            else:
                print("お預かり金が不足しています。再度入力してください")
        
        print("お買い上げありがとうございます")

    def write_receipt(self,text):
        print(text)
        with open(RECEIPT_FOLDER + "\\" + self.receipt_name,mode="a",encoding="utf-8_sig") as f:
            f.write(text+"\n")

def add_item_master_by_csv(csv_path):
    print("-----------------------")
    item_master=[]
    count=0
    try:
        item_master_df=pd.read_csv(csv_path,dtype={"item_code":object}) # CSVでは先頭の0が削除されるためこれを保持するための設定
        for item_code,item_name,price in zip(list(item_master_df["item_code"]),list(item_master_df["item_name"]),list(item_master_df["price"])):
            item_master.append(Food_MenuItem(item_code,item_name,price))
            print("{}:{}円  商品番号({})".format(item_name,price,item_code))
            count+=1
        print("{}品の登録を完了。".format(count))
        print("-----------------------")
        return item_master

    except:
        print("マスタ登録が失敗")
        print("-----------------------")
        sys.exit()


def main(item_code, item_name, price):    
    item_master=add_item_master_by_csv(ITEM_MASTER_CSV_PATH) # CSVからマスタへ登録
    eel.item_master()()
    
    order=Order(item_master) #マスタをオーダーに登録   
    
    order.view_order()
 
    order.input_order()
 
    order.input_change_money()
 
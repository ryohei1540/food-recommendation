from sklearn.neighbors import NearestNeighbors
import pandas as pd
import configparser

class Food:
    NUT_NAMES_MAP = {
        "calories" : "energy_100g",
        "carbohydrates": "carbohydrates_100g",
        "fat" : "fat_100g",
        "proteins": "proteins_100g"
    }

    def __init__(self):
        self._inifile = ""
        self._h1 = ""
        self._h2 = ""
        self._calories = ""
        self._carbohydrates = ""
        self._fat = ""
        self._proteins = ""
        self._calc_calories = ""
        self._calc_carbohydrates = ""
        self._calc_proteins = ""
        self._calc_fat = ""
        self._nutrition_df = ""
        self._nutrition_df = ""
        self._nutrition_values_df = ""
        self._NUT_DAILY_VALUES = {}
        self._recommended_products = []

    def read_init(self):
        self._inifile = configparser.ConfigParser()
        self._inifile.read('./config/config.ini', 'UTF-8')

    def create_nut_dict(self):
        self._NUT_DAILY_VALUES = {
            "calories": int(self._inifile.get('nutrition', 'calories')),
            "carbohydrates": int(self._inifile.get('nutrition', 'carbohydrates')),
            "proteins": int(self._inifile.get('nutrition', 'proteins')),
            "fat": int(self._inifile.get('nutrition', 'fat'))
        }

    def create_nutrition_values_df(self):
        self._nutrition_values_df = self._nutrition_df.drop(["product_name", "sugars_100g", "fiber_100g", "cholesterol_100g"], axis=1)
        for key, val in self._NUT_DAILY_VALUES.items():
            column = self.NUT_NAMES_MAP[key]
            self._nutrition_values_df[column] /= val

    def get_food(self):
        while True:
            self._h1 = input("食べた料理を入力してください:")
            if self._h1 in self._nutrition_df["product_name"].values:
                break
            else:
                print("入力された料理が登録されていません\n")

    def get_food_quantity(self):
        while True:
            str_h2 = input("食べた料理の量を入力してください（グラム）:")
            if not str_h2.isdecimal():
                print("数値を入力してください\n")
                continue
            self._h2 = int(str_h2)
            if self._h2 > 0:
                break


    def set_nut(self):
        self._calories = self._nutrition_df[self._nutrition_df["product_name"] == self._h1]["energy_100g"].values[0] * self._h2 / 100
        self._carbohydrates = self._nutrition_df[self._nutrition_df["product_name"] == self._h1]["carbohydrates_100g"].values[0] * self._h2 / 100
        self._fat = self._nutrition_df[self._nutrition_df["product_name"] == self._h1]["fat_100g"].values[0] * self._h2 / 100
        self._proteins = self._nutrition_df[self._nutrition_df["product_name"] == self._h1]["proteins_100g"].values[0] * self._h2 / 100

    def print_nut(self):
        self.print_intake_nut()
        self.print_need_nut()
        self.print_recommend_food()
        
    def print_intake_nut(self):
        print("\nあなたが摂取した栄養値：")
        print("カロリー：{}g".format(round(self._calories,1)))
        print("炭水化物：{}g".format(round(self._carbohydrates,1)))
        print("たんぱく質：{}g".format(round(self._proteins,1)))
        print("脂肪：{}g\n".format(round(self._fat,1)))

    def print_need_nut(self):
        print("あなたが一日に必要とする残りの栄養値（割合）：")
        print("カロリー：{}%".format(int(round((self._NUT_DAILY_VALUES["calories"] - self._calories) / self._NUT_DAILY_VALUES["calories"],2) * 100)))
        print("炭水化物：{}%".format(int(round((self._NUT_DAILY_VALUES["carbohydrates"] - self._carbohydrates) / self._NUT_DAILY_VALUES["carbohydrates"],2) * 100)))
        print("たんぱく質：{}%".format(int(round((self._NUT_DAILY_VALUES["proteins"] - self._proteins) / self._NUT_DAILY_VALUES["proteins"],2) * 100)))
        print("脂質：{}%\n".format(int(round((self._NUT_DAILY_VALUES["fat"] - self._fat) / self._NUT_DAILY_VALUES["fat"],2) * 100)))

    def print_recommend_food(self):
        print("オススメする食事")
        print("次の食事を摂取した場合に、必要となる残りの栄養値を表示します\n")
        for i, food in enumerate(self._recommended_products):
            print("{}:{}".format(i+1, food))
            self._calc_calories = self._calories + round(self._nutrition_df[self._nutrition_df["product_name"] == food]["energy_100g"].values[0], 1)
            self._calc_carbohydrates = self._carbohydrates + round(self._nutrition_df[self._nutrition_df["product_name"] == food]["carbohydrates_100g"].values[0], 1)
            self._calc_proteins = self._proteins + round(self._nutrition_df[self._nutrition_df["product_name"] == food]["proteins_100g"].values[0], 1)
            self._calc_fat = self._fat + round(self._nutrition_df[self._nutrition_df["product_name"] == food]["fat_100g"].values[0], 1)
            print("カロリー：{}%".format(int(round((self._NUT_DAILY_VALUES["calories"] - self._calc_calories) / self._NUT_DAILY_VALUES["calories"],2) * 100)))
            print("炭水化物：{}%".format(int(round((self._NUT_DAILY_VALUES["carbohydrates"] - self._calc_carbohydrates) / self._NUT_DAILY_VALUES["carbohydrates"],2) * 100)))
            print("たんぱく質：{}%".format(int(round((self._NUT_DAILY_VALUES["proteins"] - self._calc_proteins) / self._NUT_DAILY_VALUES["proteins"],2) * 100)))
            print("脂質：{}%\n".format(int(round((self._NUT_DAILY_VALUES["fat"] - self._calc_fat) / self._NUT_DAILY_VALUES["fat"],2) * 100)))

if __name__=="__main__":
    f = Food()
    f.read_init()
    f.create_nut_dict()
    f._nutrition_df = pd.read_csv("./data/nutrition_values.csv", header=0)
    f.create_nutrition_values_df()
    f.get_food()
    f.get_food_quantity()
    f.set_nut()
    knn = NearestNeighbors(n_neighbors=5,
                               algorithm='brute',
                               metric="euclidean").fit(f._nutrition_values_df)
    distances, indices = knn.kneighbors([[(f._NUT_DAILY_VALUES["calories"] - f._calories) / f._NUT_DAILY_VALUES["calories"] ,
                                              (f._NUT_DAILY_VALUES["carbohydrates"] - f._carbohydrates) / f._NUT_DAILY_VALUES["carbohydrates"] ,
                                              (f._NUT_DAILY_VALUES["proteins"] - f._proteins) / f._NUT_DAILY_VALUES["proteins"] ,
                                              (f._NUT_DAILY_VALUES["fat"] - f._fat) / f._NUT_DAILY_VALUES["fat"]]])
    f._recommended_products = [f._nutrition_df.loc[i]['product_name'] for i in indices[0]]
    f.print_nut()
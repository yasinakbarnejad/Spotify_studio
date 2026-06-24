import numpy as np
class BaseOutlierHandler:
    def handle(self, df):
        self.length = len(df)
        self.num_cols = df.select_dtypes(include='number').columns.tolist()
        return df
class IQROutlierHandler(BaseOutlierHandler):
    def handle(self,df):
        super().handle(df)
        for variable in self.num_cols:
            Q1 = df[variable].quantile(0.25)
            Q3 = df[variable].quantile(0.75)
            IQR = Q3-Q1
            lower, upper = Q1-1.5*IQR, Q3+1.5*IQR
            df = df[(df[variable]>= lower) & (df[variable]<=upper)]
        print(len(df)-self.length,"songs deleted")
        return df
class ZScoreOutlierHandler(BaseOutlierHandler):
    def handle(self,df):
        super().handle(df)
        for variable in self.num_cols:
            mean = df[variable].mean()
            deviation = df[variable].std()
            if deviation==0:
                continue
            z_scores = np.abs((df[variable]-mean)/deviation)
            df = df[z_scores<3]
        print(len(df)-self.length,"songs deleted")

        return df
class BaseImputer:
    def impute(self, df):
        self.length = len(df)
        print(df.isnull().sum().sum(), "songs feauture missing")
        self.num_cols = df.select_dtypes(include='number').columns.tolist()
        self.str_cols = df.select_dtypes(include='object').columns.tolist()
        df.dropna(subset=self.str_cols, inplace=True)
        return df

class MeanImputer(BaseImputer):
    def impute(self,df):
        from sklearn.impute import SimpleImputer      
        df = super().impute(df)
        df[self.num_cols] = SimpleImputer(strategy='mean').fit_transform(df[self.num_cols])
        print("done")
        return df
class MedianImputer(BaseImputer):
    def impute(self,df):
        from sklearn.impute import SimpleImputer      
        df = super().impute(df)
        df[self.num_cols] = SimpleImputer(strategy='median').fit_transform(df[self.num_cols])
        print("done")
        return df
class KNNImputer(BaseImputer):
    def impute(self,df):
        from sklearn.impute import KNNImputer
        df = super().impute(df)
        df = df.reset_index(drop=True)
        num_df = df[self.num_cols]
        knn_imputer = KNNImputer(n_neighbors=5)
        df_imputed = knn_imputer.fit_transform(num_df)
        df[self.num_cols] = df_imputed
        print("done")       
        return df
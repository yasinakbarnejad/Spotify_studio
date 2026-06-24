from src import data_loader,data_cleaner,data_analyzer,ml,data_visualizer,song
import os, pandas,time
def main():
    df = pandas.DataFrame()
    while True:
        os.system("cls")
        print("===============   Spotify Data Studio ==============")
        print("1. Load Dataset\n2. Clean dataset\n3. Handle outliers\n4. Classify dataset\n5. Add new song\n6. give genre insight\n7. exit")
        print("====================================================")
        choice = -1
        while(choice<1 or choice>7):
            choice = int(input("Enter your choice (1-7): "))
        match (choice):
            case 1:
                df = load_data_menu()
            case 2:
                if not df.empty:
                    clean_menu(df)
                else:
                    print("You need to load data first")
                    time.sleep(1)
            case 3:
                if not df.empty:
                    handle_outlier_menu(df)
                else:
                    print("You need to load data first")
                    time.sleep(1)
            case 4:
                os.system("cls")
                if not df.empty:
                    df = data_loader.classify_data(df)
                    time.sleep(2)
                else:
                    print("You need to load data first")
                    time.sleep(1)
            case 5:
                os.system("cls")
                song.Song.new_song()
            case 6:
                if not df.empty:
                    insight_menu(df)
                else:
                    print("You need to load data first")
                    time.sleep(1)
            case 7:
                return

                
def clean_menu(df):
    while True:
        os.system("cls")
        print("===============   Clean Menu ==============")
        print("1. KNN imputer\n2. Mean imputer\n3. Median imputer\n4. exit")
        imputer_num = int(input("Enter cleaning method: "))
        imputer = data_cleaner.BaseImputer()
        if(imputer_num>4 or imputer_num<1):
            print("try again")
            time.sleep(1)
            continue
            
        match (imputer_num):
            case 1:
                imputer =data_cleaner.KNNImputer()
                break
            case 2:
                imputer =data_cleaner.MeanImputer()
                break
            case 3:
                imputer =data_cleaner.MedianImputer()
                break
            case 4:
                return
    df = imputer.impute(df)
    return df
    
def handle_outlier_menu(df):
    while True:
        os.system("cls")
        print("===============   Outlier Menu ==============")
        print("1. IQR method\n2. Z-score method\n3. exit")
        handler_num = int(input("Enter the outlier method: "))
        handler = data_cleaner.BaseOutlierHandler()
        if(handler_num>3 or handler_num<1):
            print("try again")
            time.sleep(1)
            continue
        match (handler_num):
            case 1:
                handler =data_cleaner.IQROutlierHandler()
                break
            case 2:
                handler =data_cleaner.ZScoreOutlierHandler()
                break
            case 3:
                return
    df =handler.handle(df)
    return df

def insight_menu(df):
    while True:
        os.system("cls")
        print("===============   Charts Menu ==============")
        print("1. Correlation matrix\n2. Box plot\n3. top genres popularity\n4. scatter plot\n5. top artists popularity\n6. exit")
        chart_num = int(input("Enter chart you want: "))
        if(chart_num>6 or chart_num<1):
            print("try again")
            time.sleep(1)
            continue
        match (chart_num):
            case 1:
                data_visualizer.plot_correlation_heatmap(df)
            case 2:
                data_visualizer.show_diffrence(df,data_cleaner.ZScoreOutlierHandler().handle(df),"popularity")
            case 3:
                data_visualizer.genres_chart(df)
            case 4:
                data_visualizer.dance_energy(df)
            case 5:
                data_visualizer.artist_chart(df)
            case 6:
                return
    
                        
def load_data_menu():
    while True:
        os.system("cls")
        print("===============   Data loading ==============")
        path = input("Enter your dataset path or enter default or exit for going back: ")
        if path=="exit":
            return pandas.DataFrame()
        elif path=="default":
            df = data_loader.load_file()
            return df
        else:
            try:
                df = data_loader.load_file(path)
                return df
            except FileNotFoundError:
                print("path doesn't exist")
                time.sleep(1)
    
if __name__ == "__main__":
    main()
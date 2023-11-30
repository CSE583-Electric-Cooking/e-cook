import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def extract_data():
    os.chdir(('../data/kosko'))
    files = os.listdir()
    kosko_data = []
    for file in files: 
        if ".csv" in file:
            kosko_data.append(file)
    kosko_data = sorted(kosko_data) ## SORTED LIST OF CSV DATA
    return kosko_data #### ADD TEST PULLS ONLY CSV DATA

def deaggregate(kosko_data):
    user_dict = {}
    for data in kosko_data:
        id = data.split("_")[1]
        user_dict[id] = pd.read_csv(data)
    return user_dict ### ADD TEST BUT I DONT KNOW

def query(dictionary):
    print("BASIC VISUALIZATION KOSKO\n")
    print("AVALIABLE DATA:")
    print_user = lambda id: print(f"USER ID: {id}")
    ids = []
    for item in dictionary.items():
        ids.append(item[0])
        print_user(item[0])

    while True:
        user_input = input("PLEASE SELECT USER FROM LIST: ")
        if user_input in ids:
            return user_input
        else:
            print("INVALID INPUT") ## INVALID INPUT TEST

def visualize(id,dictionary):
    df = dictionary[id] ##GRAB DATA FRAME
    #print(df.columns)
    t = df["TIME"].values
    V = df["VOLTAGE"].values
    I = df["CURRENT"].values
    W = df["WATT"].values
    kwH = df["KWH"].values

    status = df["DEVICE STATUS"].values

    on = status == "ON"
    off = status == "OFF"
    fig, axs = plt.subplots(2, 2)
    marker_size = .1
    axs[0, 0].plot(t, V,'k-.')
    axs[0, 0].plot(t[on], V[on],'b.')
    axs[0, 0].plot(t[off], V[off],'r.')
    axs[0, 0].set_title('Voltage')

    axs[0, 1].plot(t, I,'k-.')
    axs[0, 1].plot(t[on], I[on],'b.')
    axs[0, 1].plot(t[off], I[off],'r.')
    axs[0, 1].set_title('Current')

    axs[1, 0].plot(t, W,'k-.')
    axs[1, 0].plot(t[on], W[on],'b.')
    axs[1, 0].plot(t[off],W[off],'r.')
    axs[1, 0].set_title('Watt')

    axs[1, 1].plot(t, kwH,'k-.')
    axs[1, 1].plot(t[on], kwH[on],'b.')
    axs[1, 1].plot(t[off],kwH[off],'r.')
    axs[1, 1].set_title('Kilowatt Hour')


    # Show the plot
    plt.show()

"""




def visualize(id, dictionary):
    df = dictionary[id]  # Grab DATA FRAME

    t = df["TIME"].values
    V = df["VOLTAGE"].values
    I = df["CURRENT"].values
    W = df["WATT"].values
    kwH = df["KWH"].values

    status = df["DEVICE STATUS"].values

    on = status == "ON"
    off = status == "OFF"
    fig, axs = plt.subplots(2, 2, figsize=(12, 8))

    # Use Seaborn to create scatter plots with different colors for ON and OFF
    sns.scatterplot(x=t, y=V, hue=status, ax=axs[0, 0], palette={"ON": "blue", "OFF": "red"}, s=10)
    axs[0, 0].set_title('Voltage')

    sns.scatterplot(x=t, y=I, hue=status, ax=axs[0, 1], palette={"ON": "blue", "OFF": "red"}, s=10)
    axs[0, 1].set_title('Current')

    sns.scatterplot(x=t, y=W, hue=status, ax=axs[1, 0], palette={"ON": "blue", "OFF": "red"}, s=10)
    axs[1, 0].set_title('Watt')

    sns.scatterplot(x=t, y=kwH, hue=status, ax=axs[1, 1], palette={"ON": "blue", "OFF": "red"}, s=10)
    axs[1, 1].set_title('Kilowatt Hour')

    # Show the plot
    plt.tight_layout()
    plt.show()
    


"""
if __name__ == "__main__":
    data = extract_data()
    dictionary = deaggregate(data)
    id = query(dictionary)
    visualize(id,dictionary)





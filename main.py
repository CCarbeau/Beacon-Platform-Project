import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import streamlit as sl

def main():

    data = pd.read_csv("github_dataset.csv")
    data = data.dropna()
    data = data.drop_duplicates()
    data = data.set_index(data["repositories"])
    langs=pd.Series(index=["Total"],data=[0])
    langs["Total"]=data["language"].count()
    for index, value in data["language"].items():
        if pd.isnull(value)==False:
            if value in langs.index:
                langs.loc[value]=langs.loc[value]+1
            else:
                update = pd.Series(index=[value], data = 1)
                langs = pd.concat([langs,update])
    stats = pd.DataFrame(index=langs.index, columns=["Total Projects", "Total Errors","Total Forks", "Total Contributors"])
    stats["Total Projects"]=langs
    stats = stats.fillna(0)
    i=0
    for index, row in data.iterrows(): 
        stats.loc["Total","Total Errors"]=(stats.loc["Total","Total Errors"]+row.loc["issues_count"])
        stats.loc["Total","Total Contributors"]=(stats.loc["Total","Total Contributors"]+row.loc["contributors"])
        stats.loc["Total","Total Forks"]=(stats.loc["Total","Total Forks"]+row.loc["forks_count"])
        stats.loc[row.loc["language"],"Total Errors"]=(stats.loc[row.loc["language"],"Total Errors"]+row.loc["issues_count"])
        stats.loc[row.loc["language"],"Total Contributors"]=(stats.loc[row.loc["language"],"Total Contributors"]+row.loc["contributors"])
        stats.loc[row.loc["language"],"Total Forks"]=(stats.loc[row.loc["language"],"Total Forks"]+row.loc["forks_count"])
    
    sl.title("Python's Need for A Code Integrator:")
    sl.subheader("By Christian Carbeau")
    sl.caption("Mechanical Engineering and Computer Science major, Duke University Class of 2026")


    labels = "JavaScript", "Python", "HTML", "Java", "C Variants", "Other"
    sizes = [stats.loc["JavaScript","Total Projects"],stats.loc["Python","Total Projects"],stats.loc["HTML","Total Projects"],stats.loc["Java","Total Projects"],(stats.loc["C++","Total Projects"]+stats.loc["C","Total Projects"]+stats.loc["C#","Total Projects"]+stats.loc["Objective-C","Total Projects"]+stats.loc["CSS","Total Projects"]),stats.loc["Total","Total Projects"]-stats.loc["JavaScript","Total Projects"]-stats.loc["Python","Total Projects"]-stats.loc["HTML","Total Projects"]-stats.loc["Java","Total Projects"]-stats.loc["C++","Total Projects"]-stats.loc["C","Total Projects"]-stats.loc["C#","Total Projects"]-stats.loc["Objective-C","Total Projects"]-stats.loc["CSS","Total Projects"]]
    explode = (0, 0.1, 0, 0, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    sl.header("Python's Popularity:")
    sl.pyplot(fig1)
    sl.text("Python is widely known as one of the most popular programming languages, \nespecially amongst first time coders. Its easy syntax, large and helpful community,\nand powerful capabilites all make Python a very attractive programming language to \nlearn. The GitHub repository data examined in this report statistically confirms \nPython's popularity. Of the 1000 GitHub repositories examined, Python was the main \nlanguage in 17.8 percent of them, only second to JavaScript.")

    fig, ax = plt.subplots()
    plt.xlabel("Number of Contributors")
    plt.ylabel("Number of Issues")

    cont = pd.Series(index=data.index, data = data["contributors"])
    issues = pd.Series(index=data.index, data = data["issues_count"])
    for index, row in data.iterrows():
        if (row.loc["contributors"] > 200) or (row.loc["issues_count"] > 100) or row.loc["contributors"]==0 :
            cont=cont.drop(index)
            issues=issues.drop(index)

    ax.scatter(cont,issues,s=3)
    a,b =np.polyfit(cont,issues,1)
    ax.plot(cont, a*cont)
    # sl.text("Contributors vs Issues")
    # sl.text("Slope: ")
    # sl.text(a)
    # sl.text("Correlation:")
    # sl.text(cont.corr(issues))
    # sl.text("Y int:")
    # sl.text(b)

    sl.header("What Leads to Poor Python Code?")
    sl.text("The most surprising metric I noticed in this dataset was that the highest \ncontributing factor to a repository's issue count was the amount of contributors it\nhad. The figure below shows a scatter plot of every repositories number of \ncontributors plotted against its number of issues as well as a line of best fit.")
    sl.pyplot(fig)
    sl.text("The slope of the line of best fit is 0.247 and has a correlation of +0.444. Both of\nthese values were the highest out of any other x-axis metric.")

    fig2, ax2 = plt.subplots()
    plt.ylabel("Issues per Contributor")
    plt.xlabel("Programming Language")
    ax2.bar(x=["Python","JavaScript","HTML","Java","C Variants","Other"], height = [stats.loc["Python","Total Errors"]/stats.loc["Python","Total Contributors"],
                                    stats.loc["JavaScript","Total Errors"]/stats.loc["JavaScript","Total Contributors"],
                                    stats.loc["HTML","Total Errors"]/stats.loc["HTML","Total Contributors"],
                                    stats.loc["Java","Total Errors"]/stats.loc["Java","Total Contributors"], 
                                    (stats.loc["C++","Total Errors"]+stats.loc["C","Total Errors"]+stats.loc["C#","Total Errors"]+stats.loc["Objective-C","Total Errors"]+stats.loc["CSS","Total Errors"])/(stats.loc["C++","Total Contributors"]+stats.loc["C","Total Contributors"]+stats.loc["C#","Total Contributors"]+stats.loc["Objective-C","Total Contributors"]+stats.loc["CSS","Total Contributors"]),
                                    (stats.loc["Total","Total Errors"]-stats.loc["JavaScript","Total Errors"]-stats.loc["Python","Total Errors"]-stats.loc["HTML","Total Errors"]-stats.loc["Java","Total Errors"]-stats.loc["C++","Total Errors"]-stats.loc["C","Total Errors"]-stats.loc["C#","Total Errors"]-stats.loc["Objective-C","Total Errors"]-stats.loc["CSS","Total Errors"])/(stats.loc["Total","Total Contributors"]-stats.loc["JavaScript","Total Contributors"]-stats.loc["Python","Total Contributors"]-stats.loc["HTML","Total Contributors"]-stats.loc["Java","Total Contributors"]-stats.loc["C++","Total Contributors"]-stats.loc["C","Total Contributors"]-stats.loc["C#","Total Contributors"]-stats.loc["Objective-C","Total Contributors"]-stats.loc["CSS","Total Contributors"])],
                                color = "orange")
    sl.header("Python's Issue with Issues:")
    sl.pyplot(fig2)
    sl.text("As shown by the figure above, Python has the highest issues per contributor rate \namongst all programming languages with a ratio of 1.17 issues per contributor. \n\nIn addition, Python has a high issues per project ratio of 9.755:")

    fig3, ax3 = plt.subplots()
    plt.ylabel("Issues per Project")
    plt.xlabel("Programming Language")
    ax3.bar(x=["Python","JavaScript","HTML","Java","C Variants","Other"], height = [stats.loc["Python","Total Errors"]/stats.loc["Python","Total Projects"],
                                    stats.loc["JavaScript","Total Errors"]/stats.loc["JavaScript","Total Projects"],
                                    stats.loc["HTML","Total Errors"]/stats.loc["HTML","Total Projects"],
                                    stats.loc["Java","Total Errors"]/stats.loc["Java","Total Projects"], 
                                    (stats.loc["C++","Total Errors"]+stats.loc["C","Total Errors"]+stats.loc["C#","Total Errors"]+stats.loc["Objective-C","Total Errors"]+stats.loc["CSS","Total Errors"])/(stats.loc["C++","Total Projects"]+stats.loc["C","Total Projects"]+stats.loc["C#","Total Projects"]+stats.loc["Objective-C","Total Projects"]+stats.loc["CSS","Total Projects"]),
                                    (stats.loc["Total","Total Errors"]-stats.loc["JavaScript","Total Errors"]-stats.loc["Python","Total Errors"]-stats.loc["HTML","Total Errors"]-stats.loc["Java","Total Errors"]-stats.loc["C++","Total Errors"]-stats.loc["C","Total Errors"]-stats.loc["C#","Total Errors"]-stats.loc["Objective-C","Total Errors"]-stats.loc["CSS","Total Errors"])/(stats.loc["Total","Total Projects"]-stats.loc["JavaScript","Total Projects"]-stats.loc["Python","Total Projects"]-stats.loc["HTML","Total Projects"]-stats.loc["Java","Total Projects"]-stats.loc["C++","Total Projects"]-stats.loc["C","Total Projects"]-stats.loc["C#","Total Projects"]-stats.loc["Objective-C","Total Projects"]-stats.loc["CSS","Total Projects"])],
                                color = "red")
    sl.pyplot(fig3)
    sl.header("Python's Need for a Code Integrator:")
    sl.text("Python's high rate of issues per contributor and issues per project highlight its \nneed for a code integrator. I suspect that the reason for Python's high rate of \nissue's per contributor results from the difficultly in integrating one's code to \nanother. I have experienced this myself when working on various group projects and\nknow that it is mainly a stylistic discrepancy that results in the integration \ndifficulty. While the Python community has tried to push a standardized form of code\nstyle, it is difficult for many experienced coders to adjust their styles and many \nbeginner coders do not even know that such a standardization exists. Thus, a \nprogram that can automatically convert any python code to a standardized format \nwould be extremely useful in eliminating code integration errors. Such a program \ncould be made by using machine learning technology and could easily be trained on \nthe enormous amount of public python programs. It would provide a massive amount of value to the Python\ncommunity and allow people to spend more time coding and innovating than debugging.")

    # fig2, ax2 = plt.subplots()
    # ax2.scatter(data["forks_count"],data["issues_count"],s=3)
    # a,b =np.polyfit(data["forks_count"],data["issues_count"],1)
    # ax2.plot(data["forks_count"], a*data["forks_count"])
    # sl.text("Forks vs Issues")
    # sl.text(data["forks_count"].corr(data["issues_count"]))
    
    # sl.pyplot(fig2)

    # fig3, ax3 = plt.subplots()
    # ax3.scatter(data["pull_requests"],data["issues_count"],s=3)
    # a,b =np.polyfit(data["pull_requests"],data["issues_count"],1)
    # ax3.plot(data["pull_requests"], a*data["pull_requests"])
    # sl.text("Pull Request vs Issues")
    # sl.text(data["pull_requests"].corr(data["issues_count"]))

    #sl.pyplot(fig3)

    

    

if __name__ == "__main__":
    main()
#!/user/bin/env python
# -*- coding:UTF-8 -*-
# Author:Young.Shi
# Date: 20XX-00-00

import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import animation
# pth = r"population.csv"

df = pd.read_csv("population.csv",usecols=["name","group","year","value"],encoding="gbk")
plt.rcParams["font.family"]="Microsoft yahei"
fig,ax = plt.subplots(figsize=(12,8),dpi=100)
dic = {}
color = ['#adb0ff', '#ffb3ff', '#90d595', '#e48381','#aafbff',"#eafb50"]
name_ddf = list(set(df["name"].values))
colors = zip(name_ddf,color)
#数据的name和每个颜色写成字典对应
[dic.update({i:j}) for i,j in colors]
def create_plot(year):
    # ddf = df[df["year"]==2018].sort_values(by="value").tail(3)
    ddf = df[df["year"]==year].sort_values(by="value").head(10)
    ax.cla() #生成数据前先清除之前的数据
    ax.barh(range(len(ddf["name"].values)),ddf["value"],height = 0.4,color = [dic[i] for i in ddf["name"].values ])
    max_a = max(ddf["value"].values)
    for i,(value,name) in enumerate(zip(ddf["value"].values,ddf["name"].values)):
        ax.text(value,i,name,ha="right",size = 10,va="center_baseline") #添加每个数据的name
        ax.text(value,i-0.3,ddf["group"].values[i],ha="right",size = 15,va="top")#添加每个数据的group
        ax.text(value+100,i,"%s (单位:万)"%value,ha="left",size = 15,va="center",weight = 500) #添加每个数据的value
    #transform = ax.transAxes 这个参数可以让text里的文本内容按照整个axes的百分比放置
    ax.text(1.1,0.6,"%s年"%year,size = 40, transform = ax.transAxes, ha="right")
    ax.text(0,1.10,"The most populous cities in the China from 1968 to 2018",size = 18,weight = 600, transform = ax.transAxes, ha="left")

    # ax.set_yticks(range(len(ddf["name"].values)))
    # ax.set_yticklabels(ddf["name"].values)
    #设置内边距 2个参数分别代表左右和上下
    ax.margins(0,0.05)
    #设置axes的大小显示范围
    ax.set_xbound(0,max_a+3000)
    ax.grid(which="major",axis="x")
    #x轴的ticks数据放到顶部
    ax.xaxis.set_ticks_position(position="top")
    #把y轴的数据隐藏
    ax.set_yticks([])
    #隐藏图的边框
    plt.box(False)
    # plt.show()

# create_plot(2017)
animator = animation.FuncAnimation(fig,create_plot,frames = range(1961,2019),interval = 175)
plt.show()
# animator.save(r"C:\Users\Young\Desktop\1.gif")
from flask import Flask, render_template,request, url_for
import pandas as pd
import matplotlib.pyplot as plt
import plotly as py
import plotly.graph_objs as go
import cufflinks as cf

app = Flask(__name__)



def read_data():
    return pd.read_csv('hurun_unicorn.tsv', encoding='utf-8', delimiter="\t")

@app.route("/get_hurun_info")
def hurun():
  df=read_data()
  df_中国=df[df['国家'].str.contains('中国')]
  杭州大湾区城市名称替换={
    '杭州':'杭州大湾区','上海':'杭州大湾区','南京':'杭州大湾区','无锡':'杭州大湾区','绍兴':'杭州大湾区'
  }
  df_new=df_中国.set_index('城市').rename(index=杭州大湾区城市名称替换).reset_index()
  df_杭州大湾区=df_new[df_new['城市'].str.contains('杭州大湾区')].head(n=10)
  粤港澳大湾区城市名称替换={
    '广州':'粤港澳大湾区','深圳':'粤港澳大湾区','珠海':'粤港澳大湾区','佛山':'粤港澳大湾区','惠州':'粤港澳大湾区','东莞':'粤港澳大湾区','中山':'粤港澳大湾区','江门':'粤港澳大湾区','肇庆':'粤港澳大湾区'
  }
  df_new2=df_中国.set_index('城市').rename(index=粤港澳大湾区城市名称替换).reset_index()
  df_粤港澳大湾区=df_new2[df_new2['城市'].str.contains('粤港澳大湾区')].head(n=10)
  return render_template(
    "hurun_info.html",
    # Animation_data=df_animation.to_html(classes='animation',index=False),
    df_粤港澳大湾区=df_粤港澳大湾区.to_html(classes='animation',index=False),
    df_杭州大湾区=df_杭州大湾区.to_html(classes='animation',index=False),
    data=[{'粤港澳大湾区详情':'a1'},{'杭州大湾区详情':'a2'},{'湾区指标对比':'a'},{'湾区各行业对比':'b'},{'湾区同有行业对比':'c'},{'杭州大湾区投机机构详情':'d'},{'粤港澳大湾区投资机构详情':'e'}])


@app.route("/test" , methods=['GET', 'POST'])
def test():
  select = request.form.get('comp_select')
  df=read_data()
  df_中国=df[df['国家'].str.contains('中国')]
  杭州大湾区城市名称替换={
    '杭州':'杭州大湾区','上海':'杭州大湾区','南京':'杭州大湾区','无锡':'杭州大湾区','绍兴':'杭州大湾区'
  }
  df_new=df_中国.set_index('城市').rename(index=杭州大湾区城市名称替换).reset_index()
  df_杭州大湾区=df_new[df_new['城市'].str.contains('杭州大湾区')]
  粤港澳大湾区城市名称替换={
    '广州':'粤港澳大湾区','深圳':'粤港澳大湾区','珠海':'粤港澳大湾区','佛山':'粤港澳大湾区','惠州':'粤港澳大湾区','东莞':'粤港澳大湾区','中山':'粤港澳大湾区','江门':'粤港澳大湾区','肇庆':'粤港澳大湾区'
  }
  df_new2=df_中国.set_index('城市').rename(index=粤港澳大湾区城市名称替换).reset_index()
  df_粤港澳大湾区=df_new2[df_new2['城市'].str.contains('粤港澳大湾区')]
  df_杭州大湾区产业估值总和=df_杭州大湾区['估值（亿人民币）'].sum()
  df_粤港澳大湾区产业估值总和=df_粤港澳大湾区['估值（亿人民币）'].sum()
  df_杭州大湾区产业均值=df_杭州大湾区['估值（亿人民币）'].mean()
  df_粤港澳大湾区产业均值=df_粤港澳大湾区['估值（亿人民币）'].mean()
  dfall=pd.DataFrame({'指标':['杭州大湾区产业估值总和','粤港澳大湾区产业估值总和','杭州大湾区产业均值','粤港澳大湾区产业均值'],'值':[df_杭州大湾区['估值（亿人民币）'].sum(),df_粤港澳大湾区['估值（亿人民币）'].sum(),df_杭州大湾区['估值（亿人民币）'].mean(),df_粤港澳大湾区['估值（亿人民币）'].mean()]})
  fig = dfall.iplot(kind="bar", x="指标", y="值", asFigure=True,title='湾区指标对比')
  py.offline.plot(fig, filename="example.html",auto_open=False)
  with open("example.html", encoding="utf8", mode="r") as f:
    plot_all = "".join(f.readlines())
  df_粤港澳产业估值合计=df_粤港澳大湾区.groupby('行业').sum().drop(['成立年份','排名'],axis=1).reset_index()
  df_杭州大湾区产业估值合计=df_杭州大湾区.groupby('行业').sum().drop(['成立年份','排名'],axis=1).reset_index()
  fig = df_粤港澳产业估值合计.iplot(kind="bar", x="行业", y="估值（亿人民币）", asFigure=True,title='粤港澳产业估值合计')
  py.offline.plot(fig, filename="example2.html",auto_open=False)
  with open("example2.html", encoding="utf8", mode="r") as f:
    plot_all2 = "".join(f.readlines())
  fig = df_杭州大湾区产业估值合计.iplot(kind="bar", x="行业", y="估值（亿人民币）", asFigure=True,title='杭州大湾区产业估值合计')
  py.offline.plot(fig, filename="example3.html",auto_open=False)
  with open("example3.html", encoding="utf8", mode="r") as f:
    plot_all3 = "".join(f.readlines())
  粤港澳行业列表_list=df_粤港澳产业估值合计['行业'].to_list()
  杭州大湾区行业列表_list=df_杭州大湾区产业估值合计['行业'].to_list()
  共有行业=[a for a in 粤港澳行业列表_list if a in 杭州大湾区行业列表_list]
  df_对比_杭州大湾区=df_杭州大湾区产业估值合计[df_杭州大湾区产业估值合计['行业'].isin(共有行业)]
  df_对比_粤港澳=df_粤港澳产业估值合计[df_粤港澳产业估值合计['行业'].isin(共有行业)]
  杭州大湾区行业=df_对比_杭州大湾区['估值（亿人民币）'].to_list()
  粤港澳行业=df_对比_粤港澳['估值（亿人民币）'].to_list()
  pyplt = py.offline.plot
  labels = 共有行业
  values = 粤港澳行业
  trace = [go.Pie(labels=labels, values=values)]
  layout = go.Layout(title = '湾区共有行业估值（粤港澳）',)
  fig = go.Figure(data = trace, layout = layout)
  py.offline.plot(fig, filename="example4.html",auto_open=False)
  with open("example4.html", encoding="utf8", mode="r") as f:
    plot_all4 = "".join(f.readlines())
  pyplt = py.offline.plot
  labels = 共有行业
  values = 杭州大湾区行业
  trace = [go.Pie(labels=labels, values=values)]
  layout = go.Layout(title = '湾区共有行业估值（杭州大湾区）',)
  fig = go.Figure(data = trace, layout = layout)
  py.offline.plot(fig, filename="example5.html",auto_open=False)
  with open("example5.html", encoding="utf8", mode="r") as f:
    plot_all5 = "".join(f.readlines())
  df_杭州大湾区.index.name="序号"
  df_投资机构拆分_杭州大湾区 =pd.merge(df_杭走大湾区,df_杭州大湾区['部分投资机构'].str.split(',', expand=True).stack().reset_index(level=1,drop=True).rename('部分投资机构(拆)'),on="序号")
  df_粤港澳大湾区.index.name="序号"
  df_投资机构拆分_粤港澳 =pd.merge(df_粤港澳大湾区,df_粤港澳大湾区['部分投资机构'].str.split('、', expand=True).stack().reset_index(level=1,drop=True).rename('部分投资机构(拆)'),on="序号")
  df杭州大湾区投资机构=df_投资机构拆分_杭州大湾区[['企业名称','部分投资机构(拆)','估值（亿人民币）']]\
                .groupby(['部分投资机构(拆)'])\
                .agg({'企业名称':'count','估值（亿人民币）':'sum'})\
                .sort_values('估值（亿人民币）',ascending=False)\
                .rename(columns={'企业名称':'企业数量'})
  df粤港澳投资机构=df_投资机构拆分_粤港澳[['企业名称','部分投资机构(拆)','估值（亿人民币）']]\
                .groupby(['部分投资机构(拆)'])\
                .agg({'企业名称':'count','估值（亿人民币）':'sum'})\
                .sort_values('估值（亿人民币）',ascending=False)\
                .rename(columns={'企业名称':'企业数量'})
  return render_template(
    "info.html",
    select=select,
 		# "hurun_info.html",
 		# Animation_data=df_animation.to_html(classes='animation',index=False),
    df_粤港澳大湾区=df_粤港澳大湾区.to_html(classes='animation',index=False),
    df_杭州大湾区=df_杭州大湾区.to_html(classes='animation',index=False),
    dfall=dfall.to_html(classes='animation',index=False),
    df_杭州大湾区产业估值合计=df_杭州大湾区产业估值合计.to_html(classes='animation',index=False),
    df_粤港澳产业估值合计=df_粤港澳产业估值合计.to_html(classes='animation',index=False),
    tu=plot_all,
    tu2=plot_all2,
    tu3=plot_all3,
    tu4=plot_all4,
    tu5=plot_all5,
    gongyou=df_对比_杭州大湾区,
    df_js1=df杭州大湾区投资机构.to_html(classes='animation'),
    df_js2=df粤港澳投资机构.to_html(classes='animation'),)




if __name__=='__main__':
 	app.run(
 		debug=True
 		)


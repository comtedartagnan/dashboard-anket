from re import L, sub
from textwrap import wrap
from tokenize import group
from trace import Trace
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns


st.set_page_config(page_title='Dashboard',
                   page_icon=':bar_chart:',
                   layout='wide',
                   )

@st.cache
def get_data_from_excel():
    #df = pd.read_excel(io='dataset.xlsx',
    #                engine='openpyxl', sheet_name='Sheet1',
    #                )
    df = pd.read_csv('dataset.csv')
    df.rename(columns={'1-Yaşınız':'Yaş','2-Cinsiyetiniz':'Cinsiyet',
                    '3-Eğitim düzeyiniz':'Eğitim Düzeyi', '5-Hemşirelik meslek yılınız':'Hemşirelik meslek yılı'.title(),
                    '6-Okul sağlığı hemşiresi olarak mesleki yılınız':'Okul sağlığı hemşiresi olarak mesleki yılı'.title(),
                    '7-Görev yaptığınız il':'Görev yapılan il'.title()}, inplace=True)
    dusunceler = df.iloc[:,13:26]
    beceri = df.iloc[:,26:49]
    motivasyon = df.iloc[:,49:-2]
    return df, dusunceler, beceri, motivasyon

df, dusunceler, beceri, motivasyon = get_data_from_excel()



# --- SIDEBAR
#st.sidebar.header('Please Filter Here:')


# st.dataframe(sub_selection)

# -- main page --
#st.title(':bar_chart: ')
#st.markdown("#")

#counts, bins = np.histogram(df['Yaş'], )
#bins = 0.5 * (bins[:-1] + bins[1:])
#fig_age_dist = px.bar(x=bins, y=counts, labels={'x':'Yaş', 'y':'Adet'}, color=)
fig_age_dist = px.bar(df, 
    x='Yaş',
    #x=bins,
    #
    # y=counts,
    orientation='v',
    #title='<b>Yaş Dağılımı</b>',
    #color_discrete_sequence=["#0083B8"] * len(df),
    template='plotly_white',
    color='Cinsiyet',
    labels={'index':''}
)

fig_gender_dist = px.pie(df, names='Cinsiyet', )

#fig_marital_status = px.pie(df, names='4-Medeni Durumunuz')

fig_edu_level = px.pie(df, names='Eğitim Düzeyi')

fig_device = px.pie(df, names='9-Hizmet içi eğitimlere aşağıdaki cihazlardan hangisini kullanarak katıldınız?')

left_col, right_col = st.columns(2)

with left_col:
    st.subheader('Yaş Dağılımı:')
    st.plotly_chart(fig_age_dist)




with right_col:
    st.subheader('Cinsiyet Dağılımı:')
    st.plotly_chart(fig_gender_dist)

st.markdown('---')

d_left_col, d_right_col = st.columns(2)

with d_left_col:
    st.subheader('Eğitim Seviyesi Dağılımı:')
    st.plotly_chart(fig_edu_level)

with d_right_col:
    st.subheader('Eğitime Bağlanmakta kullanılan cihaz:')
    st.plotly_chart(fig_device)

k_left_col, k_right_col = st.columns([1,4])

#st.subheader('Medeni Durum Dağılımı')
#st.plotly_chart(px.pie(df, names='4-Medeni durumunuz'))

fig_city = px.bar(df, 
    x='Görev Yapılan Il',
    color='Cinsiyet'
)
st.markdown('---')
k_left_col, k_right_col = st.columns(2)
with k_left_col:
    st.subheader('Görev Yapılan İl:')
    st.plotly_chart(fig_city, )

fig_occ_period = px.bar(df.groupby(['Hemşirelik Meslek Yılı']).mean(),y='Yaş',)

#groups = df.group_by('Hemşirelik Meslek Yılı').mean()

with k_right_col:
    #st.write(df.groupby(['Hemşirelik Meslek Yılı']).mean())
    #st.subheader('')
    st.plotly_chart(fig_occ_period)

st.markdown('---')


m_left_col, m_mid_col, m_right_col = st.columns(3)


fig_edu_choice = px.pie(df, names='11-Aşağıdaki eğitim yöntemlerinden hangisini tercih edersiniz?')

with m_left_col:
    #st.write(df.columns)

    st.subheader('Tercih Edilen Eğitim Yöntemi:')
    st.plotly_chart(fig_edu_choice)

fig_occ_period_scn = px.bar(df.groupby(['Okul Sağlığı Hemşiresi Olarak Mesleki Yılı']).mean(),y='Yaş',)


with m_right_col:
    st.plotly_chart(fig_occ_period_scn)

fig_prob_percent = px.pie(df, names='10-Hizmetiçi eğitimlere çevrimiçi (online) katılım durumunuzu hangisi en iyi ifade eder?')
with m_mid_col:
    st.subheader('Katılım Durumu:')
    st.plotly_chart(fig_prob_percent)

st.markdown('---')
st.header('# ')
sub_dict = {'Düşünceler':dusunceler, 'Beceri ve Hazır Bulunuşluk Analizi':beceri,
            'Motivasyon - İsteklilik':motivasyon}

#subs = st.select_slider(
#    label='Sub Filter:',
#    options=list(sub_dict.keys()),
#)





#sub_selection = sub_dict[subs]

#@st.cache
def plotter(sub_selection):
    if sub_selection.equals(dusunceler):
        fig, axes = plt.subplots(3,5, figsize=(25,20))
        for i, ax in zip(range(13), axes.flat):
            sns.histplot(ax=ax, x=dusunceler.iloc[:,i], hue=dusunceler.iloc[:,i],legend=False)
            ax.set_title(dusunceler.iloc[:,i].name.split('[')[1][:-1], wrap=True, loc='center')
            ax.set(xlabel=None,ylabel='Adet')
            ax.tick_params(axis='x', rotation=90)
        fig.subplots_adjust(wspace=5, hspace=1, )
        fig.delaxes(axes[2][3])
        fig.delaxes(axes[2][4])

        #plt.subplots_adjust(left=0.125, right=0.9, top=0.9, wspace=0.2, hspace=0.25)

        fig.tight_layout()
        #plt.rcParams['figure.constrained_layout.use'] = True
        #plt.savefig('plots\\dusunceler.png', dpi=100)
    elif sub_selection.equals(beceri):
        fig, axes = plt.subplots(3,5, figsize=(25,20))
        for i, ax in zip(range(13), axes.flat):
            sns.histplot(ax=ax, x=beceri.iloc[:,i], hue=beceri.iloc[:,i], legend=False)
            ax.set_title(beceri.iloc[:,i].name.split('[')[1][:-1], wrap=True, loc='center')
            ax.set(xlabel=None, ylabel='Adet')
            ax.tick_params(axis='x', rotation=90)
        fig.delaxes(axes[2][3])
        fig.delaxes(axes[2][4])
        fig.tight_layout()
        #plt.savefig('plots\\beceri.png')
    elif sub_selection.equals(motivasyon):
        fig, axes = plt.subplots(3,3, figsize=(25,20))
        for i, ax in zip(range(7), axes.flat):
            sns.histplot(ax=ax, x=motivasyon.iloc[:,i], hue=motivasyon.iloc[:,i], legend=False)
            ax.set_title(motivasyon.iloc[:,i].name.split('[')[1][:-1], wrap=True, loc='center')
            ax.set(xlabel=None, ylabel='Adet')
            ax.tick_params(axis='x', rotation=90)
        fig.delaxes(axes[2][2])
        fig.delaxes(axes[2][1])
        fig.tight_layout()
        #plt.savefig('plots\\motivasyon.png')


for plot in sub_dict.values():
    plotter(plot)


#def download_button(url):
#    url
#    with open(path, 'rb') as file:
#        st.download_button(
#            label='Download the plot',
#            data=file,
#            file_name=""
#
#        )
dus, bec, mot=st.tabs(['Düşünceler', 'Beceri ve Hazır Bulunuşluk Analizi','Motivasyon - İsteklilik'])

with dus:
    st.header('')
    st.image("https://github.com/comtedartagnan/dashboard-anket/blob/main/plots/dusunceler.png?raw=true")

with bec:
    st.header('')
    st.image("https://github.com/comtedartagnan/dashboard-anket/blob/main/plots/beceri.png?raw=true")

with mot:
    st.header('')
    st.image("https://github.com/comtedartagnan/dashboard-anket/blob/main/plots/motivasyon.png?raw=true")

#from PIL import Image
#if sub_selection.equals(dusunceler):
#    path = 'plots\\dusunceler.png'
#elif sub_selection.equals(beceri):
#    path = 'plots\\beceri.png'
#elif sub_selection.equals(motivasyon):
#    path = 'plots\\motivasyon.png'
    
#st.image(Image.open(path))
#download_button()



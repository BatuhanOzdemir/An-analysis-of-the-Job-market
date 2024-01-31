import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from collections import Counter
from wordcloud import WordCloud
import streamlit as st


file_path = Path(Path.home(),"Desktop","Job_Ad_Project","Kariyer.xlsx")

df = pd.read_excel(file_path)

words = df["İlan-Metni"].values

st.set_page_config(page_title="Data Mining App",layout="wide")

st.title("Data Mining App")

st.header("Kategori Dağılımı")




ad_count, position, corporate_count = st.columns(3)

ad_count.metric(label="İlan Sayısı",value=len(df["İlan-ID"]))
position.metric(label="Pozisyon",value=len(pd.unique(df["Pozisyon"])))
corporate_count.metric(label="Şirket Sayısı",value=len(pd.unique(df["Firma"])))
st.subheader("En çok Kullanılan Kelimeler")
st.divider()
df_new = df[df["Sektör"].str.contains("Bilişim",na=False)]
#st.write(df_new["İlan-Metni"])
text = list(df["İlan-Metni"])
stopwords_list = ["ve","veya","için","of","to","and","in","with","ile","the","for","xa0","iş","genel","nitelikler","TANIMI","en","az","bölümlerinden","ilgili","NİTELİKLER","mezun","Tercihen","olarak","İŞ","olan","satış"]
wordcloud = WordCloud(width=1920,height=1080,background_color="white", stopwords=stopwords_list).generate(str(text))
fig = plt.figure(figsize=(8,8), facecolor=None)
plt.imshow(wordcloud,interpolation="bilinear")
plt.axis("off")
plt.show()
st.pyplot(fig)
st.divider()
st.subheader("Graphic Plotter")
col1,col2 = st.columns(2)
with col1:
	x_axis = st.selectbox(label="Select the x axis",options=[col for col in df.columns])
with col2:
	y_axis = st.selectbox(label="Select the y axis",options=[col for col in df.columns])
create_button = st.button(label="Create the graph",help="Creates the graph :)")
if create_button:

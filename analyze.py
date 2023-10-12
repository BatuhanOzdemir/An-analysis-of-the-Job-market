import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from collections import Counter
from wordcloud import WordCloud


file_path = Path(Path.home(),"Desktop","Job_Ad_Project","Kariyer.csv")

df = pd.read_csv(file_path)

word_freq = Counter()
df_new = df[df["Sektör"].str.contains("Bilişim",regex=False)].copy()


for text in df_new["İlan-Metni"]:
    word_freq.update(text.split())

wordcloud = WordCloud(width=600,height=600,background_color="white").generate_from_frequencies(word_freq)

plt.figure(figsize=(8,8),facecolor=None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad=0)
plt.show()
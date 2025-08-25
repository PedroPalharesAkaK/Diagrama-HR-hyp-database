import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
df = pd.read_csv(r'C:/Users/Pedro/Desktop/Diagrama HR/hyg_v42.csv')


def tamanho_estrela_cyano(star_corknown):
    if len(star_corknown) < 15:
       return 10
    else:
       return 8
#print(df.head(5))
#print(df.columns)
colour_index = df['ci']
luminosidade = df['lum']
nome = df['proper']
tipo_estrela = df['spect']
magnitude = df['mag']
distancia = df['dist']
mag_tipoB8V = [] #all B8V stars
dist_tipoB8V = [] #idem
star_lumknown = [] #cordenadas em HR apenas para nomes conhecidos
star_corknown = [] #idem
tipo_especial_cyano = "B8V"
n = 0
count = 0

while n < len(tipo_estrela):
    if tipo_estrela[n] == tipo_especial_cyano: #troque 'B8V' para qualquer outro spect e.g: 'F8V' 'G2V' 'K0'
        if not pd.isna(nome[n]) : #printa os Nomes de estrelas conhecidas taken from the International Astronomical Union
            print('Nome:',nome[n], '/Lum:',int(luminosidade[n]),'/B-V:',colour_index[n]) 
            star_lumknown.append(luminosidade[n]) 
            star_corknown.append(colour_index[n])
        if distancia[n] < 10000 and magnitude[n] > 0:
             #limites para fazer o segundo gráfico, 
             # para referencia a maior magnitude é -26 (quanto maior o número mais fraca a luz)
            mag_tipoB8V.append(magnitude[n])
            dist_tipoB8V.append(distancia[n]) #pontos para fazer segundo gráfico
            count += 1 #quantos dados tem desse tipo
    n += 1
print('quantidade:',count)
n = 0


cor_limpa = [] #criar nova lista, alguns dados de colour_inder estão NaN
lum_limpa = []
cor_cutoff = 2.2
while n < len(colour_index):
    if colour_index[n] < cor_cutoff and colour_index[n] != 1.5: #poucos dados em > 2.2 ; erro no sensor em 1.5
        cor_limpa.append(colour_index[n])
        lum_limpa.append(luminosidade[n])
    n += 1
#Pontos para fazer digrama HR estão limpos
n = 0
tamanhos = []
while n < len(lum_limpa):
    if lum_limpa[n] < 0.01 and cor_limpa[n] < 1.1 : #pontos maiores em bottom left
        tamanhos.append(1.0)
    elif lum_limpa[n] > 10000: #parte de cima
        tamanhos.append(0.3)
    else: 
        tamanhos.append(0.08) #tem que ser feito uma lista de len(tamanhos) == len(lum_limpa) para manter paridade
    n += 1



size = tamanho_estrela_cyano(star_corknown)


plt.style.use('dark_background') #deixa fundo preto
plt.figure(figsize=(12,8))
plt.subplot(1, 2, 1) # 1 linha, 2 colunas, posição 1
plt.scatter(cor_limpa,lum_limpa ,  s=tamanhos, alpha=tamanhos, c=cor_limpa, cmap = 'rainbow') 
#scatter = plot de ponto ; s = size ; alpha = quão Faint o ponto é em % (<=1) ; c = colour; 
#c aqui esta associado com o eixo x e cmap faz um gradiente de cores em x 
plt.plot(0.656, 1, marker = "*" , markersize=10,  c = "yellow",label = "Sol", linestyle = '') #novo ponto
plt.plot(star_corknown, star_lumknown, marker = "*" , markersize=size,  c = "cyan",label = "estrela B8V com Nome",  linestyle = '')
#plota as estrelas com nome do tipo escolhido no diagrama
plt.yscale('log')
plt.grid(True, alpha= 0.3)
plt.title('Diagrama HR', fontsize=16, color='lightblue', loc='left', pad=10)
plt.legend(fontsize = 10, handlelength=2,   handleheight=2,   markerscale=2, loc = 'upper right') #faz o label de plt.plot ; linha 77
plt.xlabel('The stars color index B-V', fontsize=14)
plt.ylabel('Luminosidade Solar', fontsize=14)
#fazendo subplot

plt.subplot(1, 2, 2)
plt.scatter(dist_tipoB8V, mag_tipoB8V, alpha=1, s=1, c =dist_tipoB8V, cmap = 'Wistia' )
plt.gca().invert_yaxis()
plt.title('Magnitude em função da distancia tipo B8V', fontsize=16, color='lightblue', loc='left', pad=10)
plt.xlabel('distancia em parsec', fontsize=14)
plt.ylabel('Mag Absoluta', fontsize=14)
plt.tight_layout()
#plt.savefig('my_plot2.png')
plt.show()
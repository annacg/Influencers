__author__ = 'Felipe Santana'
import pandas as pd

class Conversor():
    _dataset = ""
    _treino = []
    _classes = []
    _features = []
    _arquivoWeka = 'train_formatoWeka.arff'

    def __init__(self):
        pass

    def getDataset(self):
        return self._dataset

    def setDataset(self,valor):
        self._dataset = valor

    def getClasses(self):
        return self._classes

    def setClasses(self,valor):
        self._classes = valor

    def getTreino(self):
        return self._treino

    def setTreino(self,valor):
        self._treino = valor

    def getFeatures(self):
        return self._features

    def setFeatures(self,valor):
        self._features = valor


    def carrega_dados(self):
        self.setDataset("train.csv")                    #Seta o dataset
        dados = pd.read_csv(self.getDataset(),sep=',')
        self.setClasses(dados['Choice'])              #Coleta as classes do dataset.
        self.setTreino(dados.drop('Choice',axis=1))   #Retira as classes do dataset.

    def modela_dados(self):
        self.carrega_dados()
        dados = self.getTreino()
        dados = dados.fillna(0)                                                         #Substituindo valores vazios por 0.
        self.setFeatures(dados.columns.values)                                          #Setando os valores das features.
        self.setTreino(dados)

    def gera_arquivo_formato_weka(self):
        self.modela_dados()
        arquivo = open(self._arquivoWeka,'w')
        arquivo.write('@relation Influencers_Weka\n')
        arquivo.write('\n')
        for feature in self.getFeatures():
            tipo_feature = ' numeric'                                                    #Caso sejam features numericas o tipo do atributo sera numerico.
            arquivo.write('@attribute '+ feature + tipo_feature+'\n')                        #Escreve o nome do atributo e seus valores possiveis.
        arquivo.write('@attribute Choice {'+ str(self.getClasses().unique()).replace('[','').replace(']','').replace(' ',',') + '}')
        arquivo.write('\n\n')
        arquivo.write('@data\n')                                                        #Declara a secao de dados.
        dados = self.getTreino()
        dados['Classe'] = self.getClasses()                                  #Concatena o valor do treino com a classe para escrever no arquivo.
        dados.to_csv(arquivo,index=False,header=False)

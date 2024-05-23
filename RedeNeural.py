import numpy as np
import pickle

BIAS = 1


def relu(x):
    return np.maximum(0, x)


def relu_derivative(x):
    return np.where(x > 0, 1, 0)


class Neuronio:
    def __init__(self, quantidade_ligacoes):
        self.peso = np.random.uniform(-1, 1, quantidade_ligacoes)
        self.erro = 0
        self.saida = 1
        self.quantidade_ligacoes = quantidade_ligacoes


class Camada:
    def __init__(self, quantidade_neuronios, quantidade_ligacoes):
        self.neuronios = [Neuronio(quantidade_ligacoes) for i in range(quantidade_neuronios)]
        self.quantidade_neuronios = quantidade_neuronios


class RedeNeural:
    def __init__(self, quantidade_escondidas, qtd_neuronios_entrada, qtd_neuronios_escondida, qtd_neuronios_saida):
        qtd_neuronios_entrada += BIAS
        qtd_neuronios_escondida += BIAS

        # Criando neuronios da camada de entrada sem nenhuma ligação
        self.camada_entrada = Camada(qtd_neuronios_entrada, 0)

        # Criando camadas escondidadas
        self.camada_escondida = []
        for i in range(quantidade_escondidas):
            if i == 0:
                # Criando neuronios da primeira camada escondida com ligações a camada de entrada
                self.camada_escondida.append(Camada(qtd_neuronios_escondida, qtd_neuronios_entrada))
                continue

            # Criando neuronios das seguintes camadas escondidas de entrada com ligações da camada de entrada
            self.camada_escondida.append(Camada(qtd_neuronios_escondida, qtd_neuronios_escondida))

        # Criando neuronios da camada de saida com ligações a ultima camada de escondida
        self.camada_saida = Camada(qtd_neuronios_saida, qtd_neuronios_escondida)
        self.quantidade_escondidas = quantidade_escondidas

    # Copia os pesos em um vetor de uma dimensão para as camadas da rede
    def copiar_vetor_para_camadas(self, vetor):
        j = 0
        for camada in self.camada_escondida:
            for neuronio in camada.neuronios:
                neuronio.peso = vetor[j:j + neuronio.quantidade_ligacoes]
                j += neuronio.quantidade_ligacoes

        for neuronio in self.camada_saida.neuronios:
            neuronio.peso = vetor[j:j + neuronio.quantidade_ligacoes]
            j += neuronio.quantidade_ligacoes

    # Copia os pesos das camadas da rede para um vetor de uma dimensão
    def copiar_camadas_para_vetor(self):
        vetor = []
        for camada in self.camada_escondida:
            for neuronio in camada.neuronios:
                vetor.extend(neuronio.peso)

        for neuronio in self.camada_saida.neuronios:
            vetor.extend(neuronio.peso)

        return vetor

    # Atribui os valores de entra da rede
    def copiar_para_entrada(self, vetor_entrada):
        for i in range(len(self.camada_entrada.neuronios) - BIAS):
            self.camada_entrada.neuronios[i].saida = vetor_entrada[i]

    def quantidade_pesos(self):
        soma = 0
        for ca in self.camada_escondida:
            for neuronio in ca.neuronios:
                soma += neuronio.quantidade_ligacoes

        for neuronio in self.camada_saida.neuronios:
            soma += neuronio.quantidade_ligacoes

        return soma

    # Copia os valores de saida da rede para um vetor
    def copiar_da_saida(self, vetor_saida):
        for i, neuronio in enumerate(self.camada_saida.neuronios):
            vetor_saida.append(neuronio.saida)

    def calcular_saida(self):
        for i, neuronio in enumerate(self.camada_escondida[0].neuronios[:-BIAS]):
            mult = []
            for neuronio_entrada, peso in zip(self.camada_entrada.neuronios, neuronio.peso):
                mult.append(neuronio_entrada.saida * peso)

            somatorio = sum(mult)
            neuronio.saida = relu(somatorio)

        for k in range(1, self.quantidade_escondidas):
            for i, neuronio in enumerate(self.camada_escondida[k].neuronios[:-BIAS]):
                mult = []
                for neuronio_anterior, peso in zip(self.camada_escondida[k - 1].neuronios, neuronio.peso):
                    mult.append(neuronio_anterior.saida * peso)
                somatorio = sum(mult)
                neuronio.saida = relu(somatorio)

        for i, neuronio in enumerate(self.camada_saida.neuronios):
            mult = []
            for neuronio_anterior, peso in zip(self.camada_escondida[-1].neuronios, neuronio.peso):
                mult.append(neuronio_anterior.saida * peso)
            somatorio = sum(mult)
            neuronio.saida = relu(somatorio)

    def print_pesos(self):
        print("Pesos da Camada de Entrada:")
        for neuronio in self.camada_entrada.neuronios:
            print(neuronio.peso)

        for i, camada in enumerate(self.camada_escondida):
            print(f"Pesos da Camada Escondida {i + 1}:")
            for neuronio in camada.neuronios:
                print(neuronio.peso)

        print("Pesos da Camada de Saída:")
        for neuronio in self.camada_saida.neuronios:
            print(neuronio.peso)

    def print_saidas(self):
        print("Saídas da Camada de Entrada:")
        for neuronio in self.camada_entrada.neuronios:
            print(neuronio.saida)

        for i, camada in enumerate(self.camada_escondida):
            print(f"Saídas da Camada Escondida {i + 1}:")
            for neuronio in camada.neuronios:
                print(neuronio.saida)

        print("Saídas da Camada de Saída:")
        for neuronio in self.camada_saida.neuronios:
            print(neuronio.saida)


def main():
    rede = RedeNeural(3, 5, 5, 1)
    entrada = [1, 2, 3, 4, 5]

    rede.copiar_para_entrada(entrada)

    rede.calcular_saida()

    saida_obtida = []
    rede.copiar_da_saida(saida_obtida)

    print(f'Saída obtida: {saida_obtida}')


if __name__ == "__main__":
    main()

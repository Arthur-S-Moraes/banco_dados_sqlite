'''Menu de opções:
ao iniciar deve aparecer as opções:
1- Adicionar uma nova tarefa com uma descrição
2- Visualizar Tarefas
3- marcar Tarefas concluidas
4- Remover tarefas especificas
5- Salvar e Carregar Tarefas
'''

import sqlite3


def criar_sql():
    conexao = sqlite3.connect('tarefas.db')
    cursor = conexao.cursor()
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS Tarefas (
                id INTEGER PRIMARY KEY,
                Tarefa TEXT NOT NULL,
                Concluido BOOLEAN NOT NULL,
                DataInicio TEXT NOT NULL
                );
                ''')
    conexao.commit()
        
    return conexao


def adicionar_dados(conexao, id, tarefa, concluido, data):
    cursor = conexao.cursor()
    cursor.execute('INSERT INTO Tarefas VALUES(?, ?, ?, ?)', (id, tarefa, concluido, data))
    conexao.commit()

def visualizar(conexao):
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM Tarefas')
    tarefas = cursor.fetchall()
    for tarefa in tarefas:
        print(tarefa)
        print('')


def editar(conexao, concluido, id):
    cursor = conexao.cursor()
    cursor.execute('UPDATE Tarefas SET Concluido = ? WHERE id = ?',(concluido, id))
    conexao.commit()

def excluir(conexao,id):
    cursor = conexao.cursor()
    cursor.execute('DELETE FROM Tarefas WHERE id = ?',(id,))
    conexao.commit()


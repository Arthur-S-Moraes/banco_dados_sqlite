import PySimpleGUI as sg
from app import *
from datetime import datetime
from time import sleep


sg.theme('dark')


def janela_principal():
    layout = [
        [sg.Text('escolha o que deseja fazer com os dados cadastrados:')],
        [sg.Button('Adicionar', size=(10)), sg.Button('Editar', size=(10)), sg.Button('Visualizar', size=(10)), sg.Button('Excluir', size=(10))],
    ]
    return sg.Window('Janela principal', layout=layout, finalize=True)

def janela_adicionar():
    layout = [
        [sg.Text('ID:', size=(8,1)), sg.Input(key='id',size=(9,1))],
        [sg.Text('Tarefas:', size=(8,1)), sg.Input(key='tarefa',size=(29,1))],
        [sg.Text('Concluido:', size=(8,1)), sg.Radio('Sim','concluido',key='radio_sim'), sg.Radio('Não','concluido',key='radio_nao', default=True)],
        [sg.Text('Data YYYY-MM-DD:', size=(16,1) ), sg.Input(key='data',size=(20,1))],
        [sg.Button('Salvar'), sg.Button('Salvar e voltar', key='salvar_voltar'), sg.Button('cancelar e voltar', key='voltar')]
    ]
    return sg.Window('Adicionar', layout=layout, finalize=True)

def janela_editar():
    layout = [
        [sg.Text('ID, Tarefa, Concluido, Data')],
        [sg.Output(size=(50,15), key='limpar')],
        [sg.Text('qual item (ID) você deseja alterar de sim para não ou vice versa?')],
        [sg.Input(key='id_editar')],
        [sg.Text('Concluido:', size=(8,1)), sg.Radio('Sim','concluido',key='radio_sim', default=True), sg.Radio('Não','concluido',key='radio_nao')],
        [sg.Button('Editar'), sg.Button('Voltar')],
        
    ]
    return sg.Window('editar', layout, finalize=True)

def janela_visualizar():
    layout = [
        [sg.Text('ID, Tarefa, Concluido, Data')],
        [sg.Output(size=(50,15))],
        [sg.Button('Voltar')]
    ]
    return sg.Window('janela_visualizar', layout=layout, finalize=True)

def janela_excluir():
    layout = [
        [sg.Text('ID, Tarefa, Concluido, Data')],
        [sg.Output(size=(50,15), key='limpar')],
        [sg.Text('escolha 1 item para excluir: '),sg.Input(size=4, key='valor_id'), sg.Button('Confirmar'), sg.Button('Voltar')]
    ]
    return sg.Window('Excluir', layout, finalize=True)

janela_principal_, janela_adicionar_, janela_visualizar_, janela_editar_, janela_excluir_ = janela_principal(), None, None, None, None


conexao = criar_sql()
while True:
    window, event, values = sg.read_all_windows()
    if event == sg.WIN_CLOSED:
        break
    
    if window == janela_principal_:
        if event == 'Adicionar':
            janela_principal_.hide()
            janela_adicionar_ = janela_adicionar()
        if event == 'Visualizar':
            janela_principal_.hide()
            janela_visualizar_ = janela_visualizar()
            visualizar(conexao)
        if event == 'Editar':
            janela_principal_.hide()
            janela_editar_ = janela_editar()
            visualizar(conexao)
        if event == 'Excluir':
            janela_principal_.hide()
            janela_excluir_ = janela_excluir()
            visualizar(conexao)
  
    if window == janela_adicionar_:
        tarefa = values['tarefa']
        data = values['data']
        concluido = values['radio_sim']
        id = values['id']
        
        if event == 'Salvar':
            try:
                datetime.strptime(data, '%Y-%m-%d')
            except:
                sg.popup('formato da data incorreta')
            if concluido == True:
                try:
                    adicionar_dados(conexao, id, tarefa, 'sim', data )
                    sg.popup('Dados salvos com sucesso')
                except:
                    sg.popup('ID já está sendo utilizado')
            else:
                try:
                    adicionar_dados(conexao, id, tarefa, 'não', data )
                    sg.popup('Dados salvos com sucesso')
                except:
                    sg.popup('ID já está sendo utilizado')
                    
        elif event == 'salvar_voltar':
                try:
                    datetime.strptime(data, '%Y-%m-%d')
                except:
                    sg.popup('formato da data incorreta')

                if concluido == True:
                    try:
                        adicionar_dados(conexao, id, tarefa, 'sim', data )
                        sg.popup('Dados salvos com sucesso')
                        janela_adicionar_.hide()
                        janela_principal_.un_hide()
                    except:
                        sg.popup('ID já está sendo utilizado')

                else:
                    try:
                        adicionar_dados(conexao, id, tarefa, 'não', data )
                        sg.popup('Dados salvos com sucesso')
                        janela_adicionar_.hide()
                        janela_principal_.un_hide()
                    except:
                        sg.popup('ID já está sendo utilizado')
               
        elif event == 'voltar':
            janela_adicionar_.hide()
            janela_principal_.un_hide()

    if window == janela_visualizar_:
        if event == 'Voltar':
            janela_visualizar_.hide()
            janela_principal_.un_hide()
            
    if window == janela_editar_:
        if event == 'Editar':
            try:
                id = int(values['id_editar'])
                if values['radio_sim'] == True:
                    editar(conexao, 'sim', id)
                    window['limpar'].update('')
                    sleep(0.4)
                    visualizar(conexao)
                    print(f'''#################
você alterou o item de ID {id}
###############''')
                
                if values['radio_sim'] == False:
                    editar(conexao, 'não', id)
                    window['limpar'].update('')
                    sleep(0.4)
                    visualizar(conexao)
                    print(f'''#################
você alterou o item de ID {id}
###############''')

            except:
                sg.popup('item inexistente na lista')
                continue
        elif event == 'Voltar':
            janela_editar_.close()
            janela_principal_.un_hide()
            
    if window == janela_excluir_:
        if event == 'Confirmar':
            try:
                id = int(values['valor_id'])
                valor = sg.popup_ok_cancel(f'Desejá mesmo deletar o ID {id}')
            except:
                print('digite um numero válido')
                continue

            if valor == 'OK':
                excluir(conexao, id)
                window['limpar'].update('')
                sleep(0.2)
                visualizar(conexao)
                print(f'''#################
você deletou o item de ID {id}
###############''')
        elif event == 'Voltar':
            janela_excluir_.close()
            janela_principal_.un_hide()

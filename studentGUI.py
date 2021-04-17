import PySimpleGUI as sg
import pandas as pd

# Define theme
sg.theme('DarkAmber')  # Add a touch of color


# Callback function
def calculateStudentDifference(UNOPath, fakturaPath):
    inputsAreOK = True
    try:
        dfFaktura = pd.read_excel(fakturaPath)

        dfUNO = pd.read_excel(UNOPath)

        vareNrListFaktura = dfFaktura['VareNr'].tolist()
        vareNrListUNO = dfUNO['Varenr.'].tolist()

        same_values = list(set(vareNrListFaktura) & set(vareNrListUNO))
        onlyInUNO = list(set(vareNrListUNO) - set(vareNrListFaktura))
        onlyInFaktura = list(set(vareNrListFaktura) - set(vareNrListUNO))
    except:
        onlyInUNO = []
        onlyInFaktura = []
        inputsAreOK = False

    return onlyInUNO, onlyInFaktura, inputsAreOK


# Lookup dictionary that maps button to function to call
dispatch_dictionary = {'Find forskelle': calculateStudentDifference}

# All the stuff inside your window.
layout = [[sg.Text('UNO Excelark:', size=(15, 1)), sg.Input(key='-INUNO-'),
           sg.FileBrowse('Åbn', file_types=(('Excel fil', '*.*'),))],
          [sg.Text('Faktura Excelark:', size=(15, 1)), sg.Input(key='-INfaktura-'), sg.FileBrowse('Åbn', file_types=(('Excel fil', '*.*'),))],
          [sg.Button('Find forskelle')],
          [sg.Output(size=(80, 10), key='-OUTforskelle-')],
          [sg.Cancel('Afslut')]]

# Create the Window
window = sg.Window('Elevoversigt').layout(layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Afslut':  # if user closes window or clicks cancel
        break
    # Lookup event in function dictionary
    if event in dispatch_dictionary:
        func_to_call = dispatch_dictionary[event]   # get function from dispatch dictionary
        lUNO, lFaktura, inputOK = func_to_call(values['-INUNO-'], values['-INfaktura-'])
        window['-OUTforskelle-'].update('')
        if inputOK:
            print('Kun i UNO:')
            print(lUNO)
            print('')
            print('Kun i Faktura:')
            print(lFaktura)
        else:
            print('Fejl i excelfilerne. Prøv igen')
    else:
        print('Event {} not in dispatch dictionary'.format(event))

window.close()

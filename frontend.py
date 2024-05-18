import PySimpleGUI as psg
import distort

layout=[
    [psg.Text('Enter some parametrs', expand_x=True,
                             justification='center')],
    [psg.Text('Maps', expand_x=True, justification='center'), psg.Input(key = 'Maps')],
    [psg.Text('Video', expand_x=True, justification='center'), psg.Input(key='Video')],
    [psg.Text('Telemetry', expand_x=True, justification='center'), psg.Input(key = 'Telemetry')],
    [psg.Text('Distortion coeffs', expand_x=True, justification='center'), psg.Input(key='dis_coeffs')],
    [psg.Button('Send', key = 'Send')],
  ]

window = psg.Window('Smeshariki', layout)

while True:
    event, values =window.read()
    if event == psg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Send':
        distort.distortion(values['Video'], values['dis_coeffs'])
        print(event, values)

window.close()
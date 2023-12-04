import netmiko
from PySimpleGUI import popup
from time import sleep
import PySimpleGUI as sg
from PySimpleGUI import Input, Text, Button, Window, Output, popup_get_text, WIN_CLOSED

# def get_component

# def navigate():
CREDS = {
    "device_type": "mikrotik_routeros",
    "ip": "192.168.56.2",
    "username": "admin",
    "password": "admin",
    "port": "22",
} 

def get_page():
    column1=[
        [sg.Button("Show IP")],
        [sg.Button("Change IP")],
        [sg.Button("Add IP address")],
        [sg.Button("Remove IP Address")],
        [sg.Button("Enable ip address")],
        [sg.Button("Disable ip address")]
    ]
    column2=[
        [sg.Button("Print identity")],
        [sg.Button("Change identity")],
        [sg.Button("Show users")],
        [sg.Button("User statistics")],
        [sg.Button("Add new user")],
        [sg.Button("Remove user")]

    ]

    column3=[
        [sg.Button("Show default configuration")],
        [sg.Button("List all file details")],
        [sg.Button("Create backup file")],
        [sg.Button("Connect Internet")],
        [sg.Button("Disconnect Internet")],
        [sg.Button("Show ethernet adapters")]
    ]

    column4=[
        [sg.Button("Show services and ports")],
        [sg.Button("Change service port")],
        [sg.Button("Show firewall rules")],
        [sg.Button("Add new firewall rules")],
        [sg.Button("Remove firewall rule")],
        [sg.Button("Enable Firewall Rule")]
    ]

    column5=[
        [sg.Button("Disable Firewall Rule")],
        [sg.Button("Interface Status")]
        
    ]
    layout=[
         [sg.Text("Connect to Mikrotik")],
        [sg.Text("Enter IP"), sg.Input(CREDS['ip'], key="_ip_")],
        [sg.Text("Enter Username"), sg.Input(CREDS['username'], key="_username_")],
        [sg.Text("Enter Password"), sg.Input(CREDS['password'], key="_password_")],
        [sg.Text("Enter Port"), sg.Input(CREDS['port'], key="_port_"), sg.Button("Connect")],
        [
            sg.Column(column1, vertical_scroll_only=True),  # First column buttons
            sg.Column(column2, vertical_scroll_only=True),
            sg.Column(column3, vertical_scroll_only=True),
            sg.Column(column4, vertical_scroll_only=True),
            sg.Column(column5, vertical_scroll_only=True)   # Second column buttons
        ],
        [sg.Multiline(size=(50, 10), key="_output_", disabled=True, reroute_stdout=True)]
    ]
    return sg.Window("Main page", layout)
    # return Window("Main page", [[
    #     [Text("Connect to Mikrotik")],
    #     [Text("Enter Ip"), Input(CREDS['ip'], key="_ip_")],
    #     [Text("Enter Username"), Input(CREDS['username'], key="_username_"),],
    #     [Text("Enter Password"), Input(CREDS['password'], key="_password_"),],
    #     [Text("Enter Port"), Input(CREDS['port'], key="_port_")],
    #     [Button("Connect")],+
    #     [Button("Show services and ports")],+
    #     [Button("Show IP")],+
    #     [Button("Show default configuration")],+
    #     [Button("Print identity")],+
    #     [Button("Change identity")],+
    #     [Button("Show users")],+
    #     [Button("User statistics")],+
    #     [Button("List all file details")],+
    #     [Button("Interface Status")],+
    #     [Button("Show ethernet adapters")],+
    #     [Button("Show firewall rules")],+
    #     [Button("Change IP")],+
    #     [Button("Add IP address")],+
    #     [Button("Remove IP Address")],+
    #     [Button("Enable ip address")],+
    #     [Button("Disable ip address")],+
    #     [Button("Add new user")],+
    #     [Button("Remove user")],+
    #     [Button("Disconnect Internet")],+
    #     [Button("Create backup file")],+
    #     [Button("Connect internet")],+
    #     [Button("Add new firewall rules")],+
    #     [Button("Remove firewall rule")],+
    #     [Button("Enable Firewall Rule")],+
    #     [Button("Disable Firewall Rule")],+
    #     [Button("Change service port")]+
    # ], [Output(size=(50, 10), key="_output_")]],size=(800, 600))

page = get_page()

def clean_output():
    page["_output_"].update('')

connection = None
def connect():
    for _ in range(3): #3 defe retry edir 
            try:
                CREDS["ip"] = values["_ip_"]
                CREDS["username"] = values["_username_"]
                CREDS["password"] = values["_password_"]
                CREDS["port"] = values["_port_"]
                print("Connected")
                return netmiko.ConnectHandler(**CREDS)
            except Exception as e:
                popup('Login failed:  '+str(e)+'\nRetrying...')
                sleep(10)
                continue

while True:
    event, values = page.read()

    if event == WIN_CLOSED:
        
        break
    
    if (event == "Connect" and connection is None): # run
        connection = connect()
    
    if connection is not None:
        try:
            if event == "Show IP":
                clean_output()
                print(connection.send_command("ip address print", cmd_verify=False))
            elif event == "Change IP":
                clean_output()
                text = (popup_get_text("Enter IP"))
                interface = popup_get_text("Enter interface")

                if text and (interface.lower() in ['ether1', 'ether2', 'ether3']):
                    page['_ip_'].update(text)
                    print(connection.send_command(f"ip address set [find interface={interface}] address={text}", cmd_verify=False)) 
                elif not text and not (interface in ['ether1', 'ether2', 'ether3']):
                    print('enter everything correctly')
                elif not text:
                    print('enter ip correctly')
                elif not (interface in ['ether1', 'ether2', 'ether3']):
                    print('enter interface correctly')
                
            elif event=="Add IP address":
                clean_output()
                text = (popup_get_text("Enter IP"))
                interface = popup_get_text("Enter interface")

                if text and (interface in ['ether1', 'ether2', 'ether3']):
                    page['_ip_'].update(text)
                    print(connection.send_command(f"ip address add address={text} interface={interface}", cmd_verify=False))
                elif not text and not (interface in ['ether1', 'ether2', 'ether3']):
                    print('enter everything correctly')
                elif not text:
                    print('enter ip correctly')
                elif not (interface.lower() in ['ether1', 'ether2', 'ether3']):
                    print('enter interface correctly')
            
            elif event=="Remove IP Address":
                interface = popup_get_text("Enter interface")

                if (interface.lower() in ['ether1', 'ether2', 'ether3']):
                    clean_output()
                    print(connection.send_command(f"ip address remove [find interface={interface}]", cmd_verify=False)) 
                else:
                    clean_output()
                    print('enter interface correctly')
               
            elif event=="Enable ip address":
                number = popup_get_text("Enter number:")
                clean_output()
                print(connection.send_command(f"ip address enable {number}", cmd_verify=False)) 

            elif event=="Disable ip address":
                number = popup_get_text("Enter number:")
                clean_output()
                print(connection.send_command(f"ip address disable {number}", cmd_verify=False))
       
            elif event=="Change service port":
                service_list=['telnet','ftp','www','ssh','www-ssl','api','winbox','api-ssl']
                service= popup_get_text("Enter service name(ssh or ftp):")
                if service.lower() in service_list:
                    port = popup_get_text("Enter port number:")
                    print(connection.send_command(f"/ip service set [find name={service}] port={port}"))
                else:
                    print("Enter correct service name")
            elif event=="Add new user":
                clean_output()
                name = (popup_get_text("Enter new username"))
                password = popup_get_text("Enter new password")
                print(connection.send_command(f'user add name={name} password={password} group=full'))
            
            elif event=="Remove user":
                name = (popup_get_text("Enter the username"))
                print(connection.send_command(f'user remove {name}'))
            
            elif event=="Create backup file":
                name = (popup_get_text("Enter the backup file name:"))
                print(connection.send_command(f'system backup save name={name}'))

                
            elif event == "Show services and ports":
                clean_output()
                print(connection.send_command('ip service print', cmd_verify=False))
            elif event=="Show default configuration":
                clean_output()
                print(connection.send_command('system default-configuration print', cmd_verify=False))
            elif event=="Print identity":
                clean_output()
                print(connection.send_command('system identity print', cmd_verify=False))
            elif event=="Show users":
                clean_output()
                print(connection.send_command('user print', cmd_verify=False))
            elif event == "Change identity":
                clean_output()
                text = (popup_get_text("Enter Identity"))
                if (not text): 
                    popup("Enter Indentity correctly")
                else:
                    print(connection.send_command(f"system identity set name={text}", cmd_verify=False))
            
            elif event=="Disconnect Internet":
                print(connection.send_command('interface ethernet disable [find name!=ether2]'))

            elif event=="Connect Internet":
                print(connection.send_command('interface ethernet enable [find name!=ether2]'))    
            
            elif event=="Add new firewall rules":
                 chains=['forward','input','output']
                 chain=popup_get_text("Enter chain:(forward,input or output)")
                 if chain in chains:
                      actions=['accept','drop']
                      action=popup_get_text("Enter action(accept or drop):")
                      if action not in actions:
                          print("Enter correcr action type")
                      else:
                          print(connection.send_command(f'ip firewall filter add chain={chain} action={action}'))
                 else:
                     print("Enter correct chain type")

            elif event=="Remove firewall rule":
                    rule_number=popup_get_text("Enter firewall rule number")
                    print(connection.send_command(f"ip firewall filter remove {rule_number}"))
            
            elif event=="Enable Firewall Rule":
                rule_number =popup_get_text("Enter firewall rule number")
                print(connection.send_command(f"ip firewall filter enable {rule_number}"))
            
            elif event=="Disable Firewall Rule":
                rule_number =popup_get_text("Enter firewall rule number")
                print(connection.send_command(f"ip firewall filter disable {rule_number}"))

            elif event=="User statistics":
                clean_output()
                print(connection.send_command('user active print', cmd_verify=False))
            elif event=="List all file details":
                clean_output()
                print(connection.send_command('file print detail', cmd_verify=False))
            elif event=="Interface Status":
                clean_output()
                print(connection.send_command('interface print detail', cmd_verify=False))
            elif event=="Show ethernet adapters":
                clean_output()
                print(connection.send_command('interface ethernet print', cmd_verify=False))
            elif event=="Show firewall rules":
                clean_output()
                print(connection.send_command('ip firewall filter print', cmd_verify=False))
            
          


        except Exception as e:
            popup("Reopen App")
            page.close()
            connection = None
            page = get_page()
  

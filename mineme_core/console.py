import os


class Console:
    def __init__(self):
        self.main_command = '' 
        self.arguments = []
    
    def get_input(self):
        command_args = input('> ').lower().split()
        try:
            self.main_command = command_args[0]
            self.arguments = command_args[1:]
        except:
            return
        
    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

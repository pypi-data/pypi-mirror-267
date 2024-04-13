from colorama import Fore, Style, Back as bg
from typing import Optional

import colorama

reset = Style.RESET_ALL
brighten = Style.BRIGHT
dim_message = Style.DIM

class Colors:
    def Show():
        """
        Shows all available colors 
        """
        Title_Print("All Colors", color=Colors.Cyan)
        Colored_Message("Red", color=Colors.Red)
        Colored_Message("Light Red", color=Colors.Light_Red)
        Colored_Message("Green", color=Colors.Green)
        Colored_Message("Light Green", color=Colors.Light_Green)
        Colored_Message("Blue", color=Colors.Blue)
        Colored_Message("Light Blue", color=Colors.Light_Blue)
        Colored_Message("Black", color=Colors.Black)
        Colored_Message("Light Black", color=Colors.Light_Black)
        Colored_Message("Yellow", color=Colors.Yellow)
        Colored_Message("Light Yellow", color=Colors.Light_Yellow)
        Colored_Message("Cyan", color=Colors.Cyan)
        Colored_Message("Light Cyan", color=Colors.Light_Cyan)
        Colored_Message("White", color=Colors.White)
        Colored_Message("Light White", color=Colors.Light_White)
        Colored_Message("Magenta", color=Colors.Magenta)
        Colored_Message("Light Magenta", color=Colors.Light_Magenta)
        
    Red = Fore.RED
    Green = Fore.GREEN
    Blue = Fore.BLUE
    Black = Fore.BLACK
    Yellow = Fore.YELLOW
    Cyan = Fore.CYAN
    White = Fore.WHITE
    Magenta = Fore.MAGENTA
    Light_Red = Fore.LIGHTRED_EX
    Light_Green = Fore.LIGHTGREEN_EX
    Light_Blue = Fore.LIGHTBLUE_EX
    Light_Black = Fore.LIGHTBLACK_EX
    Light_Yellow = Fore.LIGHTYELLOW_EX
    Light_Cyan = Fore.LIGHTCYAN_EX
    Light_White = Fore.LIGHTWHITE_EX
    Light_Magenta = Fore.LIGHTMAGENTA_EX


class Highlights:
    def Show():
        """
        Shows all available highlight colors 
        """
        Title_Print("All Colors", color=Colors.Cyan)
        Colored_Message("Red", color=Colors.Red)
        Colored_Message("Light Red", color=Colors.Light_Red)
        Colored_Message("Green", color=Colors.Green)
        Colored_Message("Light Green", color=Colors.Light_Green)
        Colored_Message("Blue", color=Colors.Blue)
        Colored_Message("Light Blue", color=Colors.Light_Blue)
        Colored_Message("Black", color=Colors.Black)
        Colored_Message("Light Black", color=Colors.Light_Black)
        Colored_Message("Yellow", color=Colors.Yellow)
        Colored_Message("Light Yellow", color=Colors.Light_Yellow)
        Colored_Message("Cyan", color=Colors.Cyan)
        Colored_Message("Light Cyan", color=Colors.Light_Cyan)
        Colored_Message("White", color=Colors.White)
        Colored_Message("Light White", color=Colors.Light_White)
        Colored_Message("Magenta", color=Colors.Magenta)
        Colored_Message("Light Magenta", color=Colors.Light_Magenta)
        
    Red = bg.RED
    Green = bg.GREEN
    Blue = bg.BLUE
    Black = bg.BLACK
    Yellow = bg.YELLOW
    Cyan = bg.CYAN
    White = bg.WHITE
    Magenta = bg.MAGENTA
    Light_Red = bg.LIGHTRED_EX
    Light_Green = bg.LIGHTGREEN_EX
    Light_Blue = bg.LIGHTBLUE_EX
    Light_Black = bg.LIGHTBLACK_EX
    Light_Yellow = bg.LIGHTYELLOW_EX
    Light_Cyan = bg.LIGHTCYAN_EX
    Light_White = bg.LIGHTWHITE_EX
    Light_Magenta = bg.LIGHTMAGENTA_EX


def Info_Message(message, color: Colors = Colors.White, highlight: Highlights = '', title_color: Colors = Colors.Blue):  
    """
    This function prints out an informational message.
    
    color: color your direct message a specific color, default is white.
    
    highlight: highlight the message in a specific color!
    
    title_color: Color the title of the message, default is blue.
    """
    print(f"{title_color + brighten}Info{reset}: {highlight + color + message + reset}")
    
def Error_Message(message, color: Colors = Colors.White, highlight: Highlights = '', title_color: Colors = Colors.Red):
    """
    This function prints out an error message.
    
    color: color your direct message a specific color, default is white.
    
    highlight: highlight the message in a specific color!
    
    title_color: Color the title of the message, default is red.
    """
    print(f"{title_color}Error{reset}: {highlight + color + message + reset}")

    
def Connection_Error_Message(message, color: Colors = Colors.White, highlight: Highlights = '', title_color: Colors = Colors.Red):
    """
    This function prints out a failed connection message.
    
    color: color your direct message a specific color, default is white.
    
    highlight: highlight the message in a specific color!
    
    title_color: Color the title of the message, default is red.
    """
    print(f"{title_color}Connection Error{reset}: {highlight + color +  message + reset}")
    
def Success_Message(message, color: Colors = Colors.White, highlight: Highlights = '', title_color: Colors = Colors.Green):
    """
    This function prints out a success message.
    
    color: color your direct message a specific color, default is white.
    
    highlight: highlight the message in a specific color!
    
    title_color: Color the title of the message, default is green.
    """
    print(f"{title_color + brighten}Success{reset}: {highlight + color + message + reset}")
    
def Successful_Connection_Message(message, color: Colors = Colors.White, highlight: Highlights = '', title_color: Colors = Colors.Green):
    """
    This function prints out a successful connection message.
    
    color: color your direct message a specific color, default is white.
    
    highlight: highlight the message in a specific color!
    
    title_color: Color the title of the message, default is green.
    """
    print(f"{title_color + brighten}Successful Connection{reset}: {highlight + color + message + reset}")
    
def Note_Message(message, color: Colors = Colors.White, highlight: Highlights = '', title_color: Colors = Colors.Yellow):
    """
    This function prints out something the user should take note of.
    
    color: color your direct message a specific color, default is white.
    
    highlight: highlight the message in a specific color!
    
    title_color: Color the title of the message, default is yellow.
    """
    print(f"{title_color}Note{reset}: {highlight + color +  message + reset}")
    
def Warning_Message(message, color: Colors = Colors.White, highlight: Highlights = '', title_color: Colors = Colors.Yellow):
    """
    This function prints out a warning message.
    
    color: color your direct message a specific color, default is white.
    
    highlight: highlight the message in a specific color!
    
    title_color: Color the title of the message, default is yellow.
    """
    print(f"{title_color}Warning{reset}: {highlight + color +  message + reset}")    

    
def Title_Print(title, color: Colors = Colors.Green, highlight: Highlights = ''):
    """
    This function prtins out a title.
    
    color: color your direct message a specific color, default is green.
    
    highlight: highlight the message in a specific color!
    """
    print(f"=== {highlight + color + brighten + title + reset} ===")    

     
def Redacted_Message(message, color: Colors = Colors.White, highlight: Highlights = '', title_color: Colors = Colors.Red):
    """
    This function prints out a redacted message.
    
        The use of this is un-realistic, i just made it for fun.
    
    color: color your direct message a specific color, default is white.
    
    highlight: highlight the message in a specific color!
    
    title_color: Color the title of the message, default is yellow.
    """
    print(f"{title_color}REDACTED{reset}: {highlight + color + message + reset}")    


def Colored_Message(message, color: Colors = Colors.White, highlight: Highlights = ''):
    """
    This function allows you to print out your own colored message with ease!
    
    color: color your direct message a specific color, default is white.
    
    highlight: highlight the message in a specific color!
    """
    print(highlight + color + message + reset)
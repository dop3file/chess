import random


def startup_menu():
    from gui.menu import Menu
    menu = Menu()
    menu.start_main_menu()

def get_random_rgb_color():
    return (
        random.randint(1,255),
        random.randint(1,255),
        random.randint(1,255)
    )
import sys
from ..views import BookConsoleView


class MainMenu:
    """
    Main menu for the library management system.
    """

    class MenuChoices:
        ADD_BOOK = "1"
        DELETE_BOOK = "2"
        SEARCH_BOOK = "3"
        DISPLAY_BOOKS = "4"
        CHANGE_STATUS = "5"
        EXIT = "6"

    MENU_OPTIONS = {
        "1": "Добавить книгу",
        "2": "Удалить книгу",
        "3": "Поиск книг",
        "4": "Показать все книги",
        "5": "Изменить статус книги",
        "6": "Выход",
    }

    PROMPT_MENU_OPTION = "Введите номер опции: "
    MSG_INVALID_OPTION = "Неверный выбор. Пожалуйста, попробуйте снова."
    MSG_EXITING = "Выход из приложения."

    def __init__(self):
        self.view = BookConsoleView()

    def display_menu(self):
        self.view._print("\nСистема управления библиотекой")
        for key, value in self.MENU_OPTIONS.items():
            print(f"{key}. {value}")

    def run(self):
        while True:
            self.display_menu()
            choice = self.view._input(self.PROMPT_MENU_OPTION).strip()
            if choice == self.MenuChoices.ADD_BOOK:
                self.view.create()
            elif choice == self.MenuChoices.DELETE_BOOK:
                self.view.delete()
            elif choice == self.MenuChoices.SEARCH_BOOK:
                self.view.search()
            elif choice == self.MenuChoices.DISPLAY_BOOKS:
                self.view.display_all()
            elif choice == self.MenuChoices.CHANGE_STATUS:
                self.view.change_status()
            elif choice == self.MenuChoices.EXIT:
                self.view._print(self.MSG_EXITING)
                sys.exit()
            else:
                self.view._print(self.MSG_INVALID_OPTION)

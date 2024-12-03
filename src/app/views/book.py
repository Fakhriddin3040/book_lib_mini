from typing import Any, Dict
from src.app.services import BookService
from utils.settings import lazy_settings


class BookConsoleView:
    """
    s1mple console view for book entity
    for interaction with the book entity
    and the user(my braza ahaahah)
    """

    # Constants for field validators
    _fields_validators = {
        lazy_settings.PRIMARY_KEY_LOOKUP: lazy_settings.PRIMARY_KEY_TYPE_CONVERTER,  # Assuming the primary key is an integer
        "title": str,
        "author": str,
        "year": int,
        "status": "_validate_status",
    }

    # Status oooptions for my braza(user)
    class StatusOptions:
        AVAILABLE = "в наличии"
        ISSUED = "выдана"

    class SearchChoices:
        TITLE = "1"
        AUTHOR = "2"
        YEAR = "3"

    # Status options for user(ma braza xD) selection
    status_options = {
        "1": StatusOptions.AVAILABLE,
        "2": StatusOptions.ISSUED,
    }

    # Constants for user prompts and messages(user is my braza)
    PROMPT_TITLE = "Введите название книги: "
    PROMPT_AUTHOR = "Введите автора книги: "
    PROMPT_YEAR = "Введите год издания: "
    PROMPT_BOOK_ID = "Введите ID книги: "
    PROMPT_BOOK_ID_DELETE = "Введите ID книги для удаления: "
    PROMPT_SEARCH_OPTION = "Введите номер опции: "
    PROMPT_STATUS_OPTION = "Введите номер статуса: "
    PROMPT_CONFIRM_DELETE = "Вы уверены, что хотите удалить книгу? (y/n): "

    MSG_BOOK_ADDED = "Книга добавлена с ID: {id}"
    MSG_BOOK_DELETED = "Книга успешно удалена."
    MSG_BOOK_STATUS_UPDATED = "Статус книги успешно обновлен."
    MSG_NO_BOOKS_FOUND = "Книги не найдены."
    MSG_LIBRARY_EMPTY = "Библиотека пуста."
    MSG_INVALID_INPUT = "Неверный выбор. Пожалуйста, попробуйте снова."
    MSG_ERROR = "Ошибка: {error}"

    MENU_SEARCH = "Поиск по:\n1. Названию\n2. Автору\n3. Году издания"
    MENU_STATUS = "Выберите новый статус:\n1. В наличии\n2. Выдана"

    def __init__(self, service: BookService = None):
        """"init class, yoooo"""
        self.service = service or BookService()

    def print_separator(self) -> None:
        """Just print some separators"""
        print("-" * 50)

    def _print(self, message: str) -> None:
        """My own print"""
        print("\n\n\n" + message)
        self.print_separator()

    def _input(self, message: str) -> str:
        """My own input"""
        return input("\n\n" + message)

    def validate(self, **data) -> Dict[str, Any]:
        """
        Validates fields of data, mapping them to their
        validators, which are getting from the _fields_validators
        If u need some help, just ask me, my braza ahahaahhahah.
        My credentials:
        base64 -d <<< 'aHR0cHM6Ly9naXRodWIuY29tL0Zha2hyaWRkaW4zMDQwCg==' xD
        """
        if not self._fields_validators:
            raise ValueError(
                f"No fields provided for validation in {self.__class__.__name__}"
            )
        result = {}
        for field, value in data.items():
            self.check_field(field)
            validator = self._fields_validators[field]
            if callable(validator):
                try:
                    result[field] = validator(value)
                except ValueError as e:
                    raise ValueError(f"Invalid value for {field}: {e}")
            elif isinstance(validator, str):
                method_name = validator
                if hasattr(self, method_name):
                    method = getattr(self, method_name)
                    result[field] = method(value)
                else:
                    raise ValueError(
                        f"Validator method '{method_name}' not found in {self.__class__.__name__}"
                    )
            else:
                raise ValueError(f"Invalid validator for field '{field}'")
        return result

    def check_field(self, field: str) -> None:
        if field not in self._fields_validators:
            raise ValueError(
                f"Invalid field '{field}' for model '{self.__class__.__name__}'"
            )

    def _validate_status(self, value):
        if value not in [self.StatusOptions.AVAILABLE, self.StatusOptions.ISSUED]:
            raise ValueError(
                f"Статус должен быть '{self.StatusOptions.AVAILABLE}' или '{self.StatusOptions.ISSUED}'"
            )
        return value

    def create(self) -> None:
        """
        Create a new book.
        """
        try:
            self._create()
        except ValueError as e:
            self._print("Ошибка в процессе создания книги: {error}".format(error=e))

    def delete(self) -> None:
        """
        Delete a book.
        """
        try:
            self._delete()
        except ValueError as e:
            self._print("Ошибка в процессе удаления книги: {error}".format(error=e))

    def search(self) -> None:
        """
        Search for books.
        """
        try:
            self._search()
        except ValueError as e:
            self._print("Ошибка в процессе поиска книг: {error}".format(error=e))

    def change_status(self) -> None:
        """
        Change the status of a book.
        """
        try:
            self._change_status()
        except ValueError as e:
            self._print("Ошибка в процессе изменения статуса книги: {error}".format(error=e))

    def _create(self) -> None:
        """
        Book creation via console input.
        """
        data = {}
        data["title"] = input(self.PROMPT_TITLE).strip()
        data["author"] = input(self.PROMPT_AUTHOR).strip()
        data["year"] = input(self.PROMPT_YEAR).strip()
        data["status"] = self.StatusOptions.AVAILABLE
        validated_data = self.validate(**data)
        book = self.service.create(**validated_data)
        self._print(self.MSG_BOOK_ADDED.format(id=book.id))

    def _delete(self) -> None:
        """
        Deletes a book via console input.
        """
        book_id = input(self.PROMPT_BOOK_ID_DELETE).strip()
        confirmed = input(self.PROMPT_CONFIRM_DELETE).strip().lower()
        if confirmed != "y":
            self._print("Удаление отменено.")
            return
        validated_data = self.validate(**{lazy_settings.PRIMARY_KEY_LOOKUP: book_id})
        self.service.delete(**validated_data)
        self._print(self.MSG_BOOK_DELETED)

    def _search(self) -> None:
        """
        Handles searching for books via console input.
        """
        self._print(self.MENU_SEARCH)
        choice = input(self.PROMPT_SEARCH_OPTION).strip()
        filters = {}
        if choice == self.SearchChoices.TITLE:
            title = input(self.PROMPT_TITLE).strip()
            filters["title"] = title
        elif choice == self.SearchChoices.AUTHOR:
            author = input(self.PROMPT_AUTHOR).strip()
            filters["author"] = author
        elif choice == self.SearchChoices.YEAR:
            year = input(self.PROMPT_YEAR).strip()
            filters["year"] = year
        else:
            self._print(self.MSG_INVALID_INPUT)
            return

        validated_filters = self.validate(**filters)
        books = self.service.filter(**validated_filters)
        if books:
            for book in books:
                self._print(book)
        else:
            self._print(self.MSG_NO_BOOKS_FOUND)

    def display_all(self) -> None:
        """
        Displays all books in the library.
        """
        books = self.service.all()

        if books:
            for book in books:
                self._print(book)

        else:
            self._print(self.MSG_LIBRARY_EMPTY)

    def _change_status(self) -> None:
        """
        Book's status change via console input.
        """
        book_id = input(self.PROMPT_BOOK_ID).strip()
        self._print(self.MENU_STATUS)
        status_choice = input(self.PROMPT_STATUS_OPTION).strip()
        status = self.status_options.get(status_choice)

        if not status:
            self._print(self.MSG_INVALID_INPUT)
            return

        validated_data = self.validate(
            **{lazy_settings.PRIMARY_KEY_LOOKUP: book_id, "status": status}
        )
        self.service.update(
            {
                lazy_settings.PRIMARY_KEY_LOOKUP: validated_data[
                    lazy_settings.PRIMARY_KEY_LOOKUP
                ]
            },
            status=validated_data["status"],
        )
        self._print(self.MSG_BOOK_STATUS_UPDATED)

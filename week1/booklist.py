"""
Book navigation data structure.
@author: R.J. Both & Vlad Niculae

Gilian Honkoop 13710729
"""

from __future__ import annotations
import pytest
from typing import Optional


class Page:
    def __init__(self, text: str, link=None):
        self.text = text
        self.link = link


class Chapter:
    def __init__(self, first_page: Optional[Page], link=None, rlink=None):
        self.first_page = first_page
        self.link = link
        self.rlink = rlink


class Book:
    def __init__(self) -> None:
        """Initialize an empty book."""
        self.first_chap = None

    def print_book(self) -> None:
        """Displays the book structure in stdout."""
        curr_chapter_number = 1

        print("[[")

        curr_chapter = self.first_chapter
        while curr_chapter is not None:
            print("Chapter {}:".format(curr_chapter_number))
            next_chapter = curr_chapter.link
            stop_at = next_chapter.first_page if next_chapter else None
            curr_page = curr_chapter.first_page
            while curr_page != stop_at:
                print("-", curr_page.text)
                curr_page = curr_page.link

            curr_chapter = next_chapter
            curr_chapter_number += 1

        print("]]")

    def print_book_backward(self) -> None:
        """Displays the book structure backwards in stdout. (see exercise)"""
        curr_chapter_number = self.chapter_count()

        print("[[")

        curr_chapter = self.last_chapter
        while curr_chapter is not None:
            print("Chapter {}:".format(curr_chapter_number))
            curr_page = curr_chapter.first_page
            print("-", curr_page.text)

            curr_chapter = curr_chapter.rlink
            curr_chapter_number -= 1

        print("]]")

    @property
    def first_chapter(self) -> Optional[Chapter]:
        """Returns the first chapter in the book,
        or None if the book is empty."""
        if self.first_chap:
            return self.first_chap

        return None

    @property
    def last_chapter(self) -> Optional[Chapter]:
        """Returns the last chapter in the book,
        or None if the book is empty"""
        if self.first_chap:
            curr_chap = self.first_chap

            while curr_chap.link:
                curr_chap = curr_chap.link

            return curr_chap

        return None

    @property
    def first_page(self) -> Optional[Page]:
        """Returns the first page in the book, or None if the book is empty."""
        if self.first_chap:
            if self.first_chap.first_page:
                return self.first_chap.first_page

        return None

    @property
    def last_page(self) -> Optional[Page]:
        """Returns the last page in the book, or None if the book is empty"""
        if self.first_chap:
            curr_chap = self.first_chap

            while curr_chap.link:
                previous_chap = curr_chap
                curr_chap = curr_chap.link

            if not curr_chap.first_page:
                curr_chap = previous_chap

            curr_page = curr_chap.first_page

            while curr_page.link:
                curr_page = curr_page.link

            return curr_page

        return None

    def prepend_chapter(self, text):
        """Creates a new chapter, at the start of the book, with a page
        containing text"""
        new_page = Page(text, link=self.first_page)

        if self.first_chap:
            curr_chap = self.first_chap
        else:
            curr_chap = None

        new_chap = Chapter(new_page, link=curr_chap)

        if self.first_chap:
            self.first_chap.rlink = new_chap

        self.first_chap = new_chap

    def append_chapter(self, text):
        """Creates a new chapter, at the end of the book, with a page
        containing text"""
        new_page = Page(text, link=None)

        if self.last_page:
            self.last_page.link = new_page

        new_chap = Chapter(new_page, link=None, rlink=self.last_chapter)

        if self.first_chap:
            self.last_chapter.link = new_chap
        else:
            self.first_chap = new_chap

    def prepend_page(self, text: str, new_chapter=False) -> Book:
        """Prepend a new page with the given text, at the start of the book.

        To create a new chapter containing the new page,
        set `new_chapter=True`,
        otherwise the new page should be part of the first chapter.

        Return the book itself, so multiple calls can be chained.
        """
        if not new_chapter and not self.first_chap:
            raise ValueError("There is no chapter yet")
        elif new_chapter or not self.first_chap:
            self.prepend_chapter(text)
        else:
            if self.first_chap.first_page:
                curr_first_page = self.first_chap.first_page
            else:
                curr_first_page = None

            new_page = Page(text, link=curr_first_page)
            self.first_chap.first_page = new_page

        return self

    def append_page(self, text: str, new_chapter=False) -> Book:
        """Append a new page with the given text, at the end of the book.

        To create a new chapter containing the new page,
        set `new_chapter=True`,
        otherwise the new page should be part of the last chapter.

        Return the book itself, so multiple calls can be chained.
        """
        if not new_chapter and not self.first_chap:
            raise ValueError("There is no chapter yet")
        elif new_chapter or not self.first_chap:
            self.append_chapter(text)
        else:
            new_page = Page(text, link=None)
            self.last_page.link = new_page

        return self

    def get_page(self, page_num: int) -> Page:
        """Return the given page from the book.

        If the page do not exist (the book has less than page_num pages),
        raises an IndexError.
        """
        if (
            page_num == 0
            or self.length() < page_num
            or not self.first_chap.first_page
        ):
            raise IndexError("The requested page does not exist.")

        else:
            curr_page = self.first_chap.first_page
            for _ in range(page_num - 1):
                curr_page = curr_page.link

            return curr_page

    def get_chapter_page(self, chapter_num: int, page_num: int) -> Page:
        """Return the given page from the given chapter.

        If the chapter or the page do not exist, raises an IndexError.

        (Note: requests that run past the end of a chapter into the next one
         are allowed. For example, get_chapter_page(chapter_num=1, page_num=k)
        should return the same page as get_page(page_num=k) even if there are
        multiple chapters in between.)
        """
        if not self.first_chapter:
            raise IndexError("There is no chapter in the book")
        if not self.first_chap.first_page:
            raise IndexError("The requested page does not exist.")
        if chapter_num == 0 or page_num == 0:
            raise IndexError("The requested chapter does not exist.")

        else:
            curr_chapter = self.first_chap

            for _ in range(chapter_num - 1):
                if not curr_chapter.link:
                    raise IndexError("The requested chapter does not exist.")

                curr_chapter = curr_chapter.link

            if not curr_chapter.first_page:
                raise IndexError(
                    "The requested chapter does not contain a page."
                )

            curr_page = curr_chapter.first_page

            for _ in range(page_num - 1):
                if not curr_page.link:
                    raise IndexError("The requested page does not exist.")

                curr_page = curr_page.link

            return curr_page

    def length(self) -> int:
        """Return the number of pages in the book."""
        if not self.first_chap:
            return 0

        if not self.first_chap.first_page:
            return 0

        curr_page = self.first_chap.first_page
        count = 1

        while curr_page.link:
            curr_page = curr_page.link
            count += 1

        return count

    def chapter_length(self, chapter_num: int) -> int:
        """Return the number of pages in the requested chapter.

        If the chapter does not exist, raises an IndexError.
        """
        if chapter_num == 0 or not self.first_chap.first_page:
            raise IndexError("The requested chatper does not exist.")

        else:
            curr_chapter = self.first_chap

            for _ in range(chapter_num - 1):
                if not curr_chapter.link:
                    raise IndexError("The requested chapter does not exist.")

                curr_chapter = curr_chapter.link

            if curr_chapter.link:
                if curr_chapter.link.first_page:
                    end_page = curr_chapter.link.first_page
                else:
                    end_page = None
            else:
                end_page = None

            curr_page = curr_chapter.first_page
            count = 0

            while curr_page != end_page:
                curr_page = curr_page.link
                count += 1

            return count

    def chapter_count(self):
        if not self.first_chap:
            return 0

        curr_chapter = self.first_chap
        count = 1

        while curr_chapter.link:
            curr_chapter = curr_chapter.link
            count += 1

        return count


#  Some tests for you to check your implementation.
#  You can run them with `pytest booklist.py` (you need pytest installed).


def compare_book(book_got: Book, chapters_pages: list[list[str]]):
    assert book_got.length() == sum(len(pages) for pages in chapters_pages)
    if len(chapters_pages) == 0:
        assert book_got.first_chapter is None
    else:
        assert book_got.first_chapter.first_page.text == chapters_pages[0][0]
    for chapter_num, pages in enumerate(chapters_pages, 1):
        assert book_got.chapter_length(chapter_num) == len(pages)
        for page_num, text in enumerate(pages, 1):
            page = book_got.get_chapter_page(chapter_num, page_num)
            assert page.text == text


def test_empty_book():
    book = Book()
    compare_book(book, [])


def test_one_page_book():
    text = "Hello reader"
    book = Book()
    book.prepend_page(text, True)
    compare_book(book, [[text]])


def test_multiple_chapters():
    text1_1 = "1_1"
    text1_2 = "1_2"
    text2_1 = "2_1"
    text3_1 = "3_1"
    text3_2 = "3_2"
    book = Book()
    book.prepend_page(text2_1, True).prepend_page(text1_2, True).prepend_page(
        text1_1
    ).append_page(text3_1, True).append_page(text3_2)
    book.print_book()
    compare_book(book, [[text1_1, text1_2], [text2_1], [text3_1, text3_2]])


def test_empty_book_exceptions():
    book = Book()
    with pytest.raises(ValueError):
        book.prepend_page("...", False)
    with pytest.raises(ValueError):
        book.append_page("...", False)
    with pytest.raises(IndexError):
        book.get_page(1)


def test_non_empty_book_exceptions():
    book = Book()
    book.prepend_page("...", True)
    with pytest.raises(IndexError):
        book.get_page(2)
    with pytest.raises(IndexError):
        book.get_chapter_page(2, 1)
    with pytest.raises(IndexError):
        book.get_chapter_page(1, 2)


if __name__ == "__main__":
    # Write your own tests below to test if your functions work properly.
    # You don't need to hand them in, but it might help you to debug.
    # Example:

    # Make sure to create an example to display your backward implementation.
    # Use book.print_book_backward() for this.
    book = Book()

using System;
using System.Linq;

namespace BooksAndShelvesTask
{
	class Program
	{
		static void Main(string[] args)
		{
			const int shelfWidth = 100;
			const int maxHeight = 50;
			const int shelvesCount = 5;
			var shelves = Shelf.GenerateShelves(shelvesCount, shelfWidth, maxHeight).ToArray();
			var commonBooksWidth = 0;
			var books = Book
				.GenerateBooks(100, shelves.Max(shelf => shelf.Height), 20, 2)
				.TakeWhile(book =>
				{
					commonBooksWidth += book.Width;
					return commonBooksWidth <= shelvesCount * shelfWidth;
				});
			var bookCase = new Bookcase(shelves);
			bookCase.PlaceBooks(books);
			bookCase.Print(shelfWidth);
		}
	}
}
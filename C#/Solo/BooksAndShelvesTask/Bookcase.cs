using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

namespace BooksAndShelvesTask
{
	public class Bookcase
	{
		private readonly IEnumerable<Shelf> shelves;

		public Bookcase(IEnumerable<Shelf> shelves)
		{
			this.shelves = shelves;
		}

		public void PlaceBooks(IEnumerable<Book> books)
		{
			var orderedShelves = shelves.OrderByDescending(shelf => shelf.Height).ToArray();
			books = books.OrderByDescending(book => book.Height);
			foreach (var book in books)
			{
				foreach (var shelf in orderedShelves)
					if (shelf.TryAddBook(book))
					{
						book.Placed = true;
						break;
					}
				if (!book.Placed)
					Console.WriteLine($"Book:{book} can't be placed");
			}
		}

		public void Print(int shelfLength)
		{
			Console.WriteLine(new string('=', shelfLength + 2));
			foreach (var shelf in shelves.OrderByDescending(shelf => shelf.Height))
			{
				Console.Write("|");
				foreach (var book in shelf)
				{
					Console.Write("[");
					Console.Write(new string('.', book.Width - 2));
					if (book.Width > 1)
						Console.Write("]");
				}
				Console.Write(new string('_', shelf.EmptySpace));
				Console.Write($"|Height:{shelf.Height}");
				Console.WriteLine();
			}
			Console.WriteLine(new string('=', shelfLength + 2));
		}
	}
}
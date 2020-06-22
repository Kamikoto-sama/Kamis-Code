using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;

namespace BooksAndShelvesTask
{
	public class Shelf: IEnumerable<Book>
	{
		public int Width { get; }
		public int Height { get; }
		public int EmptySpace { get; private set; }
		private readonly List<Book> books;

		public Shelf(int width, int height)
		{
			Width = width;
			Height = height;
			EmptySpace = width;
			books = new List<Book>();
		}

		public bool TryAddBook(Book book)
		{
			if (book.Height > Height || book.Width > EmptySpace)
				return false;
			books.Add(book);
			EmptySpace -= book.Width;
			return true;
		}

		public static IEnumerable<Shelf> GenerateShelves(int count, int width, int maxHeight, 
			int minHeight=1, Random random = null)
		{
			if (minHeight < 1)
				throw new ArgumentException("Min height must be a positive number");
			random ??= new Random();
			return Enumerable.Range(0, count).Select(_ =>
			{
				var shelfHeight = random.Next(minHeight, maxHeight);
				return new Shelf(width, shelfHeight);
			});
		}

		public IEnumerator<Book> GetEnumerator() => books.GetEnumerator();

		public override string ToString() => $"Width:{Width} Height:{Height} SpaceLeft:{EmptySpace}";
		
		IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();
	}
}
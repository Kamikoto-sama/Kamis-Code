using System;
using System.Collections.Generic;
using System.Linq;

namespace BooksAndShelvesTask
{
	public class Book
	{
		public int Width { get; }
		public int Height { get; }
		public bool Placed { get; set; }

		public Book(int width, int height)
		{
			Width = width;
			Height = height;
		}

		public static IEnumerable<Book> GenerateBooks(int count, int maxHeight, int maxWidth, 
			int minWidth=1, Random random = null)
		{
			if (minWidth < 1)
				throw new ArgumentException("Min width must be a positive number");
			random ??= new Random();
			return Enumerable.Range(0, count).Select(_ =>
			{
				var bookWidth = random.Next(minWidth, maxWidth);
				var bookHeight = random.Next(1, maxHeight);
				return new Book(bookWidth, bookHeight);
			});
		}

		public override string ToString() => $"Width:{Width} Height:{Height}";
	}
}
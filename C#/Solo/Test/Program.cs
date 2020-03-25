using System;

namespace Test
{
	class Program
	{
		public static void Main(string[] args)
		{
			for (var i = 1; i <= 10; i++)
				Console.WriteLine($"{i} -> {M(i)}");
		}

		private static int M(int n)
		{
			var step = n;
			var counter = 0;

			while (step > 0)
			{
				for (var i = step; i < n; i += 1)
				for (var j = i; j >= step; j -= 1)
				for (var l = 0; l < 1; l++)
					counter++;
				step /= 2;
			}

			return counter;
		}
	}
}
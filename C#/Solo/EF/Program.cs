using System;
using Microsoft.EntityFrameworkCore;

namespace EF
{
	class Program
	{
		static void Main(string[] args)
		{
			Console.WriteLine("Hello World!");
		}
	}

	class User
	{
		public int Id { get; set; }
		public int Age { get; set; }
		public string Name { get; set; }
	}
}
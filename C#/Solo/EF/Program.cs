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

	class AppContext: DbContext
	{
		public DbSet<User> Users { get; set; }

		protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
		{
			optionsBuilder.UseSqlServer("Server=(localdb)\\mssqllocaldb; DataBase=TestDB; " +
			                            "Trusted_Connection=True");
		}
	}
	
	class User
	{
		public int Id { get; set; }
		public int Age { get; set; }
		public string Name { get; set; }
	}
}
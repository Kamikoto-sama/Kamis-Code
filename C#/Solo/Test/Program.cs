using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using Useful.Extensions;

namespace Test
{
	class Program
	{
		public static void Main(string[] args)
		{
			/*
			 * def findsums(elements, targetSum):
					sums = [[] for _ in range(targetSum + 1)]
					sums[0].append((0, 0))
					for element in elements:
						for i in range(targetSum, element - 1, -1):
							for sumPart in sums[i - element]:
									sums[i].append((element, sumPart[1] + 1))
					result = []
					for lastNumber, count in sums[-1]:
						result.append([lastNumber])
						for i in range(count - 1):
							prevNumberIndex = targetSum - lastNumber
							lastNumber, count = sums[prevNumberIndex][0]
							result[-1].insert(0, lastNumber)

					print(len(result))
					return
			 */
			var random = new Random();
			for (var i = 300; i < 1000; i++)
			{
				var elements = Enumerable.Range(0, i).Select(_ => random.Next(1, 10));
				var timer = new Stopwatch();
				timer.Restart();
				var count = Count(elements, 5);
				timer.Stop();
				Console.WriteLine($"{i} {count} - {timer.Elapsed.Seconds}:{timer.Elapsed.Milliseconds}");
			}
		}

		private static int Count(IEnumerable<int> elements, int sum)
		{
			var sums = Enumerable.Range(0, sum + 1).Select(_ => new List<(int, int)>()).ToArray();
			sums[0].Add((0, 0));
			foreach (var element in elements)
				for (var i = sum; i > element - 1; i--)
					foreach (var sumPart in sums[i - element])
						sums[i].Add((element, sumPart.Item1 + 1));					
			
			var result = new List<List<int>>();
			foreach (var (item1, item2) in sums[sums.Length - 1])
			{
				var (lastNumber, count) = (item1, item2);
				result.Add(new List<int>{lastNumber});
				for (var i = 0; i < count - 1; i++)
				{
					var prevNumber = sum - lastNumber;
					(lastNumber, count) = sums[prevNumber][0];
					result[result.Count - 1].Add(lastNumber);
				}
			}

			return result.Count;
		}
	}
}
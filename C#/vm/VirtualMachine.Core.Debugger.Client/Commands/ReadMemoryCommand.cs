using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace VirtualMachine.Core.Debugger.Client.Commands
{
	public class ReadMemoryCommand : ICommandWithResult<(Word InitialAddresss, Word[][] Rows, int ColumnsCount)>
	{
		private const int ColumnsCount = 4;

		public string Name { get; } = "mem-read";
		public string Info { get; } = "Read from memory";
		public IReadOnlyList<string> ParameterNames { get; } = new[] {"from", "words count"};
		
		public (Word InitialAddresss, Word[][] Rows, int ColumnsCount) Result { get; set; }

		public async Task ExecuteAsync(DebuggerModel model, string[] parameters)
		{
			var from = uint.Parse(parameters[0]);
			var words = uint.Parse(parameters[1]);

			var rowTasks = Enumerable.Range(0, (int) Math.Ceiling(words / 1.0 / ColumnsCount))
				.Select(i => LoadRow(model.Client, new Word(from) + new Word(i * ColumnsCount * Word.Size)))
				.ToArray();

			var rows = await Task.WhenAll(rowTasks).ConfigureAwait(false);

			Result = (new Word(from), rows, ColumnsCount);
		}

		private static async Task<Word[]> LoadRow(DebuggerClient client, Word address)
		{
			var tasks = Enumerable.Range(0, ColumnsCount)
				.Select(i => address + new Word(i * Word.Size))
				.Select(a => client.ReadWordAsync(a.ToUInt()))
				.ToArray();

			return (await Task.WhenAll(tasks).ConfigureAwait(false)).Select(w => new Word(w)).ToArray();
		}
	}
}
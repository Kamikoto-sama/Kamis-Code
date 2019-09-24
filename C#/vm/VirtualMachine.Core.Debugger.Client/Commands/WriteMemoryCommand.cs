using System.Collections.Generic;
using System.Threading.Tasks;

namespace VirtualMachine.Core.Debugger.Client.Commands
{
	public class WriteMemoryCommand : ICommand
	{
		public string Name { get; } = "mem-write";
		public string Info { get; } = "Write word into memory";
		public IReadOnlyList<string> ParameterNames { get; } = new[] {"address", "word"};
		public Task ExecuteAsync(DebuggerModel model, string[] parameters)
		{
			var address = uint.Parse(parameters[0]);
			var word = uint.Parse(parameters[1]);

			return model.Client.WriteWordAsync(address, word);
		}
	}
}
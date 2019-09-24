using System.Collections.Generic;
using System.Threading.Tasks;

namespace VirtualMachine.Core.Debugger.Client.Commands
{
	public class ExitCommand: ICommand
	{
		public string Name { get; } = "exit";
		public string Info { get; } = "Stops CPU";
		public IReadOnlyList<string> ParameterNames { get; } = new string[0];
		public Task ExecuteAsync(DebuggerModel model, string[] parameters)
		{
			return model.Client.ExitAsync();
		}
	}
}
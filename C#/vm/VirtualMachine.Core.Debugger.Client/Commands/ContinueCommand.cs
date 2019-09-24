using System.Collections.Generic;
using System.Threading.Tasks;

namespace VirtualMachine.Core.Debugger.Client.Commands
{
	public class ContinueCommand : ICommand
	{
		public string Name { get; } = "continue";
		public string Info { get; } = "Continue execution (to next step or breakpoint)";
		public IReadOnlyList<string> ParameterNames { get; } = new string[0];
		public Task ExecuteAsync(DebuggerModel model, string[] parameters)
		{
			return model.Client.ContinueAsync();
		}
	}
}
using System.Collections.Generic;
using System.Threading.Tasks;

namespace VirtualMachine.Core.Debugger.Client.Commands
{
	public class RemoveBreakPointCommand : ICommand
	{
		public string Name { get; } = "bp-remove";
		public string Info { get; } = "Delete break point";
		public IReadOnlyList<string> ParameterNames { get; } = new[] {"name"};

		public Task ExecuteAsync(DebuggerModel model, string[] parameters)
		{
			return model.Client.RemoveBreakPointAsync(parameters[0]);
		}
	}
}
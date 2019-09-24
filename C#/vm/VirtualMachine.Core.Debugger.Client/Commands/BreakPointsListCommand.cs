using System.Collections.Generic;
using System.Threading.Tasks;
using VirtualMachine.Core.Debugger.Model;

namespace VirtualMachine.Core.Debugger.Client.Commands
{
	public class BreakPointsListCommand : ICommandWithResult<BreakPointDto[]>
	{
		public string Name { get; } = "bp-list";
		public string Info { get; } = "Show breakpoints list";
		public IReadOnlyList<string> ParameterNames { get; } = new string[0];

		public BreakPointDto[] Result { get; set; }

		public async Task ExecuteAsync(DebuggerModel model, string[] parameters)
		{
			Result = await model.Client.GetBreakPointsAsync().ConfigureAwait(false);
		}
	}
}
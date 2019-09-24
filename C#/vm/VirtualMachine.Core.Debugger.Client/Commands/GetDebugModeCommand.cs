using System.Collections.Generic;
using System.Threading.Tasks;
using VirtualMachine.Core.Debugger.Model;

namespace VirtualMachine.Core.Debugger.Client.Commands
{
	public class GetDebugModeCommand : ICommandWithResult<DebugMode>
	{
		public string Name { get; } = "mode-get";
		public string Info { get; } = "Get debug mode";
		public IReadOnlyList<string> ParameterNames { get; } = new string[0];
		
		public DebugMode Result { get; set; }

		public async Task ExecuteAsync(DebuggerModel model, string[] parameters)
		{
			Result = await model.Client.GetDebugModeAsync().ConfigureAwait(false);
		}
	}
}
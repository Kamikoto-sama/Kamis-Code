using System.Collections.Generic;
using System.Threading.Tasks;

namespace VirtualMachine.Core.Debugger.Client.Commands
{
	public class IsPausedCommand : ICommandWithResult<bool>
	{
		public string Name { get; } = "paused";
		public string Info { get; } = "Check application is paused";
		public IReadOnlyList<string> ParameterNames { get; } = new string[0];
		public bool Result { get; set; }

		public async Task ExecuteAsync(DebuggerModel model, string[] parameters)
		{
			Result = await model.Client.IsPausedAsync().ConfigureAwait(false);
		}
	}
}
using System.Collections.Generic;
using System.Threading.Tasks;

namespace VirtualMachine.Core.Debugger.Client.Commands
{
	public class ReadIpCommand : ICommandWithResult<uint>
	{
		public string Name { get; } = "ip-read";
		public string Info { get; } = "Read instruction pointer";
		public IReadOnlyList<string> ParameterNames { get; } = new string[0];
		
		public uint Result { get; set; }

		public async Task ExecuteAsync(DebuggerModel model, string[] parameters)
		{
			Result = await model.Client.ReadIpAsync().ConfigureAwait(false);
		}
	}
}
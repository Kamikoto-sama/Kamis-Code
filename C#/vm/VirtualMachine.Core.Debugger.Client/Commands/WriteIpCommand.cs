using System.Collections.Generic;
using System.Threading.Tasks;

namespace VirtualMachine.Core.Debugger.Client.Commands
{
	public class WriteIpCommand : ICommand
	{
		public string Name { get; } = "ip-write";
		public string Info { get; } = "Write instruction pointer";
		public IReadOnlyList<string> ParameterNames { get; } = new[] {"ip"};
		public Task ExecuteAsync(DebuggerModel model, string[] parameters)
		{
			return model.Client.WriteIpAsync(uint.Parse(parameters[0]));
		}
	}
}
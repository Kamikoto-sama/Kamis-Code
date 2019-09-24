using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using VirtualMachine.Core.Debugger.Model;

namespace VirtualMachine.Core.Debugger.Client.Commands
{
	public class SetDebugModeCommand : ICommand
	{
		public string Name { get; } = "mode-set";
		public string Info { get; } = $"Set debug mode ({string.Join(",", Enum.GetNames(typeof(DebugMode)))})";
		public IReadOnlyList<string> ParameterNames { get; } = new[] {"mode"};

		public Task ExecuteAsync(DebuggerModel model, string[] parameters)
		{
			return model.Client.SetDebugModeAsync((DebugMode) Enum.Parse(typeof(DebugMode), parameters[0]));
		}
	}
}
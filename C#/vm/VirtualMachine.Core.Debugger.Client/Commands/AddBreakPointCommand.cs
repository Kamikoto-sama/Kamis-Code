using System.Collections.Generic;
using System.Threading.Tasks;
using VirtualMachine.Core.Debugger.Model;

namespace VirtualMachine.Core.Debugger.Client.Commands
{
    public class AddBreakPointCommand : ICommand
    {
        public string Name { get; } = "bp-add";
        public string Info { get; } = "Add break point";
        public IReadOnlyList<string> ParameterNames { get; } = new[] {"name", "address"};

        public Task ExecuteAsync(DebuggerModel model, string[] parameters)
        {
            var bp = new BreakPointDto
            {
                Name = parameters[0],
                Address = uint.Parse(parameters[1])
            };
            return model.Client.AddBreakPointAsync(bp);
        }
    }
}
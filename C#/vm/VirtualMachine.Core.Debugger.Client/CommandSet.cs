using System;
using System.Collections.Generic;
using VirtualMachine.Core.Debugger.Client.Commands;

namespace VirtualMachine.Core.Debugger.Client
{
    public class CommandSet
    {
        public CommandSet()
        {
            Add(new AddBreakPointCommand());
            Add(new BreakPointsListCommand());
            Add(new ContinueCommand());
            Add(new GetDebugModeCommand());
            Add(new IsPausedCommand());
            Add(new ReadIpCommand());
            Add(new ReadMemoryCommand());
            Add(new RemoveBreakPointCommand());
            Add(new SetDebugModeCommand());
            Add(new WriteIpCommand());
            Add(new WriteMemoryCommand());
        }
        
        public bool TryFindCommand(string commandName, out ICommand command) => commands.TryGetValue(commandName, out command);

        public IReadOnlyCollection<ICommand> GetAll() => commands.Values;

        public void Add(ICommand command)
        {
            commands.Add(command.Name, command);
        }

        private readonly Dictionary<string, ICommand> commands = new Dictionary<string, ICommand>(StringComparer.InvariantCultureIgnoreCase);
    }
}
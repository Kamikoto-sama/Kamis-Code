using System;
using System.Collections.Generic;
using VirtualMachine.Core.Debugger.Client;
using VirtualMachine.Debugger.Client.Console.CommandResultWriters;

namespace VirtualMachine.Debugger.Client.Console
{
    public class CommandResultWriterSet
    {
        public CommandResultWriterSet()
        {
            Add(new BreakPointsListCommandResultWriter());
            Add(new GetDebugModeCommandResultWriter());
            Add(new IsPausedCommandResultWriter());
            Add(new ReadIpCommandResultWriter());
            Add(new ReadMemoryCommandResultWriter());
        }
        
        public bool TryFindWriter(ICommand command, out ICommandResultWriter writer) => writers.TryGetValue(command.GetType(), out writer);

        public void Add(ICommandResultWriter writer)
        {
            writers.Add(writer.CommandType, writer);
        }

        private readonly Dictionary<Type, ICommandResultWriter> writers = new Dictionary<Type, ICommandResultWriter>();
    }
}
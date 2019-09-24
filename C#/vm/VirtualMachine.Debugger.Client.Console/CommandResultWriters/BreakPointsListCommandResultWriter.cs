using System;
using VirtualMachine.Core.Debugger.Client;
using VirtualMachine.Core.Debugger.Client.Commands;
using VirtualMachine.Debugger.Client.Console.Helpers;

namespace VirtualMachine.Debugger.Client.Console.CommandResultWriters
{
    public class BreakPointsListCommandResultWriter : ICommandResultWriter
    {
        public Type CommandType => typeof(BreakPointsListCommand);
        
        public void WriteResult(ICommand command)
        {
            var breakPointsListCommand = (BreakPointsListCommand) command;
            var breakpoints = breakPointsListCommand.Result;
            
            foreach (var breakpoint in breakpoints)
            {
                ConsoleColor.Yellow.Write(breakpoint.Address.ToBHex());
                ConsoleColor.White.WriteLine($":\t{breakpoint.Name}");
            }
        }
    }
}
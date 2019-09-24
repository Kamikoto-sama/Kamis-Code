using System;
using VirtualMachine.Core.Debugger.Client;
using VirtualMachine.Core.Debugger.Client.Commands;
using VirtualMachine.Debugger.Client.Console.Helpers;

namespace VirtualMachine.Debugger.Client.Console.CommandResultWriters
{
    public class GetDebugModeCommandResultWriter : ICommandResultWriter
    {
        public Type CommandType => typeof(GetDebugModeCommand);
        
        public void WriteResult(ICommand command)
        {
            var getDebugModeCommand = (GetDebugModeCommand) command;
            
            ConsoleColor.White.Write("Debug mode:\t");
            ConsoleColor.Yellow.WriteLine(getDebugModeCommand.Result.ToString());
        }
    }
}
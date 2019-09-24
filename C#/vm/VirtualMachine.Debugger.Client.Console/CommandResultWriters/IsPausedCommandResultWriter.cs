using System;
using VirtualMachine.Core.Debugger.Client;
using VirtualMachine.Core.Debugger.Client.Commands;
using VirtualMachine.Debugger.Client.Console.Helpers;

namespace VirtualMachine.Debugger.Client.Console.CommandResultWriters
{
    public class IsPausedCommandResultWriter : ICommandResultWriter
    {
        public Type CommandType => typeof(IsPausedCommand);
        
        public void WriteResult(ICommand command)
        {
            var isPausedCommand = (IsPausedCommand) command;
            var isPaused = isPausedCommand.Result;
            
            ConsoleColor.White.Write("App is ");
            ConsoleColor.Yellow.WriteLine(isPaused ? "paused" : "running");
        }
    }
}
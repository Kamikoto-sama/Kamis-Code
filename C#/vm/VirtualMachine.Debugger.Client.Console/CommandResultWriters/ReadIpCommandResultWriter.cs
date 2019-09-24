using System;
using VirtualMachine.Core.Debugger.Client;
using VirtualMachine.Core.Debugger.Client.Commands;
using VirtualMachine.Debugger.Client.Console.Helpers;

namespace VirtualMachine.Debugger.Client.Console.CommandResultWriters
{
    public class ReadIpCommandResultWriter : ICommandResultWriter
    {
        public Type CommandType => typeof(ReadIpCommand);
        
        public void WriteResult(ICommand command)
        {
            var readIpCommand = (ReadIpCommand) command;
            var ip = readIpCommand.Result;
            
            ConsoleColor.White.Write("IP = ");
            ConsoleColor.Yellow.WriteLine(ip.ToBHex());
        }
    }
}
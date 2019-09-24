using System;
using VirtualMachine.Core.Debugger.Client;

namespace VirtualMachine.Debugger.Client.Console
{
    public interface ICommandResultWriter
    {
        Type CommandType { get; }
        void WriteResult(ICommand command);
    }
}
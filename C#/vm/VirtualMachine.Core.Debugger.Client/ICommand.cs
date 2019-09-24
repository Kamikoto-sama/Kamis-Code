using System.Collections.Generic;
using System.Threading.Tasks;

namespace VirtualMachine.Core.Debugger.Client
{
    public interface ICommand
    {
        string Name { get; }
        string Info { get; }
        IReadOnlyList<string> ParameterNames { get; }

        Task ExecuteAsync(DebuggerModel model, string[] parameters);
    }
    
    public interface ICommandWithResult<out TResult> : ICommand
    {
        TResult Result { get; }
    }
}
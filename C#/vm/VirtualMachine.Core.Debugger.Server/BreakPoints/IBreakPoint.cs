using VirtualMachine.Core;

namespace VirtualMachine.Core.Debugger.Server.BreakPoints
{
    public interface IBreakPoint
    {
        Word Address { get; }
        string Name { get; }
        bool ShouldStop(IReadOnlyMemory memory);
    }
}
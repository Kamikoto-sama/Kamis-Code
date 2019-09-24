using VirtualMachine.CPU;
using VirtualMachine.Core.Debugger.Model;
using VirtualMachine.Core.Debugger.Server.BreakPoints;

namespace VirtualMachine.Core.Debugger.Server
{
    public interface IPauseContext
    {
        IMemory Memory { get; }
        ICpu Cpu { get; }

		StopReason StopReason { get; }
		IBreakPoint StopBreakPoint { get; }
        string StopMessage { get; }
    }
}
using VirtualMachine.Core;

namespace VirtualMachine.CPU
{
    public interface ISupervisor
    {
        Decision OnStep(ICpu cpu, IMemory memory);
        Decision OnInstructionDecodeError(ICpu cpu, IMemory memory, string message);
        Decision OnInstructionExecuteError(ICpu cpu, IMemory memory, string message);
    }
}
using VirtualMachine.Core;

namespace VirtualMachine.CPU
{
    public class FakeSupervisor : ISupervisor
    {
        public Decision OnStep(ICpu cpu, IMemory memory)
        {
            return Decision.Continue;
        }

        public Decision OnInstructionDecodeError(ICpu cpu, IMemory memory, string message)
        {
            return Decision.Terminate;
        }

        public Decision OnInstructionExecuteError(ICpu cpu, IMemory memory, string message)
        {
            return Decision.Terminate;
        }
    }
}
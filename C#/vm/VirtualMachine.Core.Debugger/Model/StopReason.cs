namespace VirtualMachine.Core.Debugger.Model
{
    public enum StopReason
    {
        Step = 0,
        Breakpoint = 1,
        InstructionDecodeError = 2,
        InstructionExecutionError = 3
    }
}
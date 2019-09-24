using VirtualMachine.Core;

namespace VirtualMachine.CPU
{
    public interface IInstruction
    {
		string Name { get; }
        Word OpCode { get; }
        int OperandsCount { get; }
        void Execute(ICpu cpu, IMemory memory, Word[] operands);
    }
}
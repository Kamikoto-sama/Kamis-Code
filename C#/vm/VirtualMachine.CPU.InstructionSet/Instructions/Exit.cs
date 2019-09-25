using VirtualMachine.Core;

namespace VirtualMachine.CPU.InstructionSet.Instructions
{
	public class Exit: InstructionBase
	{
		public Exit() : base(8, OperandType.Ignored, OperandType.Ignored, OperandType.Ignored)
		{
		}

		protected override void ExecuteInternal(ICpu cpu, IMemory memory, Operand _, Operand __, Operand ___)
		{
			cpu.InstructionPointer = new Word(-1);
		}
	}
}
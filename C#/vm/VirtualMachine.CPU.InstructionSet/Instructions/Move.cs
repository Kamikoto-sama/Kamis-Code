using VirtualMachine.Core;

namespace VirtualMachine.CPU.InstructionSet.Instructions
{
    public class Move : InstructionBase
    {
        public Move(OperandType first, OperandType second) : base(1, first, second, OperandType.Ignored)
        { }

        protected override void ExecuteInternal(ICpu _, IMemory __, Operand src, Operand dst, Operand ___)
        {
            dst.Value = src.Value;
        }
    }
}
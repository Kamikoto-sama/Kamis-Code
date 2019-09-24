using VirtualMachine.Core;

namespace VirtualMachine.CPU.InstructionSet
{
    public abstract class MathInstructionBase : InstructionBase
    {
        protected MathInstructionBase(byte opCode, OperandType first, OperandType second, OperandType third) 
            : base(opCode, first, second, third)
        { }

        protected abstract Word Calculate(Word a, Word b);

        protected sealed override void ExecuteInternal(ICpu _, IMemory __, Operand op0, Operand op1, Operand op2)
        {
            op2.Value = Calculate(op0.Value, op1.Value);
        }
    }
}
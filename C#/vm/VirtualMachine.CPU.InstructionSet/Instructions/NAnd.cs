using VirtualMachine.Core;

namespace VirtualMachine.CPU.InstructionSet.Instructions
{
    public class NAnd : MathInstructionBase
    {
        public NAnd(OperandType first, OperandType second, OperandType third)
            : base(7, first, second, third)
        { }

        protected override Word Calculate(Word a, Word b)
        {
            return new Word(~(a.ToUInt() & b.ToUInt()));
        }
    }
}
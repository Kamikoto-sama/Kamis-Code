using VirtualMachine.Core;

namespace VirtualMachine.CPU.InstructionSet.Instructions
{
    public class SSub : MathInstructionBase
    {
        public SSub(OperandType first, OperandType second, OperandType third) : base(6, first, second, third)
        { }

        protected override Word Calculate(Word a, Word b)
        {
            unchecked
            {
                return new Word(a.ToInt() - b.ToInt());
            }
        }
    }
}
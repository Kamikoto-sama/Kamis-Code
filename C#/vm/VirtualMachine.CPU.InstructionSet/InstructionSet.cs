using System.Collections.Generic;
using VirtualMachine.Core;
using VirtualMachine.CPU.InstructionSet.Instructions;

namespace VirtualMachine.CPU.InstructionSet
{
    public class InstructionSet : IInstructionSet
    {
        private static readonly IReadOnlyList<OperandType> Readable = new []
        {
            OperandType.Constant,
            OperandType.Address,
            OperandType.AddressOfAddress
        };

        private static readonly IReadOnlyList<OperandType> Writable = new []
        {
            OperandType.Address,
            OperandType.AddressOfAddress
        };

        public InstructionSet()
        {
            foreach (var from in Readable)
            foreach (var to in Writable)
            { 
                AddInstruction(new Move(@from, to));
            }

            foreach (var a in Readable)
            foreach (var b in Readable)
            {
                AddInstruction(new If(a, b));
            }

            foreach (var a in Readable)
            foreach (var b in Readable)
            foreach (var dest in Writable)
            {
                AddInstruction(new Add(a, b, dest));
                AddInstruction(new Sub(a, b, dest));
                AddInstruction(new SAdd(a, b, dest));
                AddInstruction(new SSub(a, b, dest));
                AddInstruction(new NAnd(a, b, dest));
            }
            AddInstruction(new Exit());
        }

        public IInstruction FindInstruction(Word opCode) => instructions.TryGetValue(opCode, out var instruction) ? instruction : null;

        public IEnumerable<IInstruction> GetAll() => instructions.Values;

        private void AddInstruction(IInstruction instruction)
        {
            instructions.Add(instruction.OpCode, instruction);
        }

        private readonly Dictionary<Word, IInstruction> instructions = new Dictionary<Word, IInstruction>();
    }
}
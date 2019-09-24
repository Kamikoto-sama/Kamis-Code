using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using VirtualMachine.Core;
using VirtualMachine.CPU;

namespace VirtualMachine.SimpleAssembler
{
	public class SimpleAssembler : IAssembler
	{
		public SimpleAssembler(IInstructionSet instructions)
		{
			this.instructions = instructions.GetAll().ToDictionary(i => i.Name.Trim());
			this.parser = new Parser(this.instructions.Keys.ToArray());
		}

		public byte[] Assembly(string code)
		{
			return parser.Parse(code).SelectMany(ToBytes).ToArray();
		}

		private IEnumerable<byte> ToBytes(Token token)
		{
			switch (token.Type)
			{
				case TokenType.Comment: return CommentToBytes(token);
				case TokenType.HexWord: return HexWordToBytes(token);
				case TokenType.Instruction: return InstructionToBytes(token);
				default:
					throw new ArgumentOutOfRangeException(token.Type.ToString());
			}
		}

		private IEnumerable<byte> CommentToBytes(Token token) => Array.Empty<byte>();

		private IEnumerable<byte> HexWordToBytes(Token token)
		{
			var value = token.Value.Replace(" ", "").Replace("\t", "");
			for (var i = 0; i < Word.Size; i++)
				yield return byte.Parse(value.Substring(i * 2, 2), NumberStyles.HexNumber);
		}

		private IEnumerable<byte> InstructionToBytes(Token token)
		{
			if (!instructions.TryGetValue(token.Value, out var instruction))
				throw new InvalidOperationException($"Unknown instruction in line #{token.Line}: '{token.Value}'");

			yield return instruction.OpCode.First;
			yield return instruction.OpCode.Second;
			yield return instruction.OpCode.Third;
			yield return instruction.OpCode.Fourth;
		}

		private readonly IReadOnlyDictionary<string, IInstruction> instructions;
		private readonly IParser parser;
	}
}
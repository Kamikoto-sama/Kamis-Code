using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Text.RegularExpressions;

namespace VirtualMachine.SimpleAssembler
{
	public class Parser : IParser
	{
		private readonly IReadOnlyCollection<string> instructions;

		public Parser(IReadOnlyCollection<string> instructions) => this.instructions = instructions;

		public Token[] Parse(string code)
		{
			return code.Split('\n').SelectMany(ParseLine).ToArray();
		}

		private IEnumerable<Token> ParseLine(string line, int lineIndex)
		{
			var match = lineRegex.Match(line);
			if (!match.Success)
				throw new InvalidOperationException($"Cant parse line #{lineIndex} '{line}'");

			var payload = match.Groups["payload"].Value;
			var comment = match.Groups["comment"].Value;

			return string.IsNullOrWhiteSpace(comment)
				? ParsePayload(payload, lineIndex)
				: ParsePayload(payload, lineIndex).Concat(new[] {new Token(lineIndex, TokenType.Comment, comment)});
		}

		private IEnumerable<Token> ParsePayload(string payload, int lineIndex)
		{
			if (string.IsNullOrWhiteSpace(payload))
				yield break;

			payload = payload.TrimStart();

			var match = hexWordRegex.Match(payload);
			if (match.Success)
			{
				var hex = match.Groups["value"].Value;
				yield return new Token(lineIndex, TokenType.HexWord, hex);
				payload = payload.Substring(hex.Length + 1);
			}
			else
			{
				var instruction = instructions.FirstOrDefault(i => payload.StartsWith(i)) ??
				                  throw new InvalidOperationException($"Invalid line #{lineIndex}: '{payload}'");
				yield return new Token(lineIndex, TokenType.Instruction, instruction);
				payload = payload.Substring(instruction.Length);
			}

			foreach (var token in ParsePayload(payload, lineIndex))
				yield return token;
		}

		private readonly Regex hexWordRegex = new Regex(@"^\$(?<value>(?:[0-9a-fA-F]\s*){8})");
		private readonly Regex lineRegex = new Regex(@"^(?<payload>[^#]+)?(?:#(?<comment>.+)?)?$");
	}
}
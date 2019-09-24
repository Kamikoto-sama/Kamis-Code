using System;
using System.IO;
using System.Linq;
using System.Text;
using VirtualMachine.CPU;

namespace VirtualMachine.SimpleAssembler
{
	public static class EntryPoint
	{
		public static void Main(string[] args)
		{
			var instructions = LoadInstructionSet(args[0]);

			if (args.Length < 3)
			{
				Console.WriteLine(string.Join("\n", instructions.GetAll().Select(i => i.Name)));
				return;
			}

			var code = File.ReadAllText(args[1], Encoding.UTF8);
			var destFileName = args[2];

			var assembled = new SimpleAssembler(instructions).Assembly(code);

			File.WriteAllBytes(destFileName, assembled);
		}

		private static IInstructionSet LoadInstructionSet(string instructionSetAssemblyFileName)
		{
			try
			{
				var instructionSetAssembly = System.Reflection.Assembly.LoadFrom(instructionSetAssemblyFileName);
				var constructor = instructionSetAssembly
					.GetTypes()
					.Where(t => typeof(IInstructionSet).IsAssignableFrom(t))
					.Select(t => t.GetConstructor(new Type[0]))
					.Single(c => c != null);
				return (IInstructionSet) constructor.Invoke(new object[0]);
			}
			catch (Exception e)
			{
				throw new InvalidOperationException(
					$"Cant load instruction set from '{instructionSetAssemblyFileName}'", e);
			}
		}
	}
}

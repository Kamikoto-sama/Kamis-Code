using VirtualMachine.Core;
using VirtualMachine.Core.Debugger.Model;

namespace VirtualMachine.Core.Debugger.Server.BreakPoints
{
	public class BreakPointsConverter
	{
		public IBreakPoint FromDto(BreakPointDto dto)
		{
			return new BreakPoint(new Word(dto.Address), dto.Name);
		}

		public BreakPointDto ToDto(IBreakPoint bp)
		{
			return new BreakPointDto
			{
				Name = bp.Name,
				Address = bp.Address.ToUInt()
			};
		}

		private class BreakPoint : IBreakPoint
		{
			public BreakPoint(Word address, string name)
			{
				Address = address;
				Name = name;
			}

			public Word Address { get; }
			public string Name { get; }
			public bool ShouldStop(IReadOnlyMemory memory) => true;
		}
	}
}
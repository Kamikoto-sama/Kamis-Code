using System;
using System.Collections.Generic;
using System.Linq;
using VirtualMachine.Core;

namespace VirtualMachine.Core.Debugger.Server.BreakPoints
{
    public class BreakPointCollection
    {
        public void Add(IBreakPoint breakPoint)
        {
            if (!breakPoints.TryGetValue(breakPoint.Address, out var set))
                breakPoints[breakPoint.Address] = set = new HashSet<IBreakPoint>();
            set.Add(breakPoint);
            nameToBreakPoint[breakPoint.Name] = breakPoint;
        }

        public void Remove(IBreakPoint breakPoint)
        {
            if (breakPoints.TryGetValue(breakPoint.Address, out var set))
                set.Remove(breakPoint);
            if (nameToBreakPoint.TryGetValue(breakPoint.Name, out var bp) && bp.Equals(breakPoint))
	            nameToBreakPoint.Remove(breakPoint.Name);
        }

        public IBreakPoint Find(string name) => nameToBreakPoint.TryGetValue(name, out var bp) ? bp : null;

        public IReadOnlyCollection<IBreakPoint> Find(Word address)
        {
            return breakPoints.TryGetValue(address, out var set)
                ? (IReadOnlyCollection<IBreakPoint>) set
                : Array.Empty<IBreakPoint>();
        }

        public IEnumerable<IBreakPoint> BreakPoints => nameToBreakPoint.Values;

        private readonly Dictionary<Word, HashSet<IBreakPoint>> breakPoints = new Dictionary<Word, HashSet<IBreakPoint>>();
        private readonly Dictionary<string, IBreakPoint> nameToBreakPoint = new Dictionary<string, IBreakPoint>();
    }
}
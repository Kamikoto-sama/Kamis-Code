using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;

namespace ConturZipper
{
    public static class XZipper
    {
        public static string Compress(string[] input)
        {
            var previous = new LimitedQueue<string>(16);
            var result = input
                .Select(target => GetCompressed(previous, target));
            return string.Join("\n", result);
        }

        private static string GetCompressed(LimitedQueue<string> previous, string target)
        {
            if (previous.Count != 0)
                return previous
                    .Select((temp, i) 
                        => CompressString(target, temp, previous.Count - i))
                    .Min(s => s)
                    .Value;

            previous.Add(target);
            return target;
        }

//        12.222.17.217 - - [03/Feb/2003:03:08:13 +0100] "GET /jettop.htm HTTP/1.1"
//        12.222.17.217 - - [03/Feb/2003:03:08:14 +0100] "GET /jetstart.htm HTTP/1.1"
        //(166)4(144)start.htm(137) 
        public static StringWithLength CompressString(string target, string template,
            int tempIndex)
        {
            var maxString = Math.Max(target.Length, template.Length);
            var result = new StringBuilder(maxString);
            var matchesCount = 0;
            var mismatch = false;

            result.Append($"({128 + tempIndex - 1})");
            for (int i = 0, targetShift = 0, templateShift = 0; i < maxString; i++)
            {
                var targetChar = target[i - targetShift];
                var templateChar = template[i - templateShift];
                if (targetChar == templateChar)
                {
                    if (mismatch)
                    {
                        mismatch = false;
                        continue;
                    }
                    matchesCount++;
                }
                else
                {
                    mismatch = true;
                    if (targetChar == ' ')
                        targetShift++;
                    else if (templateChar == ' ')
                        templateShift++;
                }

                if (!mismatch && i != maxString - 1) continue;
                if(matchesCount > 0)
                {
                    result.Append($"({128 + matchesCount})");
                    matchesCount = 0;
                }
                if(mismatch)
                    result.Append(targetChar.ToString());
            }

            return new StringWithLength(result.ToString());
        }
    }

    public class StringWithLength: IComparable
    {
        public string Value { get; }

        public StringWithLength(string value) => Value = value;
        
        public int CompareTo(object obj)
        {
            if (obj is string value)
                return Value.Length.CompareTo(value);
            return Value.CompareTo(obj);
        }
    }
}
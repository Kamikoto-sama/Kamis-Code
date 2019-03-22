using System;
using System.Collections.Generic;
using System.Text;
using System.Text.RegularExpressions;

namespace ConturZipper
{
    public static class XZipper
    {
        public static string Compress(string input)
        {
            throw new Exception();
        }

//        12.222.17.217 - - [03/Feb/2003:03:08:13 +0100] "GET /jettop.htm HTTP/1.1"
//        12.222.17.217 - - [03/Feb/2003:03:08:14 +0100] "GET /jetstart.htm HTTP/1.1"
        public static string CompressString(string target, string template)
        {
            var maxString = Math.Max(target.Length, template.Length);
            var result = new List<string>(maxString);
            var matchesCount = 0;
            
            for (int i = 0, targetShift = 0, templateShift = 0; i < maxString; i++)
            {
                var targetChar = target[i - targetShift];
                var templateChar = template[i - templateShift];
                if (targetChar == templateChar)
                        matchesCount++;
                else if (targetChar == ' ')
                    targetShift++;
                else if (templateChar == ' ')
                    templateShift++;
                if ((targetChar != templateChar || i == maxString - 1) && matchesCount > 0)
                {
                    result.Add($"({128 + matchesCount - 1})");
                    matchesCount = 0;
                }
                if(targetChar != templateChar && matchesCount == 0)
                    result.Add(targetChar.ToString());
            }

            return string.Join("", result);
        }
    }
}
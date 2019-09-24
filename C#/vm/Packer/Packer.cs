using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;

namespace Packer
{
    public class Packer
    {
        public static string Pack(string[] args)
        {
            var dirs = args.Length > 0 ? args : new[] {@"."};

            var ignoredPatterns = new[] {@"bin\\", @"obj\\", @"bin\/", @"obj\/"};
            var sources =
                dirs.SelectMany(
                        dir =>
                            Directory
                                .EnumerateFiles(dir, "*.cs", SearchOption.AllDirectories)
                                .Where(fn => !ignoredPatterns.Any(p => Regex.IsMatch(fn, p, RegexOptions.IgnoreCase)))
                                .Select(fn => new {name = fn, src = File.ReadAllText(fn)}))
                    .OrderByDescending(x => File.GetLastAccessTimeUtc(x.name))
                    .ToList();

            var usings = new HashSet<string>();
            var sb = new StringBuilder();

            foreach (var file in sources)
            {
                Console.WriteLine($"use {file.name}");
                var source = file.src;
                var pattern = @"using [A-Z0-9.]+;\r?\n";
                var usingLines = Regex.Matches(source, pattern, RegexOptions.Multiline | RegexOptions.IgnoreCase)
                                      .Cast<Match>()
                                      .Select(m => m.Value).ToList();
                foreach (var usingLine in usingLines)
                {
                    usings.Add(usingLine);
                }

                var sourceWithNoUsings =
                    Regex.Replace(source, pattern, "", RegexOptions.Multiline | RegexOptions.IgnoreCase)
                         .Trim();
                sb.AppendLine(sourceWithNoUsings);
                sb.AppendLine();
            }

            sb.Insert(0, string.Join("", usings) + "\r\n");
            var result = sb.ToString();
            return result;
        }
    }
}
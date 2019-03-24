using System;

namespace ExMath
{
    public static class RandomExtention
    {
        public static double NextDouble(this Random random, double minValue, double maxValue)
        {
            return minValue + random.NextDouble() * (maxValue - minValue);
        }
    }
}
using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace ExMath
{
    public class Matrix: IEnumerable<double>
    {
        private double[,] Values { get; set; }
        public int RowCount => Values.GetLength(0);
        public int ColumnCount => Values.GetLength(1);

        public double this[int i, int j]
        {
            get => Values[i, j];
            set => Values[i, j] = value;
        }

        public Matrix(double[,] values) => Values = values;

        public Matrix(int rowCount, int columnCount, double value=0)
        {
            var values = new double[rowCount, columnCount];
            Values = GetNewValues(values, (i, j) => value);
        }
        
        public Matrix Clone() => new Matrix((double[,])Values.Clone());

        public void PrintInLine()
        {
            Console.Write("( ");
            for (var i = 0; i < RowCount; i++)
            {
                Console.Write("{ ");
                for (var j = 0; j < ColumnCount; j++)
                    Console.Write(Values[i, j] + " ");
                Console.Write("} ");
            }
            Console.Write(")");
        }

        public static Matrix operator +(Matrix left, Matrix right)
        {
            var rows = left.RowCount;
            var columns = left.ColumnCount;
            if(rows != right.RowCount || columns != right.ColumnCount)
                throw new Exception("Matrix sizes aren't equal");
            
            var newValues = GetNewValues(left.Values, 
                (i, j) => left[i, j] + right[i, j]);
            return new Matrix(newValues);
        }

        public static Matrix operator *(Matrix matrix, double value)
        {
            var newValues = GetNewValues(matrix.Values, 
                (i, j) => matrix[i, j] * value);
            return new Matrix(newValues);
        }

        public static Matrix operator *(double value, Matrix matrix) => matrix * value;

        public static Matrix operator *(Matrix left, Matrix right)
        {
            if(right.ColumnCount != left.RowCount)
                throw new Exception("left.ColumnCount must " +
                                    "be equal to right.RowCount");

            var newValues = new double[right.RowCount, left.ColumnCount];
            for (int i = 0, j; i < right.RowCount * left.ColumnCount; i++)
            {
                var cellValue = 0.0;
                for (j = 0; j < right.ColumnCount; j++)
                    cellValue += left[i / right.ColumnCount, j] * right[j, i % right.RowCount];

                newValues[i / right.ColumnCount, i % right.ColumnCount] = cellValue;
            }
            
            return new Matrix(newValues);
        }

        public static Matrix operator /(Matrix matrix, double value)
        {
            return matrix * (1 / value);
        }

        public static Matrix operator /(double value, Matrix matrix) => matrix / value;
        
        private static double[,] GetNewValues(double[,] values, 
            Func<int, int, double> operation)
        {
            var newValues = new double[values.GetLength(0), values.GetLength(1)];
            for (var i = 0; i < values.GetLength(0); i++)
            for (var j = 0; j < values.GetLength(1); j++)
                newValues[i, j] = operation(i, j);
            return newValues;
        }

        public IEnumerator<double> GetEnumerator()
        {
            return Values.Cast<double>().GetEnumerator();
        }

        IEnumerator IEnumerable.GetEnumerator()
        {
            return GetEnumerator();
        }

        public override string ToString()
        {
            var lines = new StringBuilder[RowCount];
            var maxLength = 0;
            for (var i = 0; i < RowCount; i++)
            {
                lines[i] = new StringBuilder();
                lines[i].Append("| ");
                for (var j = 0; j < ColumnCount; j++)
                    lines[i].Append(Values[i, j] + " ");
                if (lines[i].Length > maxLength) maxLength = lines[i].Length;
            }
            var result = lines
                .Select(line => line
                    .Append(new string(' ', maxLength - line.Length) + "|"));
            return string.Join("\n", result);
        }
    }
}
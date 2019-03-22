using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;

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
        
        public Matrix(int rows, int columns)
        {
            Values = new double[rows, columns];
        }

        public Matrix(double[,] values) => Values = values;

        public static Matrix operator +(Matrix left, Matrix right)
        {
            var rows = left.RowCount;
            var columns = left.ColumnCount;
            if(rows != right.RowCount
               && columns != right.ColumnCount)
                throw new Exception("Sizes aren't equals");
            
            var newValues = GetNewValues(left, (i, j) => left[i, j] + right[i, j]);
            return new Matrix(newValues);
        }

        public static Matrix operator *(Matrix matrix, double value)
        {
            var newValues = GetNewValues(matrix, (i, j) => matrix[i, j] * value);
            return new Matrix(newValues);
        }

        public static Matrix operator *(double value, Matrix matrix) => matrix * value;

        public static Matrix operator *(Matrix right, Matrix left)
        {
            if(right.ColumnCount != left.RowCount)
                throw new Exception("right.ColumnCount must be equal left.RowCount");

            var newValues = new double[right.RowCount, right.ColumnCount];
            var cellValue = .0;
            for (int i = 0; i < right.RowCount; i++)
            for (int j = 0; j < right.ColumnCount; j++)
            {
                cellValue += right[i, j] * left[j, i]              
            }
        }

        public static Matrix operator /(Matrix matrix, double value)
        {
            return matrix * (1 / value);
        }

        public static Matrix operator /(double value, Matrix matrix) => matrix / value;

        
        private static double[,] GetNewValues(Matrix matrix, 
            Func<int, int, double> operation)
        {
            var newValues = new double[matrix.RowCount, matrix.ColumnCount];
            for (var i = 0; i < matrix.RowCount; i++)
            for (var j = 0; j < matrix.ColumnCount; j++)
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
    }
}
using Microsoft.VisualStudio.TestTools.UnitTesting;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;

namespace Optimization
{
    public class RecursiveTravellerSalesman
    {
        private int[] indices;
        private int[] bestTourIndices;
        private float bestTourDst;
        private Dictionary<int,KeyValuePair<int,int>> coordinates;
        private int searched;
        private Stopwatch watch;

        public RecursiveTravellerSalesman(Dictionary<int, KeyValuePair<int, int>> pCoordinates, int[] pIndices)
        {
            Assert.IsNotNull(pCoordinates, "There can be no empty coordinates.");
            Assert.IsNotNull(pIndices, "There can be no empty indices.");

            indices = new int[pIndices.Length];
            Array.Copy(pIndices, indices, pIndices.Length);

            coordinates = new Dictionary<int, KeyValuePair<int, int>>();
            foreach (int c in indices)
            {
                coordinates.Add(c, pCoordinates[c]);
            }
            bestTourDst = float.MaxValue;
            bestTourIndices = new int[pIndices.Length];
        }

        public void Solve()
        {
            //Call will length -1 to keep one element fixed in place. This avoids wasting time
            //evaluating tours that are identical except for beginning at a different point
            searched = 0;
            watch  = Stopwatch.StartNew();
            GenerateSolutions(indices, indices.Length - 1);
            watch.Stop();
        }

        /// <summary>
        /// Heap's algorithm for generating all permutations
        /// </summary>
        /// <param name="indices"></param>
        /// <param name="n"></param>
        protected void GenerateSolutions(int[] indices, int n)
        {
            searched++;
            if (n == 1)
            {
                EvaluateSolution(indices);
            }
            else
            {
                for(int i=0; i<n; i++)
                {
                    //searched++;
                    GenerateSolutions(indices, n - 1);
                    int swapIndex = (n % 2 == 0) ? i : 0;
                    //(indices[swapIndex], indices[n - 1]) = (indices[n - 1], indices[swapIndex]);
                    int aux = indices[swapIndex];
                    indices[swapIndex] = indices[n - 1];
                    indices[n - 1] = aux;
                }
            }
        }

        protected void EvaluateSolution(int[] indices)
        {
            //searched++;
            // Ignore solutions which are just reverse of another solution
            if(indices[0] < indices[indices.Length - 2])
            {
                //Calculate length of the path (including returning to start point)
                float tourDst = 0;
                for(int i=0; i<indices.Length; i++)
                {
                    int nextIndex = (i + 1) % indices.Length;
                    tourDst += LookUpDistance(indices[i], indices[nextIndex]);
                }

                //Save the path indices if this is the best solution found so far
                if(tourDst < bestTourDst)
                {
                    bestTourDst = tourDst;
                    System.Array.Copy(indices, bestTourIndices, indices.Length);
                }
            }
        }

        private float LookUpDistance(int v1, int v2)
        {
            KeyValuePair<int, int> c1 = coordinates[v1];
            KeyValuePair<int, int> c2 = coordinates[v2];

            return (float) Math.Sqrt(Math.Pow(c1.Key - c2.Key, 2) + Math.Pow(c1.Value - c2.Value, 2));
        }

        public static Dictionary<int, KeyValuePair<int, int>> TwelveTowns()
        {
            return new Dictionary<int, KeyValuePair<int, int>>
            {
                { 1, new KeyValuePair<int, int>( 5,8 )},
                { 2, new KeyValuePair<int, int>( 6,12 )},
                { 3, new KeyValuePair<int, int>( 8,9 )},
                { 4, new KeyValuePair<int, int>( 10,16 )},
                { 5, new KeyValuePair<int, int>( 10,28 )},
                { 6, new KeyValuePair<int, int>( 14,8 )},
                { 7, new KeyValuePair<int, int>( 14,20 )},
                { 8, new KeyValuePair<int, int>( 16,15 )},
                { 9, new KeyValuePair<int, int>( 22,15 )},
                { 10, new KeyValuePair<int, int>( 21,22 )},
                { 11, new KeyValuePair<int, int>( 21,26 )},
                { 12, new KeyValuePair<int, int>( 29,13 )}
            };
        }

        public string Results
        {
            get
            {
                StringBuilder sb = new StringBuilder();
                sb.AppendLine($"Solved state of {indices.Length} town problem");
                sb.AppendLine($"Searched: {searched}");
                sb.AppendLine($"Duration: {watch.ElapsedMilliseconds/1000.0} seconds");
                sb.AppendLine($"Best dst: {bestTourDst}");
                sb.AppendLine($"Original indices: {string.Join(",", indices)}");
                sb.AppendLine($"Optimized indices: {string.Join(",", bestTourIndices)}");
                sb.Append($"Optimized coords: [");
                for (int i = 0; i < bestTourIndices.Length - 1; i++)
                {
                    sb.Append($"({coordinates[bestTourIndices[i]].Key},{coordinates[bestTourIndices[i]].Value}), ");
                }
                sb.AppendLine($"({coordinates[bestTourIndices[bestTourIndices.Length - 1]].Key},{coordinates[bestTourIndices[bestTourIndices.Length - 1]].Value})]");
                return sb.ToString();
            }
        }
    }
}

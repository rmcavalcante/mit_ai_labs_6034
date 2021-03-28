using Microsoft.VisualStudio.TestTools.UnitTesting;
using Optimization;
using System.Collections.Generic;
using System.Linq;

namespace UnitTestProject1
{
    [TestClass]
    public class UnitTest1
    {
        [TestMethod]
        public void TestRecursiveTravelerSalesman12Towns()
        {
            //5,8	6,13	8,9	10,20	9,35	14,7	13,28	16,21	18,28	20,36	21,19	27,14
            Dictionary<int, KeyValuePair<int, int>> coords = RecursiveTravellerSalesman.TwelveTowns();

            RecursiveTravellerSalesman rts = new RecursiveTravellerSalesman(coords, coords.Keys.Select(x => x).ToArray());
            rts.Solve();
            System.Diagnostics.Debug.Print(rts.Results);

        }
    }
}

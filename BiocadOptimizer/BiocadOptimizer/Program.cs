using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

namespace BiocadOptimizer
{ 
    class Reservation
    {
        string EquipmentID { get; set; }
        string OrderID { get; set; }
        string Amount { get; set; }
        string Start { get; set; }
        string Finish { get; set; }
    }

    class Configuration
    {
        public Configuration(List<EquipmentClass> eq_cl, List<OrderClass> ord_cl)
        {
            EquipementClasses = eq_cl.ToArray();

            OrderClasses = ord_cl.ToArray();

            foreach (var ord in OrderClasses)
            {
                ord.Link = new Dictionary<EquipmentClass, double>();
            }
        }

        private EquipmentClass[] EquipementClasses { get; set; }

        private OrderClass[] OrderClasses { get; set; }

        private Random rand = new Random();

        public double[][] GetMatrice()
        {
            double[][] koefMatrice = new double[EquipementClasses.Length][];

            for(int i = 0; i < koefMatrice.Length; ++i)
            {
                koefMatrice[i] = new double[EquipementClasses[i].orderClasses.Count()];
            }

            return koefMatrice;
        }

        public void ApplyMatrice(double[][] koefMatrice)
        {
            for (int i = 0; i < koefMatrice.Length; ++i)
            {
                for (int j = 0; j < EquipementClasses[i].orderClasses.Count; ++j)
                {
                    EquipementClasses[i].orderClasses[j].Link[EquipementClasses[i]] = koefMatrice[i][j];
                }
            }
        }

        public int OptimizeOrders()
        {
            int total = 0;

            foreach (var ord in OrderClasses)
            {
                double power = 0;

                foreach (var curLink in ord.Link)
                {
                    power += curLink.Value * curLink.Key.Power;
                }

                DateTime start = new DateTime(2019, 03, 18);

                var orders = ord.Orders;

                orders.Sort((x, y) => (x.Amount).CompareTo(y.Amount));

                int prodValue = 0;

                int processedNumber = 0;

                foreach (var curOrder in orders)
                {
                    prodValue = (int)(curOrder.Deadline - start).TotalHours * (int)power - curOrder.Amount;

                    if (prodValue < 0)
                    {
                        break;
                    }

                    processedNumber++;
                }

                total += processedNumber;
            }
            return total;
        }

        public void OptimizeByGen()
        {
            double[][] matr = GetMatrice();

            double[][][] generation = new double[10][][];

            for (int i = 0; i < 10; ++i)
            {
                generation[i] = new double[matr.Length][];

                for (int j = 0; j < matr.Length; ++j)
                {
                    generation[i][j] = new double[matr[j].Length];

                    var randRange = new List<double>
                    {
                        0.0
                    };

                    for (int k = 0; k < matr[j].Length; ++k)
                    {
                        randRange.Add(rand.NextDouble());
                    }

                    randRange.Sort();

                    for (int k = 0; k < matr[j].Length; ++k)
                    {
                        generation[i][j][k] = randRange[k + 1] - randRange[k];
                    }
                }
            }

            int stepsLim = 50;

            for (int i = 0; i < stepsLim; ++i)
            {
                var resultArr = new List<int>();

                for (int j = 0; j < generation.Length; ++j)
                {
                    ApplyMatrice(generation[j]);

                    resultArr.Add(OptimizeOrders());
                }

                resultArr.Sort();

                resultArr.Reverse();
            }
        }

    }

    class Program
    {
        static void Main(string[] args)
        {
            DataReader dataReader = new DataReader();

            DataProcessor dataProcessor = new DataProcessor(dataReader.Equipements, dataReader.Products, dataReader.Orders);

            var conf = dataProcessor.GetConfiguration();

            var mat = conf.GetMatrice();

            for (int i = 0; i < mat.Length; ++i)
            {
                for (int j = 0; j < mat[i].Length; ++j)
                {
                    mat[i][j] = 1.0 / mat[i].Length;
                }
            }

            conf.ApplyMatrice(mat);
        }
    }
}

using System;
using System.Collections.Generic;
using System.Text;

namespace BiocadOptimizer
{
    class Equipement
    {
        public string ID { get; set; }
        public string Type { get; set; }
        public string AH { get; set; }

        public int Velocity { get; set; }
    }

    class Order
    {
        public string ID { get; set; }
        public string _ProdID { get; set; }
        public Product Prod { get; set; }
        public int Amount { get; set; }
        public DateTime Deadline { get; set; }
    }

    class Product
    {
        public string ID { get; set; }
        public string[] EquipClassArray { get; set; }
    }
}

using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

namespace BiocadOptimizer
{
    class EquipmentClass
    {

        public EquipmentClass()
        {
            Equipements = new List<Equipement>();

            orderClasses = new List<OrderClass>();
        }

        public List<Equipement> Equipements { get; set; }

        public List<OrderClass> orderClasses { get; set; }

        public string Name { get; set; }

        public int Power { get; set; }
    }

    class OrderClass
    {
        public OrderClass()
        {
            Orders = new List<Order>();
        }

        public List<Order> Orders { get; set; }

        public Dictionary<EquipmentClass, double> Link { get; set; }

        public string[] Equip { get; set; }
    }

    class DataReader
    {
        private readonly string folder = @"C:\Users\I\Documents\DenisProjects\Hackaton\biocadData\";


        private readonly string equipment = "equipment_new.csv";

        private readonly string order = "order_new.csv";

        private readonly string product = "product_new.csv";


        public Equipement[] Equipements { get; set; }

        public Order[] Orders { get; set; }

        public Product[] Products { get; set; }


        public DataReader()
        {
            string[] equipLines = File.ReadAllLines(folder + equipment).Skip(1).ToArray();

            string[] orderLines = File.ReadAllLines(folder + order).Skip(1).ToArray();

            string[] prodLines = File.ReadAllLines(folder + product).Skip(1).ToArray();


            var equipData = from csvline in equipLines
                            let data = csvline.Split(';')
                            select new Equipement
                            {
                                ID = data[1],
                                Type = data[2],
                                AH = data[3],
                                Velocity = int.Parse(data[4])
                            };



            var orderData = from csvline in orderLines
                            let data = csvline.Split(';')
                            select new Order
                            {
                                ID = data[1],
                                _ProdID = data[2],
                                Amount = int.Parse(data[3]),
                                Deadline = DateTime.Parse(data[4])

                            };

            var prodData = from csvline in prodLines
                           let data = csvline.Split(';')
                           select new Product
                           {
                               ID = data[1],
                               EquipClassArray =
                                   data[2]
                                   .Replace("\\xa0", " ")
                                   .Split(',')
                           };

            Products = prodData.ToArray();
            Orders = orderData.ToArray();
            Equipements = equipData.ToArray();

            foreach (var pr in Products)
            {
                for (int i = 0; i < pr.EquipClassArray.Count(); ++i)
                {
                    pr.EquipClassArray[i] = pr.EquipClassArray[i]
                                            .Substring(1, pr.EquipClassArray[i].Count() - 2)
                                            .Trim('\'');
                }
            }

            foreach (var ord in Orders)
            {
                ord.Prod = Products.FirstOrDefault(x => x.ID == ord._ProdID);
            }
        }
    }

    class DataProcessor
    {
        //DataSet
        private Equipement[] Equipements { get; set; }

        public Product[] Products { get; set; }

        public Order[] Orders { get; set; }
        //...

        public Dictionary<string, EquipmentClass> EquipmentClasses { get; set; }

        public Dictionary<string, OrderClass> OrderClasses { get; set; }

        public DataProcessor(Equipement[] eq, Product[] pr, Order[] ord)
        {
            Equipements = eq;
            Products = pr;
            Orders = ord;

            EquipmentClasses = new Dictionary<string, EquipmentClass>();

            OrderClasses = new Dictionary<string, OrderClass>();
        }

        public Configuration GetConfiguration()
        {
            DivideEquipement();

            DivideOrdersByProduct();

            List<EquipmentClass> equip = new List<EquipmentClass>();

            List<OrderClass> ordCl = new List<OrderClass>();

            foreach (var it in EquipmentClasses)
            {
                equip.Add(it.Value);
            }

            foreach (var it in OrderClasses)
            {
                ordCl.Add(it.Value);
            }

            Configuration conf = new Configuration(equip, ordCl);

            return conf;
        }

        private void DivideEquipement()
        {
            foreach (var eq in Equipements)
            {
                if (EquipmentClasses.TryGetValue(eq.Type, out EquipmentClass value))
                {
                    value.Power += eq.Velocity;
                    value.Equipements.Add(eq);
                }
                else
                {
                    var newEq = new List<Equipement>
                    {
                        eq
                    };

                    EquipmentClasses.Add(eq.Type, new EquipmentClass { Equipements = newEq, Power = eq.Velocity, Name = eq.Type });
                }
            }
        }

        private void DivideOrdersByProduct()
        {
            foreach (var ord in Orders)
            {
                if (!OrderClasses.ContainsKey(ord._ProdID))
                {
                    var orderCl = new OrderClass { Equip = ord.Prod.EquipClassArray, Orders = new List<Order> { ord } };
                    OrderClasses.Add(ord._ProdID, orderCl);
                    for (int i = 0; i < orderCl.Equip.Length; i++)
                    {
                        if (EquipmentClasses.TryGetValue(orderCl.Equip[i], out EquipmentClass eqCl))
                        {
                            EquipmentClasses[orderCl.Equip[i]].orderClasses.Add(orderCl);
                        }
                    }
                }
                else
                {
                    OrderClasses[ord._ProdID].Orders.Add(ord);
                }
            }
        }

        private Random rand = new Random();
    }
}

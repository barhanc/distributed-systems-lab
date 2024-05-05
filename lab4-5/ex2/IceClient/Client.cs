using Complex;
using Ice;
using Exception = System.Exception;

namespace IceClient;

public static class Client
{
    public static int Main(string[] args)
    {
        try
        {
            var communicator = Util.initialize(ref args);
            var proxy = communicator.stringToProxy("SimpleCalc:default -h localhost -p 10000");

            string? line = null!;
            do
            {
                try
                {
                    Console.Write("==> ");
                    Console.Out.Flush();
                    line = Console.In.ReadLine();
                    if (line == null)
                    {
                        break;
                    }

                    switch (line)
                    {
                        case "sum":
                        {
                            var outStream = new OutputStreamI(communicator);
                            outStream.startEncapsulation();
                            outStream.writeIntSeq([1, 2, 3, 4]);
                            outStream.endEncapsulation();

                            if (!proxy.ice_invoke("sum", OperationMode.Normal, outStream.finished(), out var _))
                            {
                                Console.Error.WriteLine("Unknown user exception");
                            }

                            break;
                        }
                        case "len":
                        {
                            var outStream = new OutputStreamI(communicator);
                            outStream.startEncapsulation();
                            outStream.writeIntSeq([1, 2, 3, 4]);
                            outStream.endEncapsulation();

                            if (!proxy.ice_invoke("len", OperationMode.Normal, outStream.finished(), out var _))
                            {
                                Console.Error.WriteLine("Unknown user exception");
                            }

                            break;
                        }
                        case "csum":
                        {
                            var outStream = new OutputStreamI(communicator);
                            outStream.startEncapsulation();
                            ComplexInt[] seq = [new ComplexInt(1, 2), new ComplexInt(3, 4)];
                            ComplexIntSeqHelper.write(outStream, seq);
                            outStream.endEncapsulation();

                            if (!proxy.ice_invoke("csum", OperationMode.Normal, outStream.finished(), out var _))
                            {
                                Console.Error.WriteLine("Unknown user exception");
                            }
                            
                            break;
                        }
                        case "":
                        case "x":
                            break;
                        default:
                            Console.Error.WriteLine("Unknown command. Usage: 'sum', 'len', 'csum'. To exit type 'x'.");
                            break;
                    }
                }
                catch (LocalException ex)
                {
                    Console.Error.WriteLine(ex);
                }
            } while (line != null && !line.Equals("x"));

            return 0;
        }
        catch (Exception ex)
        {
            Console.Error.WriteLine(ex);
            return 1;
        }
    }
}
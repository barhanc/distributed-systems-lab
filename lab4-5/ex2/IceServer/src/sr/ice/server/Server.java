package sr.ice.server;

import com.zeroc.Ice.*;
import com.zeroc.Ice.Object;

public class Server {
    public static void main(String[] args) {
        Communicator communicator = Util.initialize(args);
        ObjectAdapter adapter = communicator.createObjectAdapterWithEndpoints("SimpleCalcAdapter", "default -p 10000");
        Object object = new CalcI();

        adapter.add(object, com.zeroc.Ice.Util.stringToIdentity("SimpleCalc"));
        adapter.activate();

        System.out.println("Server started");
        communicator.waitForShutdown();
    }
}

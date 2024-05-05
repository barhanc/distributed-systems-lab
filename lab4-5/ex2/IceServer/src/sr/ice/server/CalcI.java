package sr.ice.server;

import com.zeroc.Ice.*;
import gen.ComplexInt;
import gen.ComplexIntSeqHelper;

import java.util.Arrays;

public class CalcI implements Blobject {
    @Override
    public Ice_invokeResult ice_invoke(byte[] inParams, Current current) {
        Communicator communicator = current.adapter.getCommunicator();
        InputStream in = new InputStream(communicator, inParams);

        Ice_invokeResult result = new Ice_invokeResult();
        result.returnValue = true;

        String operation = current.operation;

        switch (operation) {
            case "sum" -> {
                in.startEncapsulation();
                int[] seq = in.readIntSeq();
                in.endEncapsulation();

                System.out.println("sum" + "(" + Arrays.toString(seq) + ")" + " = " + Arrays.stream(seq).sum());
            }
            case "len" -> {
                in.startEncapsulation();
                int[] seq = in.readIntSeq();
                in.endEncapsulation();

                System.out.println("len" + "(" + Arrays.toString(seq) + ")" + " = " + seq.length);
            }
            case "csum" -> {
                in.startEncapsulation();
                ComplexInt[] seq = ComplexIntSeqHelper.read(in);
                in.endEncapsulation();

                int re = 0, im = 0;
                for (ComplexInt c : seq) {
                    re += c.re;
                    im += c.im;
                }
                System.out.println("csum" + " = " + re + " + " + im + "i");
            }
            default -> {
                System.out.println("Unknown operation: " + operation);
                result.returnValue = false;
            }
        }

        return result;
    }
}
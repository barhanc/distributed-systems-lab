package lab1.ex1;

import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.util.Arrays;

public class server {
    public static void main(String args[]) throws Exception {
        System.out.println("JAVA UDP SERVER");
        DatagramSocket socket = null;
        int portNumber = 9008;

        try {
            byte[] receiveBuffer = new byte[1024];
            socket = new DatagramSocket(portNumber);

            while (true) {
                // Listen
                Arrays.fill(receiveBuffer, (byte) 0);
                DatagramPacket receivePacket = new DatagramPacket(receiveBuffer, receiveBuffer.length);
                socket.receive(receivePacket);

                // Print received msg
                String msg = new String(receivePacket.getData());
                System.out.println("Msg from client: " + msg);

                // Send confirmation msg to sender
                byte[] sendBuffer = ("hello " + receivePacket.getAddress()).getBytes();
                DatagramPacket sendPacket = new DatagramPacket(sendBuffer, sendBuffer.length,
                        receivePacket.getAddress(), receivePacket.getPort());
                socket.send(sendPacket);

            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            if (socket != null) {
                socket.close();
            }
        }

    }
}

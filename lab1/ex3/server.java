package lab1.ex3;

import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.util.Arrays;
import java.nio.ByteBuffer;

public class server {
    public static void main(String args[]) {
        System.out.println("JAVA UDP SERVER");
        DatagramSocket socket = null;
        int portNumber = 9008;

        try {
            socket = new DatagramSocket(portNumber);
            byte[] receiveBuffer = new byte[1024];

            while (true) {
                Arrays.fill(receiveBuffer, (byte) 0);
                DatagramPacket receivePacket = new DatagramPacket(receiveBuffer, receiveBuffer.length);
                socket.receive(receivePacket);

                // Print
                int num = ByteBuffer.wrap(receiveBuffer).getInt();
                System.out.println("received num: " + num);

                // Increment and send back
                byte[] sendBuffer = ByteBuffer.allocate(4).putInt(num + 1).array();
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

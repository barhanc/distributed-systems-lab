package lab1.ex1;

import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.util.Arrays;

public class client {
    public static void main(String args[]) throws Exception {
        System.out.println("JAVA UDP CLIENT");
        DatagramSocket socket = null;
        int portNumber = 9008;

        try {
            socket = new DatagramSocket();
            InetAddress address = InetAddress.getByName("localhost");
            byte[] buffer = "Ping Java Udp".getBytes();

            // Send packet to server
            DatagramPacket sendPacket = new DatagramPacket(buffer, buffer.length, address, portNumber);
            socket.send(sendPacket);

            // Wait for response from the server
            Arrays.fill(buffer, (byte) 0);
            DatagramPacket receivePacket = new DatagramPacket(buffer, buffer.length);
            socket.receive(receivePacket);

            // Print received msg
            String msg = new String(receivePacket.getData());
            System.out.println("Msg from server: " + msg);

        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            if (socket != null) {
                socket.close();
            }
        }
    }
}

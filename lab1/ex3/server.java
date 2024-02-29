package lab1.ex3;

import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.util.Arrays;
import java.util.Collection;
import java.util.List;

import javax.swing.plaf.basic.BasicSplitPaneUI.BasicHorizontalLayoutManager;

import java.nio.ByteBuffer;
import java.nio.ByteOrder;

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

                // Get int and print
                ByteBuffer rcvByteBuffer = ByteBuffer.wrap(receiveBuffer);
                rcvByteBuffer.order(ByteOrder.LITTLE_ENDIAN);
                int num = rcvByteBuffer.getInt();
                System.out.println("received num: " + num);

                // Increment and send back
                ByteBuffer sndByteBuffer = ByteBuffer.allocate(4);
                sndByteBuffer.order(ByteOrder.LITTLE_ENDIAN);
                sndByteBuffer.putInt(num + 1);
                byte[] sendBuffer = sndByteBuffer.array();
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

    public static void reverse(byte[] array) {
        if (array == null) {
            return;
        }
        int i = 0;
        int j = array.length - 1;
        byte tmp;
        while (j > i) {
            tmp = array[j];
            array[j] = array[i];
            array[i] = tmp;
            j--;
            i++;
        }
    }
}

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.Objects;

public class Z1_Producer {

    public static void main(String[] argv) throws Exception {

        // info
        System.out.println("Z1 PRODUCER");

        // connection & channel
        ConnectionFactory factory = new ConnectionFactory();
        factory.setHost("localhost");
        Connection connection = factory.newConnection();
        Channel channel = connection.createChannel();

        // queue
        String QUEUE_NAME = "queue1";
        channel.queueDeclare(QUEUE_NAME, false, false, false, null);        

        // producer (publish msg)
//        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line = null;
        java.io.BufferedReader in = new java.io.BufferedReader(new java.io.InputStreamReader(System.in));
        do{
            System.out.print("==> ");
            line = in.readLine();
            if (line.matches("\\d+")){
                channel.basicPublish("", QUEUE_NAME, null, line.getBytes());
                System.out.println("Sent: " + line);
            } else if (line.equals("x")){
                System.out.println("Goodbye");
            } else if (line.isEmpty())
            {
                // pass
            }
            else {
                System.out.println("Wrong input. Only integers or 'x' to quit are allowed.");
            }
        } while(!Objects.equals(line, "x"));

        for(int i=0; i<4; i++){
            String message = "1";
            channel.basicPublish("", QUEUE_NAME, null, message.getBytes());
            System.out.println("Sent: " + message);

            message = "5";
            channel.basicPublish("", QUEUE_NAME, null, message.getBytes());
            System.out.println("Sent: " + message);
        }

        // close
        channel.close();
        connection.close();
    }
}

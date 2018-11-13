import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import com.sun.deploy.net.HttpRequest;
import com.sun.deploy.net.HttpResponse;
import org.apache.commons.codec.binary.Base64;
import org.apache.commons.io.FileUtils;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.DefaultHttpClient;

import java.io.DataInputStream;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLConnection;
import java.util.ArrayList;
import java.util.List;

/**
 * Created by maciejszwaczka on 13.11.2018.
 */
public class Client {

    public static void main(String[] args)
    {
        try {


            File file = new File("C:\\Users\\maciejszwaczka\\Desktop\\spaghetti_bolognese_00.jpg");
            byte[] encoded = Base64.encodeBase64(FileUtils.readFileToString(file,"UTF8").getBytes());

            HttpClient httpClient = new DefaultHttpClient();
            HttpPost httpPost = new HttpPost("http://40.89.133.248:8080/v1/models/dishrecognizer:predict");
            httpPost.setHeader("Content-type", "application/json");
            try {


                JsonObject object = new JsonObject();
                JsonArray arr = new JsonArray();
                JsonObject instance=new JsonObject();
                instance.put("b64",new String(encoded));
                arr.add(instance);
                object.add("instances",arr);
                StringEntity stringEntity = new StringEntity(object.());
                httpPost.getRequestLine();
                httpPost.setEntity(stringEntity);
                httpPost.setHeader("Content-type", "application/json");
                org.apache.http.HttpResponse response=httpClient.execute(httpPost);
                System.out.println(response.getStatusLine());
                DataInputStream stream=(DataInputStream) response.getEntity().getContent();
                byte[] body=new byte[stream.available()];
                stream.read(body);
                String jsonBody = new String(body);
                int x=1;
            } catch (Exception e) {
                throw new RuntimeException(e);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

}

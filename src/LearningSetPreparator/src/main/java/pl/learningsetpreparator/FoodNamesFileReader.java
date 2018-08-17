package pl.learningsetpreparator;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import pl.learningsetpreparator.entities.FoodResource;

/**
 * Created by maciejszwaczka on 01.06.2018.
 */
public class FoodNamesFileReader {
    public static File fileWithNames=new File(System.getProperty("user.dir")+"\\src\\main\\java\\pl\\learningsetpreparator\\foodNames.txt");
    public List<FoodResource> readFoodNames()
    {
        List<FoodResource> foodNames=new ArrayList<>();
        try(BufferedReader buffReader=new BufferedReader
            (new InputStreamReader
            (new FileInputStream(fileWithNames),"UTF8")))
        {
            String foodRes;
            while((foodRes=buffReader.readLine())!=null)
            {
                String foodName=foodRes.split(":")[0];
                int foodAmount=Integer.parseInt(foodRes.split(":")[1]);
                FoodResource newResource=new FoodResource(foodName,foodAmount);
                foodNames.add(newResource);
                System.out.println(foodName);
            }
            buffReader.close();
        }
        catch(IOException e)
        {
            e.printStackTrace();
        }
        return foodNames;
    }
}

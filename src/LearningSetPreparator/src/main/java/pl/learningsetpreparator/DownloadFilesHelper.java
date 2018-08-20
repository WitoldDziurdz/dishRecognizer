/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package pl.learningsetpreparator;
import java.awt.image.BufferedImage;
import java.io.ByteArrayOutputStream;
import javax.imageio.IIOException;
import java.io.File;
import java.io.IOException;
import java.net.HttpURLConnection;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.imageio.ImageIO;
import javax.net.ssl.SSLHandshakeException;
import pl.learningsetpreparator.entities.FoodResource;
import pl.learningsetpreparator.entities.URLPhotoResource;
import pl.learningsetpreparator.enumparameters.AdditionalWords;
/**
 *
 * @author maciejszwaczka
 */
public class DownloadFilesHelper {
    
    public static final String learningSetFolder=System.getProperty("user.dir")+"\\Learning set";
    
    public SearchHelper searchHelper;
    
    public DownloadFilesHelper()
    {
        this.searchHelper = new SearchHelper();
        new File(learningSetFolder).mkdir();
    }
    public void downloadFilesOfFood(List<String> foodNames) {
       for(String foodRes:foodNames) {
           File folderWithPhotosOfDish=new File(learningSetFolder+"\\"+foodRes);
           folderWithPhotosOfDish.mkdir();
           for(URLPhotoResource urlRes:searchHelper.getPhotosOfFood(foodRes))
                {
                    try {
                        downloadFileFromUrl(urlRes,folderWithPhotosOfDish);
                    } catch (Exception ex) {
                        System.out.println(urlRes.getUrl());
                        ex.printStackTrace();
                    }
                }
            }
       }
    public void downloadFileFromUrl(URLPhotoResource url,File folderWithPhotos) throws Exception
    {
        System.setProperty("http.agent", "");       
        ImageResizer imgHelper=new ImageResizer(800,800);
        File newFile=new File(folderWithPhotos.getAbsolutePath()+"\\"+url.getName());
        String[] parts=url.getName().split("\\.");                
        HttpURLConnection connection = (HttpURLConnection) url.getUrl().openConnection();
        connection.setRequestProperty("User-Agent",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31");
        BufferedImage image =null;
        image = ImageIO.read(connection.getInputStream());
        if(image!=null){
            image=imgHelper.resizeImage(image);
            newFile.createNewFile();
            ImageIO.write(image, parts[parts.length-1],newFile);
        }          
    }  
}
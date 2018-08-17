/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package pl.learningsetpreparator;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.Reader;
import pl.learningsetpreparator.*;
import java.net.URL;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;
import java.util.stream.Collectors;
import pl.learningsetpreparator.entities.*;
/**
 *
 * @author maciejszwaczka
 */
public class Main {
    public static void main(String[] args) throws InterruptedException  {
            System.setProperty("file.encoding", "UTF-8");
            FoodNamesFileReader reader=new FoodNamesFileReader();
            List<FoodResource> foodNames=reader.readFoodNames();
            DownloadFilesHelper downloadHelper=new DownloadFilesHelper();
            downloadHelper.downloadFilesOfFood(foodNames.stream().map(FoodResource::getName).collect(Collectors.toList()));
    }
}

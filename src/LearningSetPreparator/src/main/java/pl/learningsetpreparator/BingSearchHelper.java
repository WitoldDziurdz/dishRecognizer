/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package pl.learningsetpreparator;

import java.net.MalformedURLException;
import java.net.URI;
import java.net.URL;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.utils.URIBuilder;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;
import org.codehaus.jettison.json.JSONArray;
import org.codehaus.jettison.json.JSONException;
import org.codehaus.jettison.json.JSONObject;
import pl.learningsetpreparator.entities.FoodResource;
import pl.learningsetpreparator.entities.URLPhotoResource;

/**
 *
 * @author maciejszwaczka
 */
public class BingSearchHelper {
    public BingSearchHelper()
    {
        
    }
    public Set<URL> getResultsImages(String foodName)
    {
        HttpClient httpclient = HttpClients.createDefault();
        Set<URL> foodPhotosAddresses=new HashSet<>();
        try
        {
            for(int i=0;8>i;i++)
            {
                URIBuilder builder = new URIBuilder("https://api.cognitive.microsoft.com/bing/v7.0/images/search");

                builder.setParameter("q", foodName);
                builder.setParameter("count", "150");
                builder.setParameter("offset", Integer.toString((150)*i));
                builder.setParameter("mkt", "en-us");
                builder.setParameter("safeSearch", "Moderate");
                URI uri = builder.build();
                HttpGet request = new HttpGet(uri);
                request.setHeader("Ocp-Apim-Subscription-Key", "5ce7dd43b63c43d48fbeca48ba1fd3de");

                HttpResponse response = httpclient.execute(request);
                HttpEntity entity = response.getEntity();
                if (entity != null) 
                {
                    Set newSet=parseJson(EntityUtils.toString(entity));
                    foodPhotosAddresses.addAll(newSet);
                    System.out.println(foodPhotosAddresses.size());
                }
            }
            Thread.sleep(1000);
        }
        catch (Exception e)
        {
            System.out.println(e.getMessage());
        }
        return foodPhotosAddresses;
    }
    private Set<URL> parseJson(String requestStr) throws MalformedURLException
    {
        int x = requestStr.indexOf("{");
        Set<URL> newSet=new HashSet<>();
        requestStr = requestStr.substring(x);
        try { 
            JSONObject json = new JSONObject(requestStr.trim());
            JSONObject request=new JSONObject(requestStr);
            JSONArray rateArray=request.getJSONArray("value");
            System.out.println(rateArray.length());
            for(int i=0;rateArray.length()>i;i++)
            {
                JSONObject obj=rateArray.getJSONObject(i);
                newSet.add(new URL(obj.getString("contentUrl")));
            }
        } catch (JSONException ex) {
            Logger.getLogger(BingSearchHelper.class.getName()).log(Level.SEVERE, null, ex);
        }
        return newSet;
    }
}

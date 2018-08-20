/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package pl.learningsetpreparator;

import java.net.URL;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.concurrent.ForkJoinPool;
import java.util.Set;
import java.util.concurrent.ExecutionException;
import java.util.logging.Level;
import java.util.logging.Logger;
import java.util.stream.Collectors;
import pl.learningsetpreparator.entities.URLPhotoResource;
import pl.learningsetpreparator.enumparameters.AdditionalWords;

/**
 *
 * @author maciejszwaczka
 */
public class SearchHelper {
    private GoogleSearchHelper googleHelper;
    
    private BingSearchHelper bingHelper;
    
    private NameExtractor nameExtractor;
    
    public SearchHelper()
    {
        this.googleHelper=new GoogleSearchHelper();
        this.bingHelper= new BingSearchHelper();
        this.nameExtractor= new NameExtractor();
    }
    public List<URLPhotoResource> getPhotosOfFood(String name)
    {
        Set<URL> addresses = new HashSet<>();
        /*try {
            
            ForkJoinPool threadPool=new ForkJoinPool(10);
            threadPool.submit( () -> Arrays.asList(AdditionalWords.values()).
                    parallelStream().
                    map(value -> addresses.
                            addAll(bingHelper.getResultsImages(name+" "+value)))).get();
            threadPool.submit( () -> Arrays.asList(AdditionalWords.values()).
                    parallelStream().
                    map(value -> addresses.
                            addAll(googleHelper.getResultsImages(name+" "+value)))).get();
            } catch (InterruptedException ex) {
                Logger.getLogger(SearchHelper.class.getName()).log(Level.SEVERE, null, ex);
            } catch (ExecutionException ex) {
                Logger.getLogger(SearchHelper.class.getName()).log(Level.SEVERE, null, ex);
            }
            System.out.println("before"+addresses.size());*/
            for(AdditionalWords additionalWord:AdditionalWords.values())
            {
                addresses.addAll(bingHelper.getResultsImages(name+" "+additionalWord));
                addresses.addAll(googleHelper.getResultsImages(name+" "+additionalWord));
            }
            /*System.out.println("after"+addresses.size());*/
            List<URLPhotoResource> result = addresses.stream().
                    map(addr -> new URLPhotoResource(addr,nameExtractor.extractNameFromURL(addr))).
                    collect(Collectors.toList());
            return result;
    }
}

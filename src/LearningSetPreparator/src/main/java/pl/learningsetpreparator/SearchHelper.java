/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package pl.learningsetpreparator;

import java.net.URL;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
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
    private URLPhotoResource createURLPhotoResource(URL addr)
    {
        return new URLPhotoResource(addr,nameExtractor.extractNameFromURL(addr));
    }
    public List<URLPhotoResource> getPhotosOfFood(String name)
    {
        Set<URL> addresses = new HashSet<>();
        /*for(AdditionalWords additionalWord:AdditionalWords.values())
        {*/
            addresses.addAll(bingHelper.getResultsImages(name+" "/*+additionalWord*/));
            addresses.addAll(googleHelper.getResultsImages(name+" "/*+additionalWord*/));
        /*}*/
        List<URLPhotoResource> result = addresses.stream().
                map(addr -> new URLPhotoResource(addr,nameExtractor.extractNameFromURL(addr))).
                collect(Collectors.toList());
        return result;
    }
}

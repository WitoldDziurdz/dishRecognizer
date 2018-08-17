/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package pl.learningsetpreparator;

import java.net.MalformedURLException;
import java.net.URL;
import java.util.logging.Level;
import java.util.logging.Logger;
import pl.learningsetpreparator.entities.URLPhotoResource;

/**
 *
 * @author maciejszwaczka
 */
public class NameExtractor {

    public NameExtractor() {
        
    }
    
    public String extractNameFromURL(URL address)
    {
        String parts[]=address.toString().split("/");
        String name=parts[parts.length-1];
        parts=name.split("\\?");
        name=parts[0];
        return name;
    }
    
}

/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package pl.learningsetpreparator.entities;

import java.net.URL;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
/**
 *
 * @author maciejszwaczka
 */
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class URLPhotoResource {
    private URL url;
    private String name;
}

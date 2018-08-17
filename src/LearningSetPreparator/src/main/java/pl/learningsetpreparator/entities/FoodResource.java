/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package pl.learningsetpreparator.entities;

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
public class FoodResource {
    private String name;
    private int amountOfPhotos;
    /*@Override*/
    /*public boolean equals(Object o)
    {
        if(o instanceof FoodResource)
        {
            FoodResource toCheckEqualityObject=(FoodResource)o;
            return name.equals(toCheckEqualityObject.name) && amountOfPhotos
        }
    }*/
}

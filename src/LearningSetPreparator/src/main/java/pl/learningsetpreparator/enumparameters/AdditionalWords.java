/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package pl.learningsetpreparator.enumparameters;

import java.util.Arrays;
import java.util.List;

/**
 *
 * @author maciejszwaczka
 */
public enum AdditionalWords {
    Skladniki,
    Przepis,
    Fit,
    Warzywne,
    Miesne,
    Porcja,
    EMPTY("");
    final String name;
    AdditionalWords(String name) { this.name = name; }
    AdditionalWords() { this(null); }
}

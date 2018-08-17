package pl.learningsetpreparator;
import java.awt.Graphics2D;
import java.awt.Image;
import java.awt.image.BufferedImage;
import java.io.BufferedReader;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 * @author maciejszwaczka
 */
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class ImageResizer {
    private int width;
    private int height;
    public BufferedImage resizeImage(BufferedImage image) throws NullPointerException{
        /*Image img=image.getScaledInstance(width, height, Image.SCALE_SMOOTH);
        image = new BufferedImage(800,800,Image.SCALE_DEFAULT);
        Graphics2D g2d = image.createGraphics();
        g2d.drawImage(img, 0, 0, null);
        g2d.dispose();*/
        return image;
    }
}

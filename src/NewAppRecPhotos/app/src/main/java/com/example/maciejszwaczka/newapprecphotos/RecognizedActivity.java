package com.example.maciejszwaczka.newapprecphotos;

import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.support.constraint.ConstraintLayout;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;

public class RecognizedActivity extends AppCompatActivity {

    private ImageView view;

    private Bitmap bitmap;

    private ImageClassifier classifier;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_recognized);
        Intent intent = getIntent();
        try {
            classifier = new ImageClassifier(this);
        } catch (IOException e) {
            e.printStackTrace();
        }
        String locOfBitmap = intent.getExtras().get("bitmapLoc").toString();
        InputStream inputStream = null;
        try {
            inputStream = getContentResolver().openInputStream(Uri.fromFile(new File(locOfBitmap)));
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
        Bitmap pictureBitmap = BitmapFactory.decodeStream(inputStream);
        view = findViewById(R.id.take_picture_image_view);
        int ivWidth = getApplicationContext().getResources().getDisplayMetrics().widthPixels;
        int newWidth = ivWidth;
        int newHeight = (int) Math.floor((double) pictureBitmap.getHeight() *( (double) newWidth / (double) pictureBitmap.getWidth()));
        Bitmap newbitMap = Bitmap.createScaledBitmap(pictureBitmap, newWidth, newHeight, true);
        bitmap = newbitMap;
        view.setImageBitmap(newbitMap);
    }

    @Override
    protected void onPostCreate(Bundle savedInstanceState)
    {
        super.onPostCreate(savedInstanceState);
        try {
            String res=classifier.classifyPhoto(bitmap);
            TextView foodNameView = findViewById(R.id.foodNameView);
            foodNameView.setText(res);
            foodNameView.setVisibility(View.VISIBLE);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}

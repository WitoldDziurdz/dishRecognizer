package com.example.maciejszwaczka.newapprecphotos;

import android.content.CursorLoader;
import android.content.Intent;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.provider.DocumentsContract;
import android.provider.MediaStore;
import android.provider.OpenableColumns;
import android.support.constraint.ConstraintLayout;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.ViewTreeObserver;
import android.widget.ImageView;
import android.widget.LinearLayout;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;

public class RecognizedActivity extends AppCompatActivity {

    public int width;

    public int height;

    public ConstraintLayout layout;

    public ImageView view;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_recognized);
        Intent intent = getIntent();
        layout= findViewById(R.id.reclayout);
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
        view.setImageBitmap(newbitMap);
    }
}

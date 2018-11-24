package com.example.maciejszwaczka.newapprecphotos;

import android.database.Cursor;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;

import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.os.Environment;
import android.provider.MediaStore;
import android.support.v4.content.FileProvider;
import android.view.View;
import android.widget.Button;

import java.io.File;
import java.io.IOException;
import java.util.UUID;

public class RecognizingActivity extends AppCompatActivity {

    private static final int REQUEST_CODE_TAKE_PICTURE = 1;

    private static final int PICK_IMAGE = 2;

    private Context context= this;

    public String mCurrentPhotoPath;

    private Button takePictureButton;

    private Button selectPictureButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_recognizing);
        selectPictureButton = findViewById(R.id.select_picture);
        selectPictureButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent;
                intent = new Intent(
                        Intent.ACTION_PICK,
                        android.provider.MediaStore.Images.Media.EXTERNAL_CONTENT_URI);
                intent.setType("image/*");
                startActivityForResult(Intent.createChooser(intent, "Select Picture"),PICK_IMAGE);
            }
        });
        takePictureButton = findViewById(R.id.take_picture_button);
        takePictureButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent takePictureIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
                if (takePictureIntent.resolveActivity(getPackageManager()) != null) {
                    File photoFile = null;
                    try {
                        photoFile = createImageFile();
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                    if (photoFile != null) {
                        Uri photoURI = FileProvider.getUriForFile(context,
                                "com.example.android.fileprovider",
                                photoFile);
                        takePictureIntent.putExtra(MediaStore.EXTRA_OUTPUT, photoURI);
                        startActivityForResult(takePictureIntent, REQUEST_CODE_TAKE_PICTURE);
                    }
                }
            }
        });
    }

    private File createImageFile() throws IOException {
        String imageFileName = UUID.randomUUID().toString();
        File storageDir =
                getExternalFilesDir(Environment.DIRECTORY_PICTURES);
        File image = new File(storageDir,
                imageFileName+".png");
        image.createNewFile();
        mCurrentPhotoPath = image.getAbsolutePath();
        return image;
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        if (requestCode == REQUEST_CODE_TAKE_PICTURE) {
            if (resultCode == RESULT_OK) {
                Intent recognizedIntent= new Intent(context, RecognizedActivity.class);
                recognizedIntent.putExtra("bitmapLoc", mCurrentPhotoPath);
                startActivity(recognizedIntent);
            }
        }
        else if(requestCode == PICK_IMAGE)
        {
            if (resultCode == RESULT_OK) {
                Uri x=data.getData();
                String path = getRealPathFromURI(this, x);
                Intent recognized = new Intent(this, RecognizedActivity.class);
                recognized.putExtra("bitmapLoc",path);
                startActivity(recognized);
            }
        }
    }

    private String getRealPathFromURI(Context context, Uri contentUri) {
        Cursor cursor = null;
        try {
            String[] proj = { MediaStore.Images.Media.DATA };
            cursor = context.getContentResolver().query(contentUri,  proj, null, null, null);
            int column_index = cursor.getColumnIndexOrThrow(MediaStore.Images.Media.DATA);
            cursor.moveToFirst();
            return cursor.getString(column_index);
        } catch (Exception e) {
            e.printStackTrace();
            return "";
        } finally {
            if (cursor != null) {
                cursor.close();
            }
        }
    }
}

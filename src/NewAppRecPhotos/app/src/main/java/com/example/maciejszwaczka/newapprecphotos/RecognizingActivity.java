package com.example.maciejszwaczka.newapprecphotos;

import android.Manifest;
import android.content.pm.PackageManager;
import android.database.Cursor;
import android.support.v4.content.ContextCompat;
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

    private String mCurrentPhotoPath;

    private Button takePictureButton;

    private Button selectPictureButton;

    private static final int FILES_PERMISSIONS_GRANTED=1;

    private static final int CAMERA_PERMISSIONS_GRANTED=2;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_recognizing);
        selectPictureButton = findViewById(R.id.select_picture);
        selectPictureButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (ContextCompat.checkSelfPermission(context, Manifest.permission.READ_EXTERNAL_STORAGE)
                        != PackageManager.PERMISSION_GRANTED) {
                    requestPermissions(new String[]{Manifest.permission.READ_EXTERNAL_STORAGE},FILES_PERMISSIONS_GRANTED);
                }
                else {
                    onRequestPermissionsResult(FILES_PERMISSIONS_GRANTED, new String[]{Manifest.permission.READ_EXTERNAL_STORAGE}, new int[]{PackageManager.PERMISSION_GRANTED});
                }
            }
        });
        takePictureButton = findViewById(R.id.take_picture_button);
        takePictureButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (ContextCompat.checkSelfPermission(context, Manifest.permission.CAMERA)
                        != PackageManager.PERMISSION_GRANTED || ContextCompat.checkSelfPermission(context, Manifest.permission.WRITE_EXTERNAL_STORAGE)
                        != PackageManager.PERMISSION_GRANTED) {
                    requestPermissions(new String[]{Manifest.permission.READ_EXTERNAL_STORAGE,Manifest.permission.WRITE_EXTERNAL_STORAGE,Manifest.permission.CAMERA},CAMERA_PERMISSIONS_GRANTED);
                }
               else {
                    onRequestPermissionsResult(CAMERA_PERMISSIONS_GRANTED, new String[]{Manifest.permission.READ_EXTERNAL_STORAGE,Manifest.permission.WRITE_EXTERNAL_STORAGE, Manifest.permission.CAMERA}, new int[]{PackageManager.PERMISSION_GRANTED,PackageManager.PERMISSION_GRANTED, PackageManager.PERMISSION_GRANTED});
                }
            }
        });
    }
    private boolean isAllPermissionsGranted(int[] grantResults)
    {
        for(int result:grantResults)
        {
            if(result != PackageManager.PERMISSION_GRANTED)
            {
                return false;
            }
        }
        return true;
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        if(isAllPermissionsGranted(grantResults)) {
            switch (requestCode) {
                case CAMERA_PERMISSIONS_GRANTED:
                    Intent takePictureIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
                    if (takePictureIntent.resolveActivity(getPackageManager()) != null) {
                        File photoFile = null;
                        try {
                            photoFile = createImageFile();
                            Uri photoURI = FileProvider.getUriForFile(context,
                                    "com.example.android.fileprovider",
                                    photoFile);
                            takePictureIntent.putExtra(MediaStore.EXTRA_OUTPUT, photoURI);
                            startActivityForResult(takePictureIntent, REQUEST_CODE_TAKE_PICTURE);
                        } catch (IOException e) {
                            e.printStackTrace();
                        }
                    }
                    break;
                case FILES_PERMISSIONS_GRANTED:
                    Intent intent;
                    intent = new Intent(
                            Intent.ACTION_PICK,
                            android.provider.MediaStore.Images.Media.EXTERNAL_CONTENT_URI);
                    intent.setType("image/*");
                    startActivityForResult(intent, PICK_IMAGE);
                    break;
            }
        }
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

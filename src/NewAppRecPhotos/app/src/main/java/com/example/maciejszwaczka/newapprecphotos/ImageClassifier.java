package com.example.maciejszwaczka.newapprecphotos;

import android.app.Activity;
import android.graphics.Bitmap;
import android.os.StrictMode;

import com.example.maciejszwaczka.newapprecphotos.models.Inputs;
import com.example.maciejszwaczka.newapprecphotos.models.Request;
import com.example.maciejszwaczka.newapprecphotos.models.Results;
import com.google.gson.Gson;
import com.mashape.unirest.http.HttpResponse;
import com.mashape.unirest.http.Unirest;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** Classifies images with Tensorflow Lite. */

public class ImageClassifier {

    private static final String LABEL_PATH = "labels.txt";

    private static final int RESULTS_TO_SHOW = 3;

    private static final int DIM_BATCH_SIZE = 1;

    private static final int DIM_PIXEL_SIZE = 3;

    static final int DIM_IMG_SIZE_X = 256;

    static final int DIM_IMG_SIZE_Y = 256;

    private List<String> labelList;


    ImageClassifier(Activity activity) throws IOException {
        labelList = loadLabelList(activity);
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);
    }

    public String classifyPhoto(Bitmap bitmap) throws Exception {

        float[][][][] data=convertBitmapToByteBuffer(bitmap);
        Request req=new Request(new Inputs(data));
        Gson gson = new Gson();
        HttpResponse<String> jsonResponse = Unirest.post("http://40.89.133.248:8080/v1/models/dishrecognizer:predict")
                .header("accept", "application/json")
                .body(gson.toJson(req)).asString();
        Results results=gson.fromJson(jsonResponse.getBody(),Results.class);
        if(Collections.max(results.getOutputs().get(0))>0.2f) {
            return labelList.get(results.getOutputs().get(0).indexOf(Collections.max(results.getOutputs().get(0))));
        }
        else{
            return "Not recognized";
        }
    }

    private float[][][][] convertBitmapToByteBuffer(Bitmap bitmap) {
        Bitmap newbitMap = Bitmap.createScaledBitmap(bitmap, DIM_IMG_SIZE_X, DIM_IMG_SIZE_Y, true);
        float[][][][] photoTensor = new float[DIM_BATCH_SIZE][DIM_IMG_SIZE_X][DIM_IMG_SIZE_Y][DIM_PIXEL_SIZE];
        for (int i = 0; i < DIM_IMG_SIZE_X; ++i) {
            for (int j = 0; j < DIM_IMG_SIZE_Y; ++j) {
                int val=newbitMap.getPixel(i,j);
                photoTensor[0][i][j][0]=(((val >> 16) & 0xFF)/255.0f);
                photoTensor[0][i][j][1]=(((val >> 8) & 0xFF)/255.0f);
                photoTensor[0][i][j][2]=(((val) & 0xFF)/255.0f);
            }
        }
        return photoTensor;
    }


    private List<String> loadLabelList(Activity activity) throws IOException {
        List<String> labelList = new ArrayList<>();
        BufferedReader reader =
                new BufferedReader(new InputStreamReader(activity.getAssets().open(LABEL_PATH)));
        String line;
        while ((line = reader.readLine()) != null) {
            labelList.add(line);
        }
        reader.close();
        return labelList;
    }

    }

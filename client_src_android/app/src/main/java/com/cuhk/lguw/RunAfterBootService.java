package com.cuhk.lguw;

import android.app.Service;
import android.app.job.JobParameters;
import android.content.Intent;
import android.os.Binder;
import android.os.Build;
import android.os.IBinder;
import android.util.Log;
import android.widget.Toast;

import android.app.job.JobParameters;
import android.app.job.JobService;
import android.content.Intent;

import androidx.annotation.RequiresApi;


@RequiresApi(api = Build.VERSION_CODES.LOLLIPOP)
public class RunAfterBootService extends JobService {
    private static final String TAG = "SyncService";

    @RequiresApi(api = Build.VERSION_CODES.M)
    @Override
    public boolean onStartJob(JobParameters params) {
        //Intent service = new Intent(getApplicationContext(), LocalWordService.class);
        //getApplicationContext().startService(service);
        Log.d(TAG, "RunAfterBootService onStartJob()");
        new Thread() {
            @Override
            public void run() {
                Wireless w = new Wireless();
                w.getFormatted();
            }
        }.start();
        Util.scheduleJob(getApplicationContext()); // reschedule the job
        return true;
    }

    @Override
    public boolean onStopJob(JobParameters params) {
        return true;
    }

}

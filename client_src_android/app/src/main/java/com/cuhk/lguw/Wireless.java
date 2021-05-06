package com.cuhk.lguw;

import android.os.Build;
import android.util.Log;

import androidx.annotation.RequiresApi;

import org.json.JSONObject;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.Socket;
import java.net.URL;
import java.net.URLConnection;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;

import static java.lang.Integer.parseInt;


public class Wireless {
    String t;
    boolean got = false;
    boolean fail = false;
    public void getContent() throws Exception{

        Log.d("LGUW URL", "start2");
        URL oracle = new URL("https://nt-r.cuhk.edu.cn");
        Log.d("LGUW URL", "start3");
        BufferedReader in = new BufferedReader(
                new InputStreamReader(oracle.openStream()));
        Log.d("LGUW URL", "start4");
        String inputLine;
        String text="";
        while ((inputLine = in.readLine()) != null) text+=inputLine;
        Log.d("LGUW URL", text);
        in.close();
        this.t = text;
        this.got = true;
        return;
    }
    public String getAny(String name){
        //get content if not got

            if(!this.got){
                try {
                    getContent();
                }
                catch (Exception e){
                    Log.d("LGUW URL", "getAny Error");
                    this.fail = true;
                    return "";
                }
            }
        String t = this.t;
        int start = t.indexOf(name+":<b>")+(name+":<b>").length();
        int end = t.indexOf("</b>",start);
        return t.substring(start,end);
    }
    public String getAnySpace(String name){
        //get content if not got
        if(!this.got){
            try {
                getContent();
            }
            catch (Exception e){
                this.fail = true;
                return "";
            }
        }
        String t = this.t;
        int start = t.indexOf(name+" : <b>")+(name+" : <b>").length();
        int end = t.indexOf("</b>",start);
        return t.substring(start,end);
    }
    public String getAnyStrong(String name){
        //get content if not got
        if(!this.got){
            try {
                getContent();
            }
            catch (Exception e){
                this.fail = true;
                return "";
            }
        }
        String t = this.t;
        int start = t.indexOf(name+" : <strong>")+(name+" : <strong>").length();
        int end = t.indexOf("</strong>",start);
        return t.substring(start,end);
    }
    @RequiresApi(api = Build.VERSION_CODES.KITKAT)
    public void getFormatted(){//to be compatible with iOS shortcut format
        Log.d("LGUW URL", "start");
        String msg = "Time:"+getAnyStrong("Time")+"\n"+"Location:"+ getAnySpace("Location")
                + "\n"+"AP Name:"+getAny("AP Name")+"\n "+"STA_2G:"+getAny("STA_2G")+"\n"
                + "STA_5G:"+getAny("STA_5G")+"\n" + "Account:"+ getAnySpace("Account")+"\n";
        Log.d("LGUW URL", msg);
        String time = getAnyStrong("Time");
        String loc = getAnySpace("Location");
        String ap = getAny("AP Name");
        String ac = getAnySpace("Account");
        Integer twog = parseInt(getAny("STA_2G"));
        Integer fiveg = parseInt(getAny("STA_5G"));
        Integer total = twog+fiveg;
        if(this.fail) return;
        try
        {
            Socket socket = new Socket( "138.128.215.15", 12335 );
            OutputStream out = socket.getOutputStream();
            JSONObject obj = new JSONObject();
            obj.put("Time",time);
            obj.put("Location",loc);
            obj.put("AP",ap);
            obj.put("2.4 GHz",twog);
            obj.put("5 GHz",fiveg);
            obj.put("Total",total);
            obj.put("Account",ac);
            byte[] dict_s = obj.toString().getBytes();
            out.write(dict_s);
            out.close();
            socket.close();

        }
        catch (Exception e){Log.d("LGU ExceptionL", e.getMessage());}



    }
}


package com.ministone.common;

import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;

public class WSProxy {
	
    public static String handleGetWithStringResponse(String requestURI){
        HttpURLConnection connection=null;
        try {             
            URL url = new URL(requestURI);
            connection = (HttpURLConnection)url.openConnection();
            connection.setConnectTimeout(10000);
            connection.setRequestMethod("GET");
            connection.setReadTimeout(5000);
            connection.connect();

            if (connection.getResponseCode() != 200)
            	throw new RuntimeException("fail to open url,error code:"+String.valueOf(connection.getResponseCode()));

            String result= IOUtil.toString(connection.getInputStream(), "UTF-8");

            return result;
        } catch (Exception e) {
            e.printStackTrace();
        }finally{
            if(connection!=null)
                connection.disconnect();
        }
        return null;
    }
    
    /**
     * The given output stream will not be closed within this method body.
     * */
    public static void handleGetWithInputStreamResponse(String requestURI,OutputStream outputStream){
    	HttpURLConnection connection=null;
    	try {             
    		URL url = new URL(requestURI);
    		connection = (HttpURLConnection)url.openConnection();
    		connection.setConnectTimeout(10000);
    		connection.setRequestMethod("GET");
    		connection.setReadTimeout(5000);
    		connection.connect();
    		
    		if (connection.getResponseCode() != 200)
    			throw new RuntimeException("fail to open url,error code:"+String.valueOf(connection.getResponseCode()));
    		
 
    	} catch (Exception e) {
    		e.printStackTrace();
    	}finally{
    		if(connection!=null)
    			connection.disconnect();
    	}
 
    }

    public static String handlePostWithStringResponse(String requestURI,String parameters){
    	HttpURLConnection connection=null;
    	try {
    		URL url = new URL(requestURI);
    		connection = (HttpURLConnection)url.openConnection();
    		connection.setConnectTimeout(10000);
    		connection.setRequestMethod("POST");
    		connection.setReadTimeout(5000);
    		connection.setDoOutput(true);
    		connection.connect();
    		connection.getOutputStream().write(parameters.getBytes("UTF-8")); 
    		connection.getOutputStream().flush();
    		connection.getOutputStream().close();
    		
    		if (connection.getResponseCode() != 200)
    			throw new RuntimeException("fail to open url,error code:"+String.valueOf(connection.getResponseCode()));
    		
    		String result= IOUtil.toString(connection.getInputStream(), "UTF-8");
    		
    		return result;
    	} catch (Exception e) {
    		e.printStackTrace();
    	}finally{
    		if(connection!=null)
    			connection.disconnect();
    	}
    	return null;
    }

}

package com.ministone.android.app.bookscanner;

import android.app.Activity;
import android.content.ActivityNotFoundException;
import android.content.Intent;
import android.graphics.Color;
//import android.net.http.AndroidHttpClient;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import com.ministone.common.*;
import com.ministone.android.app.bookscanner.R;

import java.net.HttpURLConnection;
import java.net.URL;
import java.util.HashSet;
import java.util.Set;

import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;

/**
 * User: gjkv86 Sep 15, 2010 4:38:39 PM
 * <p/>
 * notes:11/6/2010 10:41:36 AM export is passed This activity start the scanner and got the result
 */
public class BookScanner extends Activity {
	private Button mScanButton;
	private Button mScanSearchButton;
	private TextView mIsbnCounter;
	private TextView mIsbn;
	private EditText mIsbnInput;
	private Button mIsbnSearchButton;
	private Set<String> isbnSet = new HashSet<String>();

	// how to make this configurable?
	// private String baseURL="http://bmlist01.appspot.com";
	private String baseURL = "http://192.168.0.108:8080";

	/**
	 * Called when the activity is first created.
	 */
	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.main);

		// init buttons
		mScanButton = (Button) findViewById(R.id.scanButton);

		mIsbnCounter = (TextView) findViewById(R.id.isbnCounter);
		mIsbnCounter.setTextColor(Color.RED);
		mIsbnCounter.setBackgroundColor(Color.RED);
//		mIsbnCounter.setTextSize(size);
		mIsbn = (TextView) findViewById(R.id.isbn);
		mIsbnInput = (EditText) findViewById(R.id.isbnInput);
		mIsbnSearchButton = (Button) findViewById(R.id.isbnSearchButton);

		mIsbnSearchButton.setOnClickListener(new View.OnClickListener() {
			@Override
			public void onClick(View view) {
				Message msg = new Message();
				msg.what = 20;
				MessageContent messageContent = new MessageContent();
				messageContent.i = isbnSet.size();
				if (mIsbnInput.getText() != null)
					messageContent.isbn = mIsbnInput.getText().toString();
				msg.obj = messageContent;
				handler.sendMessage(msg);
			}
		});

		mScanButton.setOnClickListener(new View.OnClickListener() {
			@Override
			public void onClick(View view) {
				// send intent to barcode scanner
				Intent intent = new Intent("com.google.zxing.client.android.SCAN");
				// intent.setPackage("com.google.zxing.client.android");
				intent.putExtra("SCAN_MODE", "PRODUCT_MODE");
				try {
					startActivityForResult(intent, 0);
				} catch (ActivityNotFoundException e) {
					Log.e(Constants.TAG, "failed to start scanner", e);
					Message msg = new Message();
					msg.what = 1;
					handler.sendMessage(msg);
				}
			}
		});

	}

	@Override
	protected void onStart() {
		super.onStart();
	}

	// I BookScanner: 9787111105374,EAN_13
	public void onActivityResult(int requestCode, int resultCode, Intent intent) {
		if (requestCode == 0) {
			if (resultCode == RESULT_OK) {
				String contents = intent.getStringExtra("SCAN_RESULT");
				String format = intent.getStringExtra("SCAN_RESULT_FORMAT");

				// Handle successful scan
				Log.i(Constants.TAG, (String.format("%s,%s", contents, format)));
				isbnSet.add(contents);

				// to update the view
				{
					Message msg = new Message();
					msg.what = 20;
					MessageContent messageContent = new MessageContent();
					messageContent.i = isbnSet.size();
					messageContent.isbn = contents;
					msg.obj = messageContent;
					handler.sendMessage(msg);
				}
			} else if (resultCode == RESULT_CANCELED) {
				Log.i(Constants.TAG, "scan canceled");
			}
		}
	}

	class MessageContent {
		int i;
		String isbn;
	}

	JSONParser jsonParser = new JSONParser();
	Handler handler = new Handler() {
		@Override
		public void handleMessage(Message msg) {
			switch (msg.what) {
			case 1:
				mIsbn.setText("Please install barcode sanner");
				break;
			case 20:
				MessageContent messageContent = (MessageContent) msg.obj;
				boolean uploaded = false;
				String bookTitle = "";
				String resultCode = null;
				String status = "failed";
				String result =null;
				try {
					String requestURI = String.format("%s/ws/b/add/%d/%s", baseURL, 1, messageContent.isbn);
					Log.i(Constants.TAG, "Start request:[" + requestURI + "]");

					 result=WSProxy.handleGetWithStringResponse(requestURI);

					// parse the json?
					if (result != null && !"".equals(result)) {

						JSONObject jsonObject = (JSONObject) jsonParser.parse(result);
						resultCode = String.valueOf((Long) jsonObject.get("status"));

						if (Integer.parseInt(resultCode) == 0) {
							if (jsonObject.get("book") != null) {
								JSONObject bookObj = (JSONObject) jsonObject.get("book");
								bookTitle = (String) bookObj.get("title");
								status = "success";
							}
						} else if (Integer.parseInt(resultCode) == 1) {
							status = "NotFound";
						} else if (Integer.parseInt(resultCode) == 2) {
							status = "AlreadyExist";
						} else if (Integer.parseInt(resultCode) == 3) {
							status = "ServerError";
						}

						Log.i(Constants.TAG, "isbn searched:" + messageContent.isbn);
						uploaded = true;
						mIsbnCounter.setText(String.format("total:%d", messageContent.i));
					} else {
						mIsbnCounter.setText("response is empty");
					}

				} catch (Exception e) {
					Log.e(Constants.TAG, "failed to parse:"+result, e);
					mIsbnCounter.setText(e.getMessage());
				}

				mIsbn.setText(String.format("uploaded:%s,status:%s,isbn:%s,title:%s", uploaded, status,
						messageContent.isbn, bookTitle));
				mIsbnInput.setText("");
				break;

			default:
				mIsbnCounter.setText(msg.obj.toString());
			}
		}
	};

}
